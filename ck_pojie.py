# -*- coding: utf-8 -*-
"""
cron: 53 11 * * *
new Env('吾爱破解');
"""

import re

import requests

from notify_mtr import send
from utils import get_data


class PojieCheckIn:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def sign(headers):
        msg = ""
        try:
            session = requests.session()
            session.get(
                url="https://www.52pojie.cn/home.php?mod=task&do=apply&id=2",
                headers=headers)
            resp = session.get(
                url="https://www.52pojie.cn/home.php?mod=task&do=draw&id=2",
                headers=headers)
            content = re.findall(r'<div id="messagetext".*?\n<p>(.*?)</p>',
                                 resp.text)[0]
            if "您需要先登录才能继续本操作" in resp.text:
                msg += "吾爱破解 cookie 失效"
            elif "安域防护节点" in resp.text:
                msg += "触发吾爱破解安全防护，访问出错。自行修改脚本运行时间和次数，总有能访问到的时间"
            elif "恭喜" in resp.text:
                msg += "吾爱破解签到成功"
            else:
                msg += content
        except Exception as e:
            print("签到错误", e)
            msg += "吾爱破解出错"
        return msg

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            cookie = check_item.get("cookie")
            headers = {
                "User-Agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
                "Cookie": cookie,
                "ContentType": "text/html;charset=gbk"
            }
            try:
                uid = re.findall(r"htVD_2132_lastcheckfeed=(.*?);",
                                 cookie)[0].split("%7C")[0]
            except Exception as e:
                print(e)
                uid = "未获取到用户 uid"
            sign_msg = self.sign(headers=headers)
            msg = f"帐号信息: {uid}\n签到状态: {sign_msg}"
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("POJIE", [])
    res = PojieCheckIn(check_items=_check_items).main()
    print(res)
    send("吾爱破解", res)
