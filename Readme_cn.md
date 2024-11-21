# NodePay 多账户注册免费 Python 机器人

该 Python 机器人脚本通过指定的 HTTP 代理管理多个账户连接，支持无限代理和多个 NodePay 注册账户，处理身份验证并与服务器保持持久连接。脚本还包括自动激活 NodePay 账户的功能，并将所有数据保存到一个 CSV 文件中。

## 功能

- 使用代理创建账户，确保安全。
- 使用 **2Captcha 服务** 自动注册账户。
- 使用自定义推荐码。
- 将所有邮箱、令牌、密码、用户名保存到 Excel 文件中，方便未来运行节点。
- 自动激活账户，无需手动激活！
- 支持多线程和从数组中选择多个推荐码！

# 获取 2Captcha API Key

1. 打开 2Captcha 链接并注册：[https://2captcha.com/](https://2captcha.com/)
2. 使用加密货币作为支付方式充值 2-3 美元。
3. 复制 API Key 并将其粘贴到 `main.py` 文件的 [第 233 行](https://github.com/Solana0x/NodepayRefferal/blob/6913c17f72d4a37de0638d32017b8721f776d826/main.py#L233)。
4. ![image](https://github.com/user-attachments/assets/a4375bfe-5bdd-476c-b0c9-3c7627d33dad)

# 获取 NodePay 账户的推荐码并将其添加到数组中！

1. 在 `main.py` 文件的 [第 232 行](https://github.com/Solana0x/NodepayRefferal/blob/6913c17f72d4a37de0638d32017b8721f776d826/main.py#L232) 添加您想要的推荐码。

# 生成账户凭据

1. 在 `accgen.py` 文件的第 4 行添加您的邮箱，在第 51 行编写您想要生成的凭据数量。

## 运行代码的步骤 -

在运行脚本之前，确保您的机器上已经安装了 Python。然后，使用以下命令安装必要的 Python 包：

1. ``` git clone https://github.com/Solana0x/NodepayRefferal.git ```
2. ``` cd NodepayRefferal ```
3. ``` pip install -r requirements.txt ```
4. 获取推荐码，生成账户凭据，获取 2Captcha API Key。
5. 在 `proxies.txt` 文件中添加多个代理，您可以添加 1000+ 代理！格式为 # `HTTP://username:pass@ip:port`。
6. 还需运行 `python accgen.py` 来生成账户
7. 运行脚本 `python main.py`。
8. 账户数据将保存到 `Accounts.csv` 文件中，请确保保存该文件。

## 系统要求

- NodePay 账户邀请链接 ( [https://app.nodepay.ai/register?ref=PGiwMlh6dQJVmxE](https://app.nodepay.ai/register?ref=p2k8sttKkrPvgOf) )
- Python (通过 [https://www.python.org/downloads/](https://www.python.org/downloads/) 安装 Python [Windows/Mac]) 或 Ubuntu 服务器 [`sudo apt install python3`]
- VPS 服务器！您可以通过 AWS 免费套餐、Google 免费套餐、Gitpod 或任何在线服务，每月只需 ~ 2-5 美元
- 代理服务器 - 您可以购买数据中心代理来生成账户

# NstProxy - https://app.nstproxy.com/register?i=SkKXHm

![image](https://github.com/user-attachments/assets/2d225d31-e06a-410b-adae-11caca9865f1)

## 需要任何帮助请联系：`0xphatom` 在 Discord 上 https://discord.com/users/979641024215416842

# 社交平台

# Telegram - [https://t.me/phantomoalpha](https://t.me/phantomoalpha)
# Discord - [https://discord.gg/pGJSPtp9zz](https://discord.gg/pGJSPtp9zz)
