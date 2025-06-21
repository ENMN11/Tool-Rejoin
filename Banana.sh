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
    'cookie': 'accessToken=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NzRlODA2NDIyY2FmZDQwYjIxZDI0MTYiLCJ1c2VybmFtZSI6ImlfYW1faHV5MTIiLCJhdmF0YXIiOiJhXzZlOWIyOTU4NzljMDQyZTkyZTgxZDdmMGYzZWZmYTVjIiwiZGlzY29yZF9pZCI6IjkwNTY1NzYxMjkyODk1ODQ4NCIsImNsYWltIjp0cnVlLCJpYXQiOjE3NTA0MzQ0NjgsImV4cCI6MTc1MDUyMDg2OH0.xr0S9TUPmNADppd1KuPQQtpF-vAqCiHPc7r75M5E0b7eXoP9YMtxRQaEljcFPlrSPuXKNyeke5GTevmt8__wCYMwVQQiwm3HgfcABxZcyb_RuNSO7f_He7HbEB3eAp0CtVCi1ATKZej4d7JgnPh2fXdDge0T2kCmVQHqsAo8dEw-WxPmxZvAOWBwQVyVkZsrgugt5PsYbOFzaqs-hJrp32jBcLa69mKpn7SD8S9ikx4JOjhZ-WyIUHdKRvGrlmgHQ-iRr3GiQLI9vNRku9glTz7G1rSXx3NKf8i4iaRfruUymlqre7WnDXZcUcldiGXS0JGYU_lpPDY4xTKdG49BBw; refreshToken=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NzRlODA2NDIyY2FmZDQwYjIxZDI0MTYiLCJkaXNjb3JkX2lkIjoiOTA1NjU3NjEyOTI4OTU4NDg0IiwiaWF0IjoxNzUwNDM0NDY4LCJleHAiOjE3NTEwMzkyNjh9.qz7hmEajiPjLtD3Ktj6NQWxuZnEUaU3NEsjETnZpWAYnHzB88fMNDolIfvDkBj7181F26treM-DX8iJjjVJcq0F5FRHfmxHsc6nF-oXBwYOxJX3kxMUqS9pokieuW2fRfu7y8nRWBAqBDVIobHz3kPZvPAiIXJsxFlKJz7xelcqaALEFwtCUux4KeF1tM8gc9tmQWl9QCoA-lLQgL2vyxEmMsTzAki8W3s-v7v-ZFWgyv5TklIUdHxYudpcESKeC3KGQsuzSho9SZ5Ogh2aDDw7Cq0st8tWYlssKt5JRywHITGXLzTzEnFLXeeqm5oC0vGTgm6tRfm-vG4f9N5ZXBA; cf_clearance=Ml.xu5E8D4nBa2aAfGGnKzbLgnhhxAbiBAmnYx__rjE-1750510944-1.2.1.1-fT9ZISjYx2oI6m8my5P_zbQm..D0pnMhuG0r9CIHKUmwlgR0nYv6xr5If1REkayiW1PzNfhfy4P6rvgHZQprPDc8fK3pYMhsImWGZh8zMV4FcAqoWnhjgQsayxuPfUIcNX07jxZljj6kcarvqPDS4YDrxdEF0882h9Y0zK73FswcAi0d38cK3XvZC2pp3QZxm47q1GYl1Vuqnm4FcV4o.GauawKnjbUV8W0TXbws6zM0gY5pTqu7K_JPhK65puIsArZxv_deOdv3ZLkAFZ2zZ2DhNoUlFzM119kWLzL93RcVjm93krXANQcpDPPsibRllxrKVsyZd_Wy1P7kQqKHYkoWGzT5emQ2bevupsUAmvrIPsCuuKMn1sAP9svMPlYj',
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
