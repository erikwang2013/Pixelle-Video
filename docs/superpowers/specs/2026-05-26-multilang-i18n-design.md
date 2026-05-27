# Multi-Language i18n for Pixelle-Video Web UI

## Summary

Add 12 new language translations to the Streamlit web UI via locale JSON files, using LLM batch translation from Simplified Chinese (`zh_CN.json`).

## Approach

- **Source**: `zh_CN.json` (500 translation keys)
- **Method**: LLM batch translation, 50 keys per batch
- **Code changes**: None — existing `load_locales()` auto-discovers all `*.json` files in `web/i18n/locales/`

## Languages to add

| Language | Code |
|----------|------|
| English | `en_US` (exists) |
| Simplified Chinese | `zh_CN` (exists) |
| Traditional Chinese | `zh_TW` |
| Cantonese | `yue_HK` |
| Japanese | `ja_JP` |
| Korean | `ko_KR` |
| French | `fr_FR` |
| German | `de_DE` |
| Spanish | `es_ES` |
| Filipino | `fil_PH` |
| Thai | `th_TH` |
| Vietnamese | `vi_VN` |
| Brazilian Portuguese | `pt_BR` |
| Uyghur | `ug_CN` |

## File changes

- **New**: 12 locale JSON files in `web/i18n/locales/`
- **No code changes needed**: i18n system auto-loads all JSON files

## Risks

- LLM translation quality varies by language; rare languages (Uyghur, Cantonese) may need manual review
- Translation of technical terms (API Key, ComfyUI, Workflow) should be kept in original or use standard translations
