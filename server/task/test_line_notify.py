import requests

headers = {
    "Authorization": "Bearer " + "klniRzhX0i6Qr8yR4MDA61tiii6hlcvGh5kkb8vxIgw",  # 貼上權杖碼
    "Content-Type": "application/x-www-form-urlencoded"
}
params = {"message": "測試測試"}
r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=params)