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
    def __init__(self, url: str, class_name: str, message: str = None) -> None:  # pragma: no cover
        super().__init__()
        self.url = url
        self.class_name = class_name
        self.message = message


class Processor:
    def __init__(self, formatting_title: str) -> None:
        self.class_name = self.__class__.__name__
        self.formatting_title = formatting_title
        self.url = None
        self.max_title_length = 50

    def __call__(self, url: str):
        self.url: str = url
        self.parse()
        title = self.format()
        assert (
            len(title) < self.max_title_length + 10
        ), f"title too long > {self.max_title_length}, use abbreviation\ntitle = [{title}]"
        return f"[{title}]({self.url})"

    def parse(self) -> str:  # pragma: no cover
        """
        override this function for a specific site processor

        parse the url
        """
        raise NotImplementedError(self.class_name + "should override parse function")

    def format(self):  # pragma: no cover
        """
        override this function for a specific site processor

        return title
        """
        return "[unknown]"

    def error(self, msg: str = None):  # pragma: no cover
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
        self.tab_name = None

        self.urls_re = [
            re.compile(r"^https://github\.com/?$"),
            re.compile(r"^https://github\.com/(?P<user>[^/]*?)\?tab=(?P<tab>.*?)/?$"),
            re.compile(r"^https://github\.com/(?P<user>[^/]*?)/?$"),
            re.compile(r"^https://github\.com/(?P<user>[^/]*?)/(?P<repo>[^/]*?)/?$"),
            re.compile(
                r"^https://github.com/(?P<user>[^/]*?)/(?P<repo>[^/]*?)/blob/(?P<branch>[^/]*?)/?(?P<file>.*?)?/?$"
            ),
            re.compile(
                r"^https://github\.com/(?P<user>[^/]*?)/(?P<repo>[^/]*?)/tree/(?P<branch>[^/]*?)/?(?P<file>.*?)?/?$"
            ),
        ]

        # "https://github.com/{user}"
        # "https://github.com/{user}/{repo}"
        # "https://github.com/{user}/{repo}/blob/{branch}/({folder_name}/)?{file_name}"
        # "https://github.com/{user}/{repo}/tree/{branch}"
        # "https://github.com/{user}/{repo}/tree/{branch}/({folder_name}/)?{file_name}"
        # https://github.com/fadedzipper/zCore-Tutorial/blob/dev/docs/book.toml

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
                if "tab" in res.groupdict():
                    self.tab_name = res.group("tab")
                return

        # should never reach here
        self.error()  # pragma: no cover

    def format(self):
        if self.repo_name is None and self.user_name is None:
            return f"[{self.site}]({self.url})"

        if self.repo_name:
            name = self.repo_name
            if self.file_name:
                name += f" {self.file_name}"
        else:
            name = self.user_name
            if self.tab_name:
                name += f" {self.tab_name}"

        title = self.formatting_title.replace("<site>", self.site).replace("<title>", name)
        return title


class StackoverflowProcessor(Processor):
    def __init__(self, formatting_title: str) -> None:
        super().__init__(formatting_title)
        self.site = "stackoverflow"

        self.type_name = None
        self.id = None
        self.tag_name = None
        self.user_name = None

        self.question_name = None
        self.is_answer = False

        self.urls_re = [
            re.compile(r"^https://stackoverflow\.com/?$"),
            re.compile(r"^https://stackoverflow\.com/(?P<type>[^/]*?)/tagged/(?P<tag>.*?)/?$"),
            re.compile(
                r"^https://stackoverflow\.com/(?P<type>[^/]*?)/(?P<id>[^/]*?)/(?P<question>.*?)/?$"
            ),
        ]

        # https://stackoverflow.com/questions/tagged/python
        # https://stackoverflow.com/users/5740428/jan-schultke

    def parse(self) -> str:
        for url_re in self.urls_re:
            res = url_re.match(self.url)
            if res:
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
                        html = self.get_html()
                        pattern = re.compile(r'<a .*class="question-hyperlink">(.*?)</a>')
                        self.question_name = pattern.search(html).group(1)
                elif self.type_name == "a":
                    # answer
                    # https://stackoverflow.com/a/601989/17869889
                    html = self.get_html()
                    pattern = re.compile(r'<a .*class="question-hyperlink">(.*?)</a>')
                    self.question_name = pattern.search(html).group(1)
                    self.is_answer = True
                elif self.type_name == 'users':
                    # https://stackoverflow.com/users/5740428/jan-schultke
                    self.user_name = res.group("question")
                else:
                    self.error('unknown type') # pragma: no cover
                return

    def format(self):
        title = ""
        if self.question_name:
            if len(self.question_name) >= self.max_title_length:
                title = f"{self.site}"
                if self.is_answer:
                    title += " [answer]"
                else:
                    title += " [question]"
            else:
                title = self.question_name
                if self.is_answer:
                    title += " [answer]"
        elif self.tag_name:
            title = f"{self.tag_name} tag"
        elif self.user_name:
            title = f'{self.user_name}'
        else:
            # pure https://stackoverflow.com/
            title = self.site

        return title


