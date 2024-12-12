from scipy.optimize import minimize
import numpy as np
import pandas as pd

class TrustScoreCalculator:
    def __init__(self):
        self.alpha = 0.4
        self.beta = 0.3
        self.gamma = 0.3

    def optimize_weights(self, df, target_column="trustworthiness", random_initial=False):
        def objective_function(weights):
            alpha, beta, gamma = weights
            predicted_scores = (
                alpha * df["completeness_score"]
                + beta * df["freshness_score"]
                + gamma * df["metadata_quality_score"]
            )
            error = ((df[target_column] - predicted_scores) ** 2).mean()  # Mean Squared Error
            return error

        # Generate random weights if specified
        if random_initial:
            initial_weights = np.random.rand(3)
            initial_weights = initial_weights / initial_weights.sum()  # Normalize
        else:
            initial_weights = [0.4, 0.3, 0.3]  # Default weights

        bounds = [(0, 1), (0, 1), (0, 1)]
        constraints = {"type": "eq", "fun": lambda w: sum(w) - 1}

        result = minimize(objective_function, initial_weights, bounds=bounds, constraints=constraints)

        if result.success:
            self.alpha, self.beta, self.gamma = result.x
        else:
            raise ValueError("Optimization failed!")

    def calculate_trust_score(self, 
                              completeness_score, 
                              freshness_score, 
                              metadata_quality_score, 
                              method="default", 
                              df=None, 
                              target_column="trustworthiness"):
        """
        Calculate the Trust Score using the specified method.
        
        :param completeness_score: Score for completeness
        :param freshness_score: Score for freshness
        :param metadata_quality_score: Score for metadata quality
        :param method: The method to use ("default", "optimized")
        :param df: Dataset required for "optimized" method
        :param target_column: Target column for "optimized" method
        :return: Calculated Trust Score
        """
        if method == "optimized":
            if df is None:
                raise ValueError("Dataset (df) is required for the 'optimized' method.")
            self.optimize_weights(df, target_column)

        # Calculate the Trust Score using the current weights
        trust_score = (
            self.alpha * completeness_score
            + self.beta * freshness_score
            + self.gamma * metadata_quality_score
        )
        return trust_score

# Example Usage
data = {
    "completeness_score": [0.8, 0.9, 0.7, 0.85],
    "freshness_score": [0.6, 0.75, 0.8, 0.65],
    "metadata_quality_score": [0.7, 0.8, 0.9, 0.85],
    "trustworthiness": [0.75, 0.85, 0.8, 0.8]  # Target column
}
df = pd.DataFrame(data)

calculator = TrustScoreCalculator()

# Default method
default_score = calculator.calculate_trust_score(0.85, 0.65, 0.9, method="default")
print(f"Default Trust Score: {default_score}")

# Optimized method
optimized_score = calculator.calculate_trust_score(0.85, 0.65, 0.9, method="optimized", df=df)
print(f"Optimized Trust Score: {optimized_score}")
