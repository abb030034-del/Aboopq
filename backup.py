"""
backup.py
==========
نسخ احتياطي لبيانات Redis وحفظها كملف JSON.

الاستخدام :
    python backup.py           # حفظ نسخة في backups/
    python backup.py restore backups/backup_2024-01-01.json   # استعادة
"""

import json
import os
import sys
from datetime import datetime

import redis
import config

BACKUP_DIR = os.path.join(os.path.dirname(__file__), "backups")


def get_redis():
    r = redis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=config.REDIS_DB,
        password=config.REDIS_PASSWORD,
        decode_responses=True,
    )
    r.ping()
    return r


def backup():
    """تصدير كل مفاتيح Redis إلى ملف JSON"""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    rds = get_redis()

    data = {}
    for key in rds.scan_iter("*"):
        t = rds.type(key)
        if t == "string":
            data[key] = {"type": "string", "value": rds.get(key)}
        elif t == "hash":
            data[key] = {"type": "hash", "value": rds.hgetall(key)}
        elif t == "set":
            data[key] = {"type": "set", "value": list(rds.smembers(key))}
        elif t == "list":
            data[key] = {"type": "list", "value": rds.lrange(key, 0, -1)}
        elif t == "zset":
            data[key] = {"type": "zset", "value": rds.zrange(key, 0, -1, withscores=True)}

    filename = os.path.join(BACKUP_DIR, f"backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ تم حفظ النسخة الاحتياطية : {filename}  ({len(data)} مفتاح)")
    return filename


def restore(path: str):
    """استعادة بيانات Redis من ملف JSON"""
    if not os.path.exists(path):
        print(f"❌ الملف غير موجود : {path}")
        sys.exit(1)

    rds = get_redis()
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    pipe = rds.pipeline()
    for key, info in data.items():
        t = info["type"]
        pipe.delete(key)
        if t == "string":
            pipe.set(key, info["value"])
        elif t == "hash":
            if info["value"]:
                pipe.hset(key, mapping=info["value"])
        elif t == "set":
            if info["value"]:
                pipe.sadd(key, *info["value"])
        elif t == "list":
            if info["value"]:
                pipe.rpush(key, *info["value"])
        elif t == "zset":
            if info["value"]:
                mapping = {v: s for v, s in info["value"]}
                pipe.zadd(key, mapping)
    pipe.execute()

    print(f"✅ تم استعادة {len(data)} مفتاح من : {path}")


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "restore":
        restore(sys.argv[2])
    else:
        backup()
