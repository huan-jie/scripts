# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/9/16
# @Author  : MashiroF
# @File    : BattleForRealMe.py
# @Software: PyCharm

'''
cron:  40 5,12 * * * BattleForRealMe.py
new Env('欢太-RealMe积分大乱斗');
'''

import os
import re
import sys
import time
import random
import requests

# 配置文件
try:
    from HT_config import downFlag,notifyBlackList,logger
except Exception as error:
    logger.info(f'失败原因:{error}')
    sys.exit(0)

# 判断是否发生下载行为
if downFlag == True:
    logger.info('发生下载行为,应退出程序，编辑配置文件')
    sys.exit(0)

# 配信文件
try:
    from sendNotify import send
except Exception as error:
    logger.info('推送文件有误')
    logger.info(f'失败原因:{error}')
    sys.exit(0)

# 导入账户
try:
    from HT_account import accounts
    lists = accounts
except Exception as error:
    logger.info(f'失败原因:{error}')
    lists = []

# 配信内容格式
allMess = ''
def notify(content=None):
    global allMess
    allMess = allMess + content + '\n'
    logger.info(content)

# 日志录入时间
notify(f"任务:RealMe积分大乱斗\n时间:{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())}")

class BattleForRealMe:
    def __init__(self,dic):
        self.dic = dic
        self.sess = requests.session()

    # 登录验证
    def login(self):
        url = 'https://store.oppo.com/cn/oapi/users/web/member/check'
        headers = {
            'Host': 'store.oppo.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
        }
        response = self.sess.get(url=url,headers=headers).json()
        if response['code'] == 200:
            notify(f"{self.dic['user']}\t登录成功")
            return True
        else:
            notify(f"{self.dic['user']}\t登录失败")
            return False

    def receiveAward(self,dic):
        aid = 1582
        url = 'https://hd.oppo.com/task/award'
        headers = {
            'Host': 'hd.oppo.com',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Origin': 'https://hd.oppo.com',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://hd.oppo.com/act/m/2021/jifenzhuanpan/index.html?us=gerenzhongxin&um=hudongleyuan&uc=yingjifen',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.9'
        }
        data = {
            'aid': aid,
            't_index': dic['t_index']
        }
        response = self.sess.post(url=url,headers=headers,data=data).json()
        if response['no'] == '200':
            notify(f"[{dic['title']}]\t{response['msg']}")
        else:
            notify(f"[{dic['title']}]\t{response['msg']}")
        time.sleep(random.randint(1,3))

    def shareGoods(self,count=2,flag=None,dic=None):
        url = 'https://msec.opposhop.cn/users/vi/creditsTask/pushTask'
        headers = {
            'clientPackage': 'com.oppo.store',
            'Host': 'msec.opposhop.cn',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'User-Agent': 'okhttp/3.12.12.200sp1',
            'Accept-Encoding': 'gzip',
        }
        params = {
            'marking': 'daily_sharegoods'
        }
        for i in range(count + random.randint(1,3)):
            self.sess.get(url=url,headers=headers,params=params)
            notify(f"正在执行第{i+1}次微信分享...")
            time.sleep(random.randint(7,10))
        if flag == 1: #来源积分大乱斗
            self.receiveAward(dic=dic)

    # # 直播,宠粉，浏览商品
    def runViewTask(self,dic=None):
        aid = 1582
        url = 'https://hd.oppo.com/task/finish'
        headers = {
            'Host': 'hd.oppo.com',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Origin': 'https://hd.oppo.com',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://hd.oppo.com/act/m/2021/2021/realmejifendalu/index.html',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.9'
        }
        data = {
            'aid': aid,
            't_index': dic['t_index']
        }
        response = self.sess.post(url=url,headers=headers,data=data).json()
        if response['no'] == '200':
            notify(f"[{dic['title']}]\t{response['msg']}")
            self.receiveAward(dic)
        else:
            notify(f"[{dic['title']}]\t{response['msg']}")
        time.sleep(random.randint(3,5))

    def getBattleList(self):
        aid = 1582  # 抓包结果为固定值:1582
        url = 'https://hd.oppo.com/task/list'
        headers = {
            'Host':'hd.oppo.com',
            'Connection': 'keep-alive',
            'Referer':'https://hd.oppo.com/act/m/2021/2021/realmejifendalu/index.html',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.9',
        }
        params = {
            'aid':aid
        }
        response = self.sess.get(url=url,headers=headers,params=params).json()
        time.sleep(random.randint(3,5))
        if response['no'] == '200':
            self.taskData = response['data']
            return True
        else:
            notify(f"{response['msg']}")
            return False

    def runBattleTask(self):
        for each in self.taskData:
            if each['title'] == '分享商品':
                if each['t_status'] == 0:
                    self.shareGoods(flag=1,count=2,dic=each)
                elif each['t_status'] == 1:
                    self.receiveAward(each)
                elif each['t_status'] == 2:
                    notify(f"[{each['title']}]\t领取成功")
            elif each['title'] == '参与欢太超级宠粉':
                if each['t_status'] == 0:
                    self.runViewTask(dic=each)
                elif each['t_status'] == 1:
                    self.receiveAward(each)
                elif each['t_status'] == 2:
                    notify(f"[{each['title']}]\t任务完成")
            elif each['title'] == '观看直播':
                if each['t_status'] == 0:
                    self.runViewTask(dic=each)
                elif each['t_status'] == 1:
                    self.receiveAward(each)
                elif each['t_status'] == 2:
                    notify(f"[{each['title']}]\t任务完成")
            elif each['title'] == '浏览真我Q3S' or each['title'] == '浏览真我Q3S':
                if each['t_status'] == 0:
                    self.runViewTask(dic=each)
                elif each['t_status'] == 1:
                    self.receiveAward(each)
                elif each['t_status'] == 2:
                    notify(f"[{each['title']}]\t任务完成")
            elif each['title'] == '浏览真我GT Neo2T' or each['title'] == '预约真我GT Neo2T':
                if each['t_status'] == 0:
                    self.runViewTask(dic=each)
                elif each['t_status'] == 1:
                    self.receiveAward(each)
                elif each['t_status'] == 2:
                    notify(f"[{each['title']}]\t任务完成")
            elif each['title'] == '浏览realme会场':
                if each['t_status'] == 0:
                    self.runViewTask(dic=each)
                elif each['t_status'] == 1:
                    self.receiveAward(each)
                elif each['t_status'] == 2:
                    notify(f"[{each['title']}]\t任务完成")

    # 获取积分数量(只找到这个，找不到昨天积分数据)
    def getIntegral(self):
        url = 'https://store.oppo.com/cn/oapi/credits/web/credits/show'
        headers = {
            'Host': 'store.oppo.com',
            'Connection': 'keep-alive',
            'source_type': '501',
            'clientPackage': 'com.oppo.store',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.9',
            'X-Requested-With': 'com.oppo.store',
            'Referer': 'https://store.oppo.com/cn/app/taskCenter/index?us=gerenzhongxin&um=hudongleyuan&uc=renwuzhongxin'
        }
        response = self.sess.get(url=url,headers=headers).json()
        if response['code'] == 200:
            return f"{self.dic['user']}\t总积分:{response['data']['userCredits']}"
        else:
            return f"{self.dic['user']}\t错误原因:{response}"

    # 执行欢太商城实例对象
    def start(self):
        self.sess.headers.update({
            "User-Agent":self.dic['UA']
        })
        self.sess.cookies.update({
            "Cookie": self.dic['CK']
        })
        if self.login() == True:
            if self.getBattleList() == True:              # 获取任务中心数据，判断CK是否正确(登录可能成功，但无法跑任务)
                self.runBattleTask()                        # 运行任务中心
                notify(self.getIntegral())

