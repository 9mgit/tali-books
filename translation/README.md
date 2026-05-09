# Translation Setup

Uses llm-council pattern for multi-model translation with review.

## Prerequisites

1. Get OpenRouter API key: https://openrouter.ai/
2. Install Python dependencies:
   ```bash
   pip install aiohttp python-dotenv
   ```

## Set API Key

```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
```

Or create `.env` file:
```
OPENROUTER_API_KEY=sk-or-v1-...
```

## Run Translation

```bash
# Translate to all 17 languages
python translation/translate.py

# Or translate to single language
python translation/translate.py --lang es
```

## Languages

| Code | Language | Native |
|------|----------|--------|
| es | Spanish | Español |
| fr | French | Français |
| de | German | Deutsch |
| zh-CN | Chinese Simplified | 简体中文 |
| ja | Japanese | 日本語 |
| pt | Portuguese | Português |
| ar | Arabic | العربية |
| hi | Hindi | हिन्दी |
| ru | Russian | Русский |
| ko | Korean | 한국어 |
| it | Italian | Italiano |
| tl | Tagalog | Tagalog |
| ceb | Bisaya | Bisaya |
| id | Bahasa Indonesia | Bahasa Indonesia |
| vi | Vietnamese | Tiếng Việt |
| th | Thai | ไทย |
| km | Khmer | ខ្មែរ |

## Output

Files saved to: `data/translations/chapters_{lang_code}.json`

## API Cost Estimate

~17 languages × ~100 chapters × 3 models = ~5,100 API calls
At ~$1-3/1M tokens, estimated cost: $50-200 depending on chapter length and model pricing.