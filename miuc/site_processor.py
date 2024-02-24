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
import urllib
import json
from .utils import guess_name_by_url
from re import Match
from urllib.parse import unquote

DEBUG = True


class Error(Exception):
    def __init__(self, url: str, class_name: str, message: str = None) -> None:  # pragma: no cover
        super().__init__()
        self.url = url
        self.class_name = class_name
        self.message = message


class Processor:
    def __init__(self, max_time_limit: int = 5) -> None:
        self.class_name = self.__class__.__name__
        self._url = None
        self.max_time_limit = max_time_limit
        self.urls_re = [
            # ...
        ]
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept-Encoding": "gzip",
            "Connection": "keep-alive",
            "Content-Type": "text/html;charset=utf-8",
        }

        self.article_name = None

    def __call__(self, url: str):
        self._url: str = url
        if len(self.urls_re) == 0:  # pragma: no cover
            self.error("finish urls_re in your processor class")
        for url_re in self.urls_re:
            res = re.compile(url_re).match(self._url)
            if res:
                self.parse(res)
                break
        title = unquote(self.format())
        if title is None or title == "":  # pragma: no cover
            return guess_name_by_url(self._url)
        return f"[{title}]({self._url})"

    def parse(self, res: Match) -> str:  # pragma: no cover
        """
        override this function for a specific site processor

        parse the url
        """
        raise NotImplementedError(self.class_name + "should override parse function")

    def format(self) -> str:  # pragma: no cover
        """
        override this function for a specific site processor

        return title
        """
        raise NotImplementedError(self.class_name + "should override parse function")

    def error(self, msg: str = None):  # pragma: no cover
        """
        call this function if mismatch
        """
        # print(self.url)
        raise Error(self._url, self.class_name, message=msg)

    def get_html(self):
        """
        call this function if could not parse only by url
        """
        response = requests.get(self._url, headers=self.headers, timeout=self.max_time_limit)
        if response.status_code != 200:
            self.error(f"connect {self._url} failed: status code [{response.status_code}]")  # pragma: no cover
        return response.text

    def get_element_match(self, pattern: re.Pattern, flags=0) -> str:
        html = self.get_html()
        self._debug(html)
        return re.compile(pattern, flags).search(html).group(1).strip()

    def _debug(self, html):  # pragma: no cover
        """
        only work for me to debug
        """
        if DEBUG:
            with open("a.html", "w", encoding="utf-8") as f:
                f.write(html)


