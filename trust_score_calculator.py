class TrustScoreCalculator:
    def __init__(self, alpha=0.4, beta=0.3, gamma=0.3):
        """
        Initialize with default weights. If not specified otherwise,
        defaults are alpha=0.4, beta=0.3, gamma=0.3
        """
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def set_weights(self, alpha: float, beta: float, gamma: float):
        """
        Allow dynamic adjustment of weight configurations
        """
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def calculate_trust_score(self, 
                              completeness_score: float, 
                              freshness_score: float, 
                              metadata_quality_score: float) -> float:
        """
        Formula to calculate the Trust Score:
        Trust Score = alpha * Completeness Score 
                     + beta * Freshness Score
                     + gamma * Metadata Quality Score
        """
        trust_score = (self.alpha * completeness_score 
                       + self.beta * freshness_score 
                       + self.gamma * metadata_quality_score)
        return trust_score
