
from pathlib import Path
import rasterio

DATA_DIR = Path("data/raw/lunar")

def inspect_rasters():
    files = sorted(DATA_DIR.glob("*.tif"))

    if not files:
        print("No GeoTIFF files found.")
        return

    for path in files:
        print("\n" + "=" * 60)
        print(f"FILE: {path.name}")
        print(f"SIZE: {path.stat().st_size / (1024**2):.2f} MB")

        try:
            with rasterio.open(path) as src:
                print(f"Dimensions: {src.width} x {src.height}")
                print(f"Bands: {src.count}")
                print(f"CRS: {src.crs}")
                print(f"Resolution: {src.res}")
                print(f"Bounds: {src.bounds}")
                print(f"Data type: {src.dtypes}")
                print(f"NoData value: {src.nodata}")
                print(f"Transform: {src.transform}")
                print(f"Dataset tags: {src.tags()}")
                print(f"Band tags: {src.tags(1)}")

        except Exception as error:
            print(f"Could not open raster: {error}")
            print("Check whether the download is complete.")

if __name__ == "__main__":
    inspect_rasters()
