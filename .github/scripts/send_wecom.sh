#!/usr/bin/env bash
set -euo pipefail

# 环境变量：
# WECOM_WEBHOOK_KEY - 必填（来自仓库 Secrets）
# WECOM_SIGN_SECRET - 可选（如果机器人开启加签）

if [ -z "${WECOM_WEBHOOK_KEY:-}" ]; then
  echo "WECOM_WEBHOOK_KEY is not set" >&2
  exit 1
fi

TIMESTAMP=$(date +%s)
URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=${WECOM_WEBHOOK_KEY}"

if [ -n "${WECOM_SIGN_SECRET:-}" ]; then
  export TIMESTAMP
  SIGN=$(python3 - <<'PY'
import os, hmac, hashlib, base64, urllib.parse
secret = os.environ['WECOM_SIGN_SECRET']
timestamp = os.environ['TIMESTAMP']
string_to_sign = f"{timestamp}\n{secret}"
h = hmac.new(secret.encode('utf-8'), string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()
sign = urllib.parse.quote_plus(base64.b64encode(h).decode())
print(sign)
PY
)
  URL="${URL}&timestamp=${TIMESTAMP}&sign=${SIGN}"
fi

# 运行项目脚本并获取输出，将结果作为 markdown 内容发送
# 限制内容长度以避免超过 webhook 限制（截断到 6000 字节）
OUTPUT_JSON=$(python3 - <<'PY'
import subprocess, json
try:
  proc = subprocess.run(["python3", "github_trending.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False)
  text = proc.stdout or "(no output)"
except Exception as e:
  text = f"(error running github_trending.py) {e}"
# 截断到 6000 字符
text = text[:6000]
print(json.dumps(text))
PY
)

PAYLOAD=$(printf '{"msgtype":"markdown","markdown":{"content":%s}}' "$OUTPUT_JSON")

curl -sS -H "Content-Type: application/json" -d "$PAYLOAD" "$URL"
