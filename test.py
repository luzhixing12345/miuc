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
            "https://github.com/microsoft/vscode/issues",
            "https://github.com/microsoft/vscode/issues/178962",
            "https://github.com/microsoft/vscode/pull/185924/files",
            "https://github.com/microsoft/vscode/issues/178962#issuecomment-1496530894",
            "https://github.com/microsoft/vscode/wiki/Submitting-Bugs-and-Suggestions",
            "https://github.com/microsoft/vscode/actions",
            "https://github.com/microsoft/vscode/projects?query=is%3Aopen",
            "https://github.com/microsoft/vscode/graphs/contributors",
            "https://github.com/microsoft/vscode/network/dependencies",
            "https://github.com/microsoft/vscode/commits/main",
            "https://github.com/microsoft/vscode/commit/a5727468f373af49f785a94e13e7a2890a1097af",
            "https://github.com/search?q=fcitx5+theme&type=Repositories",
            "https://github.com/search?q=linux+language%3AMarkdown&type=code&l=Markdown",
            "https://github.com/fool2fish/dragon-book-exercise-answers/blob/master/ch02/2.2/2.2.md",
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
            "https://luzhixing12345.github.io/2023/02/28/%E7%8E%AF%E5%A2%83%E9%85%8D%E7%BD%AE/VMware%E8%99%9A%E6%8B%9F%E6%9C%BA%E9%85%8D%E7%BD%AE/",
            "https://zhou-yuxin.github.io/articles/2018/Linux%E7%89%A9%E7%90%86%E5%86%85%E5%AD%98%E7%AE%A1%E7%90%86%E2%80%94%E2%80%94%E8%8E%B7%E5%8F%96%E7%89%A9%E7%90%86%E5%86%85%E5%AD%98%E5%B8%83%E5%B1%80%E3%80%81%E5%88%92%E5%88%86%E5%86%85%E5%AD%98%E5%8C%BA%E4%B8%8E%E5%88%9B%E5%BB%BANUMA%E8%8A%82%E7%82%B9/index.html",
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
            "https://stackoverflow.com/a/76521396/17869889",
        ]

        for url in urls:
            print(miuc.parse_url(url))

    def test_youtube(self):
        urls = [
            "https://www.youtube.com/",
            "https://www.youtube.com/watch?v=SZj6rAYkYOg",
            "https://www.youtube.com/watch?v=ErV-2tlf9Ls",
            "https://www.youtube.com/@techquickie",
            "https://www.youtube.com/watch?v=2pZmKW9-I_k&list=PL4cUxeGkcC9gUgr39Q_yD6v-bSyMwKPUI",
            "https://www.youtube.com/watch?v=iTZ1-85I77c&list=PL4cUxeGkcC9gUgr39Q_yD6v-bSyMwKPUI&index=2",
            "https://youtu.be/iTZ1-85I77c",
            "https://www.youtube.com/@programmingwithmosh/videos",
            "https://www.youtube.com/playlist?list=PLyzOVJj3bHQuloKGG59rS43e29ro7I57J",
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
            "https://zhuanlan.zhihu.com/p/96047937"
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
            "https://www.bilibili.com/video/BV13V4y1y73X/?spm_id_from=444.41.list.card_archive.click&vd_source=7b4c585df2dd3777eae63bf4867f6c11",
            "https://space.bilibili.com/1010983811?spm_id_from=333.337.search-card.all.click",
            "https://space.bilibili.com/261543088?spm_id_from=333.999.0.0",
            "https://www.bilibili.com/video/BV1Bh4y1x7tv/?spm_id_from=333.788&vd_source=7b4c585df2dd3777eae63bf4867f6c11",
        ]
        for url in urls:
            print(miuc.parse_url(url))

    def test_CSDN(self):
        urls = [
            "https://blog.csdn.net/",
            "https://blog.csdn.net/qq_46675545?type=blog",
            "https://blog.csdn.net/qq_46675545/article/details/131323215?spm=1001.2014.3001.5502",
            "https://blog.csdn.net/qq_46675545/article/details/131323215",
            "http://t.csdn.cn/6eAx0",
            "https://blog.csdn.net/qq_46675545/category_12120503.html",
            "https://blog.csdn.net/qq_45726331/category_12220993.html",
            "https://blog.csdn.net/weixin_38493195/article/details/126981220?spm=1001.2014.3001.5502",
            "https://blog.csdn.net/weixin_38493195/article/details/127588073?spm=1001.2014.3001.5502",
            "https://blog.csdn.net/weixin_38493195/article/details/128329873?spm=1001.2014.3001.5502",
            "https://blog.csdn.net/weixin_38493195/article/details/124870781",
        ]

        for url in urls:
            print(miuc.parse_url(url))

    def test_cnblogs(self):
        urls = [
            "https://www.cnblogs.com/pythonista/p/17501383.html",
            "https://www.cnblogs.com/chu-jian/p/17501124.html",
            "https://www.cnblogs.com/haiyux/p/17501641.html",
            "https://www.cnblogs.com/deali/p/17501704.html" "https://www.cnblogs.com/guanghe/p/11975387.html",
            "https://www.cnblogs.com/zhiyiYo/p/17492487.html",
            "https://www.cnblogs.com/pythonista/p/17501383.html",
            "https://www.cnblogs.com/zhiyiYo",
            "https://www.cnblogs.com/",
            "https://www.cnblogs.com/armlinux/archive/2010/11/26/2396888.html",
        ]
        for url in urls:
            print(miuc.parse_url(url))

    def test_Githubusercontent(self):

        urls = ["https://raw.githubusercontent.com/learner-lu/picbed/master/action.gif"]
        for url in urls:
            print(miuc.parse_url(url))

    def test_jianshu(self):

        urls = [
            "https://www.jianshu.com",
            "https://www.jianshu.com/p/b2288ef3f11e",
            "https://www.jianshu.com/u/441d207955f2",
            "https://www.jianshu.com/u/c0df9f7c15fa",
            "https://www.jianshu.com/p/b9552bcd27be",
        ]
        for url in urls:
            print(miuc.parse_url(url))

    def test_tencentcloud(self):

        urls = [
            "https://cloud.tencent.com/",
            "https://cloud.tencent.com/developer/user/7055715",
            "https://cloud.tencent.com/developer/article/1679861",
            "https://cloud.tencent.com/developer/article/1409664",
        ]
        for url in urls:
            print(miuc.parse_url(url))

    def test_douban(self):

        urls = [
            "https://book.douban.com/",
            "https://book.douban.com/subject/2334288/",
            "https://book.douban.com/subject/35966120/?source=2022_annual_book",
        ]

        for url in urls:
            print(miuc.parse_url(url))

    def test_juejin(self):

        urls = ["https://juejin.cn/post/7134950321595351047", "https://juejin.cn"]

        for url in urls:
            print(miuc.parse_url(url))

    def test_others(self):
        urls = [
            "https://www.vmware.com/products/workstation-pro.html",
            "https://gist.github.com/PurpleVibe32/30a802c3c8ec902e1487024cdea26251",
            "https://chat.openai.com/chat",
            "https://vaaandark.top/posts/cpu-%E6%B5%81%E6%B0%B4%E7%BA%BF/",
            "https://docs.python.org/zh-cn/3/library/urllib.parse.html",
            "https://about.codecov.io/",
            "https://v2raya.org/docs/prologue/introduction/",
            "http://localhost:2017/",
            "http://192.168.1.1:2017/",
            "https://csdiy.wiki/%E6%95%B0%E5%AD%A6%E5%9F%BA%E7%A1%80/MITmaths/",
            "https://wallesspku.space/",
            "https://link.zhihu.com/?target=https%3A//learnopengl.com/",
            "https://link.zhihu.com/?target=https%3A//github.com/yue/yue",
            "https://link.zhihu.com/?target=https%3A//github.com/yue/yue/issues/166",
            "https://www.shellcodes.org/CommonLisp/CommonLisp%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/Common%20Lisp%E5%BC%80%E5%8F%91%E7%8E%AF%E5%A2%83.html",
        ]
        for url in urls:
            print(miuc.parse_url(url))

    def test_wiki(self):

        urls = [
            "https://en.wikipedia.org/wiki/Roman_numerals",
            "https://en.wikipedia.org/wiki/GCC",
            "https://en.wikipedia.org/wiki/GNU_Compiler_Collection",
        ]
        for url in urls:
            print(miuc.parse_url(url))

    def test_weixin(self):

        urls = [
            "https://mp.weixin.qq.com/s/rMREBMGquxTZQXrx4sfkqw",
            "https://mp.weixin.qq.com/s/mCCi2wFRXojpxRrKEwY-8g",
        ]

        for url in urls:
            print(miuc.parse_url(url))

    def test_geeksforgeek(self):

        urls = ["https://www.geeksforgeeks.org/cache-coherence-protocols-in-multiprocessor-system/"]

        for url in urls:
            print(miuc.parse_url(url))

    def test_sourceforge(self):

        urls = [
            "https://sourceforge.net/projects/mingw-w64/files/mingw-w64/mingw-w64-release/",
            "https://sourceforge.net/projects/freepascal/files/Win32/3.2.2/",
            "https://sourceforge.net/projects/mingw-w64/files/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/8.1.0/threads-win32/seh/x86_64-8.1.0-release-win32-seh-rt_v6-rev0.7z",
            "https://sourceforge.net/projects/mingw-w64/files/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/installer/mingw-w64-install.exe",
            "https://sourceforge.net/projects/mingw-w64/files/mingw-w64/mingw-w64-release/mingw-w64-v11.0.0.zip/download",
        ]
        for url in urls:
            print(miuc.parse_url(url))

    def test_vscode_market(self):

        urls = ["https://marketplace.visualstudio.com/items?itemName=AnsonYeung.pascal-language-basics"]

        for url in urls:
            print(miuc.parse_url(url))

    def test_infoq(self):

        urls = [
            "https://xie.infoq.cn/article/386bc5366bac88552085fd4ee",
            "https://xie.infoq.cn/article/923385f5f181de629b61e5f91",
            "https://xie.infoq.cn/article/fa9056105c9e79f247e514b7e",
            "https://xie.infoq.cn/article/bb58fed4863e3c3aee072c2cf",
        ]

        for url in urls:
            print(miuc.parse_url(url))

    def test_51cto(self):

        urls = ["https://www.51cto.com/article/706997.html"]
        for url in urls:
            print(miuc.parse_url(url))

    def test_souhu(self):
        urls = ["https://www.sohu.com/a/669096209_121124373"]
        for url in urls:
            print(miuc.parse_url(url))

    def test_baidu(self):
        urls = ["https://zhidao.baidu.com/question/435213422142183884.html"]
        for url in urls:
            print(miuc.parse_url(url))

    def test_acm(self):
        urls = ["https://dl.acm.org/doi/10.5555/1991596.1991599", "https://dl.acm.org/doi/10.5555/2591272.2591300"]
        for url in urls:
            print(miuc.parse_url(url))

    def test_arxiv(self):
        urls = [
            "https://arxiv.org/abs/2308.10714",
        ]
        for url in urls:
            print(miuc.parse_url(url))

    def test_IEEE(self):
        urls = ["https://ieeexplore.ieee.org/document/10066614", "https://ieeexplore.ieee.org/document/8708249"]
        for url in urls:
            print(miuc.parse_url(url))

    def test_USENIX(self):
        urls = ["https://www.usenix.org/conference/fast20/presentation/yang"]
        for url in urls:
            print(miuc.parse_url(url))

    def test_lwn(self):
        urls = ["https://lwn.net/Articles/682911/"]
        for url in urls:
            print(miuc.parse_url(url))

    def test_lkml(self):
        urls = [
            "https://lkml.org/lkml/2018/9/25/5",
            "https://lkml.org/lkml/2018/9/25/4",
            "https://lkml.org/lkml/2018/9/25/3",
            "https://lkml.org/lkml/2018/9/25/2",
            "https://lkml.org/lkml/2018/9/25/1",
        ]
        for url in urls:
            print(miuc.parse_url(url))

    def test_lorekernel(self):
        urls = [
            "https://lore.kernel.org/linux-mm/64f1c69d-3706-41c5-a29f-929413e3dfa2@huawei.com/T/#m4c59b2ad0d5fd5b04b2768f931f27d6d194ef5bc",
            "https://lore.kernel.org/linux-mm/20241029-v5_user_cfi_series-v7-6-2727ce9936cb@rivosinc.com/T/#u",
        ]
        for url in urls:
            print(miuc.parse_url(url))


if __name__ == "__main__":
    unittest.main()