class Github(Processor):
    # https://github.com/microsoft/vscode

    def __init__(self, max_time_limit: int = 5) -> None:
        super().__init__(max_time_limit)

        self.site = "Github"
        self.user_name = None
        self.repo_name = None
        self.repo_function = None  # issues | pull | actions
        self.repo_function_name = None  # issue name
        self.branch_name = None
        self.file_name = None
        self.tab_name = None
        self.routine = None
        self.search_name = None

        self.urls_re = [
            r"^https://github\.com/?$",
            r"^https://github\.com/(?P<user>[^/]*?)\?tab=(?P<tab>.*?)/?$",
            r"^https://github\.com/(?P<user>[^/\?]*?)$/?",
            r"^https://github\.com/(?P<user>[^/]*?)/(?P<repo>[^/]*?)/?$",
            r"^https://github\.com/(?P<user>[^/]*?)/(?P<repo>[^/]*?)/blob/(?P<branch>[^/]*?)/?(?P<file>.*?)?/?$",
            r"^https://github\.com/(?P<user>[^/]*?)/(?P<repo>[^/]*?)/files/(?P<branch>[^/]*?)/?(?P<file>.*?)?/?$",
            r"^https://github\.com/(?P<user>[^/]*?)/(?P<repo>[^/]*?)/tree/(?P<branch>[^/]*?)/?(?P<file>.*?)?/?$",
            r"^https://github\.com/(?P<user>[^/]*?)/(?P<repo>[^/]*?)/commits?/(?P<commit>.*)$",
            r"^https://github\.com/(?P<user>[^/]*?)/(?P<repo>[^/]*?)/(?P<function>[^/\?]*?)/?$",
            r"^https://github\.com/(?P<user>[^/]*?)/(?P<repo>[^/]*?)/(?P<function>[^/]*?)\?.*$",
            r"^https://github\.com/(?P<user>[^/]*?)/(?P<repo>[^/]*?)/(?P<function>[^/]*?)/(?P<routine>.*?)(?:#.*)?$",
            r"^https://github\.com/search\?q=(?P<search>.*?)((&.*)|(:.*))?/?$",
        ]

        # "https://github.com/{user}"
        # "https://github.com/{user}/{repo}"
        # "https://github.com/{user}/{repo}/blob/{branch}/({folder_name}/)?{file_name}"
        # "https://github.com/{user}/{repo}/tree/{branch}"
        # "https://github.com/{user}/{repo}/tree/{branch}/({folder_name}/)?{file_name}"
        # https://github.com/fadedzipper/zCore-Tutorial/blob/dev/docs/book.toml

    def parse(self, res: re.Match) -> str:
        if "user" in res.groupdict():
            self.user_name = res.group("user")
        if "repo" in res.groupdict():
            self.repo_name = res.group("repo")
            if "commit" in res.groupdict("commit"):
                self.repo_name += " commit"
        if "function" in res.groupdict():
            self.repo_function = res.group("function")
            if "routine" in res.groupdict():
                self.routine = res.group("routine")
                has_id = self.routine.split("/")[0].isdigit()
                if has_id:
                    # for issue and pull
                    pattern = r'<bdi class="js-issue-title markdown-title">(.*?)</bdi>'
                    self.repo_function_name = self.get_element_match(pattern)
                else:
                    self.repo_function_name = self.routine.split("/")[-1]
        if "branch" in res.groupdict():
            self.branch_name = res.group("branch")
        if "file" in res.groupdict():
            self.file_name = res.group("file").split("/")[-1]
            # remove README.md -> README
            ignore_file_exts = [".md", ".txt"]
            for ext in ignore_file_exts:
                if self.file_name.endswith(ext):
                    self.file_name = self.file_name[: -len(ext)]
                    break
        if "tab" in res.groupdict():
            self.tab_name = res.group("tab")
        if "search" in res.groupdict():
            self.search_name = res.group("search")

    def format(self):
        if self.repo_name is None and self.user_name is None:
            title = self.site
        title = ""
        if self.repo_name:
            title = self.repo_name
            if self.repo_function:
                title += f" {self.repo_function}"
                if self.repo_function_name:
                    title = self.repo_function_name
            elif self.file_name:
                title += f" {self.file_name}"
        else:
            title = self.user_name
            if self.tab_name:
                title += f" {self.tab_name}"
        if self.search_name:
            title = f"{self.site} search {self.search_name}"

        return title


class Githubio(Processor):
    """
    most likely one's blog or github page document site
    """

    def __init__(self, max_time_limit: int = 5) -> None:
        super().__init__(max_time_limit)
        self.user_name = None
        self.repo_name = None
        self.routine = None

        self.urls_re = [
            r"^https://(?P<user>.*?)\.github\.io/?$",  # blog / resume
            r"^https://(?P<user>.*?)\.github\.io/(?P<repo>.*?)/(?P<routine>.+?)/?$",
            r"^https://(?P<user>.*?)\.github\.io/(?P<repo>.*?)/?$",  # github repo
        ]

    def parse(self, res: Match) -> str:

        if "user" in res.groupdict():
            self.user_name = res.group("user")
        if "repo" in res.groupdict():
            self.repo_name = res.group("repo")
        if "routine" in res.groupdict():
            origin_routines = res.group("routine").split("/")
            ignore_rountines = ["index.html", "index.htm", "#"]
            article_name = origin_routines[-1]
            if article_name in ignore_rountines:
                article_name = origin_routines[-2]
            self.routine = article_name

    def format(self):
        if self.repo_name is None:
            title = f"{self.user_name}'s blog"
        else:
            if self.routine is None:
                title = f"{self.repo_name} document"
            else:
                title = self.routine
        return title


