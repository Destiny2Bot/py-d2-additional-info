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
- [x] generate_source_info.py
- [ ] generate_event_info.py
  - Assigned to FYWinds
- [x] generate_ghost_data.py
- [ ] generate_objective_to_triumph.py
- [ ] generate_bounty_data.py
- [x] generate_catalyst_data.py
- [ ] generate_powerful_rewards.py
- [x] generate_engram_rarity_icons.py
- [ ] generate_bright_engram_data.py
- [ ] generate_workaround_items.py
- [ ] generate_spider_mats.py
- [ ] generate_rich_text_objective.py
- [ ] generate_missing_collectible_info.py
- [ ] generate_watermark_info.py
- [x] generate_enums.py
- [ ] generate_missing_faction_tokens.py
- [ ] generate_season_watermark_backup.py
- [ ] generate_extended_ich.py
- [x] generate_adept_weapon_hashes.py
- [ ] generate_masterworks_with_cond_stats.py
- [ ] generate_raid_mods.py
- [ ] generate_subclass_plug_category_hashes.py
- [ ] generate_font_glyph_enums.py
- [ ] generate_trials_objectives.py