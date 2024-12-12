import pandas as pd
import numpy as np
from scipy.stats import zscore
from typing import List, Dict, Tuple

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

def statistical_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates descriptive statistics for numerical columns.

    Parameters:
        df (pd.DataFrame): The dataset to summarize.

    Returns:
        pd.DataFrame: Summary statistics for numerical columns.
    """
    return df.describe()

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

# Example usage (replace with your actual dataset)
if __name__ == "__main__":
    url = "ted_talks_en.csv"  # Replace with a valid URL or file path
    df = pd.read_csv(url)

    # Example calls for validation
    schema = {"column1": "float64", "column2": "object"}
    print("Schema Validation:", schema_validation(df, schema))
    print("Integrity Checks:", integrity_checks(df, ["id"]))
    print("Statistical Summary:\n", statistical_summary(df))
    print("Text Data Analysis:", text_data_analysis(df, ["description"]))
    print("Temporal Validation:", temporal_validation(df, ["date_column"]))
    print("Correlation Matrix:\n", multivariate_analysis(df))
    print("Outliers:", detect_outliers(df, method='IQR'))
