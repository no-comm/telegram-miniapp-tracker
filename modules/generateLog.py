import os
import shutil

class GenerateLog:
    def __init__(self, base_path) -> None:
        self.base_path = base_path
        self.log_path = os.path.join(self.base_path, 'packets_log')

        if os.path.exists(self.log_path):
            shutil.rmtree(self.log_path)

        os.makedirs(self.log_path, exist_ok=True)
        open(os.path.join(self.log_path, 'order_packet.txt'), 'w', encoding='utf-8').close()
        open(os.path.join(self.log_path, 'order_packet_unique.txt'), 'w', encoding='utf-8').close()

    def write_to_file_packets(self, data) -> None:
        """Write data to order_packet.txt file"""
        with open(os.path.join(self.log_path, 'order_packet.txt'), 'a', encoding='utf-8') as file_packets:
            file_packets.write(data)

    def write_to_file_packets_unique(self, data) -> None:
        """Write unique data to order_packet_unique.txt file"""
        with open(os.path.join(self.log_path, 'order_packet_unique.txt'), 'a', encoding='utf-8') as file_packets_unique:
            file_packets_unique.write(data)
