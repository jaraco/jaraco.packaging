import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def static_wheel(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    subprocess.check_call(
        ['pip', 'download', '--no-deps', '--dest', str(tmp_path), 'sampleproject'],
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
    )
    (wheel,) = tmp_path.iterdir()
    monkeypatch.setenv('JARACO_PACKAGING_SPHINX_WHEEL', str(wheel))
