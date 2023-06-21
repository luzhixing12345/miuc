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


if __name__ == "__main__":
    unittest.main()
