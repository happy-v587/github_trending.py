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

# 构造消息（text 示例），按需修改成 markdown 或其他类型
PAYLOAD='{"msgtype":"text","text":{"content":"定时任务已运行：项目任务完成。"}}'

curl -sS -H "Content-Type: application/json" -d "${PAYLOAD}" "${URL}"
