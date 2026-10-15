"""Exercise restore/deploy refusal paths using only temporary server fixtures."""
import contextlib
import copy
import io
import json
import os
from pathlib import Path
import runpy
import subprocess
import tarfile
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
CHECK_BACKUP = runpy.run_path(str(ROOT / "scripts/check-backup.py"))["check"]
RUNTIME = json.loads((ROOT / "server/vanilla.lock.json").read_text())


def snapshot(directory):
    """Include file contents and directories to catch accidental installer writes."""
    result = {}
    for path in sorted(directory.rglob("*")):
        name = str(path.relative_to(directory))
        if path.is_symlink():
            result[name] = ("link", os.readlink(path))
        elif path.is_dir():
            result[name] = ("directory",)
        else:
            result[name] = ("file", path.read_bytes())
    return result


class BackupSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.data = self.root / "live-data"
        (self.data / "world").mkdir(parents=True)
        (self.data / ".runtime.json").write_text(json.dumps(RUNTIME))
        (self.data / "world/level.dat").write_bytes(b"unchanged live world")
        self.archive = self.root / "backup.tar.gz"

    def write_archive(self, marker=RUNTIME, extras=(), include_world=True):
        entries = []
        if marker is not None:
            entries.append((".runtime.json", json.dumps(marker).encode()))
        if include_world:
            entries.append(("world/level.dat", b"saved world"))
        entries.extend(extras)
        with tarfile.open(self.archive, "w:gz") as bundle:
            for name, payload in entries:
                if isinstance(payload, tarfile.TarInfo):
                    member = payload
                    member.name = name
                    bundle.addfile(member)
                else:
                    member = tarfile.TarInfo(name)
                    member.size = len(payload)
                    bundle.addfile(member, io.BytesIO(payload))

    def check(self):
        with contextlib.redirect_stdout(io.StringIO()):
            CHECK_BACKUP(self.archive, self.data)

    def test_matching_vanilla_backup_is_accepted_without_mutating_live_data(self):
        self.write_archive(extras=(("server.properties", b"gamemode=survival\n"),))
        before = snapshot(self.data)
        self.check()
        self.assertEqual(snapshot(self.data), before)

    def test_legacy_backup_without_runtime_marker_is_rejected(self):
        self.write_archive(marker=None)
        before = snapshot(self.data)
        with self.assertRaisesRegex(ValueError, "no unique vanilla runtime marker"):
            self.check()
        self.assertEqual(snapshot(self.data), before)

    def test_different_server_type_version_or_jar_is_rejected(self):
        for field, value in (("type", "neoforge"), ("minecraft", "26.2"),
                             ("server_sha1", "0" * 40)):
            with self.subTest(field=field):
                saved = copy.deepcopy(RUNTIME)
                saved[field] = value
                self.write_archive(marker=saved)
                with self.assertRaisesRegex(ValueError, "runtime/version differs"):
                    self.check()

    def test_archive_traversal_and_absolute_paths_are_rejected(self):
        for name in ("../escape", "world/../../escape", "/tmp/escape"):
            with self.subTest(path=name):
                self.write_archive(extras=((name, b"must never be extracted"),))
                with self.assertRaisesRegex(ValueError, "Unsafe or unexpected archive path"):
                    self.check()

    def test_archive_links_and_special_files_are_rejected(self):
        for kind in (tarfile.SYMTYPE, tarfile.LNKTYPE, tarfile.FIFOTYPE):
            with self.subTest(kind=kind):
                member = tarfile.TarInfo("world/unsafe")
                member.type = kind
                member.linkname = "../../escape"
                self.write_archive(extras=((member.name, member),))
                with self.assertRaisesRegex(ValueError, "Links and special files"):
                    self.check()

    def test_duplicate_runtime_marker_is_rejected(self):
        self.write_archive(extras=((".runtime.json", json.dumps(RUNTIME).encode()),))
        with self.assertRaisesRegex(ValueError, "no unique vanilla runtime marker"):
            self.check()

    def test_backup_without_world_is_rejected(self):
        self.write_archive(include_world=False)
        with self.assertRaisesRegex(ValueError, "no world/level.dat"):
            self.check()


class InstallerSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "scripts").mkdir()
        (self.root / "server").mkdir()
        self.script = self.root / "scripts/install-vanilla.py"
        self.script.write_bytes((ROOT / "scripts/install-vanilla.py").read_bytes())
        for name in ("vanilla.lock.json", "java.lock.json"):
            (self.root / "server" / name).write_bytes((ROOT / "server" / name).read_bytes())
        self.data = self.root / "data"
        self.data.mkdir()

    def assert_refused_before_network_or_mutation(self, reason):
        before = snapshot(self.root)
        with mock.patch.dict(os.environ, {"JC_DATA_DIR": str(self.data)}):
            with mock.patch("urllib.request.urlopen", side_effect=AssertionError("network attempted")) as network:
                with mock.patch("subprocess.run", side_effect=AssertionError("runtime execution attempted")) as execute:
                    with self.assertRaisesRegex(SystemExit, reason):
                        runpy.run_path(str(self.script))
        network.assert_not_called()
        execute.assert_not_called()
        self.assertEqual(snapshot(self.root), before)
        self.assertFalse((self.root / ".tools").exists())

    def test_neoforge_launcher_directory_is_rejected_before_side_effects(self):
        (self.data / "run.sh").write_text("preserved legacy launcher\n")
        self.assert_refused_before_network_or_mutation("over a modded server directory")

    def test_mods_directory_is_rejected_even_with_matching_vanilla_marker(self):
        (self.data / "mods").mkdir()
        (self.data / ".runtime.json").write_text(json.dumps(RUNTIME))
        self.assert_refused_before_network_or_mutation("over a modded server directory")

    def test_unmarked_existing_world_is_rejected_before_side_effects(self):
        (self.data / "world").mkdir()
        (self.data / "world/level.dat").write_bytes(b"irreplaceable existing world")
        self.assert_refused_before_network_or_mutation("existing world without matching vanilla runtime metadata")

    def test_other_vanilla_runtime_is_rejected_before_side_effects(self):
        other = copy.deepcopy(RUNTIME)
        other["minecraft"] = "26.2"
        (self.data / ".runtime.json").write_text(json.dumps(other))
        self.assert_refused_before_network_or_mutation("Runtime differs")


class RestoreRetentionTests(unittest.TestCase):
    def test_restore_uses_snapshot_when_backup_retention_deletes_original(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            scripts = root / "scripts"
            scripts.mkdir()
            for name in ("restore.sh", "check-backup.py"):
                (scripts / name).write_bytes((ROOT / "scripts" / name).read_bytes())
            (scripts / "common.sh").write_text(
                '#!/usr/bin/env bash\nset -euo pipefail\n'
                'JC_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"\n'
                ': "${JC_DATA_DIR:?isolated fixture data is required}"\n'
                'export JC_ROOT JC_DATA_DIR\n'
                'jc_die() { printf "%s\\n" "$*" >&2; exit 1; }\n'
                'jc_log() { printf "%s\\n" "$*"; }\n'
            )
            for name in ("backup", "stop", "start", "wait-ready", "validate"):
                action = 'rm -- "$JC_TEST_ARCHIVE"\n' if name == "backup" else ""
                fake = scripts / f"{name}.sh"
                fake.write_text(
                    '#!/usr/bin/env bash\nset -euo pipefail\n'
                    f'printf "%s\\n" "{name}" >> "$JC_TEST_CALLS"\n' + action
                )
                fake.chmod(0o700)

            data = root / "data"
            (data / "world").mkdir(parents=True)
            (data / "world/level.dat").write_bytes(b"current world before restore")
            (data / "server.properties").write_text("motd=current world\n")
            (data / ".runtime.json").write_text(json.dumps(RUNTIME))
            daily = data / "backups/daily"
            daily.mkdir(parents=True)
            archive = daily / "selected-oldest-backup.tar.gz"
            saved = {
                ".runtime.json": json.dumps(RUNTIME).encode(),
                "world/level.dat": b"selected saved world",
                "server.properties": b"motd=restored saved world\n",
            }
            with tarfile.open(archive, "w:gz") as bundle:
                for name, payload in saved.items():
                    member = tarfile.TarInfo(name)
                    member.size = len(payload)
                    bundle.addfile(member, io.BytesIO(payload))

            calls = root / "calls.txt"
            restore_tmp = root / "restore-temp"
            restore_tmp.mkdir()
            env = dict(os.environ, JC_DATA_DIR=str(data), JC_TEST_ARCHIVE=str(archive),
                       JC_TEST_CALLS=str(calls), TMPDIR=str(restore_tmp))
            result = subprocess.run(
                ["bash", str(scripts / "restore.sh"), str(archive)],
                env=env, capture_output=True, text=True, timeout=10,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertFalse(archive.exists(), "fixture retention must delete the selected original")
            self.assertEqual((data / "world/level.dat").read_bytes(), saved["world/level.dat"])
            self.assertEqual((data / "server.properties").read_bytes(), saved["server.properties"])
            self.assertEqual(json.loads((data / ".runtime.json").read_text()), RUNTIME)
            preserved = list((data / "backups").glob("pre-restore-*"))
            self.assertEqual(len(preserved), 1)
            self.assertEqual((preserved[0] / "world/level.dat").read_bytes(), b"current world before restore")
            self.assertEqual(calls.read_text().splitlines(), ["backup", "stop", "start", "wait-ready", "validate"])
            self.assertEqual(list(restore_tmp.iterdir()), [], "restore snapshot must be cleaned up")


if __name__ == "__main__":
    unittest.main()
