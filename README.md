# WeChatLog
This is the repo for the wechat log recognize by openai.
curl -X 'POST' \
  'https://wechat-ocr-wbdtphkoqm.cn-hangzhou.fcapp.run/upload/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@test.png;type=image/png'