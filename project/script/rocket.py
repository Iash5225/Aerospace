import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import math


class Rocket:
    """ Rocket class for plotting data from a CSV file.
    """    
    
    def __init__(self, filepath:str)->None:
        """  Initialise the Rocket class for plotting data from a CSV file.

        Args:
            filepath (str):  The path to the CSV file containing the data.
        """        
        # Default values for constants
        self.DATA_FILEPATH = filepath
        self.MOTOR_NAME = "M2100F"
        self.ROCKET_LENGTH = 2300
        self.ALTITUDE_INCREMENTS = 1000
        self.VERTICAL_MOTION_INCREMENTS = 50
        self.AVERAGE_THRUST = 2173.6
        self.OUTPUT_FOLDER_PATH = r"project\output"

        # Save
        self.PLOT_SAVE = False
        # Events
        self.DISPLAY_MOTOR_BURNOUT = True
        self.DISPLAY_LAUNCH = False
        self.DISPLAY_APOGEE = True
        self.DISPLAY_GROUND_HIT = False
        self.DISPLAY_LAUNCH_ROD = False

        # Load data
        self.df = self.read_csv_file()
        self.comments_df = self.extract_comments()
        self.filtered_df = self.filter_comments_from_csv()
        self.merged_df = self.merge_dataframes()

    def set_PLOT_SAVE(self, state: bool) -> None:
        """ Set the PLOT_SAVE constant to True or False.

        Args:
            state (bool):  True or False
        """        
        self.PLOT_SAVE = state

    def set_DISPLAY_MOTOR_BURNOUT(self, state: bool) -> None:
        """ Set the DISPLAY_MOTOR_BURNOUT constant to True or False.

        Args:
            state (bool):  True or False
        """        
        self.DISPLAY_MOTOR_BURNOUT = state

    def set_DISPLAY_LAUNCHT(self, state: bool) -> None:
        """ Set the DISPLAY_LAUNCH constant to True or False.

        Args:
            state (bool):  True or False
        """        
        self.DISPLAY_LAUNCH = state

    def set_DISPLAY_APOGEE(self, state: bool) -> None:
        """ Set the DISPLAY_APOGEE constant to True or False.

        Args:
            state (bool):  True or False
        """        
        self.DISPLAY_APOGEE = state

    def set_DISPLAY_GROUND_HIT(self, state: bool) -> None:
        """ Set the DISPLAY_GROUND_HIT constant to True or False.

        Args:
            state (bool):  True or False
        """        
        self.DISPLAY_GROUND_HIT = state

    def set_DISPLAY_LAUNCH_ROD(self, state: bool) -> None:
        """ Set the DISPLAY_LAUNCH_ROD constant to True or False.

        Args:
            state (bool):  True or False
        """        
        self.DISPLAY_LAUNCH_ROD = state

    def set_data_file_Path(self, filepath:str)->None:
        """ Set the DATA_FILEPATH constant to the given filepath.

        Args:
            filepath (str):  _description_
        """        
        self.DATA_FILEPATH = filepath

    def set_motor_name(self, motor_name:str)->None:
        """ Set the MOTOR_NAME constant to the given motor name.

        Args:
            motor_name (str): Motor name
        """        
        self.MOTOR_NAME = motor_name

    def set_rocket_length(self, length:int)->None:
        """ Set the ROCKET_LENGTH constant to the given length.

        Args:
            length (int):  Rocket length
        """        
        self.ROCKET_LENGTH = length

    def set_altitude_increments(self, increments:int)->None:
        """ Set the ALTITUDE_INCREMENTS constant to the given increments.

        Args:
            increments (int):  Altitude increments
        """        
        self.ALTITUDE_INCREMENTS = increments

    def set_vertical_motion_increments(self, increments:int)->None:
        """ Set the VERTICAL_MOTION_INCREMENTS constant to the given increments.

        Args:
            increments (int):  Vertical motion increments
        """        
        self.VERTICAL_MOTION_INCREMENTS = increments

    def set_average_thrust(self, average_thrust:float)->None:
        """ Set the AVERAGE_THRUST constant to the given thrust.

        Args:
            average_thrust (float):  Average thrust
        """        
        self.AVERAGE_THRUST = average_thrust

    def set_output_folder_path(self, path:str)->None:
        """ Set the OUTPUT_FOLDER_PATH constant to the given path.

        Args:
            path (str):  Output folder path
        """        
        self.OUTPUT_FOLDER_PATH = path

    def read_csv_file(self) -> pd.DataFrame:
        """ Read the CSV file and return a DataFrame.

        Returns:
            pd.DataFrame:  DataFrame containing the data from the CSV file
        """        

        try:
            df = pd.read_csv(self.DATA_FILEPATH, delimiter=",", skiprows=6)
            return df
        except Exception as e:
            print(f"An error occurred while reading the CSV file: {e}")
            return None

    def extract_time(self, text: str) -> float:
        """Extract the numerical value of time from a string containing 't ='

        Args:
            text (str): string containing 't ='

        Returns:
            float: numerical value of time or else None
        """
        match = re.search(r"t=([\d\.]+)", text)
        return float(match.group(1)) if match else None

    def remove_non_caps(self, text: str) -> str:
        """Removes all words that are not in all caps from the given text.

        Args:
            text (str): The string from which to remove non-uppercase words

        Returns:
            str: Modified string containing only uppercase words
        """
        return " ".join(word for word in text.split() if word.isupper())

    def extract_comments(self) -> pd.DataFrame:
        """  Extracts the comments from the CSV file and returns a DataFrame.

        Returns:
            pd.DataFrame:  DataFrame containing the comments from the CSV file
        """        
        df = self.df
        comments_df = df[df["# Time (s)"].astype(
            str).str.contains("#")].copy(deep=True)
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

    def filter_comments_from_csv(self)-> pd.DataFrame:
        """Filters out rows that contain comments from the dataframe.

        Returns:
            pd.DataFrame:  DataFrame containing the filtered data
        """
        df = self.df.copy(deep=True)
        filtered_df = df[~df["# Time (s)"].astype(str).str.contains("#")].copy(
            deep=True
        )
        filtered_df["Time (s)"] = pd.to_numeric(
            filtered_df["# Time (s)"], errors="coerce"
        )
        return filtered_df

    def merge_dataframes(self)->pd.DataFrame:
        """ Merges the filtered DataFrame with the comments DataFrame.

        Returns:
            pd.DataFrame:  DataFrame containing the merged data
        """        


        merged_df = self.filtered_df.merge(
            self.comments_df, on="Time (s)", how="left")
        # Dropping the 'Time (s)' column from the merged DataFrame
        merged_df.drop(columns=["Time (s)"], inplace=True)

        # Ensure 'Time (s)' in filtered_df is float, if it's not already
        merged_df["# Time (s)"] = pd.to_numeric(
            merged_df["# Time (s)"], errors="coerce"
        )

        rename_dict = {"# Time (s)": "Time (s)"}
        merged_df.rename(columns=rename_dict, inplace=True)

        return merged_df

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

    def plot_Flight_Profile(self)->None:
        """ Plot the Flight Profile data.
        """   
        df = self.merged_df.copy(deep=True)
        # df.rename(columns=rename_dict, inplace=True)

        MAX_ALTITUDE = math.ceil(int(df["Altitude (ft)"].max()) / 1000) * 1000

        pre_round_max = int(
            max(
                df["Vertical velocity (m/s)"].max(
                ), df["Vertical velocity (m/s)"].max()
            )
        )
        MAX_VERTICAL_MOTION = (
            math.ceil(pre_round_max / self.VERTICAL_MOTION_INCREMENTS)
            * self.VERTICAL_MOTION_INCREMENTS
        )

        pre_round_min = min(
            df["Vertical velocity (m/s)"].min(),
            df["Vertical acceleration (m/s²)"].min(),
        )

        MIN_VERTICAL_MOTION = (
            pre_round_min // self.VERTICAL_MOTION_INCREMENTS
        ) * self.VERTICAL_MOTION_INCREMENTS

        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Plot Altitude
        ax1.plot(df["Time (s)"], df["Altitude (ft)"],
                 "k:", label="Altitude (ft)")
        ax1.set_xlabel("TIME (s)")
        ax1.set_ylabel("ALTITUDE (ft)")

        ax1.set_xlim(0, df["Time (s)"].max())

        ax1.set_ylim(0, MAX_ALTITUDE)

        ax1.set_yticks(range(0, MAX_ALTITUDE + 1, self.ALTITUDE_INCREMENTS))

        # Set the x-axis to have ticks at regular intervals
        x_ticks_interval = 10  # or any other interval suitable for your data
        ax1.set_xticks(np.arange(0, df["Time (s)"].max(), x_ticks_interval))

        ax1.grid(True)

        # Plot Vertical velocity and Vertical acceleration on the same axis, ax2
        ax2 = ax1.twinx()
        ax2.plot(
            df["Time (s)"],
            df["Vertical velocity (m/s)"],
            "k--",
            label="Vertical velocity (m/s)",
        )
        ax2.plot(
            df["Time (s)"],
            df["Vertical acceleration (m/s²)"],
            "k-",
            label="Vertical acceleration (m/s²)",
        )
        ax2.set_ylabel(
            "VERTICAL VELOCITY (m/s); VERTICAL ACCELERATION (m/s²)", labelpad=15
        )
        ax2.set_ylim(MIN_VERTICAL_MOTION, MAX_VERTICAL_MOTION)
        ax2.set_yticks(
            np.arange(
                MIN_VERTICAL_MOTION,
                MAX_VERTICAL_MOTION + 1,
                self.VERTICAL_MOTION_INCREMENTS,
            )
        )

        # Combine legends from ax1 and ax2
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines + lines2, labels + labels2, loc="upper right")

        plt.title(f"{self.MOTOR_NAME} Motor - Vertical Motion vs Time")
        fig.tight_layout()  # Adjust layout to fit labels

        if self.DISPLAY_MOTOR_BURNOUT:
            event_time = self.find_event_time(df, "BURNOUT/EJECTION_CHARGE")
            ax1.axvline(
                x=event_time, color="r", linestyle="-", label="BURNOUT/EJECTION_CHARGE"
            )
        elif self.DISPLAY_LAUNCH:
            event_time = self.find_event_time(df, "LAUNCH/IGNITION")
            ax1.axvline(
                x=event_time, color="r", linestyle="-", label="LAUNCH/IGNITION"
            )
        elif self.DISPLAY_APOGEE:
            event_time = self.find_event_time(df, "APOGEE")
            ax1.axvline(x=event_time, color="r", linestyle="-", label="APOGEE")
        elif self.DISPLAY_GROUND_HIT:
            event_time = self.find_event_time(df, "GROUND_HIT/SIMULATION_END")
            ax1.axvline(
                x=event_time, color="r", linestyle="-", label="GROUND_HIT/SIMULATION_END"
            )
        elif self.DISPLAY_LAUNCH_ROD:
            event_time = self.find_event_time(df, "LAUNCH_ROD")
            ax1.axvline(x=event_time, color="r",
                        linestyle="-", label="LAUNCH_ROD")

        plt.show()

        if self.PLOT_SAVE:
            filename = "/Flight_Profile.png"
            self.fig.savefig(self.output_folder_path + filename)

    def run(self):
        # Optionally, you can create a run method to execute the main logic
        self.plot_Flight_Profile()


def main():
    # Usage
    csv_file_path = (
        r"C:\Users\iash.bashir\Downloads\Aerospace\project\data\Rocket Data.csv"
    )
    profile = Rocket(csv_file_path)
    profile.set_motor_name("M2100")
    profile.set_rocket_length(2500)
    profile.set_altitude_increments(1000)
    # ... other settings as needed
    profile.run()


if __name__ == "__main__":
    main()
