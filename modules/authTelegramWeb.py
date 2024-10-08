import asyncio
import json
from playwright.async_api import async_playwright

class AuthTelegramWeb:
    def __init__(self):
        self.browser = None
        self.page = None
        self.localStorage = {}

    async def get_local_storage(self) -> dict:
        """Fetch all values from localStorage on the page."""
        return await self.page.evaluate(
            """() => {
                let data = {};
                for (let i = 0; i < localStorage.length; i++) {
                    const key = localStorage.key(i);
                    data[key] = localStorage.getItem(key);
                }
                return data;
            }"""
        )

    async def wait_for_auth(self, auth_key='dc1_auth_key') -> None:
        """Wait for authentication by checking for the auth_key in localStorage."""
        while True:
            localStorage = await self.get_local_storage()
            if localStorage.get(auth_key):
                self.localStorage = localStorage
                break
            await asyncio.sleep(1)

    async def start_browser(self, headless=False) -> None:
        """Start the browser and open a new page."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless)
        self.page = await self.browser.new_page()

    async def auth_telegram(self, url="https://web.telegram.org/k/", auth_key='dc1_auth_key') -> None:
        """Main process for authenticating in Telegram."""
        await self.start_browser()
        await self.page.goto(url)
        await self.wait_for_auth(auth_key)

        # Save session data to file
        with open('session.json', 'w', encoding='utf-8') as f:
            json.dump(self.localStorage, f)
        
        await self.close_browser()

    async def close_browser(self) -> None:
        """Close the browser and stop Playwright."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
