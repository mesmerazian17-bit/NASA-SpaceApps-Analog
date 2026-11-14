from pathlib import Path
import json
import numpy as np
import rasterio
from scipy.ndimage import uniform_filter

# --------------------------------------------------
# PROJECT PATHS AND CONFIGURATION
# --------------------------------------------------

DATA_DIR = Path("data/raw/lunar")
OUTPUT_DIR = Path("data/processed")
OUTPUT_FILE = OUTPUT_DIR / "lunar_features.json"

TARGET_NAME = "Artemis III Connecting Ridge"
TARGET_ID = "lunar_south_pole"
WINDOW_SIZE = 3
MIN_VALID_NEIGHBORS = 5

RASTERS = {
    "elevation": "Site01_final_adj_5mpp_surf.tif",
    "slope": "Site01_final_adj_5mpp_slp.tif",
    "total_elevation_error": "Site01_final_adj_5mpp_toterr.tif",
    "slope_uncertainty": "Site01_final_adj_5mpp_slperr.tif",
    "ldec": "Site01_final_adj_5mpp_ldec.tif",
}

UNITS = {
    "elevation": "m",
    "slope": "degrees",
    "total_elevation_error": "m",
    "slope_uncertainty": "degrees",
    "ldec": None,
}


# --------------------------------------------------
# STATISTICS
# --------------------------------------------------

def calculate_statistics(data, valid, unit=None):
    values = data[valid]

    if values.size == 0:
        return {
            "valid_pixels": 0,
            "mean": None,
            "median": None,
            "std": None,
            "min": None,
            "max": None,
            "unit": unit,
        }

    return {
        "valid_pixels": int(values.size),
        "mean": float(np.mean(values)),
        "median": float(np.median(values)),
        "std": float(np.std(values)),
        "min": float(np.min(values)),
        "max": float(np.max(values)),
        "unit": unit,
    }


# --------------------------------------------------
# LOCAL ROUGHNESS
# --------------------------------------------------

def calculate_roughness(data, valid, window=3):
    """
    Calculate local elevation standard deviation.

    Uses a moving window and ignores invalid cells.
    A result is accepted only when at least five
    cells in the neighborhood are valid.
    """

    if window < 1 or window % 2 == 0:
        raise ValueError("Roughness window must be a positive odd number.")

    mask = valid.astype(np.float64)
    safe_data = np.where(valid, data, 0.0).astype(np.float64)

    window_cells = window * window

    count = uniform_filter(
        mask, size=window, mode="constant"
    ) * window_cells

    total = uniform_filter(
        safe_data, size=window, mode="constant"
    ) * window_cells

    total_sq = uniform_filter(
        safe_data ** 2, size=window, mode="constant"
    ) * window_cells

    mean = np.divide(
        total,
        count,
        out=np.zeros_like(total),
        where=count > 0
    )

    mean_sq = np.divide(
        total_sq,
        count,
        out=np.zeros_like(total_sq),
        where=count > 0
    )

    variance = np.maximum(mean_sq - mean ** 2, 0.0)
    roughness = np.sqrt(variance)

    roughness_valid = valid & (count >= MIN_VALID_NEIGHBORS)

    return roughness, roughness_valid


# --------------------------------------------------
# RASTER VALIDATION AND METADATA
# --------------------------------------------------

def inspect_and_read(path, reference=None):
    if not path.exists():
        raise FileNotFoundError(f"Missing raster: {path}")

    with rasterio.open(path) as src:
        if src.count != 1:
            raise ValueError(
                f"{path.name} must contain exactly one band."
            )

        if reference is not None:
            if (
                src.width != reference["width"]
                or src.height != reference["height"]
                or src.transform != reference["transform"]
                or src.crs != reference["crs"]
            ):
                raise ValueError(
                    f"Raster grid does not match reference: {path.name}"
                )

        data = src.read(1)
        valid = (src.read_masks(1) > 0) & np.isfinite(data)

        metadata = {
            "filename": path.name,
            "width": src.width,
            "height": src.height,
            "resolution": [float(v) for v in src.res],
            "crs": str(src.crs) if src.crs else None,
            "nodata": (
                str(src.nodata)
                if src.nodata is not None
                else None
            ),
            "bounds": [
                float(src.bounds.left),
                float(src.bounds.bottom),
                float(src.bounds.right),
                float(src.bounds.top),
            ],
            "transform": [
                float(v) for v in src.transform
            ],
        }

        reference_info = {
            "width": src.width,
            "height": src.height,
            "transform": src.transform,
            "crs": src.crs,
        }

    return data, valid, metadata, reference_info


# --------------------------------------------------
# MAIN EXTRACTION WORKFLOW
# --------------------------------------------------

