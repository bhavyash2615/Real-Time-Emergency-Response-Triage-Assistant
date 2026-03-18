class AccuracyTracker:

    def __init__(self):
        self.total_cases = 0
        self.correct_predictions = 0

    def update(self, predicted, actual):

        self.total_cases += 1

        if predicted.lower() == actual.lower():
            self.correct_predictions += 1

    def get_accuracy(self):

        if self.total_cases == 0:
            return 0

        return round(
            (self.correct_predictions / self.total_cases) * 100, 2
        )