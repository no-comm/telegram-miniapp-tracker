import os
import shutil
import json
from playwright.async_api import Response

class GeneratePy:
    def __init__(self, base_path, headers_in_every_func=False) -> None:
        self.base_path = base_path
        self.headers_in_every_func = headers_in_every_func

        if os.path.exists(os.path.join(self.base_path, 'py_module')):
            shutil.rmtree(os.path.join(self.base_path, 'py_module'))
        os.makedirs(os.path.join(self.base_path, 'py_module/utils'), exist_ok=True)

        self.imports = ['import asyncio', 'import aiohttp']
        self.classes = []
        self.functions = []
        self.calls = []

        self.main_class = (
            'class PacketsLog:\n'
            '    def __init__(self):\n'
            '        asyncio.run(self.run())\n\n'
            '    async def run(self):\n'
            '        async with aiohttp.ClientSession() as session:\n'
            '            self.session = session'
        )
        self.call_func = '    async def call_funcs(self):\n        '

    def write(self) -> None:
        """Write the final content to PacketsLog.py"""
        text = '\n'.join(self.imports) + '\n\n'
        text += self.main_class + '\n            '
        text += '\n            '.join(self.classes)
        text += '\n            await self.call_funcs()\n\n'
        text += self.call_func
        text += '\n        '.join(self.calls) + '\n\n'
        text += ''.join(self.functions)

        with open(os.path.join(self.base_path, 'py_module/PacketsLog.py'), 'w', encoding='utf-8') as f:
            f.write(text)

    def class_is_exist(self, name) -> bool:
        """Check if a class file already exists"""
        return os.path.exists(os.path.join(self.base_path, f'py_module/utils/{name}.py'))

    def new_class(self, name, headers) -> None:
        """Create a new class file"""
        headers_update = f'\n        self.session.headers.update({headers})' if not self.headers_in_every_func else ''
        
        class_content = (
            f'from aiohttp import ClientSession\n\n'
            f'class {name}:\n'
            f'    def __init__(self, session: ClientSession):\n'
            f'        self.session = session'
            f'{headers_update}'
        )

        with open(os.path.join(self.base_path, f'py_module/utils/{name}.py'), 'w', encoding='utf-8') as f:
            f.write(class_content)

        # Update imports and class instantiations
        self.imports.append(f'from utils.{name} import {name}')
        self.classes.append(f'self.{name} = {name}(self.session)')
        self.write()

    def new_function(self, in_class, name, packet: Response, headers) -> None:
        """Add a new function to the class and PacketsLog"""
        method = packet.request.method
        url = packet.url
        post_data = json.dumps(packet.request.post_data).replace("null", "None") if method == 'POST' else None

        function_body = (
            f'\n\n    async def {name}(self, **kwargs):\n'
            f'        return await self.session.request(method="{method}", url="{url}", **kwargs)'
        )
        with open(os.path.join(self.base_path, f'py_module/utils/{in_class}.py'), 'a', encoding='utf-8') as f:
            f.write(function_body)

        if self.headers_in_every_func:
            if method == 'POST':
                self.functions.append(
                    f'    async def {name}(self):\n'
                    f'        return await self.{in_class}.{name}(headers={headers}, data={post_data})\n\n'
                )
            else:
                self.functions.append(
                    f'    async def {name}(self):\n'
                    f'        return await self.{in_class}.{name}(headers={headers})\n\n'
                )
        else:
            if method == 'POST':
                self.functions.append(
                    f'    async def {name}(self):\n'
                    f'        return await self.{in_class}.{name}(data={post_data})\n\n'
                )
            else:
                self.functions.append(
                    f'    async def {name}(self):\n'
                    f'        return await self.{in_class}.{name}()\n\n'
                )

        self.calls.append(f'await self.{in_class}.{name}()')
        self.write()
