import os
import sys
import asyncio
import redis
from pyrogram import Client, idle

import config


def connect_redis():
    try:
        url = f"rediss://default:{config.REDIS_PASSWORD}@{config.REDIS_HOST}:{config.REDIS_PORT}"
        r = redis.from_url(url, decode_responses=True, ssl_cert_reqs=None)
        r.ping()
        print(f"✅ تم الاتصال بـ Redis على {config.REDIS_HOST}:{config.REDIS_PORT}")
        return r
    except Exception as e:
        print(f"❌ فشل الاتصال بـ Redis : {e}")
        sys.exit(1)


async def main():
    rds = connect_redis()

    app = Client(
        name="MyBot",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        bot_token=config.TOKEN,
        plugins=dict(root="plugins"),
        workdir=os.path.dirname(__file__),
    )

    app.redis = rds

    await app.start()
    me = await app.get_me()
    config.botUsername = me.username

    print("──────────────────────────────────────")
    print(f"🤖 البوت يعمل الآن : @{me.username}")
    print(f"👤 المالك (Dev_Zaid) : {config.Dev_Zaid}")
    print("──────────────────────────────────────")

    await idle()
    await app.stop()
    print("🛑 تم إيقاف البوت.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 تم الإيقاف يدويًا.")
