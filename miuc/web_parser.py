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
    Github,
    Stackoverflow,
    Zhihu,
    Bilibili,
    Githubio,
    Youtube,
    CSDN,
    Githubusercontent,
    CNblog,
    Jianshu,
    TecentCloud,
    Douban
)
from .utils import guess_name_by_url
from urllib.parse import unquote

# some frequently pages

SPECIFIC_SITES = {
    # url: page_processor
    r"^https://github\.com.*": Github,
    r"^https://.*?\.github\.io.*": Githubio,
    r"^https://stackoverflow\.com.*": Stackoverflow,
    r"^https://www\.youtube\.com.*$": Youtube,
    r"^https://youtu\.be/.*": Youtube,
    r"^https://zhuanlan\.zhihu\.com.*": Zhihu,
    r"^https://www\.zhihu\.com.*": Zhihu,
    r"^https://www\.bilibili\.com.*": Bilibili,
    r"^https://blog\.csdn\.net.*": CSDN,
    r"^http://t\.csdn\.cn/.*": CSDN,
    r"^https://raw\.githubusercontent\.com.*": Githubusercontent,
    r"^https://www\.cnblogs\.com.*": CNblog,
    r"^https://www\.jianshu\.com.*": Jianshu,
    r"^https://cloud\.tencent\.com.*": TecentCloud,
    r"^https://book\.douban\.com.*": Douban
}


def parse_url(url: str, max_time_limit: int = 5) -> str:
    """
    parse url and return the tite for the page
    """
    url = unquote(url)
    # first check the url whether in specific sites
    # if so,
    try:
        for specific_page_url in SPECIFIC_SITES:
            if re.match(specific_page_url, url):
                return SPECIFIC_SITES[specific_page_url](max_time_limit)(url)

        # response = requests.get(url, timeout=max_time_limit)
        # if response.status_code != 200:
            # 404 or other unusual error
            # return guess_name_by_url(url)
        # print('ok')
        return guess_name_by_url(url)
    except Exception as e: # pragma: no cover
        return guess_name_by_url(url)


def parse_html(html: str) -> str: # pragma: no cover
    """
    parse html and return the title
    """
    return html
