import importlib
from pathlib import Path

from pyAudioAnalysis import audioBasicIO


def test_audio_basic_io_imports_without_aifc():
    module = importlib.import_module("pyAudioAnalysis.audioBasicIO")
    assert hasattr(module, "read_audio_file")


def test_read_audio_file_supports_mp3_inputs():
    mp3_path = Path("../pyAudioAnalysis/data/beat/120 BPM Techno Drum Loop.mp3")
    sampling_rate, signal = audioBasicIO.read_audio_file(str(mp3_path))

    assert sampling_rate > 0
    assert signal.size > 0
