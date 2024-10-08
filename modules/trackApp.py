from playwright.async_api import async_playwright, Response
from modules.generateLog import GenerateLog
from modules.generatePackets import GeneratePackets
from modules.generatePy import GeneratePy
from urllib.parse import urlparse
import asyncio
import datetime
import os
import shutil

class TrackApp:
    def __init__(self) -> None:
        self.enabled = True
        self.stage = 1
        self.packets = []
        self.loop = asyncio.get_event_loop()

    async def track(self, response: Response) -> None:
        """Tracks HTTP responses of type XHR or fetch"""
        if response.request.resource_type in ["xhr", "fetch"]:
            print(response.url)
            await self.append_packet(response)

    async def get_packet_text(self, packet: Response) -> str:
        """Retrieves response text from a packet"""
        try:return await packet.text()
        except: return None

    async def append_packet(self, packet: Response) -> None:
        """Processes and logs packet information"""
        packet_to_log = {
            'time': datetime.datetime.now(),
            'url': packet.url,
            'method': packet.request.method,
            'status': packet.status
        }
        self.log_writer.write_to_file_packets(' | '.join([str(i) for i in packet_to_log.values()]) + '\n')

        if packet_to_log['url'] not in [i['url'] for i in self.packets]:
            self.log_writer.write_to_file_packets_unique(' | '.join([str(i) for i in packet_to_log.values()]) + '\n')

            name = urlparse(packet.url).path[1:].replace('/', '_').replace('-', '_').replace('.', '_')
            domain = urlparse(packet.url).netloc.replace('.', '_').replace('-', '_')

            packet_text = await self.get_packet_text(packet)

            self.packets_writer.add_to_packets_folder(domain, name, {
                'request': {
                    'method': packet.request.method,
                    'url': packet.url,
                    'headers': packet.request.headers,
                    'body': packet.request.post_data
                },
                'response': {
                    'status': packet.status,
                    'headers': packet.headers,
                    'body': packet_text
                }
            })

            if not self.py_writer.class_is_exist(domain):
                self.py_writer.new_class(domain, packet.request.headers)

            self.py_writer.new_function(domain, name, packet, packet.request.headers)

        self.packets.append(packet_to_log)

    def on_page_disconnected(self) -> None:
        """Handles page disconnection"""
        self.enabled = False

    async def start(self, game_url: str) -> None:
        """Main function to start the browser session and track packets"""
        async with async_playwright() as self.p:

            self.browser = await self.p.chromium.launch(headless=False)
            
            context = await self.browser.new_context(
                user_agent="Mozilla/5.0 (Linux; Android 8.1.0; SM-T837A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.31 Safari/537.36",
                viewport={"width": 600, "height": 900},
                is_mobile=True,
                has_touch=True,
                ignore_https_errors=True,
            )

            base_path = urlparse(game_url).netloc.replace('.', '_').replace('-', '_')

            if os.path.exists(base_path):
                shutil.rmtree(base_path)
            os.mkdir(base_path)

            self.log_writer = GenerateLog(base_path)
            self.packets_writer = GeneratePackets(base_path)
            self.py_writer = GeneratePy(base_path, headers_in_every_func=False)

            self.page = await context.new_page()
            self.page.on("response", self.track)
            self.page.on("close", self.on_page_disconnected)

            await self.page.goto(game_url)

            while self.enabled:
                await asyncio.sleep(1)

            await self.browser.close()
            
