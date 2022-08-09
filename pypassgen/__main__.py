#!/usr/bin/env python3

import json
import logging

# import click
import rich_click as click
from rich.console import Console
from rich.logging import RichHandler

# Setting up logging with rich
FORMAT = "%(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])

log = logging.getLogger("rich")

# Initializing console for rich
console = Console()

# Setting context settings for click
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help", "help"])


class PassGen:
    """Generate passwords"""

    def __init__(
        self,
        min_length,
        max_length,
        max_passwords,
        include_words,
        key,
        generate_config,
        output_file,
    ) -> None:
        self.min_length = min_length
        self.max_length = max_length
        self.max_passwords = max_passwords
        self.key = list(key)

        # Parsing information from config file
        with open(generate_config, "r") as f:
            self.config = json.load(f)

            # Seasons
            self.seasons = self.config["seasons"]

            # Checking if include_words is specified
            if include_words:
                self.words = self.config["words"]

                # Appending to words list if specfied on CLI
                self.words.append(include_words)
            else:
                self.words = self.config["words"]

            # Setting everything else
            self.months = self.config["months"]
            self.years = self.config["years"]
            self.numbers = self.config["numbers"]
            self.specials = self.config["specials"]
            f.close()
        self.output_file = output_file

    def _permutation(self, val):
        """Internal function to generate permutations"""
        for year in self.years:
            for number in self.numbers:
                for special in self.specials:

                    # idk why this works but it does
                    yield f"{val}{year}"
                    yield f"{val}{year[-2:]}"
                    yield f"{val}{year}{special}"
                    yield f"{val}{special}{year}"
                    yield f"{val}{year[-2:]}{special}"
                    yield f"{val}{number}"
                    yield f"{val}{number}{special}"

    def season(self):
        """Generate season passwords"""
        passwords = []
        for season in self.seasons:
            passwords.extend(self._permutation(season))

        return passwords

    def word(self):
        """Generate base word passwords"""
        passwords = []
        for word in self.words:
            passwords.extend(self._permutation(word))

        return passwords

    def month(self):
        """Generate month passwords"""
        passwords = []
        for month in self.months:
            passwords.extend(self._permutation(month))

        return passwords

    def all(self):
        """Generate all password permutations"""
        passwords = []
        passwords.extend(self.season())
        passwords.extend(self.word())
        passwords.extend(self.month())
        return passwords

    def parse(self, passwords):
        """Parsing generated passwords with min/max lengths and sorting"""
        passwd = []
        for password in passwords:
            if len(password) >= self.min_length and len(password) <= self.max_length:
                passwd.append(password)

        return list(set(passwd))


@click.command(no_args_is_help=True, context_settings=CONTEXT_SETTINGS)
@click.option("-min", "--min-length", default=8, help="Minimum length of passwords")
@click.option("-max", "--max-length", default=99, help="Max length of passwords")
@click.option(
    "-mp", "--max-passwords", type=int, default=None, help="Max number of passwords to generate"
)
@click.option("-iw", "--include-words", default=None, help="Include words in passwords")
@click.argument("key", type=click.Choice(["season", "word", "month", "all"]), nargs=-1)
@click.argument("generate_config", type=click.Path(exists=True))
@click.argument("output_file", default="-", type=click.Path())
def main(
    min_length, max_length, max_passwords, include_words, key, generate_config, output_file
) -> None:
    """
    pypassgen \n

    Generate passwords for spraying from a config file!
    """
    if "all" in key and len(key) > 1:
        log.error("Cannot specify all with other keys")
        exit(1)

    # Initializing PassGen object
    passgen = PassGen(
        min_length, max_length, max_passwords, include_words, key, generate_config, output_file
    )

    # Running specfied modules
    for k in passgen.key:
        module = getattr(passgen, k)
        out = passgen.parse(module())

    # Pulling int from max_passwords if specified
    if max_passwords:
        out = out[:max_passwords]

    # Writing to file
    if output_file != "-":
        with open(passgen.output_file, "w") as f:
            for password in out:
                f.write(f"{password}\n")
            f.close()
    else:
        for password in out:
            console.print(password)


if __name__ == "__main__":
    main()
