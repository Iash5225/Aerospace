from data_handler import DataHandler
from finflutter import FinFlutter
import pandas as pd
import os
import matplotlib.pyplot as plt


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
    print(data_handler.merged_df)

    # print(data_handler.merged_df["Altitude (ft)"])

    # Iterate through the 'altitude (ft)' column and calculate flutter velocity
    flutter_results = []
    altitude_list = data_handler.merged_df['Altitude (ft)'].copy(deep=True)
    for altitude in altitude_list:
        fin_flutter = FinFlutter(
            altitude=altitude, shear_modulus=380000, root_chord=9.75, tip_chord=3.75, semi_span=4.75)
        flutter_velocity = fin_flutter.calculate_flutter_velocity_eq2(
            thickness=0.125)
        flutter_results.append(flutter_velocity)


    # Add the results to the DataFrame
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(altitude_list, flutter_results, marker='o', color='b')
    plt.title('Altitude vs Flutter Velocity')
    plt.xlabel('Altitude (ft)')
    plt.ylabel('Flutter Velocity')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
