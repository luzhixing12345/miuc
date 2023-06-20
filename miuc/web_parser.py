"""
*Copyright (c) 2023 All rights reserved
*@description: parse html to generate title
*@author: Zhixing Lu
*@date: 2023-06-20
*@email: luzhixing12345@163.com
*@Github: luzhixing12345
"""

import requests
from .pages_processor import GithubProcessor, StackoverflowProcessor

# some frequently pages

SPECIFIC_PAGES = {
    # url: page_processor
    "https://github.com/": GithubProcessor,
    "https://stackoverflow.com/": StackoverflowProcessor,
}


def parse_url(url: str) -> str:
    """
    parse url and return the title for the page
    """
    response = requests.get(url)
    if response.status_code != 200:
        return f"connect {url} failed: status code [{response.status_code}]"

    for specific_page_url in SPECIFIC_PAGES:
        if url.startswith(specific_page_url):
            return SPECIFIC_PAGES[specific_page_url](url)
    return parse_html(response.text)


def parse_html(html: str) -> str:
    """
    parse html and return the title
    """
    return html
