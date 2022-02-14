# coding=utf-8 
from qnyflib import QNDK
import json
from apscheduler.schedulers.blocking import BlockingScheduler
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def auto_daka():
    stu = json.load(open("user.json", "r", encoding='utf8'))
    for user in stu:
        role = QNDK(user["YXDM"], user["XGH"], user["name"], user["password"], user["location"], user["JWD"])
        #判断是否已经打卡
        if role.isclockin():
            send_email(user["name"] + "同学，今日已打卡成功，请勿重复打卡！", user["email"])
            if user["email"] != "1196720398@qq.com":
                send_email(user["name"] + "同学，今日已打卡成功，请勿重复打卡！", "1196720398@qq.com")
        else:
            if role.Daka():
                send_email(user["name"] + "同学，" + "今日打卡成功！", user["email"])
                if user["email"] != "1196720398@qq.com":
                    send_email(user["name"] + "同学，" + "今日打卡成功！", "1196720398@qq.com")
            else:
                send_email(user["name"] + "同学，" + "，今日打卡失败！请尝试手动打卡。", user["email"])
                if user["email"] != "1196720398@qq.com":
                    send_email(user["name"] + "同学，" + "今日打卡成功！", "1196720398@qq.com")


def send_email(msg, email):
    # 发信方的信息：发信邮箱，QQ 邮箱授权码
    from_addr = '2964835492@qq.com'
    password = 'creqqlqcnmabdcdd'
    
    # 收信方邮箱
    to_addr = email
    
    # 发信服务器
    smtp_server = 'smtp.qq.com'
    
    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    msg = MIMEText(msg,'plain','utf-8')
    
    # 邮件头信息
    msg['From'] = Header(from_addr)
    msg['To'] = Header(to_addr)
    msg['Subject'] = Header('疫情自动打卡提醒')
    
    # 开启发信服务，这里使用的是加密传输
    server = smtplib.SMTP_SSL()
    server.connect(smtp_server,465)
    # 登录发信邮箱
    server.login(from_addr, password)
    # 发送邮件
    server.sendmail(from_addr, to_addr, msg.as_string())
    # 关闭服务器
    server.quit()
    

          
scheduler = BlockingScheduler(timezone='Asia/Shanghai')
# 添加任务,每天早上8.30点打卡
scheduler.add_job(auto_daka, 'cron', day_of_week='*', hour='8', minute='30', second='00')
print("任务开始！")
scheduler.start()