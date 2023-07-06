# miuc

[![codecov](https://codecov.io/gh/luzhixing12345/miuc/branch/main/graph/badge.svg?)](https://codecov.io/gh/luzhixing12345/miuc)

Markdown Intelligence Url Complete

Paste URL by <kbd>ctrl</kbd> + <kbd>v</kbd>, miuc will complete the title for you

## Features

![action](https://raw.githubusercontent.com/learner-lu/picbed/master/action.gif)

## Download

Search `miuc` in Vscode extension market or manually download the extension from [miuc-vscode-extension-market](https://marketplace.visualstudio.com/items?itemName=kamilu.miuc)

Vscode Extension miuc depends on python library [miuc](https://pypi.org/project/miuc/), if you miss the auto download, please download manually in your activate python environment

```bash
pip install miuc
```

**Actually, miuc is not mature**, if you meet any bug please report @ [miuc issues](https://github.com/luzhixing12345/miuc/issues)

## Usage

in Vscode, press <kbd>ctrl</kbd> + <kbd>v</kbd> to paste as usual, miuc will complete the title if URL in your clipboard

in command line, use `miuc <URL>` and return the markdown format url with title, you may need this one if you prefer vim/neovim and so on

```bash
$ miuc <URL>

# for example
$ miuc https://github.com/luzhixing12345/miuc
[miuc](https://github.com/luzhixing12345/miuc)
```

## Rerference

- [zood document](https://luzhixing12345.github.io/zood/)
- [brandmark](https://brandmark.io/)
- [autopep8](https://github.com/microsoft/vscode-autopep8)
- [icons8](https://icons8.com/icons/set/logo)
- [VS-Code-Extension-Doc-ZH](https://liiked.github.io/VS-Code-Extension-Doc-ZH/#/)