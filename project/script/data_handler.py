import pandas as pd
import re


class DataHandler:
    """Handles data operations for rocket analysis."""

    def __init__(self, filepath:str):
        """
        __init__  Initializes the DataHandler class with a given file path.

        :param filepath:  Filepath to the OR rocket exported CSV file
        :type filepath: str 
        """   
        self.filepath = filepath
        self.df = None
        self.comments_df = None
        self.merged_df = None
        self.filtered_df = None
        self._read_OR_csv()

    def _read_OR_csv(self)->None:
        """
        _read_OR_csv  Reads the Open Rocket CSV file and stores it in a DataFrame.
        """        
        try:
            self.df = pd.read_csv(self.filepath, delimiter=",", skiprows=6)
            self._prepare_dataframes()
        except Exception as e:
            print(f"Error reading the CSV file: {e}")

    
    def _prepare_dataframes(self)->None:
        """
        _prepare_dataframes  Prepares the dataframes for analysis. These include: initial dataframe, filtered dataframe, comments dataframe, and merged dataframe.
        """        
        self._filter_comments()
        self.filtered_df = self._filter_data()
        self.merged_df = self._merge_dataframes()

    def _filter_comments(self)->None:
        """
        _filter_comments  Filters comments from the main DataFrame and stores them separately.
        """        
        comments_mask = self.df["# Time (s)"].astype(str).str.contains("#")
        comments_df = self.df[comments_mask].copy()
        comments_df["Time (s)"] = comments_df["# Time (s)"].apply(
            self._extract_time)
        comments_df["Event"] = comments_df["# Time (s)"].apply(
            self._extract_event)
        self.comments_df = self._process_comment_events(comments_df)

    def _filter_data(self) -> pd.DataFrame:
        """
        _filter_data  Filters out comment rows from the main DataFrame.

        :return:  Filtered DataFrame
        :rtype: pd.DataFrame
        """        
        filtered_df = self.df[~self.df["# Time (s)"].astype(
            str).str.contains("#")].copy()
        filtered_df.rename(columns={"# Time (s)": "Time (s)"}, inplace=True)
        return filtered_df

    def _merge_dataframes(self) -> pd.DataFrame:
        """
        _merge_dataframes  Merges the filtered data with the comments data. As well as cleans U+200B characters.

        :return:  Merged DataFrame
        :rtype: pd.DataFrame
        """        
        # Convert 'Time (s)' in both dataframes to float
        self.filtered_df["Time (s)"] = pd.to_numeric(
            self.filtered_df["Time (s)"], errors='coerce')
        if self.comments_df is not None:
            self.comments_df["Time (s)"] = pd.to_numeric(
                self.comments_df["Time (s)"], errors='coerce')

        # Perform the merge
        merged = self.filtered_df.merge(
            self.comments_df, on="Time (s)", how="left")

        # Clean U+200B characters from data
        for column in merged.columns:
            if merged[column].dtype == object:
                merged[column] = merged[column].str.replace('\u200b', '')

        # Clean U+200B characters from column names
        merged.columns = [col.replace('\u200b', '') for col in merged.columns]

        return merged

    def _extract_time(self, text: str) -> float:
        """
        _extract_time  Extracts time from a comment string. The string must be in the format: "occurred at t=0.000 seconds"

        :param text:  Comment string
        :type text: str
        :return:  Time in seconds
        :rtype: float
        """        
        match = re.search(r"t=([\d\.]+)", text)
        return float(match.group(1)) if match else None

    def _extract_event(self, text: str) -> str:
        """
        _extract_event  Extracts event name from a comment string. The string must be in the format: "occurred at t=0.000 seconds"

        :param text:  Comment string
        :type text: str
        :return:  Event name
        :rtype: str
        """        
        return text.replace(r"occurred at t=[\d\.]+ seconds", "").replace("#", "").strip()

    def _process_comment_events(self, comments_df: pd.DataFrame) -> pd.DataFrame:
        """
        _process_comment_events  Processes events in the comments dataframe. This includes removing non-caps words, replacing events, and removing events.

        :param comments_df:  Comments DataFrame
        :type comments_df: pd.DataFrame
        :return:  Processed comments DataFrame
        :rtype: pd.DataFrame
        """        

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
        """
        find_event_time  Finds the time when a specific event occurred.

        :param event_name:  Event name
        :type event_name: str
        :return:  Time in seconds
        :rtype: float
        """        
        event_time = self.merged_df.loc[self.merged_df["Event"]
                                        == event_name, "Time (s)"]
        return float(event_time.iloc[0]) if not event_time.empty else None

    def find_event_mach(self, event_name: str) -> float:
        """
        find_event_mach  Finds the Mach number when a specific event occurred.

        :param event_name:  Event name
        :type event_name: str
        :return:  Mach number
        :rtype: float
        """        
        
        event_mach = self.merged_df.loc[self.merged_df["Event"]
                                        == event_name, "Mach number ()"]
        return float(event_mach.iloc[0]) if not event_mach.empty else None

    def remove_non_caps(self, text: str) -> str:
        """
        remove_non_caps  Removes all words that are not in all caps from the given text.

        :param text:  Text to remove non-caps words from
        :type text: str
        :return:  Text with non-caps words removed
        :rtype: str
        """        
        return " ".join(word for word in text.split() if word.isupper())
