import argparse
import sys
from typing import Optional
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse
from bs4 import BeautifulSoup
import requests

app = FastAPI()
NAME_FILE = "fileOutput.txt"


@app.get("/", response_class=HTMLResponse)
def read_root():
    comment = """
    Hello! <br> Please use "/text?url=url&length_string=length_string&save_img_link=save_img_link" 
    construction for get request. <br>
    url -> str <br>
    length_string -> int <br>
    save_img_link -> bool <br>
    For example: http://127.0.0.1:8000/text?url=https://google.com&length_string=90
    """
    return comment


@app.get("/text", response_class=PlainTextResponse)
async def read_item(
    url: str, length_string: Optional[int] = 80, save_img_link: Optional[bool] = False
):
    page = get_page(url)
    parser_data = clean_bs_item(page, length_string)
    return parser_data


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str, help="Input url")
    parser.add_argument("--length_str", dest="length_str", type=int, default=80)
    parser.add_argument(
        "--save_image_links", dest="save_image_links", action="store_true"
    )
    parser.add_argument("--save_to_file", dest="save_to_file", action="store_true")
    return parser


def get_page(url):
    page = requests.get(url)
    content = page.content.decode("utf-8")
    if page.status_code == 200:
        return BeautifulSoup(content, "html.parser")
    return None


def chunk_string(string, length):
    while len(string) > length:
        upper_bound = string.rindex(" ", 0, length)
        yield string[0:upper_bound].strip()
        string = string[upper_bound:]


def clean_bs_item(bs_item, length_string):
    lines = bs_item.find_all(text=True or "img")
    clean_tags_str = ""
    clean_html_str = ""
    blacklist = [
        "[document]",
        "noscript",
        "header",
        "html",
        "meta",
        "head",
        "input",
        "script",
        "style",
        "span",
        "svg",
        "href",
        "footer",
    ]
    for line in lines:
        if line.parent.name not in blacklist:
            clean_tags_str += "{}".format(line.replace(u"\xa0", u" "))
    for line in clean_tags_str.splitlines():
        if len(line) > 1:
            if len(line) > length_string:
                line = "\n".join(list(chunk_string(line, length_string)))
            clean_html_str += "{}\n".format(line)
    return clean_html_str


def write_data(name_file, full_text):
    with open(name_file, mode="w", encoding="utf-8") as p:
        p.write(full_text)


def main():
    parser = create_parser()
    arg = parser.parse_args(sys.argv[1:])
    url = arg
    length_string = arg.length_str
    save_img_link = arg.save_image_links
    save_to_file = arg.save_to_file

    page = get_page(url)
    parser_data = clean_bs_item(page, length_string)
    if save_to_file:
        write_data(NAME_FILE, parser_data)
    else:
        print(parser_data)


if __name__ == "__main__":
    main()
