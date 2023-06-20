"""
*Copyright (c) 2023 All rights reserved
*@description: page processors for specific sites
*@author: Zhixing Lu
*@date: 2023-06-20
*@email: luzhixing12345@163.com
*@Github: luzhixing12345
"""

import re
import requests


class Error(Exception):
    def __init__(self, url: str, class_name: str, message: str = None) -> None:
        super().__init__()
        self.url = url
        self.class_name = class_name
        self.message = message


class Processor:
    def __init__(self, formatting_title: str) -> None:
        self.class_name = self.__class__.__name__
        self.formatting_title = formatting_title
        self.url = None

    def __call__(self, url: str):
        self.url: str = url
        self.parse()
        return self.format()

    def parse(self) -> str:
        """
        override this function for a specific site processor

        parse the url
        """
        raise NotImplementedError(self.class_name + "should override parse function")

    def format(self):
        """
        override this function for a specific site processor
        """
        return f"[unknown]({self.url})"

    def error(self, msg: str = None):
        """
        call this function if mismatch
        """
        raise Error(self.url, self.class_name, message=msg)

    def get_html(self):
        """
        call this function if could not parse only by url
        """
        response = requests.get(self.url)
        if response.status_code != 200:
            self.error(f"connect {self.url} failed: status code [{response.status_code}]")
        return response.text


class GithubProcessor(Processor):
    # https://github.com/microsoft/vscode

    def __init__(self, formatting_title: str) -> None:
        super().__init__(formatting_title)

        self.site = "Github"
        self.user_name = None
        self.repo_name = None
        self.branch_name = None
        self.file_name = None

        self.urls_re = [
            re.compile(r"^https://github.com/$"),
            re.compile(r"^https://github.com/(?P<user>[^/]*?)/?$"),
            re.compile(r"https://github.com/(?P<user>[^/]*?)/(?P<repo>[^/]*?)/?$"),
            re.compile(
                r"https://github.com/(?P<user>[^/]*?)/(?P<repo>[^/]*?)/blob/(?P<branch>)/(?P<file>[^/]*?)?/?$"
            ),
            re.compile(
                r"https://github.com/(?P<user>[^/]*?)/(?P<repo>[^/]*?)/tree/(?P<branch>)/(?P<file>[^/]*?)?/?$"
            ),
        ]

        # "https://github.com/{user}"
        # "https://github.com/{user}/{repo}"
        # "https://github.com/{user}/{repo}/blob/{branch}/({folder_name}/)?{file_name}"
        # "https://github.com/{user}/{repo}/tree/{branch}"
        # "https://github.com/{user}/{repo}/tree/{branch}/({folder_name}/)?{file_name}"

    def parse(self) -> str:
        for url_re in self.urls_re:
            res = url_re.match(self.url)
            if res:
                if "user" in res.groupdict():
                    self.user_name = res.group("user")
                if "repo" in res.groupdict():
                    self.repo_name = res.group("repo")
                if "branch" in res.groupdict():
                    self.branch_name = res.group("branch")
                if "file" in res.groupdict():
                    self.file_name = res.group("file").split("/")[-1]
                return

        # should never reach here
        self.error()

    def format(self):
        if self.repo_name:
            name = self.repo_name
        else:
            name = self.user_name
        title = self.formatting_title.replace("<site>", self.site).replace("<title>", name)
        return f"[{title}]({self.url})"


class StackoverflowProcessor(Processor):
    ...


class ZhihuProcessor(Processor):
    def __init__(self, formatting_title: str) -> None:
        super().__init__(formatting_title)
        self.site = "Zhihu"
        self.type_name = None
        self.title = None

        self.urls_re = [
            re.compile(r"^https://www.zhihu.com/question/\d+/(?P<type>.*?)/(?P<id>.*?)/?$"),
            re.compile(r"^https://www.zhihu.com/(?P<type>.*?)/(?P<id>.*?)/(?P<sub_type>.*?)/?$"),
            re.compile(r"^https://www.zhihu.com/(?P<type>.*?)/(?P<id>.*?)/?$"),
            re.compile(r"^https://zhuanlan.zhihu.com/(?P<type>.*?)/(?P<id>.*?)/?$"),
        ]

        self.sub_types = {
            "answers": "回答",
            "zvideos": "视频",
            "asks": "提问",
            "posts": "文章",
            "columns": "专栏",
            "pins": "想法",
            "collections": "收藏",
            "following": "关注",
        }

        # https://zhuanlan.zhihu.com/p/347552573
        # https://www.zhihu.com/question/21099081/answer/18830200
        # Y不动点组合子用在哪里？ - RednaxelaFX的回答 - 知乎
        #

        # https://www.zhihu.com/collection/86788003

    def parse(self) -> str:
        html = self.get_html()

        for url_re in self.urls_re:
            res = url_re.match(self.url)
            if res:
                self.type_name = res.group("type")
                if self.type_name == "question":
                    # https://www.zhihu.com/question/446988424
                    pattern = re.compile(r'<h1 class="QuestionHeader-title">(.*?)</h1>')
                    self.title = pattern.search(html).group(1)
                elif self.type_name == "p":
                    # https://zhuanlan.zhihu.com/p/347552573
                    pattern = re.compile(r'<h1 class="Post-Title">(.*?)</h1>')
                    self.title = pattern.search(html).group(1)
                elif self.type_name == "answer":
                    # https://www.zhihu.com/question/21099081/answer/119347251
                    pattern = re.compile(
                        r'<a .*target="_blank" class="UserLink-link" data-za-detail-view-element_name="User">(.*?)</a>'
                    )
                    self.title = pattern.search(html).group(1) + "的回答"
                elif self.type_name == "people":
                    # https://www.zhihu.com/people/hinus
                    pattern = re.compile(r'<span class="ProfileHeader-name">(.*?)</span>')
                    self.title = pattern.search(html).group(1) + "的主页"
                    if "sub_type" in res.groupdict():
                        # https://www.zhihu.com/people/hinus/collections
                        self.title = f'{res.group("id")}的{self.sub_types[res.group("sub_type")]}'
                elif self.type_name == 'collection':
                    pattern = re.compile(r'<div class="CollectionDetailPageHeader-title">(.*?)</div>')
                    self.title = pattern.search(html).group(1) + " 收藏夹"
                else:
                    self.error()
                return

        self.error()

    def format(self):
        return f"[{self.title}]({self.url})"
