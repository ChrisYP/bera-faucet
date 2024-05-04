# bera-faucet

A simple faucet for the BERA testnet.

## Installation

```bash
git clone https://github.com/ChrisYP/bera-faucet.git
cd bera_faucet
pip install -r requirements.txt
```

## Usage

```bash
wallets.txt格式 address----private_key
(私钥非必须,随便什么都行).如果填写正确的,失败的地址会被记录在fail.txt
直接复制到wallets.txt就可以重新跑了.
```

```bash
python3 main.py
```