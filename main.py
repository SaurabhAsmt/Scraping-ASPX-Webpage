import json
import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass

# Load configuration from JSON file
with open("config.json", "r") as config_file:
    config = json.load(config_file)


# Data class to store quotes
@dataclass
class Quote:
    author: str
    content: str
    tag: str


def author(response):
    html = HTMLParser(response.text)
    viewstate = html.css_first(config["selectors"]["viewstate"]).attributes.get("value")
    options = html.css(config["selectors"]["author_options"])
    for opt in options[1:]:
        yield {"author": opt.attributes.get("value"), "__VIEWSTATE": viewstate}


def tag(author, response):
    html = HTMLParser(response.text)
    viewstate = html.css_first(config["selectors"]["viewstate"]).attributes.get("value")
    options = html.css(config["selectors"]["tag_options"])
    for opt in options[1:]:
        yield {"author": author, "tag": opt.attributes.get("value"), "__VIEWSTATE": viewstate}


def parse_quote(response):
    html = HTMLParser(response.text)
    quotes = html.css(config["selectors"]["quotes"])
    extracted_quotes = []
    for quote in quotes:
        new_quote = Quote(
            quote.css_first(config["selectors"]["author"]).text(strip=True),
            quote.css_first(config["selectors"]["content"]).text(strip=True),
            quote.css_first(config["selectors"]["tag"]).text(strip=True)
        )
        extracted_quotes.append(new_quote.__dict__)
    return extracted_quotes


def main():
    client = httpx.Client(timeout=config["http_settings"]["timeout"], headers=config["http_settings"]["headers"])
    url = config["base_url"]

    all_quotes = []
    data = client.get(url + config["endpoints"]["search"])
    for auth in author(data):
        author_html = client.post(url + config["endpoints"]["filter"], data=auth)
        for _tag in tag(auth["author"], author_html):
            quote_html = client.post(url + config["endpoints"]["filter"], data=_tag)
            all_quotes.extend(parse_quote(quote_html))

    # Save to JSON file
    with open(config.get("output_file", "quotes_output.json"), "w") as json_file:
        json.dump(all_quotes, json_file, indent=4)


if __name__ == "__main__":
    main()
