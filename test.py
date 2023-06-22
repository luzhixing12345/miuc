import miuc
import sys
import requests

url = sys.argv[1]

def main():
    try:
        result = miuc.parse_url(url,0.5)
    except Exception as e:
        result = f'[unknown]({url})'
    print(result)
    


if __name__ == "__main__":
    main()
