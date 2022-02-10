# py-d2-additional-info
命运2数据集生成 [d2-additional-info](https://github.com/DestinyItemManager/d2-additional-info) 的 Python 实现

## 对原项目的一些修改:
- 所有脚本文件名中 `-` 替换为 `_`
- 所有输出的英文字符串(值)译为中文
- 使用脚本 `generate_categories_translated` 翻译原 `categories.json` 到 `categories_translated.json`, 并生成 英-中 对照表 `translate_dict.json`
- 自行实现 manifest 功能