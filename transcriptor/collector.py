import os

class Collector:
    SUPPORTED_EXTENSIONS = ('.ogg', '.mp3', '.wav', '.mpeg', '.m4a', '.mp4')

    def __init__(self, base_dir: str = "targets"):
        self.base_dir = base_dir

    def collect(self):
        if not os.path.exists(self.base_dir):
            return []
        
        collected_files = []
        for root, _, filenames in os.walk(self.base_dir):
            for filename in filenames:
                if filename.lower().endswith(self.SUPPORTED_EXTENSIONS):
                    collected_files.append(os.path.join(root, filename))
        
        return collected_files
