import os
import json

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_settings(data: dict):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

# ====== الإعدادات الأساسية ======
API_ID       = 21802065
API_HASH     = "2a8d929f6584561a32fc93e1f044652d"
TOKEN        = "8944149921:AAHsoF3LMIeNos-CIwshQFff36nKd1QFhZo"
Dev_Zaid     = 8588392906
sudo_id      = [Dev_Zaid]
botUsername  = ""

# ====== إعدادات Redis (Upstash) ======
REDIS_HOST     = "integral-ultrafine-zany-57472.db.redis.io"
REDIS_PORT     = 18298
REDIS_DB       = 0
REDIS_PASSWORD = "y9KclYxSQe2OlJrN3aIJAeCmgHbvaYgU"
