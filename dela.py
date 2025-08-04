# meta developer: @yourusername
from .. import loader, utils

@loader.tds
class GetLinkSmartMod(loader.Module):
    """Умная генерация tg://user ссылки: реально — если ник/реплай, иначе — как есть"""

    strings = {"name": "GetLinkSmart"}

    async def getlinkcmd(self, message):
        """[реплай / @username / ID / текст] — tg://user:id..."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        # Если реплай — пробуем получить Entity
        if reply:
            user = await reply.get_sender()
            link = f"tg://user?id={user.id}"
            await utils.answer(message, f"👤 ПРОФИЛЬ: [ПРОФИЛЬ]({link})")
            return

        # Если аргумент — @username (начинается с @)
        if args and args.strip().startswith("@"):
            try:
                user = await self._client.get_entity(args.strip())
                link = f"tg://user?id={user.id}"
                await utils.answer(message, f"👤 ПРОФИЛЬ: [ПРОФИЛЬ]({link})")
            except Exception as e:
                await utils.answer(message, f"❌ Не нашёл: {e}")
            return

        # Всё остальное просто преобразуем в ссылку "как есть"
        if args:
            link = f"tg://user?id={args.strip()}"
            await utils.answer(message, f"👤 ПРОФИЛЬ: [ПРОФИЛЬ]({link})")
            return

        await utils.answer(message, "✍️ Укажи @юзернейм, ответь на сообщение или введи ID/текст.")
