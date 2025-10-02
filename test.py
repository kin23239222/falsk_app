import requests


SendKey = "SCT298095TMocelyoVHKr37C6TIe6zAExA"
"""
向微信服务号发内容
:param text:
:return:
"""
url = f"https://sctapi.ftqq.com/{SendKey}.send"
data = {"title": "text"}
req = requests.post(url, data=data)
print(req.text)