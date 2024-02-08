# Annotate messages with classes in terminal

Annotate messages with classes in the terminal.

- `pip install pandas rich`
- `cp config.ini.example config.ini`
- Adjust languages and categories in `config.ini`
- `python3 annotate.py FILE.csv`
- (optional) `python3 annotate.py --config CUSTOM_CONFIG.INI FILE.csv` to use a custom config.
- (optional) `python3 annotate.py --comment FILE.csv` to save a comment after every annotation.

## Features

- Annotate with 2-clicks (number + enter)
- Skip hard rows (hit `0`)
- Updates `*.csv` after each annotation
- Shows only rows that are not annotated yet
- Shows amount of remaining messages that need to be annotated

## Notes

The CSV needs to have a column called `message` for the content to be labelled.

The human annotation will be saved to a column called `label_class_human`.
The column gets created if not present already.

To use language filtering, you need a column `language` in the `*.csv`.
To detect languages, you can use a tool like [Lingua](https://github.com/pemistahl/lingua-py).
Or use the tool ["detect from message"](https://github.com/minthemiddle/detect-language-from-message) that builds upon `Lingua`.
Output ISO Code 639_1 codes like `DE` or `EN`.

The class list is limited to 9 options.


## License

MIT
