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

def count_unannotated_rows(df, language=None):
    if language:
        return df[(pd.isna(df['label_class_human'])) & (df['language'] == language)].shape[0]
    else:
        return pd.isna(df['label_class_human']).sum()

def main(file):
    # Load the CSV file
    df = pd.read_csv(file)

    # Check if 'label_class_human' column exists, if not add it
    if 'label_class_human' not in df.columns:
        df['label_class_human'] = pd.NA

    # Ask the annotator for their language
    language = Prompt.ask("Pick your language", choices=language_choices, default="")

    # Access and print the values
    categories_values_dict = {f'({i+1}) {config.get("Categories", option)}': config.get("Categories", option).lower() for i, option in enumerate(config.options('Categories'))}

    # Filter the DataFrame to only include rows where 'label_class_human' is NaN
    df_to_annotate = df[pd.isna(df['label_class_human'])]
    if language:
        df_to_annotate = df_to_annotate[df_to_annotate['language'] == language]

    # Iterate over the filtered DataFrame rows
    for idx, row in df_to_annotate.iterrows():
        console.clear()
        remaining = count_unannotated_rows(df, language if language else None)
        console.print(f"Remaining messages to annotate: {remaining}")
        console.print("Message:")
        console.print(row['message'])
        console.print("Select category:")

        # Join the categories into a single string with a space between each category
        categories_string = ' '.join(categories_values_dict.keys())
        categories_string += ' (0) Skip (x) Exit'

        # Print the categories string
        console.print(categories_string)

        # Get the user's choice
        choice = Prompt.ask("Your choice")

        # Check if the choice is 'x' to stop the annotation
        if choice == 'x':
            break

        if choice == '0':
            continue

        # Update the DataFrame based on the user's choice
        elif len(choice) == 1 and choice.isdigit() and 0 < int(choice) <= len(categories_values_dict):
            choice_index = int(choice) - 1
            df.loc[idx, 'label_class_human'] = list(categories_values_dict.values())[choice_index]
        else:
            console.print("Invalid choice.")

        # Save the updated DataFrame to the CSV file
        df.to_csv(file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to annotate data.")
    parser.add_argument("file", type=str, help="Input CSV file to annotate.")
    args = parser.parse_args()

    main(args.file)
