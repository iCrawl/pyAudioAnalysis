import os
import subprocess
import sys
from pathlib import Path


def test_extract_cli_writes_snippet(tmp_path):
    input_file = Path("../pyAudioAnalysis/data/beat/120 BPM Techno Drum Loop.mp3")
    output_file = tmp_path / "120 BPM Techno Drum Loop_snippet.mp3"
    env = os.environ.copy()
    env.update(
        {
            "OUTPUT_DIR": str(tmp_path),
            "SNIPPET_LENGTH": "5",
            "SNIPPET_SUFFIX": "_snippet",
            "RECURSIVE_TRAVERSAL": "",
        }
    )

    subprocess.run(
        [sys.executable, "../extract.py", str(input_file)],
        check=True,
        cwd=Path(__file__).parent,
        env=env,
    )

    assert output_file.exists()
    assert output_file.stat().st_size > 0
