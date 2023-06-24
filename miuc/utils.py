
import re
from urllib.parse import urlparse
from urllib.parse import unquote
from datetime import datetime

def guess_name_by_url(url):
    """
    when could not access the website or get the html, guess the name by url
    """

    # more info about urlparse
    # https://docs.python.org/zh-cn/3/library/urllib.parse.html

    url_info = urlparse(url)
    # print(url_info)
    url_netlocs = unquote(url_info.netloc).split('.')
    
    # set url title based on netloc
    if len(url_netlocs) <= 1: # pragma: no cover
        # only top level domain? maybe never happend
        url_title = ''
    elif len(url_netlocs) == 2:
        # remove top level domain, insert empty str
        url_title = url_netlocs[1]
    elif len(url_netlocs) >= 3:
        # remove top level domain
        url_title = f'{url_netlocs[1]}'

        ignore_third_domain = ['www','about']
        if url_netlocs[0] not in ignore_third_domain:
            url_title += f' {url_netlocs[0]}'

    # print(netlocs)

    url_path = unquote(url_info.path)
    if url_path != '' and url_path != '/':
        if url_path[0] == '/':
            url_path = url_path[1:]
        if url_path[-1] == '/':
            url_path = url_path[:-1]

    url_paths = url_path.split('/')
    path_keywords = [
        'posts',      # maybe someone's blog
        'article',
        'articles',
        'docs'
        'product',    # maybe product in a company
        'products',
        'releases',
        'library'
    ]
    for path in url_paths:
        if path in path_keywords:
            # last path may be the most important path
            important_path = url_paths[-1]
            if important_path.endswith('.html'):
                important_path = important_path.replace('.html','')
            url_title += f' {important_path}'
            break

    return f'[{url_title}]({url})'


# def is_valid_date(date_string, date_format = "%Y.%m.%d"):
#     try:
#         datetime.strptime(date_string, date_format)
#         return True
#     except ValueError:
#         return False