def main():
    print("=" * 60)
    print("PLANETARY ANALOG CAMPAIGN ARCHITECT")
    print("LUNAR FEATURE EXTRACTION")
    print("=" * 60)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    results = {}
    source_metadata = {}
    reference = None
    elevation_data = None
    elevation_valid = None

    # Load and validate all five source rasters.
    for feature_name, filename in RASTERS.items():
        path = DATA_DIR / filename

        print(f"\nReading: {filename}")

        data, valid, metadata, grid = inspect_and_read(
            path, reference
        )

        if reference is None:
            reference = grid

        if not valid.any():
            raise ValueError(
                f"No valid pixels found in {filename}"
            )

        source_metadata[feature_name] = metadata

        results[feature_name] = calculate_statistics(
            data, valid, UNITS[feature_name]
        )

        print(f"  Dimensions: {data.shape}")
        print(f"  Valid pixels: {int(valid.sum())}")
        print(f"  Coverage: {valid.mean() * 100:.4f}%")

        if feature_name == "elevation":
            elevation_data = data
            elevation_valid = valid

    # Calculate elevation coverage.
    elevation_coverage = (
        float(elevation_valid.mean() * 100)
    )

    print("\nCalculating local roughness...")

    roughness, roughness_valid = calculate_roughness(
        elevation_data,
        elevation_valid,
        WINDOW_SIZE
    )

    roughness_stats = calculate_statistics(
        roughness,
        roughness_valid,
        "m"
    )

    roughness_stats["method"] = (
        "Local standard deviation of elevation"
    )
    roughness_stats["window_pixels"] = WINDOW_SIZE
    roughness_stats["minimum_valid_neighbors"] = (
        MIN_VALID_NEIGHBORS
    )
    roughness_stats["pixel_resolution_m"] = 5

    if roughness_stats["valid_pixels"] == 0:
        raise ValueError(
            "Roughness calculation returned zero valid pixels."
        )

    # Construct output using the shared project vocabulary.
    features = {
        "elevation_m": results["elevation"],
        "slope_deg": results["slope"],
        "roughness_rms": roughness_stats,

        # Retain the previous key for compatibility.
        "local_roughness_m": roughness_stats,

        "elevation_coverage_percent": elevation_coverage,
        "total_elevation_error_m": results[
            "total_elevation_error"
        ],
        "slope_uncertainty": results["slope_uncertainty"],
        "ldec": results["ldec"],
    }

    output = {
        "schema_version": "1.0",
        "target": TARGET_NAME,
        "target_id": TARGET_ID,
        "site": "NASA LOLA Site01",
        "resolution_m": 5,
        "features": features,
        "provenance": {
            "source_name": "NASA LOLA Site01",
            "instrument_or_dataset": "LOLA gridded lunar surface products",
            "measurement_date": None,
            "spatial_resolution_m": 5,
            "value_type": "measured_and_derived",
            "source_url": None,
            "notes": (
                "Source URL and measurement date have not "
                "yet been independently documented."
            ),
        },
        "source_metadata": source_metadata,
        "quality_checks": {
            "all_rasters_grid_aligned": True,
            "all_rasters_have_valid_pixels": True,
            "all_rasters_same_dimensions": True,
            "roughness_valid_pixels": roughness_stats[
                "valid_pixels"
            ],
            "roughness_window_pixels": WINDOW_SIZE,
            "roughness_minimum_valid_neighbors": (
                MIN_VALID_NEIGHBORS
            ),
        },
    }

    # Refuse to write invalid JSON.
    serialized = json.dumps(
        output,
        indent=2,
        allow_nan=False
    )

    # Write to a temporary file, then replace the output.
    temporary_file = OUTPUT_FILE.with_suffix(".json.tmp")
    temporary_file.write_text(serialized + "\n")

    # Verify the temporary JSON can be read.
    with temporary_file.open("r") as handle:
        json.load(handle)

    temporary_file.replace(OUTPUT_FILE)

    print("\n" + "=" * 60)
    print("EXTRACTION COMPLETED")
    print("=" * 60)
    print(f"Output: {OUTPUT_FILE}")
    print(
        "Elevation valid pixels:",
        results["elevation"]["valid_pixels"]
    )
    print(
        "Roughness valid pixels:",
        roughness_stats["valid_pixels"]
    )
    print(
        "Mean roughness (m):",
        roughness_stats["mean"]
    )
    print(
        "Mean slope (degrees):",
        results["slope"]["mean"]
    )
    print(
        "Mean elevation error (m):",
        results["total_elevation_error"]["mean"]
    )
    print("\nJSON validation: PASSED")


if __name__ == "__main__":
    main()
