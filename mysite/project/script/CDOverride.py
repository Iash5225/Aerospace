import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

FILEPATH = "CD Test.CSV"
# Specify the path for the new text file
OUTPUT_FILE_PATH = "output_file.txt"


def prep_csv() -> None:
    df = pd.read_csv(FILEPATH)
    filtered_df = df[["Mach", "CD"]]
    filtered_df = filtered_df[filtered_df["Mach"] <= 2]
    # Export the DataFrame as a tab-delimited text file
    filtered_df.to_csv(OUTPUT_FILE_PATH, sep="\t", index=False)
    print(f"Data exported to {OUTPUT_FILE_PATH}")

def main():
    prep_csv()


if __name__ == "__main__":
    main()


