import sys
import argparse
import pandas as pd
from rich import print as rprint
from rich.console import Console
import configparser
from rich.prompt import Prompt

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the INI file
config.read('config.ini')

# Access and print the values
language_choices = [option.upper() for option in config.options('Languages')]

console = Console()

def main(file):
    # Load the CSV file
    df = pd.read_csv(file)

    # Ask the annotator for their language
    language = Prompt.ask("Pick your language", choices=language_choices, default="")

    # Define the list of categories
    categories_values_dict = {
        '(1) RFI': 'rfi',
        '(2) RFQ': 'rfq',
        '(3) Offer': 'offer',
        '(4) Support': 'support',
        '(5) Job': 'job',
        '(6) Partnership': 'partnership',
        '(7) Test': 'test',
        '(8) Private': 'private',
        '(9) Donations': 'donations',
        '(0) Other': 'other'
    }

    # Filter the DataFrame to only include rows where 'label_class_human' is NaN

    df_to_annotate = df[pd.isna(df['label_class_human'])]
    if language:
        df_to_annotate = df_to_annotate[df_to_annotate['language'] == language]

    # Use .loc to explicitly state that you're modifying the original DataFrame
    df.loc[df_to_annotate.index, 'label_class_human'] = ''

    # Iterate over the filtered DataFrame rows
    for idx, row in df_to_annotate.iterrows():
        console.clear()
        rprint("Message:")
        rprint(row['message'])
        rprint("Select category:")

        # Join the categories into a single string with a space between each category
        categories_string = ' '.join(categories_values_dict.keys())
        categories_string += ' Skip (+) Exit (x)'

        # Print the categories string
        rprint(categories_string)

        # Get the user's choice
        choice = input()

        # Check if the choice is 'x' to stop the annotation
        if choice == 'x':
            break

        if choice == 'n':
            continue

        # take 2
        elif len(choice) == 1 and choice.isdigit() and 0 <= int(choice) < len(categories_values_dict):
            df['label_class_human'] = df['label_class_human'].astype('object')
            df.loc[idx, 'label_class_human'] = categories_values_dict[list(categories_values_dict.keys())[int(choice) - 1]]
        else:
            rprint("Invalid choice.")

        # Save the updated DataFrame to the CSV file
        df.to_csv(file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to annotate data.")
    parser.add_argument("file", type=str, help="Input CSV file to annotate.")
    args = parser.parse_args()

    main(args.file)
