import requests

cookies = {
    'accessToken': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NzRlODA2NDIyY2FmZDQwYjIxZDI0MTYiLCJ1c2VybmFtZSI6ImlfYW1faHV5MTIiLCJhdmF0YXIiOiJhXzZlOWIyOTU4NzljMDQyZTkyZTgxZDdmMGYzZWZmYTVjIiwiZGlzY29yZF9pZCI6IjkwNTY1NzYxMjkyODk1ODQ4NCIsImNsYWltIjp0cnVlLCJpYXQiOjE3NTA0MzQ0NjgsImV4cCI6MTc1MDUyMDg2OH0.xr0S9TUPmNADppd1KuPQQtpF-vAqCiHPc7r75M5E0b7eXoP9YMtxRQaEljcFPlrSPuXKNyeke5GTevmt8__wCYMwVQQiwm3HgfcABxZcyb_RuNSO7f_He7HbEB3eAp0CtVCi1ATKZej4d7JgnPh2fXdDge0T2kCmVQHqsAo8dEw-WxPmxZvAOWBwQVyVkZsrgugt5PsYbOFzaqs-hJrp32jBcLa69mKpn7SD8S9ikx4JOjhZ-WyIUHdKRvGrlmgHQ-iRr3GiQLI9vNRku9glTz7G1rSXx3NKf8i4iaRfruUymlqre7WnDXZcUcldiGXS0JGYU_lpPDY4xTKdG49BBw',
    'refreshToken': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NzRlODA2NDIyY2FmZDQwYjIxZDI0MTYiLCJkaXNjb3JkX2lkIjoiOTA1NjU3NjEyOTI4OTU4NDg0IiwiaWF0IjoxNzUwNDM0NDY4LCJleHAiOjE3NTEwMzkyNjh9.qz7hmEajiPjLtD3Ktj6NQWxuZnEUaU3NEsjETnZpWAYnHzB88fMNDolIfvDkBj7181F26treM-DX8iJjjVJcq0F5FRHfmxHsc6nF-oXBwYOxJX3kxMUqS9pokieuW2fRfu7y8nRWBAqBDVIobHz3kPZvPAiIXJsxFlKJz7xelcqaALEFwtCUux4KeF1tM8gc9tmQWl9QCoA-lLQgL2vyxEmMsTzAki8W3s-v7v-ZFWgyv5TklIUdHxYudpcESKeC3KGQsuzSho9SZ5Ogh2aDDw7Cq0st8tWYlssKt5JRywHITGXLzTzEnFLXeeqm5oC0vGTgm6tRfm-vG4f9N5ZXBA',
    'cf_clearance': 'SpmJqLBqr50HcGlNfn.61NnFQCthd7OdMTq6UpRDrmQ-1750470251-1.2.1.1-WhGbg3_GBOse7yrjbNcPxakaMRzodns1ezDLpiTvAiLEmCX3GU148XSRZIvtSR8m88jKGBy026BKQSI.V9S8kd0ubZ_G.H13Uc7jq8HWqMus_KWwvUtRW.CzVtla31fkCpMk5iW2gMN41ErDaKCR7yy9uANVCV5Hgy_Na82aXd5u0dfrYtOXhdWDJ5zD9bTrMCxwsVLK3z9kMPdnOayAcPVjr5DpQ3rvAsejNbtFwMKjMYsIk32.y4Wzg8yW_bF8g7FwGPPJ_vGwqBslNdVQ8P9WpT9HViSbXNKB9uVnkr8epmEIje.23z7WPwmf5HrGTQ.vOYnPWMKVSn6BUUsQpEhx7Z_BL1VJaH7GFUcAYGDpIiDasY.HxZ4bGInExa1o',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
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
    'cookie': 'accessToken=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NzRlODA2NDIyY2FmZDQwYjIxZDI0MTYiLCJ1c2VybmFtZSI6ImlfYW1faHV5MTIiLCJhdmF0YXIiOiJhXzZlOWIyOTU4NzljMDQyZTkyZTgxZDdmMGYzZWZmYTVjIiwiZGlzY29yZF9pZCI6IjkwNTY1NzYxMjkyODk1ODQ4NCIsImNsYWltIjp0cnVlLCJpYXQiOjE3NTA0MzQ0NjgsImV4cCI6MTc1MDUyMDg2OH0.xr0S9TUPmNADppd1KuPQQtpF-vAqCiHPc7r75M5E0b7eXoP9YMtxRQaEljcFPlrSPuXKNyeke5GTevmt8__wCYMwVQQiwm3HgfcABxZcyb_RuNSO7f_He7HbEB3eAp0CtVCi1ATKZej4d7JgnPh2fXdDge0T2kCmVQHqsAo8dEw-WxPmxZvAOWBwQVyVkZsrgugt5PsYbOFzaqs-hJrp32jBcLa69mKpn7SD8S9ikx4JOjhZ-WyIUHdKRvGrlmgHQ-iRr3GiQLI9vNRku9glTz7G1rSXx3NKf8i4iaRfruUymlqre7WnDXZcUcldiGXS0JGYU_lpPDY4xTKdG49BBw; refreshToken=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NzRlODA2NDIyY2FmZDQwYjIxZDI0MTYiLCJkaXNjb3JkX2lkIjoiOTA1NjU3NjEyOTI4OTU4NDg0IiwiaWF0IjoxNzUwNDM0NDY4LCJleHAiOjE3NTEwMzkyNjh9.qz7hmEajiPjLtD3Ktj6NQWxuZnEUaU3NEsjETnZpWAYnHzB88fMNDolIfvDkBj7181F26treM-DX8iJjjVJcq0F5FRHfmxHsc6nF-oXBwYOxJX3kxMUqS9pokieuW2fRfu7y8nRWBAqBDVIobHz3kPZvPAiIXJsxFlKJz7xelcqaALEFwtCUux4KeF1tM8gc9tmQWl9QCoA-lLQgL2vyxEmMsTzAki8W3s-v7v-ZFWgyv5TklIUdHxYudpcESKeC3KGQsuzSho9SZ5Ogh2aDDw7Cq0st8tWYlssKt5JRywHITGXLzTzEnFLXeeqm5oC0vGTgm6tRfm-vG4f9N5ZXBA; cf_clearance=SpmJqLBqr50HcGlNfn.61NnFQCthd7OdMTq6UpRDrmQ-1750470251-1.2.1.1-WhGbg3_GBOse7yrjbNcPxakaMRzodns1ezDLpiTvAiLEmCX3GU148XSRZIvtSR8m88jKGBy026BKQSI.V9S8kd0ubZ_G.H13Uc7jq8HWqMus_KWwvUtRW.CzVtla31fkCpMk5iW2gMN41ErDaKCR7yy9uANVCV5Hgy_Na82aXd5u0dfrYtOXhdWDJ5zD9bTrMCxwsVLK3z9kMPdnOayAcPVjr5DpQ3rvAsejNbtFwMKjMYsIk32.y4Wzg8yW_bF8g7FwGPPJ_vGwqBslNdVQ8P9WpT9HViSbXNKB9uVnkr8epmEIje.23z7WPwmf5HrGTQ.vOYnPWMKVSn6BUUsQpEhx7Z_BL1VJaH7GFUcAYGDpIiDasY.HxZ4bGInExa1o',
}

json_data = {
    'key': 'c209fd9b6d62e31029a71ae8b0556f79',
}

response = requests.post('https://script.banana-hub.xyz/api/tool/resethwid', cookies=cookies, headers=headers, json=json_data)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"key":"c209fd9b6d62e31029a71ae8b0556f79"}'
#response = requests.post('https://script.banana-hub.xyz/api/tool/resethwid', cookies=cookies, headers=headers, data=data)