# 检测CK是否存在必备参数
def checkHT(dic):
    CK = dic['CK']
    if len(re.findall(r'source_type=.*?;',CK)) == 0:
        notify(f"{dic['user']}\tCK格式有误:可能缺少`source_type`字段")
        return False
    if len(re.findall(r'TOKENSID=.*?;',CK)) == 0:
        notify(f"{dic['user']}\tCK格式有误:可能缺少`TOKENSID`字段")
        return False
    if len(re.findall(r'app_param=.*?[;]?',CK)) == 0:
        notify(f"{dic['user']}\tCK格式有误:可能缺少`app_param`字段")
        return False
    return True

# 兼容云函数
def main_handler(event, context):
    global lists
    for each in lists:
        if each['CK']!='' and each['UA'] != '':
            if checkHT(each):
                battleForRealMe = BattleForRealMe(each)
                for count in range(3):
                    try:
                        time.sleep(random.randint(2,5))    # 随机延时
                        battleForRealMe.start()
                        break
                    except requests.exceptions.ConnectionError:
                        notify(f"{battleForRealMe.dic['user']}\t请求失败，随机延迟后再次访问")
                        time.sleep(random.randint(2,5))
                        continue
                else:
                    notify(f"账号: {battleForRealMe.dic['user']}\n状态: 取消登录\n原因: 多次登录失败")
                    break
        elif not all(each.values()):
            notify("账号:空账户\t状态:跳过")
        else:
            notify(f"账号: {each['user']}\n状态: 取消登录\n原因: json数据不齐全")
        notify('*' * 40 + '\n')
    if not os.path.basename(__file__).split('_')[-1][:-3] in notifyBlackList:
        send('RealMe积分大乱斗',allMess)

if __name__ == '__main__':
    main_handler(None,None)
