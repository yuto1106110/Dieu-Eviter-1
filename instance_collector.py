
import requests
import json
import time

class InstanceCollector:
    def __init__(self):
        # 取得元URLリスト
        self.sources = [
            "https://api.invidious.io/instances.json",  # Invidious公式
            "https://raw.githubusercontent.com/mochidukiyukimi/yuki-youtube-instance/main/instance.txt",  # もちづきさん
            "https://raw.githubusercontent.com/yuto1106110/yuto-yuki-youtube-1/main/APItati",
            # （必要ならここにさらに追加できる）
        ]
        # 手持ちの静的インスタンスリスト
        self.static_instances = [
            "https://vid.puffyan.us",
            "https://yewtu.be",
            "https://inv.vern.cc",
            "https://inv.riverside.rocks",
            "https://invidious.kavin.rocks",
            "https://invidious.snopyta.org",
            # （さらに追加できる）
        ]

    def fetch_instances(self):
        instances = set(self.static_instances)

        for url in self.sources:
            try:
                res = requests.get(url, timeout=10)
                content_type = res.headers.get('Content-Type', '')

                # JSONファイルならパース
                if 'application/json' in content_type:
                    data = res.json()
                    for item in data:
                        if isinstance(item, list) and item:
                            instances.add(item[0])
                else:
                    # テキストファイルなら1行ずつ
                    lines = res.text.strip().splitlines()
                    for line in lines:
                        instances.add(line.strip())
            except Exception as e:
                print(f"[fetch_instances] エラー: {url} - {e}")

        print(f"[fetch_instances] 取得完了。総数: {len(instances)}個")
        return list(instances)

    def normalize_url(self, url):
        url = url.strip()
        if not url.startswith("http"):
            url = "https://" + url
        return url.rstrip('/')

    def validate_instances(self, instance_list):
        working = []
        for instance in instance_list:
            try:
                url = self.normalize_url(instance) + "/api/v1/trending"
                start = time.time()
                res = requests.get(url, timeout=5)
                if res.status_code == 200:
                    latency = time.time() - start
                    working.append((instance, latency))
                    print(f"[validate_instances] 成功: {instance} - {latency:.2f}秒")
            except Exception as e:
                print(f"[validate_instances] 失敗: {instance} - {e}")

        working.sort(key=lambda x: x[1])  # レイテンシ順
        return [url for url, _ in working]
