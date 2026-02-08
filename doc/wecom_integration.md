# GitHub Actions 定时发送企业微信通知

本文记录如何在本项目中使用 GitHub Actions 定时运行任务并把通知发送到企业微信群机器人（WeCom）。

## 步骤概览

1. 在企业微信的群聊中添加“群机器人”，记录 webhook key；如果启用了“加签”，同时记录 sign secret。
2. 在 GitHub 仓库中添加 Secrets：
   - `WECOM_WEBHOOK_KEY`（必填）
   - `WECOM_SIGN_SECRET`（可选，当机器人开启加签时填写）
3. 在仓库中添加 workflow：`.github/workflows/schedule_wecom.yml`，按需修改 `cron` 定时（注意 GitHub Actions 的 `cron` 使用 UTC）。
4. 添加发送脚本：`.github/scripts/send_wecom.sh`，脚本会处理可选签名并 POST 消息到群机器人。
5. 手动运行或等待定时触发，验证企业微信是否收到消息。

## Secrets 配置

在仓库页面：Settings → Secrets and variables → Actions → New repository secret

- 名称：`WECOM_WEBHOOK_KEY`，值为群机器人的 key（URL 中的 key 部分）。
- 若群机器人要求“加签”，再新增：`WECOM_SIGN_SECRET`，值为提供的 secret。

## 注意事项

- `cron` 使用 UTC 时区；例如 `0 0 * * *` 表示每天 UTC 00:00。
- 发送脚本中使用 `python3` 计算 HMAC-SHA256 签名（`ubuntu-latest` 环境自带 `python3`）。

## 文件位置

- Workflow: `.github/workflows/schedule_wecom.yml`
- 脚本: `.github/scripts/send_wecom.sh`

---

如需我替你把 `cron` 时间改为本地某个时刻，或把通知内容自定义为 `markdown` 格式，请告诉我。
