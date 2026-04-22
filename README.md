# Claim Atomization

## Project Overview
Claim Atomization is an individual project developed for the Software Engineering module.

The system processes a news article and transforms it into an ordered list of atomic factual claims. The goal is not to produce a generic summary, but to extract a set of clear, non-redundant claims whose granularity remains proportional to the informational depth of the source article.

## Current Features
At the current stage, the project supports:

- processing one article through a single end-to-end pipeline;
- local `.txt` article files as input;
- article selection in interactive mode;
- single-article execution from the command line;
- basic text preprocessing before extraction;
- claim extraction through the OpenAI API;
- automatic saving of extracted claims to a `.txt` output file;
- optional inclusion of a source reference derived from a paired metadata file.

## Project Structure

```text
Giuriati_Alessandro_SoftwareEngineering_ClaimAtomization/
├── data/
│   ├── articles/
│   ├── articles_[meta]/
│   └── output/
├── src/
│   └── claim_atomization/
│       ├── __init__.py
│       ├── article_selector.py
│       ├── claim_extractor.py
│       ├── input_handler.py
│       ├── main.py
│       ├── metadata_handler.py
│       ├── output_handler.py
│       └── text_preprocessor.py
├── test/
├── pytest.ini
└── README.md
```

## Main Modules

- `main.py` orchestrates the full pipeline.
- `article_selector.py` lists available articles and parses the user selection.
- `input_handler.py` loads and validates local article files.
- `text_preprocessor.py` normalizes the article text.
- `claim_extractor.py` sends the prepared article to the OpenAI API and cleans the model output.
- `metadata_handler.py` loads optional metadata and builds a Harvard-style source reference.
- `output_handler.py` formats and saves the final claim list.

## Requirements

Before running the project, make sure you have:

- Python 3 installed;
- the required Python packages installed;
- a valid OpenAI API key exported as an environment variable.

At minimum, the current implementation requires:

```bash
pip install openai pytest
```

## OpenAI API Key Setup

The extraction step requires the `OPENAI_API_KEY` environment variable.

### macOS / Linux

```bash
export OPENAI_API_KEY="your_api_key_here"
```

You can check that it is available in the current terminal session with:

```bash
echo $OPENAI_API_KEY
```

## How to Run the Program

### Interactive mode

This mode scans the `data/articles` folder, shows the available `.txt` files, and lets you choose which ones to process.

```bash
PYTHONPATH=src python src/claim_atomization/main.py
```

You can also run:

```bash
PYTHONPATH=src python -m claim_atomization.main
```

### Single-article mode

If you already know the file path, you can pass it directly as an argument:

```bash
PYTHONPATH=src python src/claim_atomization/main.py "article_path"
```

## Interactive Selection Formats

In interactive mode, the program accepts three selection styles:

- `*` to process all available articles;
- `1,2` to select articles by their displayed index;
- `file1.txt,file2.txt` to select articles by exact file name.

## Input Format

### Articles

- Input articles must be plain `.txt` files.
- Empty files are rejected.
- The program currently expects article files inside `data/articles` when interactive mode is used.

Example:

```text
data/articles/example_article.txt
```

### Optional metadata files

If a matching metadata file exists, the program will try to include a source reference in the output.

Expected path pattern:

```text
data/articles/example_article.txt
data/articles_[meta]/example_article_[meta].txt
```

Supported metadata fields are:

```text
Title: ...
Author: ...
Source: ...
Date: ...
URL: ...
Harvard style Reference: ...
```

Notes:

- If `Harvard style Reference` is already present, it is used directly.
- Otherwise, the program builds a fallback Harvard-style reference from the available metadata.
- If no valid metadata file is found, the output is still produced and the source reference is reported as `Not Available`.

## Output

For each processed article, the program saves a text file in `data/output`.

Output naming pattern:

```text
data/output/<article_name>_claims.txt
```

Example:

```text
data/output/example_article_claims.txt
```

The saved file contains:

- a numbered list of extracted claims;
- the total number of extracted claims;
- a source reference section.

## Example Workflow

1. Put one or more article files in `data/articles/`.
2. Optionally add matching metadata files in `data/articles_[meta]/`.
3. Export your OpenAI API key.
4. Run the program in interactive or single-article mode.
5. Read the generated output files in `data/output/`.

## Running Tests

The repository also includes unit tests for core local modules.

Run them with:

```bash
pytest
```

The current `pytest.ini` sets:

```ini
[pytest]
pythonpath = src
```

## Current Limitations

At the present stage:

- the system works with local `.txt` files only;
- URL fetching and scraping are not implemented;
- claim extraction depends on external API availability;
- the quality of the output depends on the model response and the source article content.

## Notes for Development

This project follows a modular pipeline so that input handling, preprocessing, extraction, metadata handling, and output generation can be improved independently in future iterations.
