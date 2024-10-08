from modules.authTelegramWeb import AuthTelegramWeb
from modules.TdataTelegram import TdataTelegram
from modules.webTelegram import WebTelegram
from modules.trackApp import TrackApp
import asyncio
import os
import sys

async def start(method='web', username=None, short_name=None, start_param=None) -> None:
    """Start the application with a specific method."""
    if method == 'web':
        if not os.path.exists("session.json"):
            try:
                auth_instance = AuthTelegramWeb()
                await auth_instance.auth_telegram()
            except Exception as e:
                print(f"Authentication failed: {e}")
                return
        try:
            webTelegram_instance = WebTelegram()
            game_url = await webTelegram_instance.start()
        except Exception as e:
            print(f"Error during tracking: {e}")
    elif method == 'tdata':
        if not os.path.exists("tdata"):
            raise ValueError("Didnt find tdata folder")
        try:
            tdataTelegram_instance = TdataTelegram()
            game_url = await tdataTelegram_instance.start('tdata', username, short_name, start_param)
        except Exception as e:
            print(f"Error during tracking: {e}")
    track_app = TrackApp()
    await track_app.start(game_url)
    
if __name__ == "__main__":
    try:
        if len(sys.argv) == 1:
            print("Usage: python main.py <method> <username_bot> <short_app_name> <start_param>\nExample: python main.py tdata username_bot short_app_name start_param\nExample: python main.py web")
        else:
            method = sys.argv[1]
            if method == 'web':
                asyncio.run(start(method))
            elif method == 'tdata':
                if len(sys.argv) != 5:
                    raise ValueError("Invalid number of arguments. Usage: python main.py tdata <username_bot> <short_app_name> <start_param>")
                asyncio.run(start(method, sys.argv[2], sys.argv[3], sys.argv[4]))
            else:
                raise ValueError(f"Unknown method. Supported methods are: {', '.join(['web', 'tdata'])}")
    except Exception as e:
        print(f"Failed to start the application: {e}")
