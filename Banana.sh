import http.client
import json

conn = http.client.HTTPSConnection('script.banana-hub.xyz')
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.7',
    'content-type': 'application/json',
    'origin': 'https://script.banana-hub.xyz',
    'priority': 'u=1, i',
    'referer': 'https://script.banana-hub.xyz/dashboard',
    'sec-ch-ua': '"Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version-list': '"Chromium";v="136.0.0.0", "Brave";v="136.0.0.0", "Not.A/Brand";v="99.0.0.0"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'cookie': 'accessToken=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NzRlODA2NDIyY2FmZDQwYjIxZDI0MTYiLCJ1c2VybmFtZSI6ImlfYW1faHV5MTIiLCJhdmF0YXIiOiJhXzZlOWIyOTU4NzljMDQyZTkyZTgxZDdmMGYzZWZmYTVjIiwiZGlzY29yZF9pZCI6IjkwNTY1NzYxMjkyODk1ODQ4NCIsImNsYWltIjp0cnVlLCJpYXQiOjE3NTA0MzQ0NjgsImV4cCI6MTc1MDUyMDg2OH0.xr0S9TUPmNADppd1KuPQQtpF-vAqCiHPc7r75M5E0b7eXoP9YMtxRQaEljcFPlrSPuXKNyeke5GTevmt8__wCYMwVQQiwm3HgfcABxZcyb_RuNSO7f_He7HbEB3eAp0CtVCi1ATKZej4d7JgnPh2fXdDge0T2kCmVQHqsAo8dEw-WxPmxZvAOWBwQVyVkZsrgugt5PsYbOFzaqs-hJrp32jBcLa69mKpn7SD8S9ikx4JOjhZ-WyIUHdKRvGrlmgHQ-iRr3GiQLI9vNRku9glTz7G1rSXx3NKf8i4iaRfruUymlqre7WnDXZcUcldiGXS0JGYU_lpPDY4xTKdG49BBw; refreshToken=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NzRlODA2NDIyY2FmZDQwYjIxZDI0MTYiLCJkaXNjb3JkX2lkIjoiOTA1NjU3NjEyOTI4OTU4NDg0IiwiaWF0IjoxNzUwNDM0NDY4LCJleHAiOjE3NTEwMzkyNjh9.qz7hmEajiPjLtD3Ktj6NQWxuZnEUaU3NEsjETnZpWAYnHzB88fMNDolIfvDkBj7181F26treM-DX8iJjjVJcq0F5FRHfmxHsc6nF-oXBwYOxJX3kxMUqS9pokieuW2fRfu7y8nRWBAqBDVIobHz3kPZvPAiIXJsxFlKJz7xelcqaALEFwtCUux4KeF1tM8gc9tmQWl9QCoA-lLQgL2vyxEmMsTzAki8W3s-v7v-ZFWgyv5TklIUdHxYudpcESKeC3KGQsuzSho9SZ5Ogh2aDDw7Cq0st8tWYlssKt5JRywHITGXLzTzEnFLXeeqm5oC0vGTgm6tRfm-vG4f9N5ZXBA; cf_clearance=YG72Xxb8Yy4bWeNYSax1mwC8bFgPLwyb29PjXMX8CGk-1750505527-1.2.1.1-UszUexG1PgqCozse.fwzRaZ98y_MGOLk12eAbFDaXEhToLHcLiyo0JNBtEuZ7pIBdq5kC8GVhvbiawXvFyP0sn5iJ4eLKXIhOlnaCHvg9pjKy9QqLuHkL8GNsMduqRBKjTATh0dptf9zogeB3ZswlI1a8MLMBsLv6O6FHni7maxV7mshYyTC4JW1Sw80ESSpCdwKg2vJfMlocuTL6aqBvSRJzVIgEzJoLAf7yFN9_134Ic24PeZHlXBlJ14e2h5HWF7GeTwy6.eoIeEXSyu8F08vxmedyB5mUuhdA55TWD2ySWNaTOG7tKygJDK_UjqXMPkSaXr943bZQIjLplqZBfZrsn5HmwyvHNZs5T_flb4kdcMaBfGeVgGKwrCnnIev',
}
json_data = {
    'key': 'c209fd9b6d62e31029a71ae8b0556f79',
}
conn.request(
    'POST',
    '/api/tool/resethwid',
    json.dumps(json_data),
    # '{"key":"c209fd9b6d62e31029a71ae8b0556f79"}',
    headers
)
response = conn.getresponse()