class Stackoverflow(Processor):
    def __init__(self, max_time_limit: int = 5) -> None:
        super().__init__(max_time_limit)
        self.site = "stackoverflow"

        self.type_name = None
        self.id = None
        self.tag_name = None
        self.user_name = None

        self.question_name = None
        self.is_answer = False

        self.urls_re = [
            r"^https://stackoverflow\.com/?$",
            r"^https://stackoverflow\.com/(?P<type>[^/]*?)/tagged/(?P<tag>.*?)/?$",
            r"^https://stackoverflow\.com/(?P<type>[^/]*?)/(?P<id>[^/]*?)/(?P<question>.*?)/?$",
        ]

        # https://stackoverflow.com/questions/tagged/python
        # https://stackoverflow.com/users/5740428/jan-schultke

    def parse(self, res: Match) -> str:
        if "type" not in res.groupdict():
            # pure https://stackoverflow.com/
            return
        self.type_name = res.group("type")
        if self.type_name == "q" or self.type_name == "questions":
            if "tag" in res.groupdict():
                self.tag_name = res.group("tag")
                return

            if "id" in res.groupdict():
                self.id = res.group("id")
            if "question" in res.groupdict():
                # stackoverflow question name use `-` to replace ' '
                self.question_name = res.group("question").replace("-", " ")

            if self.question_name is None or self.question_name.isdigit():
                # could not get question name from url
                pattern = r'<a .*class="question-hyperlink">(.*?)</a>'
                self.question_name = self.get_element_match(pattern)
        elif self.type_name == "a":
            # answer
            # https://stackoverflow.com/a/601989/17869889

            pattern = r'<a .*class="question-hyperlink">(.*?)</a>'
            self.question_name = self.get_element_match(pattern)
            self.is_answer = True
        elif self.type_name == "users":
            # https://stackoverflow.com/users/5740428/jan-schultke
            self.user_name = res.group("question")
        else:
            self.error("unknown type")  # pragma: no cover
        return

    def format(self):
        title = ""
        if self.question_name:
            title = self.question_name
            if self.is_answer:
                title += " [answer]"
        elif self.tag_name:
            title = f"{self.tag_name} tag"
        elif self.user_name:
            title = f"{self.user_name}"
        else:
            # pure https://stackoverflow.com/
            title = self.site

        return title


class Youtube(Processor):
    def __init__(self, max_time_limit: int = 5) -> None:
        super().__init__(max_time_limit)
        self.site = "youtube"
        self.user_name = None
        self.video_name = None
        self.urls_re = [
            r"^https://www\.youtube\.com/?$",
            r"^https://www\.youtube\.com/\@(?P<user>.*?)/?$",
            r"^https://www\.youtube\.com/\@(?P<user>.*?)/.*$",
            r"^https://www\.youtube\.com/watch\?v=(?P<id>.*?)/?$",
            r"^https://youtu\.be/(?P<id>.*?)/?",
            r"^https://www\.youtube\.com/playlist\?list=(?P<list>.*?)",
        ]

        # https://www.youtube.com/watch?v=ErV-2tlf9Ls

    def _get_youtube_title(self):
        # could not directly get youtube video title, instead use the following method
        # https://stackoverflow.com/a/52664178/17869889

        params = {"format": "json", "url": self._url}
        url = f"https://www.youtube.com/oembed?{urllib.parse.urlencode(params)}"
        response = requests.get(url, timeout=self.max_time_limit)
        data = json.loads(response.text)
        return data["title"]

    def parse(self, res: Match) -> str:
        if "user" in res.groupdict():
            self.user_name = res.group("user")
        if "id" in res.groupdict():
            self.video_name = self._get_youtube_title()
        if "list" in res.groupdict():
            self.video_name = self._get_youtube_title()

    def format(self):
        if self.user_name is None and self.video_name is None:
            # pure youtube
            title = self.site
        else:
            if self.video_name is not None:
                title = self.video_name
            if self.user_name is not None:
                title = self.user_name

        return title


