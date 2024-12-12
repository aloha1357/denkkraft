import pandas as pd
import requests
from typing import Tuple

class DataFetcher:
    def __init__(self, source_url: str):
        """
        Initialize the DataFetcher with the source URL.
        
        Parameters:
            source_url (str): URL of the dataset (can be a CSV file or an API endpoint).
        """
        self.source_url = source_url
        self.df = None
        self.metadata = {}

    def fetch_data(self) -> Tuple[pd.DataFrame, dict]:
        """
        Fetch the dataset and metadata based on the source URL.

        Returns:
            Tuple[pd.DataFrame, dict]:
                - df: Pandas DataFrame containing the dataset.
                - metadata: Dictionary containing the dataset's metadata.
        """
        try:
            if self.source_url.endswith('.csv'):
                # If the source is a CSV file
                self.df = pd.read_csv(self.source_url, encoding='utf-8')
            else:
                # If the source is an API endpoint, assume JSON response
                response = requests.get(self.source_url)
                response.raise_for_status()
                data = response.json()
                self.df = pd.DataFrame(data)

            # Extract basic metadata
            self.metadata = {
                "title": self.source_url.split('/')[-1],  # Use the filename or last part of the URL as the title
                "description": "Dataset fetched from the given source URL.",
                "source": self.source_url,
                "last_update_time": pd.Timestamp.now().isoformat()  # Current timestamp as the update time
            }

            return self.df, self.metadata

        except Exception as e:
            print(f"An error occurred while fetching the dataset: {e}")
            return pd.DataFrame(), {}

    def get_metadata(self) -> dict:
        """
        Return the metadata of the fetched dataset.
        
        Returns:
            dict: Metadata information about the dataset.
        """
        return self.metadata

    def get_dataset(self) -> pd.DataFrame:
        """
        Return the dataset as a pandas DataFrame.
        
        Returns:
            pd.DataFrame: The fetched dataset.
        """
        return self.df

# Example usage (replace with your actual dataset URL)
if __name__ == "__main__":
    url = "shopping_trends.csv"  # Replace with a valid URL or path
    data_fetcher = DataFetcher(url)

    dataset, metadata = data_fetcher.fetch_data()

    print("Metadata:", metadata)
    print("Dataset Head:")
    print(dataset)