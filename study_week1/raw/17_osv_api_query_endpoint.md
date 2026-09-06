# OSV API — POST /v1/query (official docs)

원문: https://google.github.io/osv.dev/post-v1-query/

## Overview
"Lists vulnerabilities for given package and version. May also be queried by commit hash."

## Request Methods
1. By package version: `name` + `ecosystem`, or a package URL (purl), plus `version`
2. By commit hash: git commit SHA
3. By git tag: ecosystem=`GIT`, repo URL in `name`, tag in `version`

Constraint: use either the top-level `version` field OR a versioned purl, not both.

## Request Payload
```json
{
  "commit": "string",
  "version": "string",
  "package": {
    "name": "string",
    "ecosystem": "string",
    "purl": "string"
  },
  "page_token": "string"
}
```

## Example (curl)
```bash
curl -X POST https://api.osv.dev/v1/query \
  -H "Content-Type: application/json" \
  -d '{"package": {"name": "flask", "ecosystem": "PyPI"}, "version": "2.0.1"}'
```

## Response
HTTP 200 → `vulns` array: `id`, `summary`, `details`, `modified`, `published`, `references`, `affected`.

## Pagination
Responses over 1,000 vulns or taking >20s return `next_page_token` — pass it back in `page_token` for the next page. 32MiB response cap on HTTP/1.1 (no cap on HTTP/2).
