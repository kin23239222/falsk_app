from email.utils import formataddr

import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 机器人ID、聊天窗口ID
BOT_TOKEN = "7502031135:AAFiUxRD-N7sj4rGYBVCIadZsg0btLqRwLQ"
CHAT_ID = "6360891094"

# 网易邮箱授权码
WY_MAIl_PASS = "EP6YSMbtqHN3ZdAh"
WY_mail_host = "smtp.163.com"
WY_mail_user = "18476776602@163.com"

def send_tg_message(text: str):
    """
    向tg机器人发送消息
    :param text: 消息内容
    :return:
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload)


def wy_mail_send(text: str, content="任务提醒"):
    """
    向网易邮箱发送通知
    :param text: 发送标题
    :param content: 发送内容
    :return:
    """
    # ---------- 构造邮件 ----------
    # MIMEText：邮件正文，"plain" 表示纯文本，"utf-8" 保证中文不会乱码
    message = MIMEText(text, "plain", "utf-8")
    # 发件人信息（显示在邮件客户端中“发件人”字段）
    message["From"] = formataddr(("任务提醒机器人", WY_mail_user))
    # 收件人信息（显示在邮件客户端中“收件人”字段）
    message["To"] = formataddr(("18476776602@163.com", "utf-8"))
    # 邮件标题
    message["Subject"] = Header(text, "utf-8")

    # ---------- 发送邮件 ----------
    try:
        # 建立一个SSL加密的SMTP连接，163邮箱用465端口
        smtp = smtplib.SMTP_SSL(WY_mail_host, 465)
        # 登录邮箱服务器
        smtp.login(WY_mail_user, WY_MAIl_PASS)
        # 发送邮件
        smtp.sendmail(WY_mail_user, ["18476776602@163.com"], message.as_string())
        # 关闭连接
        smtp.quit()
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
