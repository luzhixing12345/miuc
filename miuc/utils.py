from urllib.parse import urlparse, unquote
import re


def guess_name_by_url(url):
    """
    when could not access the website or get the html, guess the name by url
    """

    # more info about urlparse
    # https://docs.python.org/zh-cn/3/library/urllib.parse.html
    if is_ip_address(url):
        return f'[{url}]({url})'
    url_info = urlparse(url)
    url_netlocs = url_info.netloc.split(".")

    add_last_path = False
    # set url title based on netloc
    if len(url_netlocs) <= 1:
        # only top level domain or localhost, maybe never happend
        url_title = url # pragma: no cover
    elif len(url_netlocs) == 2:
        # remove top level domain, insert empty str
        url_title = url_netlocs[0]
    elif len(url_netlocs) >= 3:
        # remove top level domain
        url_title = f"{url_netlocs[1]}"

        ignore_third_domain = ["www", "about","me"]
        if url_netlocs[0] not in ignore_third_domain:
            url_title += f" {url_netlocs[0]}"
        else:
            add_last_path = True

    # print(netlocs)

    url_path = url_info.path
    _url_paths = url_path.split("/")
    url_paths = []
    for u_p in _url_paths:
        if u_p != '':
            url_paths.append(u_p)
    # print(url_paths)

    path_keywords = [
        "posts",  # maybe someone's blog
        "article",
        "articles",
        "docs",
        "product",  # maybe product in a company
        "products",
        "releases",
        "library",
        "blogs",
        "blog"
    ]

    for path in url_paths:
        if path in path_keywords or len(url_netlocs) == 2 or add_last_path:
            # last path may be the most important path
            important_path = url_paths[-1]
            if important_path.endswith(".html"):
                important_path = important_path.replace(".html", "").replace(".htm", "")

            ignore_path_titles = ["introduction",'index']
            if important_path not in ignore_path_titles:
                url_title += f" {important_path}"
            break
    
    url_title = unquote(url_title)
    return f"[{url_title}]({url})"


def is_ip_address(ip: str):
    pattern = re.compile(
        r"(?:^https?://localhost(:\d+)?/?$)|(?:^https?://(\d+\.){3}\d+(:\d+)?/?$)"
    )
    if pattern.match(ip):
        return True
    else:
        return False