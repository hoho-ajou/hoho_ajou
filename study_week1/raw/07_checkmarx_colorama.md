# PyPI Supply Chain Attack: Colorama/Colorizr (Checkmarx)

원문: https://checkmarx.com/zero-post/python-pypi-supply-chain-attack-colorama/

## Overview
Checkmarx Zero researcher Ariel Harush discovered a malicious package campaign targeting Python and NPM users through typo-squatting attacks against `colorama` (PyPI) and `colorizr` (NPM).

## Windows Payloads
- Environment variable harvesting from Windows registry
- Persistence via Task Scheduler
- Antivirus evasion, removing Windows Defender malware definitions, disabling IOAV scanning
- Linked to GitHub account github.com/s7bhme

## Linux Payloads
Two packages (`Colorizator`, `coloraiz`) with base64-encoded payloads:
1. RSA key deployment to /tmp/pub.pem for output encryption
2. Remote bash download from gsocket.io/y installing gs-netcat for encrypted reverse shells
3. Encrypted exfiltration via Pastebin API
4. Cleanup removing temp files

Bash script offered persistence (systemd, shell profiles, crontabs), stealth (process masquerading), C2 capability, webhook notifications to Discord/Telegram.

## Key IOCs
- Package owners: rick_grimes (Colorizator), morty_smith (coloraiz), reven (coloramapkgsw, coloramapkgsdow), m5tl (coloramashowtemp), dsss (coloramapkgs, readmecolorama)
- SHA256 hashes provided for Linux bash script and Windows payload

## Recommendations
- Scan deployed code for malicious package names/IoCs
- Examine private repos/proxies for malicious packages
- Block installation on developer environments
