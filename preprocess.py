import re

class PreprocessWorkflow:
    def __init__(self, input_text, irrelevant_chars=None, punct_classes=None):
        if irrelevant_chars is None:
            irrelevant_chars = ["'", "(", ")", '"']
        if punct_classes is None:
            punct_classes = {"...": "L", ",": "A", ".": "D", "?": "Q", "!": "X", "-": "H", ":": "N"}

        self.input_text = input_text
        self.punct_classes = punct_classes
        self.irrelevant_chars = irrelevant_chars

    def replace_chars(self):
        """ Remove irrelevant chars from the text. """
        # Loop through the array of irrelevant chars and replace them
        for char in self.irrelevant_chars:
            self.input_text = self.input_text.replace(char, '')

        # Replace multiple spaces with a single space
        self.input_text = re.sub(r'\s+', ' ', self.input_text).strip()

    def words_to_lines(self):
        """ Split the text into words, each in new line. """
        words = self.input_text.split()
        self.input_text = '\n'.join(words)

    def add_labels(self, output_file):
        """ Label each word with the class of a punctuation mark that follows it. """
        lines = self.input_text.splitlines()
        processed_lines = []

        for line in lines:
            # Remove all unnecessary spaces at the end of the line.
            line = line.strip()
            if line:
                # Read last character
                last_char = line[-1]
                if last_char in self.punct_classes:
                    # Identify punctuation label
                    label = self.punct_classes[last_char]
                else:
                    # Or blank label, if there is no punctuation
                    label = "O"
                processed_lines.append(f"{line}\t{label}\n")

        # Write the modified lines to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(processed_lines)

    def workflow(self, output_file):
        """Execute the preprocessing workflow and save the result to a file."""
        self.replace_chars()  # Step 1: Clean text
        self.words_to_lines()  # Step 2: Convert words to separate lines
        self.add_labels(output_file)  # Step 3: Add labels

preprocess = PreprocessWorkflow('input.txt')
preprocess.workflow('output.txt')

