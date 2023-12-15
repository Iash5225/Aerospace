import pandas as pd
import re


class DataHandler:
    """Handles data operations for rocket analysis."""

    def __init__(self, filepath):
        """
        Initialize the DataHandler with a given file path.
        Args:
            filepath (str): Path to the CSV file.
        """
        self.filepath = filepath
        self.df = None
        self.comments_df = None
        self.merged_df = None
        self.filtered_df = None

    def read_OR_csv(self):
        """Reads the Open Rocket CSV file and stores it in a DataFrame."""
        try:
            self.df = pd.read_csv(self.filepath, delimiter=",", skiprows=6)
            self._prepare_dataframes()
        except Exception as e:
            print(f"Error reading the CSV file: {e}")

    def _prepare_dataframes(self):
        """Prepares data and comments dataframes."""
        self._filter_comments()
        self.filtered_df = self._filter_data()
        self.merged_df = self._merge_dataframes()

    def _filter_comments(self):
        """Filters comments from the main DataFrame and stores them separately."""
        comments_mask = self.df["# Time (s)"].astype(str).str.contains("#")
        comments_df = self.df[comments_mask].copy()
        comments_df["Time (s)"] = comments_df["# Time (s)"].apply(
            self._extract_time)
        comments_df["Event"] = comments_df["# Time (s)"].apply(
            self._extract_event)
        self.comments_df = self._process_comment_events(comments_df)

    def _filter_data(self) -> pd.DataFrame:
        """Filters out comment rows from the main DataFrame."""
        filtered_df = self.df[~self.df["# Time (s)"].astype(
            str).str.contains("#")].copy()
        print(filtered_df[["# Time (s)"]])
        filtered_df.rename(columns={"# Time (s)": "Time (s)"},inplace=True)
        print(filtered_df["Time (s)"])
        return filtered_df

    def _merge_dataframes(self) -> pd.DataFrame:
        """Merges filtered data with comments data."""
        merged = self.filtered_df.merge(self.comments_df, on="Time (s)", how="left")
        merged["Time (s)"] = pd.to_numeric(
            merged["# Time (s)"], errors="coerce")
        return merged.rename(columns={"# Time (s)": "Time (s)"})

    def _extract_time(self, text: str) -> float:
        """Extracts time from a comment string."""
        match = re.search(r"t=([\d\.]+)", text)
        return float(match.group(1)) if match else None

    def _extract_event(self, text: str) -> str:
        """Extracts event name from a comment string."""
        return text.replace(r"occurred at t=[\d\.]+ seconds", "").replace("#", "").strip()

    def _process_comment_events(self, comments_df: pd.DataFrame) -> pd.DataFrame:
        """Processes events in the comments dataframe."""
        comments_df["Event"] = comments_df["Event"].apply(self.remove_non_caps)
        events_to_replace = {
            "LAUNCH": "LAUNCH/IGNITION",
            "BURNOUT": "BURNOUT/EJECTION_CHARGE",
            "GROUND_HIT": "GROUND_HIT/SIMULATION_END"
        }
        events_to_remove = ["IGNITION", "EJECTION_CHARGE", "SIMULATION_END"]
        comments_df["Event"] = comments_df["Event"].replace(events_to_replace)
        comments_df = comments_df[~comments_df["Event"].isin(events_to_remove)]
        return comments_df[["Time (s)", "Event"]]

    def find_event_time(self, event_name: str) -> float:
        """Finds the time when a specific event occurred."""
        event_time = self.merged_df.loc[self.merged_df["Event"]
                                        == event_name, "Time (s)"]
        return float(event_time.iloc[0]) if not event_time.empty else None

    def find_event_mach(self, event_name: str) -> float:
        """Finds the Mach number when a specific event occurred."""
        event_mach = self.merged_df.loc[self.merged_df["Event"]
                                        == event_name, "Mach number (​)"]
        return float(event_mach.iloc[0]) if not event_mach.empty else None

    def remove_non_caps(self, text: str) -> str:
        """Removes all words that are not in all caps from the given text."""
        return " ".join(word for word in text.split() if word.isupper())