class Zhihu(Processor):
    def __init__(self, max_time_limit: int = 5) -> None:
        super().__init__(max_time_limit)
        self.site = "知乎"
        self.type_name = None
        self.title = None

        self.urls_re = [
            r"(?P<site>^https://www\.zhihu\.com)/?$",
            r"^https://www\.zhihu\.com/question/\d+/(?P<type>.*?)/(?P<id>.*?)/?$",
            r"^https://www\.zhihu\.com/(?P<type>.*?)/(?P<id>.*?)/(?P<sub_type>.*?)/?$",
            r"^https://www\.zhihu\.com/(?P<type>.*?)/(?P<id>.*?)/?$",
            r"^https://zhuanlan\.zhihu\.com/(?P<type>.*?)/(?P<id>.*?)/?$",
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
        # Y不动点组合子用在哪里? - RednaxelaFX的回答 - 知乎
        #

        # https://www.zhihu.com/collection/86788003

    def parse(self, res: Match) -> str:
        if "site" in res.groupdict():
            self.title = self.site
            return
        self.type_name = res.group("type")

        # following parse need page html elements

        if self.type_name == "question":
            # https://www.zhihu.com/question/446988424
            pattern = r'<h1 class="QuestionHeader-title">(.*?)</h1>'
            self.title = self.get_element_match(pattern)
        elif self.type_name == "p":
            # https://zhuanlan.zhihu.com/p/347552573
            pattern = r'<h1 class="Post-Title">(.*?)</h1>'
            self.title = self.get_element_match(pattern)
        elif self.type_name == "answer":
            # https://www.zhihu.com/question/21099081/answer/119347251
            # https://www.zhihu.com/question/367357782/answer/3066947505 Anonymous user
            pattern = r'<h1 class="QuestionHeader-title">(.*?)</h1>'
            self.title = self.get_element_match(pattern) + "的回答"
        elif self.type_name == "people":
            # https://www.zhihu.com/people/hinus

            pattern = r'<span class="ProfileHeader-name">(.*?)</span'
            # sometimes there will be <style ...> inside, remove it
            user_name = re.sub(r"<style.*>", "", self.get_element_match(pattern))
            self.title = user_name + "的主页"
            if "sub_type" in res.groupdict():
                # https://www.zhihu.com/people/hinus/collections
                self.title = f'{user_name}的{self.sub_types[res.group("sub_type")]}'
        elif self.type_name == "collection":
            # https://www.zhihu.com/collection/86788003
            pattern = r'<div class="CollectionDetailPageHeader-title">(.*?)</div>'
            self.title = self.get_element_match(pattern) + " 收藏夹"
        elif self.type_name == "column":
            # https://www.zhihu.com/column/hinus
            pattern = r'<div class="css-zyehvu">(.*?)</div>'
            self.title = self.get_element_match(pattern) + " 专栏"

    def format(self):
        return self.title


class Bilibili(Processor):
    def __init__(self, max_time_limit: int = 5) -> None:
        super().__init__(max_time_limit)
        self.site = "bilibli"
        self.type_name = None
        self.id = None
        self.name = None

        self.urls_re = [
            r"(?P<site>^https://www\.bilibili\.com)/?$",
            r"^https://www\.bilibili\.com/(?P<type>.*?)/(?P<id>.*?)\?.*$",
            r"^https://www\.bilibili\.com/(?P<type>.*?)/(?P<id>.*)$",
            r"^https://(?P<type>space)\.bilibili\.com/(?P<id>.*?)(\?.*)?/?$",
        ]

        # https://www.bilibili.com/video/BV1ah4y1X73M
        # https://www.bilibili.com/opus/806593844580712449?spm_id_from=333.999.0.0
        # https://www.bilibili.com/read/cv23285665?spm_id_from=333.999.0.0

    def parse(self, res: Match) -> str:
        if "site" in res.groupdict():
            return
        self.type_name = res.group("type")
        self.id = res.group("id")
        # bilibili url often following with "spm_id_from=333.999.0.0 ..."
        # clean the url
        if self.type_name != "space":
            self._url = f"https://www.bilibili.com/{self.type_name}/{self.id}"
        else:
            self._url = f"https://space.bilibili.com/{self.id}"

        if self.type_name == "video":
            pattern = r"<h1 .*>(.*?)</h1>"
            self._url = f'https://www.bilibili.com/video/{self.id}'
            self.name = self.get_element_match(pattern)
        elif self.type_name == "opus":
            pass
        elif self.type_name == "read":
            pattern = r'<title data-vue-meta="true">(.*?)</title>'
            self.name = self.get_element_match(pattern).replace(" - 哔哩哔哩", "")
        elif self.type_name == "space":
            pattern = r"<title>(.*?)的个人空间.*</title>"
            self.name = self.get_element_match(pattern)

    def format(self):
        if self.type_name is None:
            # pure bilibili
            title = self.site
        else:
            if self.type_name == "video" or self.type_name == "space":
                title = self.name
            elif self.type_name == "opus":
                title = f"B站动态"
            elif self.type_name == "read":
                title = f"{self.name} 专栏"
            else:
                self.error("unknown type")  # pragma: no cover

        return title


class CSDN(Processor):
    def __init__(self, max_time_limit: int = 5) -> None:
        super().__init__(max_time_limit)
        self.site = "csdn"
        self.user_id = None
        self.user_name = None
        self.article_id = None
        self.article_name = None

        self.urls_re = [
            r"(?P<site>^https://blog\.csdn\.net)/?$",
            r"^https://blog\.csdn\.net/(?P<user_id>.*?)/(?P<category>.*?)\.html$",
            r"^https://blog\.csdn\.net/(?P<user_id>.*?)\?type=.*$",
            r"^https://blog\.csdn\.net/(?P<user_id>.*?)/article/details/(?P<article_id>.*?)\?.*$",
            r"^https://blog\.csdn\.net/(?P<user_id>.*?)/article/details/(?P<article_id>.*?)$",
            r"^http://t\.csdn\.cn/(?P<short_id>.*?)$",
        ]

    def parse(self, res: Match) -> str:
        if "site" in res.groupdict():
            return

        # self._debug(html)

        if "article_id" in res.groupdict():
            self.user_id = res.group("user_id")
            self.article_id = res.group("article_id")
            # clean the url
            self._url = f"https://blog.csdn.net/{self.user_id}/article/details/{self.article_id}"
            pattern = r'<h1 class="title-article" id="articleContentId">(.*?)</h1>'
            self.article_name = self.get_element_match(pattern)
        elif "category" in res.groupdict():
            pattern = r'<h3 class="column_title oneline" title=.*>(.*?)</h3>'
            self.article_name = self.get_element_match(pattern)
        elif "short_id" in res.groupdict():
            # for short url

            pattern = r'<meta name="keywords" content="(.*?)">'
            self.article_name = self.get_element_match(pattern)
        else:
            # for user home page
            pattern = r'data-nickname="(.*?)"'
            self.user_name = self.get_element_match(pattern)

    def format(self) -> str:
        if self.user_name is None and self.article_name is None:
            title = self.site
        else:
            if self.article_name:
                title = self.article_name
            else:
                title = self.user_name
        return title


class Githubusercontent(Processor):
    def __init__(self, max_time_limit: int = 5) -> None:
        super().__init__(max_time_limit)

        self.urls_re = [r"^https://raw\.githubusercontent\.com.*$"]

    def parse(self, res: Match) -> str:
        return

    def format(self):
        return "image"


class CNblog(Processor):
    def __init__(self, max_time_limit: int = 5) -> None:
        super().__init__(max_time_limit)
        self.site = "博客园"
        self.author_name = None
        self.article_name = None

        self.urls_re = [
            r"(?P<site>^https://www\.cnblogs\.com)/?$",
            r"^https://www\.cnblogs\.com/(?P<author>.*?)/p/(?P<article>.*?)/?$",
            r"^https://www\.cnblogs\.com/(?P<archive>.*?)/archive/.*$",
            r"^https://www\.cnblogs\.com/(?P<author>.*?)/?$",
        ]

    def parse(self, res: Match) -> str:
        if "site" in res.groupdict():
            return

        if "article" in res.groupdict():
            pattern = r'<span role="heading" aria-level="2">(.*?)</span>'
            self.article_name = self.get_element_match(pattern)
        elif "archive" in res.groupdict():
            pattern = r'<span role="heading" aria-level="2">(.*?)</span>'
            self.article_name = self.get_element_match(pattern)
        elif "author" in res.groupdict():
            # only author
            pattern = re.compile(
                r'<a id="Header1_HeaderTitle" class="headermaintitle HeaderMainTitle" href="https://www.cnblogs.com/.*">(.*?)</a>'
            )
            self.author_name = self.get_element_match(pattern)

    def format(self):
        if self.author_name is None and self.article_name is None:
            title = self.site
        else:
            if self.article_name:
                title = self.article_name
            else:
                title = self.author_name

        return title


class Jianshu(Processor):
    def __init__(self, max_time_limit: int = 5) -> None:
        super().__init__(max_time_limit)
        self.site = "简书"
        self.article_name = None
        self.user_name = None

        self.urls_re = [
            r"(?P<site>^https://www\.jianshu\.com)/?$",
            r"^https://www\.jianshu\.com/p/(?P<article>.*?)/?$",
            r"^https://www\.jianshu\.com/u/(?P<user>.*?)/?$",
        ]

    def parse(self, res: Match) -> str:
        if "site" in res.groupdict():
            return

        if "article" in res.groupdict():
            pattern = r'<h1 class="_1RuRku">(.*?)</h1>'
            self.article_name = self.get_element_match(pattern)
        if "user" in res.groupdict():
            pattern = r'<a class="name" href=.*?>(.*?)</a>'
            self.user_name = self.get_element_match(pattern)

    def format(self):
        title = self.site
        if self.article_name:
            title = self.article_name
        elif self.user_name:
            title = self.user_name
        return title


class TecentCloud(Processor):
    def __init__(self, max_time_limit: int = 5) -> None:
        super().__init__(max_time_limit)
        self.site = "tencent cloud"
        self.article_name = None
        self.user_name = None

        self.urls_re = [
            r"(?P<site>^https://cloud.tencent.com)/?$",
            r"^https://cloud.tencent.com/developer/article/(?P<article>.*?)/?$",
            r"^https://cloud.tencent.com/developer/user/(?P<user>.*?)/?$",
        ]

    def parse(self, res: Match) -> str:
        if "site" in res.groupdict():
            return

        if "article" in res.groupdict():
            pattern = r'<h2 class="title-text">(.*?)</h2>'
            self.article_name = self.get_element_match(pattern, flags=re.S)
        elif "user" in res.groupdict():
            pattern = r'<h3 class="uc-hero-name">(.*?)</h3>'
            self.user_name = self.get_element_match(pattern)

    def format(self):
        title = self.site

        if self.article_name:
            title = self.article_name
        elif self.user_name:
            title = self.user_name

        return title


class Douban(Processor):
    def __init__(self, max_time_limit: int = 5) -> None:
        super().__init__(max_time_limit)
        self.site = "豆瓣"
        self.book_name = None

        self.urls_re = [
            r"(?P<site>https://book\.douban\.com)/?$",
            r"^https://book\.douban\.com/subject/(?P<id>.*?)(\?.*)?/?$",
        ]

    def parse(self, res: Match) -> str:
        if "site" in res.groupdict():
            return

        pattern = r'<span property="v:itemreviewed">(.*?)</span>'
        self.book_name = self.get_element_match(pattern)

    def format(self):
        title = self.site
        if self.book_name:
            title = self.book_name

        return title


class Juejin(Processor):
    def __init__(self, max_time_limit: int = 5) -> None:
        super().__init__(max_time_limit)
        self.site = "掘金"
        self.article_name = None

        self.urls_re = [
            r"(?P<site>^https://juejin\.cn/?)$",
            r"^https://juejin\.cn/post/(?P<post_id>.*)/?$",
        ]

    def parse(self, res: Match) -> str:
        if "site" in res.groupdict():
            return
        if "post_id" in res.groupdict():
            pattern = re.compile(r"<title>(.*?) - 掘金</title>")
            self.article_name = self.get_element_match(pattern)

    def format(self):
        title = self.site
        if self.article_name:
            title = self.article_name

        return title


class Wiki(Processor):
    def __init__(self, max_time_limit: int = 5) -> None:
        super().__init__(max_time_limit)
        self.site = "wikipedia"
        self.article_name = None

        self.urls_re = [r"^https://en\.wikipedia\.org/wiki/(?P<name>.*)/?$"]

    def parse(self, res: Match) -> str:
        self.article_name = res.group("name").replace("_", " ")

    def format(self):
        title = self.site
        if self.article_name:
            title = self.article_name

        return title


class Weixin(Processor):
    def __init__(self, max_time_limit: int = 5) -> None:
        super().__init__(max_time_limit)
        self.site = "微信公众号"
        self.article_name = None
        self.urls_re = [r"^https://mp\.weixin\.qq\.com/s/(?P<id>.*?)/?$"]

    def parse(self, res: Match) -> str:
        pattern = r'<h1 class="rich_media_title " id="activity-name">(.*?)</h1>'
        self.article_name = self.get_element_match(pattern, re.S).strip()

    def format(self):
        title = self.site
        if self.article_name:
            title = self.article_name
        return title


class Geeksforgeeks(Processor):
    def __init__(self, max_time_limit: int = 5) -> None:
        super().__init__(max_time_limit)
        self.article_name = None
        self.site = "geeksforgeeks"

        self.urls_re = [r"https://www\.geeksforgeeks\.org/(?P<article>.*?)/?$"]

    def parse(self, res: Match) -> str:
        self.article_name = res.group("article").replace("-", " ")

    def format(self) -> str:
        title = self.site
        if self.article_name:
            title = self.article_name

        return title


class SourceForge(Processor):
    def __init__(self, max_time_limit: int = 5) -> None:
        super().__init__(max_time_limit)
        self.site = "sourceforge"
        self.title = None
        self.is_download = False

        self.urls_re = [r"^https://sourceforge\.net/projects/(?P<id>.*?)(/download)?/?$"]

    def parse(self, res: Match) -> str:
        download_exts = [
            ".zip",
            ".rar",
            ".7z",
            ".tar",
            ".gz",
            ".tgz",
            ".bz2",
            ".xz",
            ".exe",
            ".dmg",
            ".iso",
            ".apk",
            ".deb",
            ".rpm",
            ".jar",
            ".tar.gz",
            ".tar.bz2",
            ".tar.xz",
            ".tar.Z",
            ".sit",
            ".sitx",
            ".z",
            ".gz",
            ".bz2",
            ".xz",
            ".sig",
            ".asc",
        ]
        file_path: str = res.group("id")

        for ext in download_exts:
            if file_path.endswith(ext):
                self.is_download = True
                break
        if self.is_download:
            self.title = file_path.split("/")[-1]
        else:
            pattern = r"<h1 .*?>(.*?)\n</h1>"
            self.title = self.get_element_match(pattern)

    def format(self) -> str:
        title = self.site
        if self.title:
            title = self.title
        return title


class VscodeExtension(Processor):
    def __init__(self, max_time_limit: int = 5) -> None:
        super().__init__(max_time_limit)
        self.site = "vscode extension"
        self.author_name = None
        self.extension_name = None

        self.urls_re = [
            r"^https://marketplace\.visualstudio\.com/items\?itemName=(?P<author>.*?)\.(?P<extension_name>.*?)/?$"
        ]

    def parse(self, res: Match) -> str:
        self.author_name = res.group("author")
        self.extension_name = res.group("extension_name")

    def format(self) -> str:
        title = self.site
        if self.extension_name:
            title = "vscode " + self.extension_name
        return title


class InfoQ(Processor):
    def __init__(self, max_time_limit: int = 5) -> None:
        super().__init__(max_time_limit)
        self.site = "InfoQ"
        self.article_name = None

        self.urls_re = [r"^https://xie\.infoq\.cn/article/(?P<id>.*?)/?$"]

    def parse(self, res: Match) -> str:
        pattern = r"<title>(.*?)_.*?</title>"
        self.article_name = self.get_element_match(pattern)

    def format(self) -> str:
        title = self.site
        if self.article_name:
            title = self.article_name

        return title


class CTO51(Processor):
    def __init__(self, max_time_limit: int = 5) -> None:
        super().__init__(max_time_limit)

        self.site = "51CTO"
        self.article_name = None

        self.urls_re = [r"^https://www\.51cto\.com/article/(?P<id>.*?)/?$"]

    def parse(self, res: Match) -> str:
        pattern = r"<h1>(.*?)</h1>"
        self.article_name = self.get_element_match(pattern)

    def format(self) -> str:
        title = self.site
        if self.article_name:
            title = self.article_name

        return title


class Souhu(Processor):

    def __init__(self, max_time_limit: int = 5) -> None:
        super().__init__(max_time_limit)
        self.site = "souhu"

        self.urls_re = [r"^https://www\.sohu\.com/a/(?P<id>.*?)/?$"]

    def parse(self, res: Match) -> str:

        pattern = r"<title>(.*?)_.*?</title>"
        self.article_name = self.get_element_match(pattern).strip()

    def format(self) -> str:

        title = self.site
        if self.article_name:
            title = self.article_name

        return title

