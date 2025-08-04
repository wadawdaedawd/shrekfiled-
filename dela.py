# meta developer: @tartaletkad
from .. import loader, utils

@loader.tds
class GetLinkSmartMod(loader.Module):
    """Умная генерация tg://user ссылки"""

    strings = {"name": "GetLinkSmart"}

    async def getlinkcmd(self, message):
        """[реплай/@username/ID/текст] — выдать tg://user ссылку"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        if reply:
            user = await reply.get_sender()
            link = f"tg://user?id={user.id}"
            await utils.answer(message, f"👤 ПРОФИЛЬ: {link}")
            return

        if args and args.strip().startswith("@"):
            try:
                user = await self._client.get_entity(args.strip())
                link = f"tg://user?id={user.id}"
                await utils.answer(message, f"👤 ПРОФИЛЬ: {link}")
            except Exception as e:
                await utils.answer(message, f"❌ Не нашёл: {e}")
            return

        if args:
            link = f"tg://user?id={args.strip()}"
            await utils.answer(message, f"👤 ПРОФИЛЬ: {link}")
            return

        await utils.answer(message, "✍️ Укажи @юзернейм, ответь на сообщение или введи ID/текст.")
