class MainApp:
    def __init__(self):
        self.fetcher = DataFetcher()
        self.analyzer = DataAnalyzer()
        self.calculator = TrustScoreCalculator()

    def run(self):
        self.fetcher.set_source("example_source")
        df, metadata = self.fetcher.fetch_data()
        completeness_score = self.analyzer.calculate_completeness_score(df)
        update_score = self.analyzer.calculate_update_score(metadata)
        trust_score = self.calculator.calculate_trust_score(completeness_score, update_score)
        self.calculator.visualize_scores(df, trust_score)
