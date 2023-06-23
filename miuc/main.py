"""
*Copyright (c) 2023 All rights reserved
*@description: main project
*@author: Zhixing Lu
*@date: 2023-06-20
*@email: luzhixing12345@163.com
*@Github: luzhixing12345
"""

import argparse
from .web_parser import parse_url
import io
import sys


def main():
    
    parser = argparse.ArgumentParser("Markdown Intelligence Url Complete")
    parser.add_argument("-s", "--site", action="store_true", help="add site info")
    parser.add_argument("-t", "--max-time-limit", type=int, default=5, help="max time limit")
    parser.add_argument("url", type=str, help="website url")
    args = parser.parse_args()

    if not args.url:
        print("miuc <url>")
        exit(1)

    markdown_url = parse_url(args.url, max_time_limit=args.max_time_limit)
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    print(markdown_url)
    


if __name__ == "__main__":
    main()
