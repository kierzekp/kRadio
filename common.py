import json

class ApplicationConfig:
    def __init__(self, config_file_url: str) -> None:
        self._parse_from_file(config_file_url)

    def _parse_from_file(self, config_file_url: str):
        with open(config_file_url) as f:
            raw_data = json.load(f)
            
            self.led_screen = raw_data["led_screen"]
            self.presets = raw_data["presets"]