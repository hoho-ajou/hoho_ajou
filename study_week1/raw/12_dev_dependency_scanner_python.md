# Build a Dependency Vulnerability Scanner with Python (DEV Community)

원문: https://dev.to/qingluan/build-a-dependency-vulnerability-scanner-with-python-alb

## Why Build Your Own Scanner
Tools like pip-audit and safety exist, but a custom scanner offers customizable output formats, private PyPI registry integration, and risk tolerance adjustments. "You can't easily tweak the logic to match your team's risk tolerance" with existing solutions alone.

## Setup & Dependencies
Only the `requests` library is needed for querying the National Vulnerability Database (NVD) API — lightweight approach.

## Core Implementation Steps
1. Parse requirements.txt — regex to extract package names and version specifiers, handling comments and flags
2. Query NVD API — fetch CVE data via `https://services.nvd.nist.gov/rest/json/cves/2.0`
3. Build Scanner Class — `DependencyScanner` class collects vulnerabilities and generates Markdown reports
4. CI/CD Integration — export JSON output, fail builds when critical CVEs are detected

## Key Code Pattern
The scanner extracts severity levels from CVSS metrics and creates structured vulnerability records containing package name, version, CVE ID, severity, and description.

## Recommended Extensions
pyproject.toml/poetry.lock support, SARIF output format, NVD response caching, automated vulnerability remediation features.
