"""Download the Indian medicine dataset and build data/medicines.db."""

import medicine_data

if __name__ == "__main__":
    count = medicine_data.build_database(progress=print)
    print(f"Done: {count:,} medicines loaded into {medicine_data.DB_PATH}")
