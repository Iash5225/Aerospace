from data_handler import DataHandler
import os

def main():
    # Usage
    data_file_name = "Rocket Data.csv"
    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)
    # Go up one level to the project directory
    project_dir = os.path.join(script_dir, "..")
    # Construct the path to the CSV file
    csv_path = os.path.join(project_dir, "data", data_file_name)
    # Normalize the path (optional but recommended)
    csv_path = os.path.normpath(csv_path)
    
    data_handler = DataHandler(csv_path)
    # data_handler.read_OR_csv()
    # print(data_handler.filtered_df)
    # print(data_handler.comments_df)
    print(data_handler.merged_df)
    # print(data_handler.merged_df.columns)
    # print(data_handler.merged_df["Pressure drag coefficient ()"])
    # data_handler.filter_comments()
    

if __name__ == "__main__":
    main()
