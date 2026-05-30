import pytest
from pathlib import Path
from modules.executor import move_to_backup_drive

@pytest.fixture
def setup_test_bench(tmp_path):
    source_dir = tmp_path / "Downloads_unit_test"
    backup_dir = tmp_path / "Backup_unit_test"
    source_dir.mkdir()
    backup_dir.mkdir()


    test_file = source_dir / "virtual_debug.pdf"
    test_file.write_text ("Code debugger snippet documentation.")

    return test_file, backup_dir

def test_successful_move(setup_test_bench):
    source_file, backup_dir = setup_test_bench
    dest_file = backup_dir / "Documents" / source_file.name

    result = move_to_backup_drive(source_file, dest_file)

    assert result is True
    assert dest_file.exists()
    assert not source_file.exists()


def test_integrity_failure_protection (setup_test_bench, monkeypatch):
    source_file, backup_dir = setup_test_bench
    dest_file = backup_dir / "Documents" / source_file.name

    import shutil
    def mock_corrupt_copy (src, dst):
        Path(dst).write_text("CORRUPTED DATA")

    monkeypatch.setattr(shutil, "copy2", mock_corrupt_copy)
    result = move_to_backup_drive(source_file, dest_file)

    assert result is False
    assert source_file.exists()
    assert not dest_file.exists()
