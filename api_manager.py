import time
import threading
from instance_collector import InstanceCollector

class APIManager:
    def __init__(self):
        self.api_list = []
        self.collector = InstanceCollector()
        self.update_interval = 3600  # 1時間に1回更新
        self.update_api_list()
        threading.Thread(target=self.auto_update, daemon=True).start()

    def update_api_list(self):
        print("[update_api_list] インスタンス更新開始...")
        all_instances = self.collector.fetch_instances()
        working_instances = self.collector.validate_instances(all_instances)
        self.api_list = working_instances
        print(f"[update_api_list] 使用可能API数: {len(self.api_list)}個")

    def auto_update(self):
        while True:
            time.sleep(self.update_interval)
            self.update_api_list()

    def get_api(self):
        if not self.api_list:
            raise Exception("使用可能なAPIがありません")
        return self.api_list[0]  # 速いやつ優先
