import miuc
import unittest

class MiucUnitTest(unittest.TestCase):

    def test_github(self):
        urls = [
            # "https://code.visualstudio.com/api/get-started/your-first-extension",
            "https://github.com/luzhixing12345/miuc",
            "https://github.com/luzhixing12345/MarkdownParser",
        ]
        for url in urls:
            print(miuc.parse_url(url))

    def test_zhihu(self):
        urls = [
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
            "https://www.zhihu.com/question/600808314/answer/3062270104"
        ]
        for url in urls:
            print(miuc.parse_url(url))


if __name__ == "__main__":
    unittest.main()
