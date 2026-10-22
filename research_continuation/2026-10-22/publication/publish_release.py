#!/usr/bin/env python3
"""Publish the exact approved continuation; never rebuild its scientific payload."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen
import zipfile


REPO = "Cbaird26/mqgt-scf-continued"
TAG = "v2026.10.22-spectral-profile-common-vacuum"
TITLE = "Spectral Profile Nonuniqueness at a Common Stationary Vacuum"
PREDECESSOR = "7a36e0d741cb8ddb16056d39640ada43e28ad951"
PUBLICATION = Path(__file__).resolve().parent
ROOT = PUBLICATION.parents[2]
EM_PATH = Path("research_continuation/2026-10-22/electromagnetic")
ZIP_NAME = "Spectral_Profile_Common_Vacuum_Publication_2026-10-22.zip"
PDF_NAME = "Spectral_Profile_Common_Vacuum_2026-10-21.pdf"
APPROVED = {
    ZIP_NAME: (373692, "9fa24e444bc603432673d9f9f6c3369e4e909d0706725bbb1e965cd3ee07e218"),
    PDF_NAME: (339222, "2b60f8ab3eac2a2ed4082823e9c936b69441e3b7ba04f1977fbba92151c9a5f7"),
}
ARCHIVE_ROOT_FILES = {
    "PACKAGE_README.txt", "PREPUBLICATION_RECORD.json",
    "RELEASE_NOTES.md", "SHA256SUMS.txt",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def manifest(text):
    entries = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        digest, name = line.split("  ", 1)
        require(re.fullmatch(r"[0-9a-f]{64}", digest), "Malformed manifest digest")
        require(name not in entries, "Duplicate manifest path")
        entries[name] = digest
    return entries


def verify_package():
    archive_path = PUBLICATION / ZIP_NAME
    pdf_path = ROOT / EM_PATH / PDF_NAME
    for path in (archive_path, pdf_path):
        data = path.read_bytes()
        size, digest = APPROVED[path.name]
        require(len(data) == size and sha256(data) == digest,
                f"Approved identity mismatch: {path.name}")
    with zipfile.ZipFile(archive_path) as archive:
        require(archive.testzip() is None, "Archive CRC failure")
        names = archive.namelist()
        require(len(names) == len(set(names)) == 18, "Unexpected archive membership")
        entries = manifest(archive.read("SHA256SUMS.txt").decode("utf-8"))
        require(len(entries) == 17 and set(entries) == set(names) - {"SHA256SUMS.txt"},
                "Incomplete archive manifest")
        for name in names:
            data = archive.read(name)
            if name in entries:
                require(sha256(data) == entries[name], f"Archive checksum mismatch: {name}")
            if name in ARCHIVE_ROOT_FILES:
                local_path = PUBLICATION / name
            else:
                require(name.startswith(EM_PATH.as_posix() + "/")
                        and ".." not in Path(name).parts, "Unexpected archive path")
                local_path = ROOT / name
            require(local_path.read_bytes() == data, f"Repository/archive mismatch: {name}")
        original = manifest(archive.read((EM_PATH / "PREPARATION_SHA256SUMS.txt").as_posix()).decode())
        require(len(original) == 10, "Unexpected original research file count")
        for name, digest in original.items():
            require(sha256(archive.read((EM_PATH / name).as_posix())) == digest,
                    f"Original research checksum mismatch: {name}")
    return {"archive_members": 18, "manifest_entries_verified": 17,
            "original_research_files_verified": 10,
            "repository_copies_match_archive": True}


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def prepare_assets(output, commit, checks):
    assets = output / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PUBLICATION / ZIP_NAME, assets / ZIP_NAME)
    shutil.copyfile(ROOT / EM_PATH / PDF_NAME, assets / PDF_NAME)
    record = {
        "title": TITLE,
        "record_kind": "publication_source_and_asset_record",
        "repository": REPO,
        "source_commit": commit,
        "tag": TAG,
        "release_type": "prerelease",
        "release_url": f"https://github.com/{REPO}/releases/tag/{TAG}",
        "predecessor_commit": PREDECESSOR,
        "predecessor_release": "v2026.10.21-research-continuation",
        "research_note_date": "2026-10-21",
        "publication_package_date": "2026-10-22",
        "approved_assets": {name: {"size": size, "sha256": digest}
                            for name, (size, digest) in APPROVED.items()},
        "integrity_checks": checks,
        "historical_records_preserved": True,
        "publication_time_source": "GitHub release published_at; also recorded in the workflow receipt",
        "scientific_scope": "Conditional existential nonuniqueness within the stipulated shared spectral action and positive exponential profile class; no measured-alpha derivation or complete compactification-stability claim.",
    }
    write_json(assets / "PUBLICATION_RECORD.json", record)
    names = [PDF_NAME, ZIP_NAME, "PUBLICATION_RECORD.json"]
    (assets / "RELEASE_SHA256SUMS.txt").write_text(
        "".join(f"{sha256((assets / name).read_bytes())}  {name}\n" for name in names),
        encoding="utf-8")
    names.append("RELEASE_SHA256SUMS.txt")
    return {name: {"path": assets / name, "size": (assets / name).stat().st_size,
                   "digest": "sha256:" + sha256((assets / name).read_bytes())}
            for name in names}


def api(suffix, method="GET", data=None, missing_ok=False):
    request = Request(
        "https://api.github.com/repos/" + REPO + "/" + suffix,
        data=None if data is None else json.dumps(data).encode("utf-8"),
        method=method,
        headers={"Authorization": "Bearer " + os.environ["GH_TOKEN"],
                 "Accept": "application/vnd.github+json",
                 "Content-Type": "application/json",
                 "X-GitHub-Api-Version": "2026-03-10",
                 "User-Agent": "Spectral-profile-verified-publication/1"})
    try:
        with urlopen(request, timeout=60) as response:
            return json.load(response)
    except HTTPError as error:
        if missing_ok and error.code == 404:
            return None
        # Status and API message aid diagnosis; authorization headers are never logged.
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub {method} {suffix}: HTTP {error.code}: {body}") from None


def tag_commit():
    ref = api("git/ref/tags/" + quote(TAG, safe=""), missing_ok=True)
    if ref is None:
        return None
    obj = ref["object"]
    for _ in range(4):
        if obj["type"] == "commit":
            return obj["sha"]
        require(obj["type"] == "tag", "Unexpected tag object type")
        obj = api("git/tags/" + obj["sha"])["object"]
    raise RuntimeError("Unexpected tag nesting")


def release_by_tag():
    # The authenticated release list includes drafts; tag lookup need not do so.
    releases = api("releases?per_page=100")
    matches = [release for release in releases if release["tag_name"] == TAG]
    require(len(matches) <= 1, "Multiple releases for the target tag")
    return matches[0] if matches else None


def verify_assets(release, expected, complete):
    actual = api(f"releases/{release['id']}/assets?per_page=100")
    names = [asset["name"] for asset in actual]
    require(len(names) == len(set(names)), "Duplicate release asset names")
    require(set(names) <= set(expected), "Unexpected release asset; refusing modification")
    for asset in actual:
        wanted = expected[asset["name"]]
        require(asset["state"] == "uploaded" and asset["size"] == wanted["size"]
                and asset.get("digest") == wanted["digest"],
                f"Remote asset identity mismatch: {asset['name']}")
    if complete:
        require(set(names) == set(expected), "Incomplete release asset set")
    return actual


def publish(commit, expected, output, checks):
    require(os.environ.get("GITHUB_REPOSITORY", "").lower() == REPO.lower(),
            "Unexpected repository")
    require(os.environ.get("GITHUB_REF") == "refs/heads/main", "Publication must run from main")
    require(subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
            == commit, "Checkout does not match the workflow commit")
    target = tag_commit()
    require(target in (None, commit), "Existing tag targets another commit; refusing modification")
    body = (PUBLICATION / "RELEASE_NOTES.md").read_text(encoding="utf-8")
    body += ("\n## Publication record\n\n"
             f"Source commit: [`{commit}`](https://github.com/{REPO}/commit/{commit}).\n\n"
             "The PDF and complete publication ZIP retain the exact approved bytes. "
             "`PUBLICATION_RECORD.json` identifies this publication; "
             "`RELEASE_SHA256SUMS.txt` verifies its attached files. "
             "Preparation-status statements inside the preserved ZIP are historical.\n")
    release = release_by_tag()
    if release is not None:
        require(release["target_commitish"] == commit and release["prerelease"],
                "Existing release does not match this publication")
        require(release["name"] == TITLE and release["body"] == body,
                "Existing release text differs; refusing modification")
    if release is None or release["draft"]:
        require(api("git/ref/heads/main")["object"]["sha"] == commit,
                "Default branch advanced; inspect before publishing")
        if release is None:
            release = api("releases", "POST", {"tag_name": TAG, "target_commitish": commit,
                          "name": TITLE, "body": body, "draft": True,
                          "prerelease": True, "make_latest": "false"})
        present = {asset["name"] for asset in verify_assets(release, expected, complete=False)}
        missing = [str(item["path"]) for name, item in expected.items() if name not in present]
        if missing:
            subprocess.run(["gh", "release", "upload", TAG, "--repo", REPO, *missing],
                           check=True)
        verify_assets(release, expected, complete=True)
        require(api("git/ref/heads/main")["object"]["sha"] == commit,
                "Default branch advanced before publication; draft retained")
        release = api(f"releases/{release['id']}", "PATCH",
                      {"draft": False, "prerelease": True, "make_latest": "false"})
    release = api(f"releases/{release['id']}")
    require(not release["draft"] and release["prerelease"] and release["published_at"],
            "Release is not a published prerelease")
    require(tag_commit() == commit, "Published tag target mismatch")
    assets = verify_assets(release, expected, complete=True)
    receipt = {"repository": REPO, "source_commit": commit, "tag": TAG,
               "release_id": release["id"], "release_url": release["html_url"],
               "published_at": release["published_at"], "prerelease": True,
               "workflow_run_id": os.environ.get("GITHUB_RUN_ID"),
               "integrity_checks": checks,
               "assets": [{key: asset[key] for key in
                           ("name", "size", "digest", "browser_download_url")}
                          for asset in assets]}
    write_json(output / "publication_receipt.json", receipt)
    print(json.dumps(receipt, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-only", action="store_true", help="Verify locally; no network or publication")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    checks = verify_package()
    commit = os.environ.get("GITHUB_SHA", "preflight-not-published")
    if not args.verify_only:
        require(re.fullmatch(r"[0-9a-f]{40}", commit), "Missing workflow commit")
    output = args.output_dir or Path(os.environ.get("RUNNER_TEMP", tempfile.gettempdir())) / "spectral-profile-publish"
    output.mkdir(parents=True, exist_ok=True)
    expected = prepare_assets(output, commit, checks)
    if args.verify_only:
        print(json.dumps({"status": "verified locally; no external mutation", "checks": checks,
                          "assets": {name: {"size": item["size"], "digest": item["digest"]}
                                     for name, item in expected.items()}}, indent=2))
        return
    publish(commit, expected, output, checks)


if __name__ == "__main__":
    main()
