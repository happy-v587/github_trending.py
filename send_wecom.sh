#!/usr/bin/env bash
set -euo pipefail

# send_wecom.sh
# 优先使用环境变量 JSON_OUTPUT（来自 workflow），否则运行 github_trending.py 获取输出。
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

# 获取原始输出
if [ -n "${JSON_OUTPUT:-}" ]; then
  RAW_OUTPUT="$JSON_OUTPUT"
else
  RAW_OUTPUT=$(python3 - <<'PY'
import subprocess
try:
    proc = subprocess.run(["python3", "github_trending.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False)
    text = proc.stdout or "(no output)"
except Exception as e:
    text = f"(error running github_trending.py) {e}"
print(text)
PY
)
fi

# 截断到 6000 字符以防超长
TRUNCATED=$(printf "%s" "$RAW_OUTPUT" | cut -c1-6000)

# JSON 编码文本以安全插入到 payload
ESCAPED_JSON=$(python3 - <<'PY'
import json,sys
text = sys.stdin.read()
print(json.dumps(text))
PY
<<EOF
$TRUNCATED
EOF
)

PAYLOAD=$(printf '{"msgtype":"markdown","markdown":{"content":%s}}' "$ESCAPED_JSON")

curl -sS -H "Content-Type: application/json" -d "$PAYLOAD" "$URL"
