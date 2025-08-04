# meta developer: @yourusername
from telethon.tl.types import PeerUser
from .. import loader, utils

@loader.tds
class GetLinkMod(loader.Module):
    """Получает ссылку на Telegram-профиль по ID или реплаю"""
    strings = {"name": "GetLink"}

    async def getlinkcmd(self, message):
        """[реплай / ID / username] — Получить ссылку на профиль"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        user = None

        if reply:
            user = await self._client.get_entity(reply.from_id)
        elif args:
            try:
                entity = await self._client.get_entity(args)
                user = entity
            except Exception as e:
                await utils.answer(message, f"❌ Не удалось найти пользователя: {e}")
                return
        else:
            await utils.answer(message, "👤 Укажи пользователя или сделай реплай")
            return

        if not getattr(user, "id", None):
            await utils.answer(message, "❌ Не могу получить ID пользователя")
            return

        user_link = f"tg://user?id={user.id}"
        username_link = (
            f"https://t.me/{user.username}" if user.username else user_link
        )

        output = f"🆔 ID: `{user.id}`\n🔗 Ссылка: [{user_link}]({user_link})"
        if user.username:
            output += f"\n🌐 Паблик: [@{user.username}](https://t.me/{user.username})"

        await utils.answer(message, output)
