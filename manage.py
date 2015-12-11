#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# ---------------------------------------
# Created by: Jlfme<jlfgeek@gmail.com>
# Created on: 2017-10-25 16:03:18
# ---------------------------------------


import time
from copy import copy
import requests
from encryption import encrypt_password


class RouterManager(object):

    def __init__(self, domain='http://10.10.10.1', password='password'):
        self.domain = 'http://' + domain if not domain.startswith('http') else domain
        self.password = password

        self.token_id = None

        self.session = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01'
        }

    def login(self):
        # 打开登录首页
        url = '{domain}/login_pc.htm'.format(domain=self.domain)
        self.session.get(url=url, headers=self.headers.copy())

        # 获取秘钥, 用于加密用户密码
        headers = self.headers.copy()
        headers['Referer'] = url
        resp = self.session.get(
            url=self.domain + 'router/get_rand_key.cgi?noneed=noneed&_=1471006585938',
            headers=headers
        )
        random_key = resp.json()["rand_key"]

        # 根据获取到的秘钥加密password
        encrypted_password = random_key[:32] + encrypt_password(random_key[:32], self.password)

        # 用加密后的密码登录并获取token
        resp = self.session.post(
            url=self.domain + '/router/web_login.cgi',
            data={'user': 'admin', 'pass': encrypted_password, 'from': 1},
            headers=headers
        )
        token_id = resp.json()['token_id']
        self.token_id = token_id

        return token_id

    def get_wan_ip(self):
        url = self.domain + '/router/interface_status_show.cgi'
        resp = self.session.post(url=url, data={'noneed': 'noneed'}, headers=self.headers.copy())
        return resp.json()[0]['WAN1']

    def auto_redial(self):
        token_id = self.token_id if self.token_id is not None else self.login()
        headers = self.headers.copy()
        headers['Referer'] = '{}/new_index.htm?token_id={}'.format(self.domain, token_id)
        headers['token_id'] = token_id
        url = self.domain + '/router/wan_status_set.cgi'

        # 断开连接
        self.session.post(
            url=url,
            data={'wanid': 'WAN1', 'status': 0},
            headers=headers
        )
        time.sleep(1)

        # 重新连接
        self.session.post(
            url=url,
            data={'wanid': 'WAN1', 'status': 1},
            headers=headers
        )
        time.sleep(0.5)
