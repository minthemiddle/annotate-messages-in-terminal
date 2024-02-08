import click
import pandas as pd
from rich.console import Console
import configparser

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

@click.command()
@click.argument('file', type=click.Path(exists=True))
def main(file):
    """Script to annotate data."""
    df = pd.read_csv(file)

    if 'label_class_human' not in df.columns:
        df['label_class_human'] = pd.NA

    language = click.prompt("Pick your language", type=click.Choice(language_choices), default="")

    categories_values_dict = {f'({i+1}) {config.get("Categories", option)}': config.get("Categories", option).lower() for i, option in enumerate(config.options('Categories'))}

    df_to_annotate = df[pd.isna(df['label_class_human'])]
    if language:
        df_to_annotate = df_to_annotate[df_to_annotate['language'] == language]

    for idx, row in df_to_annotate.iterrows():
        console.clear()
        remaining = count_unannotated_rows(df, language if language else None)
        console.print(f"Remaining messages to annotate: {remaining}")
        console.print("Message:")
        console.print(row['message'])
        console.print("Select category:")

        categories_string = ' '.join(categories_values_dict.keys())
        categories_string += ' (0) Skip (x) Exit'
        console.print(categories_string)

        choice = click.prompt("Your choice", default="x")

        if choice == 'x':
            break

        if choice == '0':
            continue

        elif len(choice) == 1 and choice.isdigit() and 0 < int(choice) <= len(categories_values_dict):
            choice_index = int(choice) - 1
            df.loc[idx, 'label_class_human'] = list(categories_values_dict.values())[choice_index]
        else:
            console.print("Invalid choice.")

        df.to_csv(file, index=False)

if __name__ == "__main__":
    main()
