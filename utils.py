# -*- coding: utf-8 -*-
# @Time    : 2023/3/20 21:49
# @Author  : Chris
# @Email   : 10512@qq.com
# @File    : utils.py
# @Software: PyCharm


from pynocaptcha import CloudFlareCracker
import requests


def crack_cf(proxy, user_token):
    cracker = CloudFlareCracker(
        user_token=user_token,
        href="https://artio.faucet.berachain.com/",
        proxy=proxy,
        sitekey="0x4AAAAAAARdAuciFArKhVwt",
        debug=False,
        timeout=120,
        show_ad=False
    )
    return cracker.crack()


def claim(token, user_agent, p, address):
    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': f'Bearer {token}',
        'cache-control': 'no-cache',
        'content-type': 'text/plain;charset=UTF-8',
        'dnt': '1',
        'origin': 'https://artio.faucet.berachain.com',
        'pragma': 'no-cache',
        'referer': 'https://artio.faucet.berachain.com/',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': user_agent,
    }
    params = {
        'address': address,
    }

    data = '{"address":"' + address + '"}'

    return requests.post('https://artio-80085-faucet-api-cf.berachain.com/api/claim',
                         params=params, proxies={"https": p if p.startswith("http://") else "http://" + p},
                         verify=False,
                         headers=headers, data=data).json()
