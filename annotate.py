import sys
import argparse
import pandas as pd
from rich import print as rprint

def main(file):
    # Load the CSV file
    df = pd.read_csv(file)

    # Define the list of categories
    categories = ['RFI (1)', 'Offer (2)', 'Other (3)']

    # Filter the DataFrame to only include rows where 'label_class_human' is NaN
    df_to_annotate = df[pd.isna(df['label_class_human'])]

    # Use .loc to explicitly state that you're modifying the original DataFrame
    df.loc[df_to_annotate.index, 'label_class_human'] = ''

    # Iterate over the filtered DataFrame rows
    for idx, row in df_to_annotate.iterrows():
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
    df.to_csv(file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to annotate data.")
    parser.add_argument("file", type=str, help="Input CSV file to annotate.")
    args = parser.parse_args()

    main(args.file)
