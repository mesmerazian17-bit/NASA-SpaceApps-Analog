import importlib.util
import json
import math
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

FETCHER_PATH = (
    ROOT / "data" / "raw" / "teammates" / "fetch_nasa_earth_data.py"
)

AUDIT_PATH = (
    ROOT / "data" / "processed" / "earth_diurnal_range_audit.json"
)

spec = importlib.util.spec_from_file_location(
    "earth_fetcher",
    FETCHER_PATH,
)

fetcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fetcher)


class TestMeanDailyTemperatureRange(unittest.TestCase):

    def test_all_85_audit_records(self):
        audit = json.loads(AUDIT_PATH.read_text())

        self.assertEqual(len(audit["results"]), 85)
        self.assertEqual(audit["errors"], [])

        for record in audit["results"]:
            with self.subTest(site_id=record["site_id"]):
                monthly_ranges = {
                    item["month"]: item["range_k"]
                    for item in record["monthly_ranges"]
                }

                # Use each saved monthly range as max-minus-zero.
                # This independently tests the weighting calculation.
                max_avg = monthly_ranges
                min_avg = {month: 0.0 for month in fetcher.MONTHS}

                actual = fetcher.mean_daily_temp_range(
                    max_avg,
                    min_avg,
                )

                expected = record["day_weighted_mean_k"]

                self.assertTrue(math.isfinite(actual))
                self.assertAlmostEqual(actual, expected, places=3)

    def test_missing_month_returns_nan(self):
        max_avg = {month: 20.0 for month in fetcher.MONTHS}
        min_avg = {month: 10.0 for month in fetcher.MONTHS}

        del max_avg["FEB"]

        result = fetcher.mean_daily_temp_range(max_avg, min_avg)

        self.assertTrue(math.isnan(result))

    def test_power_fill_value_returns_nan(self):
        max_avg = {month: 20.0 for month in fetcher.MONTHS}
        min_avg = {month: 10.0 for month in fetcher.MONTHS}

        max_avg["FEB"] = -999

        result = fetcher.mean_daily_temp_range(max_avg, min_avg)

        self.assertTrue(math.isnan(result))

    def test_negative_monthly_range_returns_nan(self):
        max_avg = {month: 20.0 for month in fetcher.MONTHS}
        min_avg = {month: 10.0 for month in fetcher.MONTHS}

        max_avg["MAR"] = 5.0

        result = fetcher.mean_daily_temp_range(max_avg, min_avg)

        self.assertTrue(math.isnan(result))


if __name__ == "__main__":
    unittest.main(verbosity=2)
