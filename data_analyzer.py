import pandas as pd
import math
from datetime import datetime
from data_fetcher import DataFetcher

class DataAnalyzer:
    @staticmethod
    def calculate_completeness_score(df: pd.DataFrame) -> float:
        """
        Calculate the completeness score of a DataFrame.
        
        Completeness Score = 1 - (Total Number of Missing Values / Total Data Points)

        Args:
        df (pd.DataFrame): The dataset as a pandas DataFrame.

        Returns:
        float: The completeness score (0 to 1).
        """
        if df.empty:
            return 0.0  # If the DataFrame is empty, completeness is 0.

        total_values = df.size  # Total number of data points in the DataFrame.
        missing_values = df.isnull().sum().sum()  # Total number of missing values in the DataFrame.
        completeness_score = 1 - (missing_values / total_values)

        return round(completeness_score, 4)  # Return a rounded score for simplicity.

    @staticmethod
    def calculate_update_score(metadata: dict) -> float:
        """
        Calculate the update frequency score based on metadata.

        The score is based on how recently the dataset has been updated. A dataset
        updated within 7 days receives full marks, and the score decays exponentially
        with longer intervals.

        Args:
        metadata (dict): Dictionary containing metadata with 'last_update_time' as a key.

        Returns:
        float: The update frequency score (0 to 1).
        """
        if 'last_update_time' not in metadata or not metadata['last_update_time']:
            return 0.0  # If no update time is provided, score is 0.

        try:
            # Parse the last update time from the metadata
            last_update_time = datetime.fromisoformat(metadata['last_update_time'])
            today = datetime.now()
            days_since_update = (today - last_update_time).days

            # Calculate the score with exponential decay
            # A dataset updated within 7 days receives a score close to 1.
            decay_factor = 0.1  # Controls the rate of decay
            update_score = math.exp(-decay_factor * days_since_update)

            return round(update_score, 4)  # Return a rounded score for simplicity.

        except ValueError:
            return 0.0  # Return 0 if the date format is invalid


# Example usage
if __name__ == "__main__":
    data_fetcher = DataFetcher("ted_talks_en.csv")
    dataset, metadata = data_fetcher.fetch_data()   
    
    # Initialize the DataAnalyzer
    analyzer = DataAnalyzer()

    # Calculate Completeness Score
    completeness_score = analyzer.calculate_completeness_score(dataset)
    print(f"Completeness Score: {completeness_score}")

    # Calculate Update Frequency Score
    update_score = analyzer.calculate_update_score(metadata)
    print(f"Update Frequency Score: {update_score}")
