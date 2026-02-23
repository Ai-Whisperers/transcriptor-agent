import os
import pytest
from transcriptor.collector import Collector

def test_collector_find_files(tmp_path):
    # Create a dummy structure
    d = tmp_path / "subdir"
    d.mkdir()
    (tmp_path / "audio1.mp3").write_text("dummy")
    (tmp_path / "not_audio.txt").write_text("dummy")
    (d / "audio2.ogg").write_text("dummy")
    
    collector = Collector(base_dir=str(tmp_path))
    files = collector.collect()
    
    # Should find 2 audio files
    assert len(files) == 2
    # Paths should be relative to base_dir or absolute? 
    # Let's say absolute for engine compatibility
    basenames = [os.path.basename(f) for f in files]
    assert "audio1.mp3" in basenames
    assert "audio2.ogg" in basenames
    assert "not_audio.txt" not in basenames

def test_collector_empty_dir(tmp_path):
    collector = Collector(base_dir=str(tmp_path))
    assert collector.collect() == []
