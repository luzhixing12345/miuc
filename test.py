import miuc
import sys
import requests

url = sys.argv[1]

def main():
    result = miuc.parse_url(url,5)
    # try:
        
    # except Exception as e:
    #     print("get exception")
    #     result = f'[unknown]({url})'
    print(result)
    


if __name__ == "__main__":
    main()
