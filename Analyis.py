import pandas as pd
from datetime import datetime
import math

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
        metadata (dict): Dictionary containing metadata with 'last_updated' as a key.

        Returns:
        float: The update frequency score (0 to 1).
        """
        if 'last_updated' not in metadata or not metadata['last_updated']:
            return 0.0  # If no update date is provided, score is 0.

        try:
            # Parse the last update date from the metadata
            last_updated = datetime.strptime(metadata['last_updated'], "%Y-%m-%d")
            today = datetime.now()
            days_since_update = (today - last_updated).days

            # Calculate the score with exponential decay
            # A dataset updated within 7 days receives a score close to 1.
            # Decay factor (lambda) can be adjusted; here, 7 days is the baseline.
            decay_factor = 0.1  # Controls the rate of decay
            update_score = math.exp(-decay_factor * days_since_update)

            return round(update_score, 4)  # Return a rounded score for simplicity.

        except ValueError:
            return 0.0  # Return 0 if the date format is invalid.


# Testing the Functions
if __name__ == "__main__":
    # Dummy dataset for completeness testing
    dummy_data = {
        'Name': ['Alice', 'Bob', None, 'David'],
        'Age': [25, None, 0, 0],
        'City': ['New York', 'Los Angeles', 'Chicago', None]
    }
    dummy_df = pd.DataFrame(dummy_data)

    # Dummy metadata for update frequency testing
    dummy_metadata = {
        'title': 'Dummy Dataset',
        'description': 'A dummy dataset for testing the update frequency.',
        'last_updated': '2023-12-01'  # Update date in YYYY-MM-DD format
    }

    analyzer = DataAnalyzer()

    # Test Completeness Score
    completeness_score = analyzer.calculate_completeness_score(dummy_df)
    print(f"Dummy Completeness Score: {completeness_score}")

    # Test Update Frequency Score
    update_score = analyzer.calculate_update_score(dummy_metadata)
    print(f"Dummy Update Frequency Score: {update_score}")
git 