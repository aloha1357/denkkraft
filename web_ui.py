import streamlit as st
import pandas as pd
from data_fetcher import DataFetcher
from data_analyzer import DataAnalyzer
from trust_score_calculator import TrustScoreCalculator

class WebUI:
    def __init__(self):
        # Initialize backend classes
        url = "shopping_trends.csv"  # Replace with a valid URL or path
        self.fetcher = DataFetcher(url)
        self.analyzer = DataAnalyzer()
        self.calculator = TrustScoreCalculator()

        # Initialize attributes
        self.df = None
        self.metadata = None
        self.completeness_score = 0.0
        self.update_score = 0.0
        self.trust_score = 0.0
        self.metadata_quality_score = 0.0
        self.method = "default"  # Default method for calculating trust score

    def load_data(self):
        self.df, self.metadata = self.fetcher.fetch_data()
        print(self.df)

    def analyze_data(self):
        if self.df is not None and self.metadata is not None:
            self.completeness_score = self.analyzer.calculate_completeness_score(self.df)
            self.update_score = self.analyzer.calculate_update_score(self.metadata)
            self.metadata_quality_score = self.analyzer.calculate_metadata_quality_score(self.df, self.metadata)

    def compute_trust_score(self):
        if self.method == "optimized" and self.df is not None:
            self.trust_score = self.calculator.calculate_trust_score(
                self.completeness_score, 
                self.update_score, 
                self.metadata_quality_score, 
                method="optimized", 
                df=self.df, 
                target_column="trustworthiness"
            )
        else:
            self.trust_score = self.calculator.calculate_trust_score(
                self.completeness_score, 
                self.update_score, 
                self.metadata_quality_score, 
                method="default"
            )

    def render_page(self):
        st.title("Data Trustworthiness Scoring System")

        st.subheader("Metadata")
        st.write(self.metadata)

        st.subheader("Data Preview")
        if self.df is not None:
            st.dataframe(self.df.head())

        st.subheader("Statistical Summary")
        if self.df is not None:
            stats_summary = self.analyzer.statistical_summary(self.df)
            st.dataframe(stats_summary)

        st.subheader("Outlier Detection")
        if self.df is not None:
            # Dropdown menu for selecting the outlier detection method
            method = st.selectbox("Select Outlier Detection Method", options=["IQR", "zscore"])

            # Perform outlier detection
            outliers = self.analyzer.detect_outliers(self.df, method=method)
            if outliers:
                st.write(f"Using method: {method}")
                for column, indices in outliers.items():
                    st.write(f"Column: {column}, Outliers at indices: {indices}")
            else:
                st.write(f"No outliers detected using method: {method}.")
        else:
            st.write("No data available for outlier detection.")

        st.subheader("Analysis Results")
        st.write(f"Completeness Score: {self.completeness_score:.2f}")
        st.write(f"Update Frequency Score: {self.update_score:.2f}")
        st.write(f"Metadata Quality Score: {self.metadata_quality_score:.2f}")

        # Dropdown to select the trust score calculation method
        self.method = st.selectbox(
            "Select Trust Score Calculation Method", 
            options=["default", "optimized"]
        )

        # Recompute trust score based on selected method
        self.compute_trust_score()
        st.write(f"Trust Score ({self.method.capitalize()}): {self.trust_score:.2f}")

        # Simple Visualization - Use a bar chart to display the scores
        chart_data = pd.DataFrame({
            'Metric': ['Completeness', 'Update Frequency', 'Metadata Quality Score', 'Trust Score'],
            'Score': [self.completeness_score, self.update_score, self.metadata_quality_score, self.trust_score]
        })

        st.bar_chart(chart_data.set_index('Metric'))
