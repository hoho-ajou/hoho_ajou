# PyPI JSON API — Official Docs Summary

원문: https://docs.pypi.org/api/json/

## Two Endpoints

**Project-level:** `GET /pypi/<project>/json`
Returns metadata about a project at its latest version, plus a list of all releases and project URLs. Includes a `releases` key (marked for future deprecation in favor of the Index API).

**Release-specific:** `GET /pypi/<project>/<version>/json`
Metadata for one specific version only — omits the `releases` key.

## Response Structure
- `info` object: package metadata (author, classifiers, dependencies, etc.)
- `last_serial`: monotonically increasing integer, changes on every project update
- `urls` array: distribution files with hash digests (MD5, SHA256, BLAKE2b-256)
- Each file object has a `core-metadata` key: `false`, or hash digests per PEP 658 / PEP 714

## Ownership and Vulnerabilities
- `ownership` object: project `roles` (Owner/Maintainer) + optional `organization`
- `vulnerabilities` array: known security issues per package version — each with aliases, description, fixed versions, and an OSV link. Withdrawn vulnerabilities carry RFC 3339 retraction timestamps.

## Deprecated fields (kept for backward compatibility)
`downloads`, `has_sig`, `bugtrack_url`, and (in project responses) `releases`.

## Practical use for Dependency Collector
`https://pypi.org/pypi/<패키지명>/json` 하나만 호출하면: 최신 버전, 전체 릴리즈 이력, 배포 파일 해시, **알려진 취약점 목록(OSV 링크 포함)**까지 한 번에 가져올 수 있음 — 별도 OSV API 호출 없이도 기초 취약점 확인 가능.
