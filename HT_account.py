# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/9/29
# @Author  : MashiroF
# @File    : HT_account.py
# @Software: PyCharm

## 账号管理样本
# {
#     'user':'',        # 备注,必要
#     'CK':'',          # Cookie,必要(建议全部粘贴)
#     'UA':''           # User-Agent,必要
# },

## 账号管理
# accounts = [
#     {
#         'user':'',
#         'CK':'',
#         'UA':''
#     },
#     {
#         'user':'',
#         'CK':'',
#         'UA':''
#     },
# ]
import os
cks = os.environ["HT_COOKIE"].split("&")
## 账号管理
accounts = []
for ck in cks:
    ckk=ck.split("@")
    accounts.append({'user':ckk[0],'CK':ckk[1],'UA':ckk[2]})
