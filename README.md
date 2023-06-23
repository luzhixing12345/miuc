# miuc

Markdown Intelligence Url Complete

Paste URL by <kbd>ctrl</kbd> + <kbd>v</kbd>, miuc will complete the title for you

## Features

![action](https://raw.githubusercontent.com/learner-lu/picbed/master/action.gif)

## Download

Search `miuc` in Vscode extension market or manually download the extension from [miuc-vscode-extension-market](https://marketplace.visualstudio.com/items?itemName=kamilu.miuc)

Vscode Extension miuc depends on python program miuc, it asks you to download miuc by pip for the first time, you could also download by yourself

```bash
pip install miuc
```

**Actually, miuc is not mature**, if you meet any bug please report @ [miuc issues](https://github.com/luzhixing12345/miuc/issues)

## Usage

in Vscode, press <kbd>ctrl</kbd> + <kbd>v</kbd> to paste as usual, miuc will complete the title if URL in your clipboard

in command line, use `miuc <url>` and return the markdown format url with title, you may need this one if you prefer vim/neovim and so on

```bash
$ miuc <url>
# [article-title](url)

$ miuc https://github.com/luzhixing12345/miuc
# [miuc](https://github.com/luzhixing12345/miuc)
```

see more information from [miuc document](https://luzhixing12345.github.io/miuc/)

## Rerference
  
- [brandmark](https://brandmark.io/)
- [autopep8](https://github.com/microsoft/vscode-autopep8)
