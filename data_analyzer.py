import pandas as pd
import numpy as np
from scipy.stats import zscore
from typing import List, Dict, Tuple
from datetime import datetime
import math

class DataAnalyzer:
    @staticmethod
    def schema_validation(df: pd.DataFrame, expected_schema: Dict[str, str]) -> bool:
        """
        Validates the dataset against a predefined schema.

        Parameters:
            df (pd.DataFrame): The dataset to validate.
            expected_schema (Dict[str, str]): A dictionary mapping column names to expected data types.

        Returns:
            bool: True if the schema matches, False otherwise.
        """
        for column, dtype in expected_schema.items():
            if column not in df.columns:
                print(f"Missing column: {column}")
                return False
            if not np.issubdtype(df[column].dtype, np.dtype(dtype)):
                print(f"Column {column} has incorrect type: expected {dtype}, got {df[column].dtype}")
                return False
        return True

    @staticmethod #show in UI
    def detect_outliers(df: pd.DataFrame, method: str = 'IQR') -> Dict[str, List[int]]:
        """
        Detects outliers in numerical columns.

        Parameters:
            df (pd.DataFrame): The dataset to analyze.
            method (str): Method to detect outliers ('IQR' or 'zscore').

        Returns:
            Dict[str, List[int]]: Dictionary mapping column names to indices of rows with outliers.
        """
        outliers = {}
        for column in df.select_dtypes(include=[np.number]).columns:
            if method == 'IQR':
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outlier_indices = df[(df[column] < lower_bound) | (df[column] > upper_bound)].index.tolist()
            elif method == 'zscore':
                z_scores = zscore(df[column].dropna())
                outlier_indices = np.where(np.abs(z_scores) > 3)[0].tolist()
            else:
                raise ValueError("Invalid method. Use 'IQR' or 'zscore'.")
            if outlier_indices:
                outliers[column] = outlier_indices
        return outliers

    @staticmethod
    def integrity_checks(df: pd.DataFrame, key_columns: List[str]) -> bool:
        """
        Performs integrity checks such as uniqueness of key columns.

        Parameters:
            df (pd.DataFrame): The dataset to analyze.
            key_columns (List[str]): Columns that should have unique values.

        Returns:
            bool: True if all integrity checks pass, False otherwise.
        """
        for column in key_columns:
            if column not in df.columns:
                print(f"Key column {column} not found in dataset.")
                return False
            if df[column].duplicated().any():
                print(f"Duplicates found in key column: {column}")
                return False
        return True

    @staticmethod #show in UI
    def statistical_summary(df: pd.DataFrame) -> pd.DataFrame:
        """
        Generates descriptive statistics for numerical columns.

        Parameters:
            df (pd.DataFrame): The dataset to summarize.

        Returns:
            pd.DataFrame: Summary statistics for numerical columns.
        """
        return df.describe()

    @staticmethod
    def validate_distribution(df: pd.DataFrame, column: str, expected_distribution: str = 'normal') -> bool:
        """
        Validates the distribution of a column.

        Parameters:
            df (pd.DataFrame): The dataset to analyze.
            column (str): The column to validate.
            expected_distribution (str): Expected distribution ('normal', 'uniform').

        Returns:
            bool: True if the distribution matches the expectation, False otherwise.
        """
        from scipy.stats import shapiro, kstest

        data = df[column].dropna()
        if expected_distribution == 'normal':
            stat, p_value = shapiro(data)
        elif expected_distribution == 'uniform':
            stat, p_value = kstest(data, 'uniform')
        else:
            raise ValueError("Invalid expected distribution. Use 'normal' or 'uniform'.")

        if p_value < 0.05:
            print(f"Column {column} does not follow the expected {expected_distribution} distribution.")
            return False
        return True

    @staticmethod
    def text_data_analysis(df: pd.DataFrame, text_columns: List[str]) -> Dict[str, Dict[str, int]]:
        """
        Analyzes text columns for quality.

        Parameters:
            df (pd.DataFrame): The dataset to analyze.
            text_columns (List[str]): List of text columns to analyze.

        Returns:
            Dict[str, Dict[str, int]]: Analysis results per column.
        """
        results = {}
        for column in text_columns:
            if column in df.columns:
                results[column] = {
                    "missing": df[column].isna().sum(),
                    "empty": (df[column].str.strip() == '').sum(),
                    "unique": df[column].nunique()
                }
            else:
                print(f"Text column {column} not found in dataset.")
        return results

    @staticmethod
    def temporal_validation(df: pd.DataFrame, date_columns: List[str]) -> Dict[str, bool]:
        """
        Validates date columns for consistency.

        Parameters:
            df (pd.DataFrame): The dataset to analyze.
            date_columns (List[str]): List of date columns to validate.

        Returns:
            Dict[str, bool]: Validation results per column.
        """
        results = {}
        for column in date_columns:
            if column in df.columns:
                try:
                    pd.to_datetime(df[column])  # Validate format
                    results[column] = True
                except Exception as e:
                    print(f"Error in column {column}: {e}")
                    results[column] = False
            else:
                print(f"Date column {column} not found in dataset.")
                results[column] = False
        return results

    @staticmethod
    def multivariate_analysis(df: pd.DataFrame) -> pd.DataFrame:
        """
        Analyzes correlations between numerical columns.

        Parameters:
            df (pd.DataFrame): The dataset to analyze.

        Returns:
            pd.DataFrame: Correlation matrix of numerical columns.
        """
        numeric_df = df.select_dtypes(include=[np.number])  # Select only numeric columns
        if numeric_df.empty:
            print("No numeric columns found for correlation analysis.")
            return pd.DataFrame()
        return numeric_df.corr()

    @staticmethod
    def context_specific_checks(df: pd.DataFrame, context: str = 'general') -> None:
        """
        Performs context-specific validation checks.

        Parameters:
            df (pd.DataFrame): The dataset to analyze.
            context (str): The context of the dataset ('general', 'geo', 'finance').

        Returns:
            None
        """
        if context == 'geo':
            if 'latitude' in df.columns and 'longitude' in df.columns:
                invalid_lat = df[(df['latitude'] < -90) | (df['latitude'] > 90)]
                invalid_lon = df[(df['longitude'] < -180) | (df['longitude'] > 180)]
                print(f"Invalid latitudes: {len(invalid_lat)}")
                print(f"Invalid longitudes: {len(invalid_lon)}")
        elif context == 'finance':
            if 'price' in df.columns:
                negative_prices = df[df['price'] < 0]
                print(f"Negative prices: {len(negative_prices)}")
        else:
            print("No specific checks implemented for this context.")
    
    #-------------------Checked by ALoha-------------------

    @staticmethod    
    def calculate_completeness_score(df: pd.DataFrame) -> float:
        """
        Calculate the completeness score of a DataFrame.
        
        Completeness Score = 1 - (Total Number of Missing Values / Total Number of Data Points)

        Args:
        df (pd.DataFrame): The dataset as a pandas DataFrame.

        Returns:
        float: The completeness score (0 to 1).
        """
        if df.empty:
            return 0.0  # If the DataFrame is empty, completeness is 0.

        # Total cells in the DataFrame
        total_cells = df.size

        # Total non-missing cells
        non_null_cells = df.notnull().sum().sum()

        # Calculate the completeness score
        completeness_score = non_null_cells / total_cells

        return round(completeness_score, 4)  # Return a rounded score for simplicity

    @staticmethod
    def calculate_update_score(metadata: dict) -> float:
        """
        Calculate the update frequency score based on metadata.

        Args:
        metadata (dict): Metadata containing 'last_update_time' in ISO format (YYYY-MM-DD).

        Returns:
        float: Update score (0 to 1). A dataset updated recently gets a higher score.
        """
        # Check if 'last_update_time' is in metadata
        last_update_time = metadata.get("last_update_time")
        if not last_update_time:
            return 0.5  # Default score if no update time is provided

        try:
            # Parse the last update time
            last_update_date = datetime.fromisoformat(last_update_time)
            today = datetime.now()
            days_since_update = (today - last_update_date).days

            # Calculate score using exponential decay (customize decay factor as needed)
            decay_factor = 0.1  # Adjust this value to control the rate of decay
            update_score = math.exp(-decay_factor * days_since_update)

            # Ensure the score is between 0 and 1
            return round(update_score, 4)

        except ValueError:
            # Return a default score if the date format is invalid
            return 0.5  

    @staticmethod
    def calculate_metadata_quality_score(df: pd.DataFrame, column_descriptions=None) -> float:
        """
        Calculate a metadata quality score for a given DataFrame.
        
        Args:
            df (pd.DataFrame): The input DataFrame.
            column_descriptions (dict, optional): A dictionary of column names to their descriptions.
                                                  Example: {'col1': 'Description of col1', 'col2': 'Description of col2'}

        Returns:
            float: Metadata quality score in the range [0, 1].
        """
        if df is None or df.empty:
            return 0.0  # No metadata quality if there's no data
        
        total_score = 0
        max_score = 0

        # 1. Check column name completeness
        num_columns = len(df.columns)
        meaningful_column_names = sum(1 for col in df.columns if col and "Unnamed" not in col)
        total_score += meaningful_column_names
        max_score += num_columns  # Maximum score for all columns having meaningful names

        # 2. Check data type consistency
        consistent_data_types = sum(1 for col in df.columns if df[col].apply(type).nunique() == 1)
        total_score += consistent_data_types
        max_score += num_columns  # Each column can get a point for consistency

        # 3. Check for duplicate columns
        duplicate_columns = df.T.duplicated().sum()
        total_score += (num_columns - duplicate_columns)  # Deduct points for duplicates
        max_score += num_columns  # Each column ideally is unique

        # 4. Optional: Check if column descriptions are provided
        if column_descriptions:
            described_columns = sum(1 for col in df.columns if col in column_descriptions and column_descriptions[col])
            total_score += described_columns
            max_score += num_columns  # Each column ideally has a description

        # Normalize score to a range of 0 to 1
        return total_score / max_score if max_score > 0 else 0.0

# Example usage (replace with your actual dataset)
if __name__ == "__main__":
    url = "ted_talks_en.csv"  # Replace with a valid URL or file path
    df = pd.read_csv(url)
    dataAnalyser = DataAnalyzer()
    # Example calls for validation
    schema = {"column1": "float64", "column2": "object"}
    print("Schema Validation:", dataAnalyser.schema_validation(df, schema))
    print("Integrity Checks:", dataAnalyser.integrity_checks(df, ["id"]))
    print("Statistical Summary:\n", dataAnalyser.statistical_summary(df))
    print("Text Data Analysis:", dataAnalyser.text_data_analysis(df, ["description"]))
    print("Temporal Validation:", dataAnalyser.temporal_validation(df, ["date_column"]))
    print("Correlation Matrix:\n", dataAnalyser.multivariate_analysis(df))
    print("Outliers:", dataAnalyser.detect_outliers(df, method='IQR'))
