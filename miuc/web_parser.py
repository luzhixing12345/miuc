"""
*Copyright (c) 2023 All rights reserved
*@description: parse html to generate title
*@author: Zhixing Lu
*@date: 2023-06-20
*@email: luzhixing12345@163.com
*@Github: luzhixing12345
"""
import re
import requests
from .site_processor import (
    GithubProcessor,
    StackoverflowProcessor,
    ZhihuProcessor,
    BilibiliProcessor,
    GithubioProcessor,
    YoutubeProcessor,
    CSDNProcessor,
)
from .site_processor import guess_name_by_url

# some frequently pages

SPECIFIC_SITES = {
    # url: page_processor
    r"^https://github\.com.*": GithubProcessor,
    r"^https://.*?\.github\.io.*": GithubioProcessor,
    r"^https://stackoverflow\.com.*": StackoverflowProcessor,
    r"^https://www\.youtube\.com.*$": YoutubeProcessor,
    r"^https://youtu\.be/.*": YoutubeProcessor,
    r"^https://zhuanlan\.zhihu\.com.*": ZhihuProcessor,
    r"^https://www\.zhihu\.com.*": ZhihuProcessor,
    r"^https://www\.bilibili\.com.*": BilibiliProcessor,
    r"^https://blog\.csdn\.net.*": CSDNProcessor,
    r"^http://t\.csdn\.cn/.*": CSDNProcessor
}


def parse_url(url: str, max_time_limit: int = 5) -> str:
    """
    parse url and return the tite for the page
    """

    # first check the url whether in specific sites
    # if so,
    try:
        for specific_page_url in SPECIFIC_SITES:
            if re.match(specific_page_url, url):
                return SPECIFIC_SITES[specific_page_url](max_time_limit)(url)

        response = requests.get(url, timeout=max_time_limit)
        if response.status_code != 200:
            # 404 or other unusual error
            return guess_name_by_url(url)

        return guess_name_by_url(url)
    except Exception as e:
        
        return guess_name_by_url(url)

def parse_html(html: str) -> str:
    """
    parse html and return the title
    """
    return html
