import requests

from .base import Source


class ApkPure(Source):
    def __init__(self) -> None:
        self.download_url = "https://d.apkpure.com/b/XAPK/{}?version={}"
        self.search_url = (
            "https://apkpure.com/api/v1/search_suggestion_new?key={}&limit={}"
        )
        self.headers: dict[str, str] = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            ),
            "Accept": "application/json",
        }

    def get_download_url(
        self,
        package_name: str, version:
        str = 'latest'
    ) -> str:
        return self.download_url.format(package_name, version)

    def search(self, keyword: str, limit: int = 20) -> list[dict]:
        url: str = self.search_url.format(keyword, limit)
        response: requests.Response = requests.get(url, headers=self.headers)
        try:
            items: list[dict] = []
            for item in response.json():
                if item.get('title') is None:
                    continue

                items.append({
                    'title': item.get('title'),
                    'icon_url': item.get('icon'),
                    'version': item.get('version'),
                    'total_install': item.get('installTotal'),
                    'score': item.get('score'),
                    'score_total': item.get('scoreTotal'),
                    'package_name': item.get('packageName'),
                    'file_size': item.get('fileSize'),  # file size is in bytes
                    'tags': [tag.get('name') for tag in item.get('tags', [])],
                })

            return items
        except ValueError:
            return []
