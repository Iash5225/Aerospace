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

    def extract_time(text: str) -> float:
        """Extract the numerical value of time from a string containing 't ='

        Args:
            text (str): string containing 't ='

        Returns:
            float: numerical value of time or else None
        """
        match = re.search(r"t=([\d\.]+)", text)
        return float(match.group(1)) if match else None

    def remove_non_caps(text: str) -> str:
        """Removes all words that are not in all caps from the given text.

        Args:
            text (str): The string from which to remove non-uppercase words

        Returns:
            str: Modified string containing only uppercase words
        """
        return " ".join(word for word in text.split() if word.isupper())

    def extract_comments(self):
        """
        Reads a CSV file and extracts rows that contain comments in the '# Time (s)' column.
        """
        df = self.df.__deepcopy__
        comments_df = df[df["# Time (s)"].astype(str).str.contains("#")].__deepcopy__()
        comments_df["Time (s)"] = comments_df["# Time (s)"].apply(
            lambda x: re.search(r"t=([\d\.]+)", x).group(1)
            if re.search(r"t=([\d\.]+)", x)
            else None
        )
        comments_df["Time (s)"] = pd.to_numeric(
            comments_df["Time (s)"], errors="coerce"
        )
        comments_df["Event"] = (
            comments_df["# Time (s)"]
            .str.replace(r"occurred at t=[\d\.]+ seconds", "")
            .str.replace("#", "")
            .str.strip()
        )
        # Apply the function to the 'Event' column of your DataFrame
        comments_df["Event"] = comments_df["Event"].apply(self.remove_non_caps)

        # Rename 'LAUNCH' to 'LAUNCH/IGNITION'
        comments_df["Event"] = comments_df["Event"].replace(
            {"LAUNCH": "LAUNCH/IGNITION"}
        )
        # Rename 'BURNOUT' to 'BURNOUT/EJECTION_CHARGE'
        comments_df["Event"] = comments_df["Event"].replace(
            {"BURNOUT": "BURNOUT/EJECTION_CHARGE"}
        )
        # Rename 'GROUND_HIT' to 'GROUND_HIT/SIMULATION_END'
        comments_df["Event"] = comments_df["Event"].replace(
            {"GROUND_HIT": "GROUND_HIT/SIMULATION_END"}
        )

        # Remove the 'IGNITION' row
        comments_df = comments_df[comments_df["Event"] != "IGNITION"]
        # Remove the 'EJECTION_CHARGE' row
        comments_df = comments_df[comments_df["Event"] != "EJECTION_CHARGE"]
        # Remove the 'SIMULATION_END' row
        comments_df = comments_df[comments_df["Event"] != "SIMULATION_END"]

        return comments_df[["Time (s)", "Event"]]

    # TODO
    def filter_comments_from_csv(self):
        # Implementation of filter_comments_from_csv
        pass

    # TODO
    def merge_dataframes(self):
        # Implementation of merge_dataframes
        """
        Merges the filtered DataFrame with the comments DataFrame.
        """
        merged_df = self.filtered_df.merge(self.comments_df, on="Time (s)", how="left")
        # Dropping the 'Time (s)' column from the merged DataFrame
        merged_df.drop(columns=["Time (s)"], inplace=True)

        # Ensure 'Time (s)' in filtered_df is float, if it's not already
        merged_df["# Time (s)"] = pd.to_numeric(
            merged_df["# Time (s)"], errors="coerce"
        )
        return merged_df

    # TODO
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

    # TODO
    def remove_time_phrase(self, df):
        # Implementation of remove_time_phrase
        pass

    # TODO
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
