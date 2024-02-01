import sys
import argparse
import pandas as pd
from rich import print as rprint

def main(input_file, output_file):
    # Load the CSV file
    df = pd.read_csv(input_file)
    df['label_class_human'] = ''

    # Define the list of categories
    categories = ['RFI (1)', 'Offer (2)', 'Other (3)']

    # Iterate over the DataFrame rows
    for idx, row in df.iterrows():
        rprint("Message:")
        rprint(row['message'])
        rprint("Select category:")

        # Print the categories
        for i, category in enumerate(categories, start=1):
            rprint(f"{i}. {category}")

        # Get the user's choice
        choice = input()

        # Check if the choice is 'x' to stop the annotation
        if choice == 'x':
            break

        # Check if the choice is a valid number
        elif choice.isdigit() and 1 <= int(choice) <= len(categories):
            # Save the category to the DataFrame
            df['label_class_human'] = df['label_class_human'].astype('object')
            df.loc[idx, 'label_class_human'] = categories[int(choice) - 1]
        else:
            rprint("Invalid choice.")

    # Save the updated DataFrame to the CSV file
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to annotate data.")
    parser.add_argument("input_file", type=str, help="Input CSV file to annotate.")
    parser.add_argument("output_file", type=str, help="Output CSV file to store the annotated data.")

    args = parser.parse_args()

    main(args.input_file, args.output_file)
