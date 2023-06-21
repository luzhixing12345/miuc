# miuc

Markdown Intelligence Url Complete

## Features

## Download

Search `miuc` in Vscode extension market or manually download the extension from [miuc-vscode-extension-market]()

If you prefer to use in command line, you could download miuc from PYPI

```bash
pip install miuc
``` 

## Usage

use `miuc <url>` and return the markdown format url with title

```bash
$ miuc <url>
# [article-title](url)

$ miuc https://github.com/luzhixing12345/miuc
# [miuc](https://github.com/luzhixing12345/miuc)
```

If you prefer to display the site like `Github` or `Stackoverflow`, add argument `-s`

```bash
$ miuc -s https://github.com/luzhixing12345/miuc
# [Github miuc](https://github.com/luzhixing12345/miuc)
```

To customize the title like `[Github - miuc](...)` `[Github:miuc](...)`, see more information from [miuc document]()

## Extension Settings

## Rerference

- [brandmark](https://brandmark.io/)
