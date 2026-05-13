#!/usr/bin/env python3
"""通过 GitHub API 推送 crystal-secrets.html 的修改"""
import urllib.request
import urllib.parse
import json
import base64
import os

TOKEN = os.environ.get('GITHUB_TOKEN', 'ghp_uKK7NTtTtNUL2MumCDaKqIzPFm1KXN1zm9xd')
OWNER = 'SAGEBOOL'
REPO = 'crystal-calculator'
FILE_PATH = 'crystal-secrets.html'
BRANCH = 'main'

# 读取文件内容
with open(FILE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Base64 编码
encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')

# 获取文件当前的 SHA
url_get = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{FILE_PATH}?ref={BRANCH}"
req_get = urllib.request.Request(url_get)
req_get.add_header('Authorization', f'token {TOKEN}')
req_get.add_header('Accept', 'application/vnd.github.v3+json')

try:
    with urllib.request.urlopen(req_get, timeout=10) as response:
        data = json.loads(response.read().decode('utf-8'))
        sha = data['sha']
        print(f"✓ 获取到文件 SHA: {sha}")
except Exception as e:
    print(f"✗ 获取 SHA 失败: {e}")
    exit(1)

# 更新文件
url_put = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{FILE_PATH}"
payload = {
    "message": "移除封面图片旋转动画，改为静态展示",
    "content": encoded,
    "branch": BRANCH,
    "sha": sha
}

data = json.dumps(payload).encode('utf-8')
req_put = urllib.request.Request(url_put, data=data)
req_put.method = "PUT"
req_put.add_header('Authorization', f'token {TOKEN}')
req_put.add_header('Accept', 'application/vnd.github.v3+json')
req_put.add_header('Content-Type', 'application/json')

try:
    with urllib.request.urlopen(req_put, timeout=15) as response:
        result = json.loads(response.read().decode('utf-8'))
        print(f"✓ 文件已成功更新!")
        print(f"  提交 SHA: {result['commit']['sha']}")
        print(f"  查看: https://github.com/{OWNER}/{REPO}/blob/{BRANCH}/{FILE_PATH}")
except Exception as e:
    print(f"✗ 更新失败: {e}")
    exit(1)
