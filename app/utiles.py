import requests

# 机器人ID、聊天窗口ID
BOT_TOKEN = "7502031135:AAFiUxRD-N7sj4rGYBVCIadZsg0btLqRwLQ"
CHAT_ID = "6360891094"

def send_tg_message(text: str):
    """
    向tg机器人发送消息
    :param text: 消息内容
    :return:
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload)



