from playwright.async_api import async_playwright, StorageState, Page
import json
import os

class WebTelegram:
    def on_telegram_disconnected(self) -> None:
        """Handles Telegram disconnection"""
        os._exit(0)

    async def create_browser(self) -> Page:
        """Sets up browser and localStorage"""
        with open("session.json", "r", encoding="utf-8") as f:
            localStorage = [{'name': i, 'value': k} for i, k in json.loads(f.read()).items()]
        
        storage_state = StorageState(origins=[{'origin': 'https://web.telegram.org', 'localStorage': localStorage}])
        self.browser = await self.p.chromium.launch(headless=False)
        page = await self.browser.new_page(storage_state=storage_state, ignore_https_errors=True)
        page.on('close', self.on_telegram_disconnected)
        return page
    
    async def start(self) -> str:
        """Main function to start the browser session and track packets"""
        async with async_playwright() as self.p:
            page = await self.create_browser()

            await page.goto("https://web.telegram.org/k/")
            web_app_body = await page.wait_for_selector(".web-app-body", timeout=99999)

            game_frame = await web_app_body.wait_for_selector('iframe')
            game_url = await game_frame.get_attribute('src')
            game_url = game_url.split('&')

            for i in range(len(game_url)):
                if game_url[i].startswith('tgWebAppPlatform='):
                    game_url[i] = 'tgWebAppPlatform=android'
            game_url = '&'.join(game_url)
            return game_url