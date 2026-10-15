---
role: chronicler
inputs: [entries]
output_schema: Summary
---
把下面的记录压缩成一段忠实的编年摘要，写法仿《通鉴》提纲：按季记事，先写年号与季节（如「天宝十一载冬」），再写这一季的事。
要求：
- 保留争议、延宕和未知之处。
- 不补入记录以外的史实。
- 隐藏数值只能写「风闻」。
记录：
{{ entries }}
