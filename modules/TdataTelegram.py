from TGConvertor import SessionManager
from pathlib import Path
from pyrogram.raw import functions, types

class TdataTelegram:
    async def start(self, folder, username, short_name, start_param):
        session = SessionManager.from_tdata_folder(Path(folder))
        
        client = session.pyrogram_client()
        await client.start()

        bot = await client.resolve_peer(username)

        res: types.AppWebViewResultUrl = await client.invoke(
            functions.messages.RequestAppWebView(
                peer=bot,
                app=types.InputBotAppShortName(bot_id=bot, short_name=short_name),
                platform='android',
                start_param=start_param,
                write_allowed=True
            )
        )

        await client.stop()
        
        return res.url

