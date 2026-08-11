"""Naive Bayes Classifier Example using Python's statistics.NormalDist and dataclasses.

This module demonstrates a minimal Naive Bayes classifier from scratch.
It uses dataclasses for both fruit features and feature distributions
to classify samples safely with full type-hinting support.
"""

from dataclasses import dataclass
from statistics import NormalDist


@dataclass
class FruitFeatures:
    """Represents the physical measurements of a fruit sample.

    Attributes:
        weight (float): Weight in grams (g).
        firmness (float): Penetrometer firmness in kg/cm².
    """

    weight: float
    firmness: float


@dataclass
class FeatureDistributions:
    """Holds the Gaussian NormalDist objects for each feature.

    Attributes:
        weight (NormalDist): Normal distribution for weight.
        firmness (NormalDist): Normal distribution for firmness.
    """

    weight: NormalDist
    firmness: NormalDist

    @classmethod
    def from_samples(cls, samples: list[FruitFeatures]) -> "FeatureDistributions":
        """Factory method to construct NormalDist instances directly from samples."""
        return cls(
            weight=NormalDist.from_samples([s.weight for s in samples]),
            firmness=NormalDist.from_samples([s.firmness for s in samples]),
        )

    def scores(self, fruit_features: FruitFeatures) -> float:
        return self.weight.pdf(fruit_features.weight) * self.firmness.pdf(fruit_features.firmness)


# 1. Training data
apples = [
    FruitFeatures(weight=140, firmness=7.8),
    FruitFeatures(weight=150, firmness=8.2),
    FruitFeatures(weight=160, firmness=7.1),
    FruitFeatures(weight=135, firmness=8.0),
]

oranges = [
    FruitFeatures(weight=180, firmness=4.2),
    FruitFeatures(weight=190, firmness=4.0),
    FruitFeatures(weight=200, firmness=4.8),
    FruitFeatures(weight=210, firmness=3.2),
]

# 2. Modeling: Fit Gaussian distributions using the dataclass factory method
dists_apple = FeatureDistributions.from_samples(apples)
dists_orange = FeatureDistributions.from_samples(oranges)


def predict(fruit_features: FruitFeatures) -> str:
    """Classifies a given fruit as 'Apple' or 'Orange' using a Naive Bayes model.

    Args:
        fruit (FruitFeatures): The fruit features containing weight and firmness.

    Returns:
        str: "Apple" if the calculated likelihood is higher for an apple,
             otherwise "Orange".
    """
    # Product of probabilities: P(Weight) * P(Firmness)
    score_apple = dists_apple.scores(fruit_features)
    score_orange = dists_orange.scores(fruit_features)

    return "Apple" if score_apple > score_orange else "Orange"


# 3. Tests
sample1 = FruitFeatures(weight=145, firmness=8.1)
sample2 = FruitFeatures(weight=195, firmness=4.1)

print(f"{sample1} -> Prediction: {predict(sample1)}")  # Output: Apple
print(f"{sample2} -> Prediction: {predict(sample2)}")  # Output: Orange
