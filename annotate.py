import click
import pandas as pd
from rich.console import Console
import configparser

console = Console()

def count_unannotated_rows(df, language=None):
    if language:
        return df[(pd.isna(df['label_class_human'])) & (df['language'] == language)].shape[0]
    else:
        return pd.isna(df['label_class_human']).sum()

@click.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--config', 'config_file', default='config.ini', show_default=True, help='Path to the configuration file.')
@click.option('--comment', is_flag=True, default=False, help='Prompt for a comment after each annotation.')
def main(file, config_file, comment):
    """Script to annotate data."""

    config = configparser.ConfigParser()
    config.read(config_file)

    # Access and print the values
    language_choices = [option.upper() for option in config.options('Languages')]

    df = pd.read_csv(file)

    if 'label_class_human' not in df.columns:
        df['label_class_human'] = pd.NA

    if 'comment' not in df.columns and comment:
            df['comment'] = pd.NA

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
            if comment:
                user_comment = click.prompt("Enter your comment", default="")
                df.loc[idx, 'comment'] = user_comment
        else:
            console.print("Invalid choice.")

        df.to_csv(file, index=False)

if __name__ == "__main__":
    main()
