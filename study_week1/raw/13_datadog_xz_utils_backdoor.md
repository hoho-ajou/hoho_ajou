# The XZ Utils Backdoor (CVE-2024-3094) — Complete Overview (Datadog Security Labs)

원문: https://securitylabs.datadoghq.com/articles/xz-backdoor-cve-2024-3094/
(Christophe Tafani-Dereeper, Katie Knowles / 2024-04-03, updated 2024-04-08)

## Summary
The backdoor was identified on March 28, 2024, and reported the following day. It affects xz-utils versions 5.6.0 and 5.6.1. When installed, the backdoor modifies the `sshd` binary's behavior, permitting remote code execution by attackers possessing a specific private key.

## Affected distributions
- Fedora Linux 40 beta and Rawhide
- Debian unstable, testing, and experimental
- Kali Linux
- Arch Linux (specific VM/container images, Feb 24 – Mar 28, 2024)

Ubuntu and Amazon Linux were NOT affected.

## Technical Mechanism
A malicious shared object file loaded by the dynamically-linked `sshd` binary hijacks the OpenSSL function `RSA_public_decrypt`, allowing unauthorized access while preserving normal SSH functionality to evade detection.

## Detection
Run `xz --version` — 5.6.0 or 5.6.1 indicates potential compromise. A hexdump-based detection script for liblzma is also referenced.

## Why this case matters (multi-year social-engineering attack)
The attacker ("Jia Tan") spent over 2 years building trust before injecting the backdoor:
- Jan 2022: begins contributing to XZ Utils, builds credibility
- Sep 2023: first malicious code modifications secretly introduced
- Dec 2023: v5.6.0 released with embedded backdoor
- Feb 2024: v5.6.1 released, backdoor retained + obfuscation added
- Mar 29, 2024: Andres Freund (Microsoft engineer) posts discovery on Openwall mailing list — noticed SSH logins consuming extra 500ms CPU time while debugging unrelated PostgreSQL performance complaints

This is widely regarded as the most sophisticated open-source supply chain attack ever documented — and it was found by accident, not by a scanner.

## Historical context of backdooring (50 years of precedent)
- 1975 (published 1984): Ken Thompson's compiler backdoor in Bell Labs Unix login
- 2003: malicious Linux Kernel patches enabling root privilege escalation via fake comparison operator
- 2012: GitHub vulnerability allowed unauthorized SSH key injection into Rails repo
- 2021: PHP source code servers breached, malicious code exploitable via crafted HTTP headers
- 2021: Univ. of Minnesota "hypocrite commits" research — intentionally vulnerable patches passed kernel review
- 2023: actors impersonated Dependabot, falsified commits across hundreds of repos to steal GitHub credentials

## Broader implications
Hardware backdooring precedent too: CIA's Operation Rubicon compromised Crypto AG encryption devices; NSA reportedly embedded vulnerabilities in commercial encryption systems.
