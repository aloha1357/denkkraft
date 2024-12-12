import pandas as pd
import requests
from typing import Tuple

# Define the function to fetch data and metadata
def fetch_data(source_url: str) -> Tuple[pd.DataFrame, dict]:
    """
    Fetch a dataset from a given source URL and extract metadata.

    Parameters:
        source_url (str): URL of the dataset (can be a CSV file or an API endpoint).

    Returns:
        Tuple[pd.DataFrame, dict]:
            - df: Pandas DataFrame containing the dataset.
            - metadata: Dictionary containing the dataset's metadata.
    """
    try:
        # Fetch the data from the source
        if source_url.endswith('.csv'):
            # If the source is a CSV file
            df = pd.read_csv(source_url)
        else:
            # If the source is an API endpoint, assume JSON response
            response = requests.get(source_url)
            response.raise_for_status()
            data = response.json()
            df = pd.DataFrame(data)

        # Extract basic metadata
        metadata = {
            "title": source_url.split('/')[-1],  # Use the filename or last part of the URL as the title
            "description": "Dataset fetched from the given source URL.",
            "source": source_url,
            "last_update_time": pd.Timestamp.now().isoformat()  # Current timestamp as the update time
        }

        return df, metadata

    except Exception as e:
        print(f"An error occurred while fetching the dataset: {e}")
        return pd.DataFrame(), {}

# Example usage (replace with your actual dataset URL)
if __name__ == "__main__":
    url = "ted_talks_en.csv"  # Replace with a valid URL
    dataset, meta = fetch_data(url)

    print("Metadata:", meta)
    print("Dataset Head:")
    print(dataset.head())