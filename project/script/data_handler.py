import pandas as pd
import re


class DataHandler:
    """Handles data operations for Rocket analysis."""

    def __init__(self, filepath):
        """
        Initialize the DataHandler with a given file path.

        Args:
            filepath (str): Path to the CSV file.
        """
        self.filepath = filepath
        self.df = None
        self.comments_df = None

    def read_OR_csv(self):
        """Reads the CSV file and stores it in a DataFrame."""
        try:
            self.df = pd.read_csv(self.filepath, delimiter=",", skiprows=6)
        except Exception as e:
            print(f"An error occurred while reading the CSV file: {e}")

    def filter_comments(self):
        """Extracts comments from the DataFrame and stores them in a separate DataFrame."""
        if self.df is None:
            print("Data not loaded. Please call read_csv first.")
            return

        comments_df = self.df[self.df["# Time (s)"].astype(
            str).str.contains("#")].copy()
        comments_df["Time (s)"] = comments_df["# Time (s)"].apply(
            self._extract_time)
        comments_df["Event"] = comments_df["# Time (s)"].apply(
            self._extract_event)
        self.comments_df = comments_df[["Time (s)", "Event"]]

    def merge_dataframes(self) -> pd.DataFrame:
        """Merges the filtered DataFrame with the comments DataFrame.

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

    def filter_comments_from_csv(self) -> pd.DataFrame:
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

    def _extract_time(self, text):
        """Extracts time from a comment string."""
        match = re.search(r"t=([\d\.]+)", text)
        return float(match.group(1)) if match else None

    def _extract_event(self, text):
        """Extracts event name from a comment string."""
        # Further processing can be added here based on your requirements
        return text

    def remove_non_caps(self, text: str) -> str:
        """Removes all words that are not in all caps from the given text.

        Args:
            text (str): The string from which to remove non-uppercase words

        Returns:
            str: Modified string containing only uppercase words
        """
        return " ".join(word for word in text.split() if word.isupper())

    def extract_comments(self) -> pd.DataFrame:
        """Extracts the comments from the CSV file and returns a DataFrame.

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

    def find_event_mach(self, event_name: str) -> float:
        """Find the time when a specific event occurred.

        Args:
            event_name (str): The name of the event to find

        Returns:
            float: The time when the event occurred or None if the event was not found.
        """
        event_times = self.merged_df.loc[
            self.merged_df["Event"] == event_name, "Mach number (​)"
        ]
        return float(event_times.iloc[0]) if not event_times.empty else None

    # Additional methods can be added here for more data operations
