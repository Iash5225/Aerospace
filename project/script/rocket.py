import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import math


class Rocket:
    def __init__(self, filepath):
        # Default values for constants
        self.DATA_FILEPATH = filepath
        self.MOTOR_NAME = "M2100F"
        self.ROCKET_LENGTH = 2300
        self.ALTITUDE_INCREMENTS = 1000
        self.VERTICAL_MOTION_INCREMENTS = 50
        self.AVERAGE_THRUST = 2173.6
        self.OUTPUT_FOLDER_PATH = r"project\output"
        # Load data
        self.df = self.read_csv_file()
        self.comments_df = self.extract_comments()
        self.filtered_df = self.filter_comments_from_csv()
        self.merged_df = self.merge_dataframes()

    def set_data_file_Path(self, filepath):
        self.DATA_FILEPATH = filepath

    def set_motor_name(self, motor_name):
        self.MOTOR_NAME = motor_name

    def set_rocket_length(self, length):
        self.ROCKET_LENGTH = length

    def set_altitude_increments(self, increments):
        self.ALTITUDE_INCREMENTS = increments

    def set_vertical_motion_increments(self, increments):
        self.VERTICAL_MOTION_INCREMENTS = increments

    def set_average_thrust(self, thrust):
        self.AVERAGE_THRUST = thrust

    def set_output_folder_path(self, path):
        self.OUTPUT_FOLDER_PATH = path

    def read_csv_file(self):
        """
        Reads a CSV file and returns a DataFrame.
        """
        try:
            df = pd.read_csv(self.data_filepath, delimiter=",", skiprows=6)
            return df
        except Exception as e:
            print(f"An error occurred while reading the CSV file: {e}")
            return None

    def extract_comments(self):
        # Implementation of extract_comments
        pass

    def filter_comments_from_csv(self):
        # Implementation of filter_comments_from_csv
        pass

    def merge_dataframes(self):
        # Implementation of merge_dataframes
        pass

    def plot_Flight_Profile(self):
        # Implementation of plot_Flight_Profile
        pass

    def find_event_time(self, event_name: str) -> float:
        """Find the time when a specific event occurred.

        Args:
            event_name (str): The name of the event to find

        Returns:
            float: The time when the event occurred or None if the event was not found.
        """
        event_times = self.merged_df.loc[
            self.merged_df["Event"] == event_name, "Time (s)"
        ]
        return float(event_times.iloc[0]) if not event_times.empty else None

    def remove_non_caps(self, text):
        # Implementation of remove_non_caps
        pass

    def remove_time_phrase(self, df):
        # Implementation of remove_time_phrase
        pass

    def run(self):
        # Optionally, you can create a run method to execute the main logic
        self.plot_Flight_Profile(self.merged_df)

        if self.save:
            filename = "/Flight_Profile.png"
            self.fig.savefig(self.output_folder_path + filename)


# Usage
profile = Rocket(
    r"C:\Users\iash.bashir\Downloads\Aerospace\project\data\Rocket Data.csv"
)
profile.set_motor_name("New Motor")
profile.set_rocket_length(2500)
profile.set_altitude_increments(500)
# ... other settings as needed
profile.run()
