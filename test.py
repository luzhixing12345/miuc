

import miuc


def main():

    url = 'https://code.visualstudio.com/api/get-started/your-first-extension'
    url = 'https://github.com/luzhixing12345/miuc'
    url = 'https://github.com/luzhixing12345/MarkdownParser'
    x = miuc.parse_url(url)
    print(x)





if __name__ == "__main__":
    main()