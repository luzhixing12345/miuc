"""
*Copyright (c) 2023 All rights reserved
*@description: parse html to generate title
*@author: Zhixing Lu
*@date: 2023-06-20
*@email: luzhixing12345@163.com
*@Github: luzhixing12345
"""

import requests
from .pages_processor import GithubProcessor, StackoverflowProcessor, ZhihuProcessor

# some frequently pages

SPECIFIC_PAGES = {
    # url: page_processor
    "https://github.com/": GithubProcessor,
    "https://stackoverflow.com/": StackoverflowProcessor,
    "https://zhuanlan.zhihu.com/": ZhihuProcessor,
    "https://www.zhihu.com/": ZhihuProcessor
}


FORMATTING_TITLE = '<title>'

# formatting title will be passed to processors, 
# each processor should complete format(self) to translate it into md format
# 
# other formatting title like
# FORMATTING_TITLE = '<site> <title>'
# FORMATTING_TITLE = '<site> - <title>'



def parse_url(url: str) -> str:
    """
    parse url and return the title for the page
    """

    for specific_page_url in SPECIFIC_PAGES:
        if url.startswith(specific_page_url):
            return SPECIFIC_PAGES[specific_page_url](FORMATTING_TITLE)(url)

    response = requests.get(url)
    if response.status_code != 200:
        return f"connect {url} failed: status code [{response.status_code}]"

    return parse_html(response.text)


def parse_html(html: str) -> str:
    """
    parse html and return the title
    """
    return html
