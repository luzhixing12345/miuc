import miuc
import sys

url = sys.argv[1]

def main():
    print(miuc.parse_url(url))


if __name__ == "__main__":
    main()
