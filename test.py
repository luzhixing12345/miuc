

import miuc


def main():

    url = 'https://code.visualstudio.com/api/get-started/your-first-extension'
    url = 'https://github.com/luzhixing12345/miuc'
    url = 'https://github.com/luzhixing12345/MarkdownParser'
    # url = 'https://github.com/luzhixing12345'
    url = 'https://www.zhihu.com/question/446988424'
    url = 'https://zhuanlan.zhihu.com/p/347552573'
    url = 'https://www.zhihu.com/question/21099081/answer/119347251'
    url = 'https://www.zhihu.com/question/21099081/answer/18830200'
    url = 'https://www.zhihu.com/people/hinus'
    url = 'https://www.zhihu.com/people/hinus/following'
    url = 'https://www.zhihu.com/people/hinus/collections'
    url = 'https://www.zhihu.com/collection/86788003'
    url = 'https://www.zhihu.com/collection/351872590'
    url = 'https://zhuanlan.zhihu.com/p/444188736'
    url = 'https://www.zhihu.com/people/lu-zhi-xing-66-64/following'
    url = 'https://www.zhihu.com/people/xiao-xie-xuan'
    x = miuc.parse_url(url)
    print(x)





if __name__ == "__main__":
    main()