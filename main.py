# -*- coding: utf-8 -*-
# @Time    : 2024/5/4 12:54
# @Author  : Chris
# @Email   : 10512@qq.com
# @File    : main.py
# @Software: PyCharm
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from loguru import logger

from utils import crack_cf, claim

import warnings

warnings.filterwarnings("ignore")

with open('wallets.txt', 'r') as f:
    wallets = f.read().strip().split('\n')

with open('success.txt', 'r') as f:
    success = f.read().strip().split('\n')


def run(wallet, proxy, user_token):
    address, _ = wallet.split('----')
    if address in success:
        logger.warning(f'{address} 已经领取过了')
        return
    while 1:
        try:
            ret = crack_cf(proxy=proxy, user_token=user_token)
            if ret:
                user_agent = ret.get("user_agent")
                token = ret.get("token")
                ret = claim(token, user_agent, proxy, address)
                msg = ret.get("msg", "")

                if 'to the queue' in msg or 'exceeded the rate limit' in msg:
                    logger.success(msg)
                    with open('success.txt', 'a') as fd:
                        fd.write(f'{address}\n')
                else:
                    logger.error(msg)
                    with open('failed.txt', 'a') as fd:
                        fd.write(wallet + '\n')
                break
            else:
                continue
        except BaseException as e:
            logger.error(e.__repr__())
            continue


def main(workers, proxy, user_token):
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(run, wallet=wallet, proxy=proxy, user_token=user_token) for wallet in wallets}
        completed_tasks = 0
        total_tasks = len(futures)
        for future in as_completed(futures):
            future.result()
            completed_tasks += 1
            logger.debug(
                f"完成进度: {completed_tasks}/{total_tasks} ({(completed_tasks / total_tasks) * 100:.2f}%)")


if __name__ == '__main__':
    main(workers=os.cpu_count(),  # 线程数
         proxy="代理",  # 注册地址 http://b.nxw.so/34eRo8 便宜.
         user_token="Nocaptcha打码token"  # 注册地址 http://t.nxw.so/7t8Ie   有测试点，也有包月服务，包月可以无限跑。
         )
