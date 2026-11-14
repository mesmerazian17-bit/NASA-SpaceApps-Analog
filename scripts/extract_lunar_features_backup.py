
def calculate_roughness(data, valid, window=3):
    # Local standard deviation of elevation.
    # Count valid cells rather than using their average fraction.
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

    # Require at least five valid cells in each 3x3 neighborhood.
    roughness_valid = valid & (count >= 5)

    return roughness, roughness_valid
