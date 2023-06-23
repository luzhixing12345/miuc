import miuc
import unittest


class MiucUnitTest(unittest.TestCase):
    def test_github(self):
        urls = [
            # "https://code.visualstudio.com/api/get-started/your-first-extension",
            "https://github.com/",
            "https://github.com/luzhixing12345/miuc",
            "https://github.com/luzhixing12345/MarkdownParser",
            "https://github.com/luzhixing12345?tab=followers/",
            "https://github.com/luzhixing12345?tab=following",
            "https://github.com/fadedzipper/zCore-Tutorial/tree/dev",
            "https://github.com/fadedzipper/zCore-Tutorial/blob/dev/docs/book.toml",
        ]
        for url in urls:
            print(miuc.parse_url(url))

    def test_githubio(self):

        urls = [
            "https://luzhixing12345.github.io/",
            "https://luzhixing12345.github.io",
            "https://luzhixing12345.github.io/zood/",
            "https://xuan-insr.github.io/compile_principle/4%20Semantic%20Analysis/",
            "https://luzhixing12345.github.io/tags/%E7%8E%AF%E5%A2%83%E9%85%8D%E7%BD%AE/",
            "https://luzhixing12345.github.io/2023/02/28/%E7%8E%AF%E5%A2%83%E9%85%8D%E7%BD%AE/pws/",
            "https://luzhixing12345.github.io/2023/02/28/%E7%8E%AF%E5%A2%83%E9%85%8D%E7%BD%AE/VMware%E8%99%9A%E6%8B%9F%E6%9C%BA%E9%85%8D%E7%BD%AE/"
        ]
        for url in urls:
            print(miuc.parse_url(url))

    def test_stackoverflow(self):
        urls = [
            "https://stackoverflow.com",
            "https://stackoverflow.com/questions/76500242/what-flags-are-needed-in-arm-none-eabi-gcc-to-produce-fdpic-elf-binary",
            "https://stackoverflow.com/questions/76519802/how-to-output-the-subcommand-execution-process-to-the-terminal",
            "https://stackoverflow.com/questions/76519939/python-filter-from-array-list-based-on-multiple-condition",
            "https://stackoverflow.com/questions/393554/python-sqlite3-and-concurrency",
            "https://stackoverflow.com/q/76519939/17869889",
            "https://stackoverflow.com/q/76500242/17869889",
            "https://stackoverflow.com/questions/tagged/python",
            "https://stackoverflow.com/q/393554/17869889",
            "https://stackoverflow.com/a/601989/17869889",
            "https://stackoverflow.com/users/5740428/jan-schultke",
            "https://stackoverflow.com/a/76520661/17869889",
            "https://stackoverflow.com/a/76521396/17869889"
        ]

        for url in urls:
            print(miuc.parse_url(url))

    def test_youtube(self):

        urls = [
            "https://www.youtube.com/watch?v=SZj6rAYkYOg",
            "https://www.youtube.com/watch?v=ErV-2tlf9Ls",
            "https://www.youtube.com/@techquickie",
            "https://www.youtube.com/watch?v=2pZmKW9-I_k&list=PL4cUxeGkcC9gUgr39Q_yD6v-bSyMwKPUI",
            "https://www.youtube.com/watch?v=iTZ1-85I77c&list=PL4cUxeGkcC9gUgr39Q_yD6v-bSyMwKPUI&index=2",
            "https://youtu.be/iTZ1-85I77c",
            "https://www.youtube.com/@programmingwithmosh/videos"
        ]
        for url in urls:
            print(miuc.parse_url(url))

    def test_zhihu(self):
        urls = [
            "https://www.zhihu.com",
            "https://www.zhihu.com/question/446988424",
            "https://zhuanlan.zhihu.com/p/347552573",
            "https://www.zhihu.com/question/21099081/answer/119347251",
            "https://www.zhihu.com/question/21099081/answer/18830200",
            "https://www.zhihu.com/people/hinus",
            "https://www.zhihu.com/people/hinus/following",
            "https://www.zhihu.com/people/hinus/collections",
            "https://www.zhihu.com/collection/86788003",
            "https://www.zhihu.com/collection/351872590",
            "https://zhuanlan.zhihu.com/p/444188736",
            "https://www.zhihu.com/people/lu-zhi-xing-66-64/following",
            "https://www.zhihu.com/people/xiao-xie-xuan",
            "https://www.zhihu.com/people/lu-zhi-xing-66-64",
            "https://www.zhihu.com/question/600808314/answer/3062270104",
            "https://www.zhihu.com/column/hinus",
        ]
        for url in urls:
            print(miuc.parse_url(url))

    def test_bilibili(self):
        urls = [
            "https://www.bilibili.com/",
            "https://www.bilibili.com/video/BV1ah4y1X73M",
            "https://www.bilibili.com/opus/806593844580712449?spm_id_from=333.999.0.0",
            "https://www.bilibili.com/read/cv23285665?spm_id_from=333.999.0.0",
            "https://www.bilibili.com/video/BV1J14y1D7Sw/?spm_id_from=333.999.list.card_archive.click&vd_source=7b4c585df2dd3777eae63bf4867f6c11",
            "https://www.bilibili.com/video/BV13V4y1y73X/?spm_id_from=444.41.list.card_archive.click&vd_source=7b4c585df2dd3777eae63bf4867f6c11"
        ]
        for url in urls:
            print(miuc.parse_url(url))


    def test_CSDN(self):

        urls = [
            "https://blog.csdn.net/qq_46675545?type=blog",
            "https://blog.csdn.net/qq_46675545/article/details/131323215?spm=1001.2014.3001.5502",
            "https://blog.csdn.net/qq_46675545/article/details/131323215",
            "http://t.csdn.cn/6eAx0",
            "https://blog.csdn.net/qq_46675545/category_12120503.html",
            "https://blog.csdn.net/qq_45726331/category_12220993.html"
        ]

        for url in urls:
            print(miuc.parse_url(url))

if __name__ == "__main__":
    unittest.main()
