# web_ui.py

import streamlit as st
import pandas as pd
from data_fetcher import DataFetcher
from data_analyzer import DataAnalyzer
from trust_score_calculator import TrustScoreCalculator

class WebUI:
    def __init__(self):
        # 初始化後端類別
        url = "ted_talks_en.csv"  # Replace with a valid URL or path
        self.fetcher = DataFetcher(url)
        self.analyzer = DataAnalyzer()
        self.calculator = TrustScoreCalculator()

        # 屬性初始值
        self.df = None
        self.metadata = None
        self.completeness_score = 0.0
        self.update_score = 0.0
        self.trust_score = 0.0

    def load_data(self):
        self.df, self.metadata = self.fetcher.fetch_data()

    def analyze_data(self):
        if self.df is not None and self.metadata is not None:
            self.completeness_score = self.analyzer.calculate_completeness_score(self.df)
            self.update_score = self.analyzer.calculate_update_score(self.metadata)

    def compute_trust_score(self):
        self.trust_score = self.calculator.calculate_trust_score(self.completeness_score, self.update_score)

    def render_page(self):
        st.title("Data Trustworthiness Scoring System")

        st.subheader("Metadata")
        st.write(self.metadata)

        st.subheader("Data Preview")
        if self.df is not None:
            st.dataframe(self.df.head())

        st.subheader("Analysis Results")
        st.write(f"Completeness Score: {self.completeness_score:.2f}")
        st.write(f"Update Frequency Score: {self.update_score:.2f}")
        st.write(f"Trust Score: {self.trust_score:.2f}")

        # Simple Visualization - Use a bar chart to display the scores
        chart_data = pd.DataFrame({
            'Metric': ['Completeness', 'Update Frequency', 'Trust Score'],
            'Score': [self.completeness_score, self.update_score, self.trust_score]
        })

        st.bar_chart(chart_data.set_index('Metric'))
