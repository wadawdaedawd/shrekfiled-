# meta developer: @yourusername
from .. import loader, utils
from telethon.tl.types import PeerUser
from telethon.errors import UsernameNotOccupiedError

@loader.tds
class GetLinkMod(loader.Module):
    """Выдает ссылку tg://user?id= по ID, юзернейму или реплаю"""
    strings = {"name": "GetLink"}

    async def getlinkcmd(self, message):
        """[реплай / ID / username] — Получить tg:// ссылку на профиль"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        user = None

        if reply:  # если реплай
            user = await self._client.get_entity(reply.from_id)
        elif args:  # если что-то передано в аргументах
            try:
                if args.isdigit():
                    user = await self._client.get_entity(int(args))
                else:
                    user = await self._client.get_entity(args)
            except UsernameNotOccupiedError:
                await utils.answer(message, "❌ Такого пользователя нет.")
                return
            except Exception as e:
                await utils.answer(message, f"❌ Ошибка: {e}")
                return
        else:
            await utils.answer(message, "✍️ Укажи ID, ник, или ответь на сообщение.")
            return

        user_id = getattr(user, "id", None)
        if not user_id:
            await utils.answer(message, "❌ Не удалось получить ID пользователя.")
            return

        link = f"tg://user?id={user_id}"
        output = f"👤 ПРОФИЛЬ: [ПРОФИЛЬ]({link})"

        await utils.answer(message, output)
