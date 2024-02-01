import sys
import argparse
import pandas as pd
from rich import print as rprint
from rich.console import Console

console = Console()
from rich.prompt import Prompt

def main(file):
    # Load the CSV file
    df = pd.read_csv(file)

    # Ask the annotator for their language
    language = Prompt.ask("Pick your language", choices=["EN", "DE"], default="")

    # Define the list of categories
    categories = ['RFI (1)', 'RFQ (2)', 'Offer (3)', 'Support (4)', 'Job (5)', 'Partnership (6)', 'Test (7)', 'Private (8)', 'Donations (9)', 'Other (0)']
    values = ['rfi','rfq','offer','support','job','partnership','test','private','donations','other']

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
        categories_string = ' '.join(categories)
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

        # Check if the choice is a valid number
        elif choice.isdigit() and 1 <= int(choice) <= len(categories):
            # Save the category to the DataFrame
            df['label_class_human'] = df['label_class_human'].astype('object')
            df.loc[idx, 'label_class_human'] = values[int(choice) - 1]
        else:
            rprint("Invalid choice.")

        # Save the updated DataFrame to the CSV file
        df.to_csv(file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to annotate data.")
    parser.add_argument("file", type=str, help="Input CSV file to annotate.")
    args = parser.parse_args()

    main(args.file)
