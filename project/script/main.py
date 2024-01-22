from data_handler import DataHandler
import os
import matplotlib.pyplot as plt


def main():
    # Usage
    data_file_name = "CD Test.csv"
    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)
    # Go up one level to the project directory
    project_dir = os.path.join(script_dir, "..")
    # Construct the path to the CSV file
    csv_path = os.path.join(project_dir, "data", data_file_name)
    # Normalize the path (optional but recommended)
    csv_path = os.path.normpath(csv_path)

    data_handler = DataHandler(ras_filepath=csv_path)
    
    data_file_name = "output_file2.txt"
    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)
    # Go up one level to the project directory
    project_dir = os.path.join(script_dir, "..")
    # Construct the path to the CSV file
    output_path = os.path.join(project_dir, "output", data_file_name)
    # Normalize the path (optional but recommended)
    output_path = os.path.normpath(output_path)
    data_handler.export_mach_cd_df_to_txt(output_path)
    print(data_handler.filtered_ras_df)


    # print(data_handler.merged_df["Altitude (ft)"])

    # Read RAS CSV
    



if __name__ == "__main__":
    main()
