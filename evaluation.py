from collections import defaultdict

class PunctuationMetrics:
    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2
        self.file1_punct_count = defaultdict(int) # Count instances of each punctuation class
        self.file2_punct_count = defaultdict(int)
        self.character_match_count = defaultdict(int)

    def count_matching_characters(self):
        """ Count characters from both files and matches between them. """
        with open(self.file1, 'r') as f1, open(self.file2, 'r') as f2:
            for line1, line2 in zip(f1, f2):
                char1 = line1[-1]
                char2 = line2[-1]

                self.file1_punct_count[char1] += 1
                self.file2_punct_count[char2] += 1

                if char1 == char2:
                    self.character_match_count[char1] += 1

    def calculate_metrics(self):
        """ Calculate precision, recall, and F1 scores for each punctuation mark."""
        metrics = {}
        punctuation_marks = set(self.file1_punct_count.keys()).union(self.file2_punct_count.keys())

        for punct in punctuation_marks:
            true_positive = self.character_match_count[punct]
            false_positive = self.file2_punct_count[punct] - true_positive
            false_negative = self.file1_punct_count[punct] - true_positive

            precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) > 0 else 0
            recall = true_positive / (true_positive + false_negative) if (true_positive + false_negative) > 0 else 0
            f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

            metrics[punct] = {
                'precision': precision,
                'recall': recall,
                'f1_score': f1_score
            }

        return metrics

    def workflow(self):
        self.count_matching_characters()
        # Calculate and display metrics for each punctuation class
        metrics = self.calculate_metrics()
        for punct, values in metrics.items():
            print(f"Punctuation class: '{punct}' | Precision: {values['precision']:.2f}, Recall: {values['recall']:.2f}, F1 Score: {values['f1_score']:.2f}")

metrics = PunctuationMetrics('expected.txt', 'generated_output.txt')
metrics.workflow()