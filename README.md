<div align="center">

# pypassgen

pypassgen is a command line tool for generating password spraying lists.

<br>

[Installation](#installation) •
[Getting started](#getting-started) •
[Usage](#usage) •
[Coming Soon](#coming-soon)

</div><br>

</div>
<br>

## Installation

pypassgen can be installed for the PyPi using the following command:

```
pipx install pypassgen
```

If this tool is not yet availible via PyPi, you can install it directly from the repository using:

```
pipx install git+https://github.com/puzzlepeaches/pypassgen.git
```

For development, clone the repository and install it locally using poetry.

```
git clone https://github.com/puzzlepeaches/pypassgen.git
cd pypassgen
poetry shell
poetry install
```

<br>

## Getting started

pypassgen is very simple to use. First, modify the included `config.json` file to your liking. An example `config.json` file is included in the root of the repository. Note that no additional keys can be added to the config file. Modify the config file to your liking and then run the following command:

```
ppg all config.json -
```

This will output password permutations to stdout for review. Alternatively, you can replace `-` to a file name to write results to a file. For example:

```
ppg all config.json passwords.txt
```

<br>

## Usage

The help menu for pypassgen is shown below:

```
 Usage: ppg [OPTIONS] [[season|word|month|all]]... GENERATE_CONFIG
            [OUTPUT_FILE]

 pypassgen
 Generate passwords for spraying from a config file!

╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --min-length     -min  INTEGER  Minimum length of passwords                                                               │
│ --max-length     -max  INTEGER  Max length of passwords                                                                   │
│ --max-passwords  -mp   INTEGER  Max number of passwords to generate                                                       │
│ --include-words  -iw   TEXT     Include words in passwords                                                                │
│ --help           -h             Show this message and exit.                                                               │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

On runtime, it is possible to add additional words to the generation process without modifying the config file. For example:

```
ppg -iw Changeme all config.json -
```

It is possible to also set a minimum and maximum length for passwords based on your needs. Finally, and most importantly, pypassgen allows you to only generate a specific set of passwords by referencing the season, word, month, or month values in the config file. For example:

```
ppg month config.json -
```

This will only generate passwords for the month values set in `config.json`. Due to the nature of pypassgen, you can save a use several configuration profiles to meet your needs for specific engagements.

<br>

## Coming Soon

Some planned features coming in the next release:

- More granular control over the permutations used for password generation.

<br>

## Thanks

Almost all thanks here goes to [@Tw1sm](https://twitter.com/Tw1sm) for the original idea in [spraycharles](https://github.com/Tw1sm/spraycharles). An honorable mention here is also [goPassGen](https://github.com/bigb0sss/goPassGen) from [@bigb0sss](https://github.com/bigb0sss) (Sorry can't find your Twitter!).
