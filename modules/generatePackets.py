import os
import shutil
import json

class GeneratePackets:
    def __init__(self, base_path) -> None:
        self.base_path = base_path
        self.packets_path = os.path.join(self.base_path, 'packets')

        if os.path.exists(self.packets_path):
            shutil.rmtree(self.packets_path)
        os.makedirs(self.packets_path, exist_ok=True)

    def add_to_packets_folder(self, domain, name, data) -> None:
        """Add packet data to the corresponding domain folder"""
        domain_path = os.path.join(self.packets_path, domain)

        os.makedirs(domain_path, exist_ok=True)

        file_path = os.path.join(domain_path, f'{name}.json')
        with open(file_path, 'w', encoding='utf-8') as file_packets:
            json.dump(data, file_packets, ensure_ascii=False, indent=4)
