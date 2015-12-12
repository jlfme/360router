#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# ---------------------------------------
# Created by: Jlfme<jlfgeek@gmail.com>
# Created on: 2015-12-12 18:48:18
# ---------------------------------------


import time
from splinter import Browser


def manage_router(url='http://10.10.10.1', password=None):
    if password is None:
        raise ValueError('The password must be not None')
    b = Browser("firefox")
    b.visit(url)

    # login
    b.find_by_id('login_pwd').fill(password)
    b.find_by_css('.btn_login').click()

    # open the setting page
    b.find_by_id('nav_setting_b').click()
    url = b.url.split("#")[0] + "#extitem/router_info/nav_setting"
    b.visit(url)

    while True:
        time.sleep(10)
        b.find_by_id("cutoff_link").click()
