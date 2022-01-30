# py-d2-additional-info
命运2数据集生成 [d2-additional-info](https://github.com/DestinyItemManager/d2-additional-info) 的 Python 实现

## 对原项目的一些修改:
- 所有脚本文件名中 `-` 替换为 `_`
- 所有输出的英文字符串(值)译为中文
- 使用脚本 `generate_categories_translated` 翻译原 `categories.json` 到 `categories_translated.json`, 并生成 英-中 对照表 `translate_dict.json`

## TODO
- [x] manifest.py
- [x] flipped_enums.py
- [x] generate_categories_translated
- [x] generate_season_info.py
- [x] generate_season_to_source.py
- [x] generate_mod_slot_data.py
- [x] generate_mod_slot_data
- [ ] generate_source_info.py
- [ ] generate-event-info.js
- [x] generate-ghost-data.js
- [ ] generate-objective-to-triumph.js
- [ ] generate-bounty-data.js
- [x] generate-catalyst-data.js
- [ ] generate-powerful-rewards.js
- [x] generate-engram-rarity-icons.js
- [ ] generate-bright-engram-data.js
- [ ] generate-workaround-items.js
- [ ] generate-spider-mats.js
- [ ] generate-rich-text-objective.js
- [ ] generate-missing-collectible-info.js
- [ ] generate-watermark-info.js
- [x] generate-enums.js
- [ ] generate-missing-faction-tokens.js
- [ ] generate-season-watermark-backup.js
- [ ] generate-extended-ich.js
- [x] generate-adept-weapon-hashes.js
- [ ] generate-masterworks-with-cond-stats.js
- [ ] generate-raid-mods.js
- [ ] generate-subclass-plug-category-hashes.js
- [ ] generate-font-glyph-enums.js
- [ ] generate-trials-objectives.js