class ZhihuProcessor(Processor):
    def __init__(self, formatting_title: str) -> None:
        super().__init__(formatting_title)
        self.site = "Zhihu"
        self.type_name = None
        self.title = None

        self.urls_re = [
            re.compile(r"^https://www\.zhihu\.com/?$"),
            re.compile(r"^https://www\.zhihu\.com/question/\d+/(?P<type>.*?)/(?P<id>.*?)/?$"),
            re.compile(r"^https://www\.zhihu\.com/(?P<type>.*?)/(?P<id>.*?)/(?P<sub_type>.*?)/?$"),
            re.compile(r"^https://www\.zhihu\.com/(?P<type>.*?)/(?P<id>.*?)/?$"),
            re.compile(r"^https://zhuanlan\.zhihu\.com/(?P<type>.*?)/(?P<id>.*?)/?$"),
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
        for url_re in self.urls_re:
            res = url_re.match(self.url)
            if res:
                if "type" not in res.groupdict():
                    self.title = "知乎"
                    return
                self.type_name = res.group("type")

                # following parse need page html elements
                html = self.get_html()

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
                    # https://www.zhihu.com/question/367357782/answer/3066947505 Anonymous user

                    pattern = re.compile(r'<h1 class="QuestionHeader-title">(.*?)</h1>')
                    self.title = pattern.search(html).group(1) + "的回答"
                elif self.type_name == "people":
                    # https://www.zhihu.com/people/hinus

                    pattern = re.compile(r'<span class="ProfileHeader-name">(.*?)</span')
                    # sometimes there will be <style ...> inside, remove it
                    user_name = re.sub(r"<style.*>", "", pattern.search(html).group(1))
                    self.title = user_name + "的主页"
                    if "sub_type" in res.groupdict():
                        # https://www.zhihu.com/people/hinus/collections
                        self.title = f'{user_name}的{self.sub_types[res.group("sub_type")]}'
                elif self.type_name == "collection":
                    # https://www.zhihu.com/collection/86788003
                    pattern = re.compile(
                        r'<div class="CollectionDetailPageHeader-title">(.*?)</div>'
                    )
                    self.title = pattern.search(html).group(1) + " 收藏夹"
                elif self.type_name == "column":
                    # https://www.zhihu.com/column/hinus
                    pattern = re.compile(r'<div class="css-zyehvu">(.*?)</div>')
                    self.title = pattern.search(html).group(1) + " 专栏"
                else:
                    self.error()  # pragma: no cover
                return

        self.error()  # pragma: no cover

    def format(self):
        return self.title


class BilibiliProcessor(Processor):

    def __init__(self, formatting_title: str) -> None:
        super().__init__(formatting_title)
        self.site = "bilibli"
        self.type_name = None
        self.user_name = None
        self.id = None
        self.name = None

        self.urls_re = [
            re.compile(r'^https://www\.bilibili\.com/?$'),
            re.compile(r'^https://www\.bilibili\.com/(?P<type>.*?)/(?P<id>.*?)\?.*$'),
            re.compile(r'^https://www\.bilibili\.com/(?P<type>.*?)/(?P<id>.*)$'),
        ]

        # https://www.bilibili.com/video/BV1ah4y1X73M
        # https://www.bilibili.com/opus/806593844580712449?spm_id_from=333.999.0.0
        # https://www.bilibili.com/read/cv23285665?spm_id_from=333.999.0.0

    def parse(self) -> str:
        
        for url_re in self.urls_re:
            res = url_re.match(self.url)

            if res:
                
                if "type" not in res.groupdict():
                    # pure bilibili
                    return
                self.type_name = res.group("type")
                self.id = res.group("id")
                # bilibili url often following with "spm_id_from=333.999.0.0 ..."
                # clean the url
                self.url = f'https://www.bilibili.com/{self.type_name}/{self.id}'
                
                html = self.get_html()

                if self.type_name == 'video':
                    pattern = re.compile(r'<h1 .*>(.*?)</h1>')
                    self.name = pattern.search(html).group(1)
                elif self.type_name == 'opus':
                    pass
                elif self.type_name == 'read':
                    pattern = re.compile(r'<title data-vue-meta="true">(.*?)</title>')
                    self.name = pattern.search(html).group(1).replace(' - 哔哩哔哩','')
                return

    def format(self):

        if self.type_name is None:
            # pure bilibili
            title = self.site
        else:
            if self.type_name == 'video':
                title = self.name
            elif self.type_name == 'opus':
                title = f'B站动态'
            elif self.type_name == 'read':
                title = f'{self.name} 专栏'
            else:
                self.error("unknown type") # pragma: no cover

        return title