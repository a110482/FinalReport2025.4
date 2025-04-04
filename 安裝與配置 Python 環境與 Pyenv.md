# 安裝與配置 Python 環境與 Pyenv

這篇教學將引導你如何在 macOS 上安裝與配置 Python 3.13，並使用 Pyenv 來管理虛擬環境。

## 安裝依賴

首先，使用 Homebrew 安裝所需的套件和工具：

```bash
brew install python-tk@3.13
brew install tcl-tk
brew install pyenv
brew install xz
brew install pyenv-virtualenv
```

## 接下來，您需要配置 shell 以便正確加載 Pyenv。

在 .zprofile 中添加以下配置：

```
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
```
在 .zshrc 中添加以下配置：

```
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
export PATH="/opt/homebrew/opt/python@3.13/bin:$PATH"
```

## 配置 Tcl/Tk 路徑並安裝 python 3.13.2

在終端機使用以下指令

```
export LDFLAGS="-L/usr/local/opt/tcl-tk/lib"
export CPPFLAGS="-I/usr/local/opt/tcl-tk/include"
export PKG_CONFIG_PATH="/usr/local/opt/tcl-tk/lib/pkgconfig"
pyenv install 3.13.2
```
## 創建與啟動虛擬環境
使用 Pyenv 安裝完 Python 後，您可以創建一個虛擬環境並啟動它：

```
pyenv virtualenv 3.13.2 env
pyenv activate env
```
## 升級 pip 並安裝所需的套件
在虛擬環境中，首先升級 pip，然後安裝 openai 套件：

```
pip install --upgrade pip
pip install openai
```

## 運行 Python 程式
現在您可以運行您的 Python 程式：

```
python main.py
```
