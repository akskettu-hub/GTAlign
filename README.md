# GTAlign

GTAlign is a Python script that aligns the tokens in the column `Token` in an `.xlsx` file with the original text in the CEEC corpus. It can then generates new `.xlsx` files, with the added `Original Token` column, which has the corresponding token from the original CEEC text.

**Note**: this tool is a work in process!

The purpose of this tool is to provide a column `Original Token` for spreadsheets used for gold standard POS annotation, which originally used only normalised text as the basis of its tokenisation and POS annotation. The script implements a version of the [Needleman-Wunch algorithm](https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm), which is used to get the best possible alignment two sequences.

## Installation

- Python 3.13.7 (Might work on other versions, but not tested.)
- NOTE: Will not work on out of the box Windows. All paths are unix style and these would have to be manually adjusted.
`TODO:` make path handling more flexible and compatible with Windows

```bash
git clone <repo-url>

cd <repo-name>
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows NOTE: all paths are unix style

pip install -r requirements.txt
```

By default, it is assumed that a directory `./data/` exists and contains the following:

- A clone of the `CEEC-400` repo
- A directory containing the `.xlsx` files

These have to be added by the user
  `TODO:` make this process smoother

## Usage

Currently the programme is run from the file `gt_allign.py`, uncomment one of the functions and run them one at a time.

- The function `process_all_to_tuple_list()` produces a list of tuples with the alignment with the format (<Token Id>, <Token>, <Original Tokens>). This list needs to be hand aligned, although most pairs are handled without any issue.
- The function `alignment_lists_to_excel()`, uses the previous aligned list of tuples to generate new `.xlsx` files with the added `Original Token` column added.

`TODO:` write better ui
