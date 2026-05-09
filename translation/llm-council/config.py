LANGUAGES = [
    ("es", "Spanish", "Español"),
    ("fr", "French", "Français"),
    ("de", "German", "Deutsch"),
    ("zh-CN", "Chinese Simplified", "简体中文"),
    ("ja", "Japanese", "日本語"),
    ("pt", "Portuguese", "Português"),
    ("ar", "Arabic", "العربية"),
    ("hi", "Hindi", "हिन्दी"),
    ("ru", "Russian", "Русский"),
    ("ko", "Korean", "한국어"),
    ("it", "Italian", "Italiano"),
    ("tl", "Tagalog", "Tagalog"),
    ("ceb", "Bisaya", "Bisaya"),
    ("id", "Bahasa Indonesia", "Bahasa Indonesia"),
    ("vi", "Vietnamese", "Tiếng Việt"),
    ("th", "Thai", "ไทย"),
    ("km", "Khmer", "ខ្មែរ"),
]

SOURCE_FILE = "data/chapters.json"
OUTPUT_DIR = "data/translations"

TRANSLATION_PROMPT = """You are translating a literary work from English to {target_lang} ({target_name}).

translate the following chapter faithfully, preserving:
- The literary tone and emotional depth
- The *emphasis* markers (asterisks for italic)
- The --- dividers
- The question format with *italics*
- Chapter structure exactly

Keep the JSON format identical. Only translate the text content, not the structure keys.

Chapter to translate:
{chapter_json}

Output ONLY the translated JSON, no explanation."""

COUNCIL_MODELS = [
    "google/gemini-2.5-pro-preview",
    "anthropic/claude-sonnet-4.5",
    "openai/gpt-5.1",
]

CHAIRMAN_MODEL = "google/gemini-2.5-pro-preview"

BATCH_SIZE = 5