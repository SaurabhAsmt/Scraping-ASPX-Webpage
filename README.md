# Quote Scraper

## Overview
This project is a Python-based web scraper designed to extract quotes from a website using `httpx` and `selectolax`. The scraper retrieves quotes along with their authors and tags, then saves them in a JSON file.

## Features
- Scrapes quotes, authors, and tags from a website.
- Uses `httpx` for HTTP requests.
- Parses HTML efficiently with `selectolax`.
- Stores extracted quotes in a structured JSON format.
- Configurable via `config.json`.
- Stores output to a file `quotes_output.json`.

## Requirements
Ensure you have the following dependencies installed before running the script:

```bash
pip install httpx selectolax
```

## Configuration
The scraper reads settings from `config.json`.

## Output
The scraper stores output to file `quotes_output.json`

## Usage
To run the scraper, execute:

```bash
python main.py
```

The script will fetch quotes and save them in `quotes_output.json`.

## Code Structure
- `Quote`: A dataclass representing a quote.
- `author(response)`: Extracts author options from the response.
- `tag(author, response)`: Extracts tags related to a given author.
- `parse_quote(response)`: Parses quotes from the response.
- `main()`: Handles HTTP requests, iterates over authors and tags, and saves quotes to a JSON file.

## License
This project is licensed under the MIT License.


