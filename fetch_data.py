import pandas as pd

class DataFetcher:
    def __init__(self, source: str = ""):
        self.source = source
        self.df = None
        self.metadata = {}

    def fetch_data(self) -> tuple[pd.DataFrame, dict]:
        # Placeholder: Logic to fetch data
        self.df = pd.DataFrame({"example_column": [1, 2, 3]})
        self.metadata = {"source": self.source, "rows": len(self.df)}
        return self.df, self.metadata

    def set_source(self, source: str) -> None:
        self.source = source
