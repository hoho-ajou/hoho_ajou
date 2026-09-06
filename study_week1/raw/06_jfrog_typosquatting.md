# Typosquatting in the Software Supply Chain (JFrog)

원문: https://jfrog.com/learn/devsecops/typosquatting/

## Definition
Typosquatting is a social engineering attack targeting package ecosystems by registering malicious libraries with misspelled names of popular open-source dependencies. When developers make subtle typing errors, build processes automatically download compromised components, enabling attackers to exfiltrate credentials and embed backdoors into production applications.

## What It Is
Creating malicious packages with names nearly identical to legitimate ones (e.g. "requests" → "requets" or "reqeusts"). Unlike traditional phishing, targets developers and DevOps pipelines rather than end users.

## How It Works
Attackers upload malicious packages to npm, PyPI, Maven. Fast CLI/automation workflows mean a single unnoticed typo downloads attacker-controlled packages.

## Real-World Examples
- 2021: hundreds of typosquatted PyPI packages attempting credential theft or reverse shells
- npm: character swaps/omissions targeting widely-used packages

## Impacts
- Developers: compromised local environments, stolen credentials, infected connected systems
- Organizations: data theft, IP compromise, embedded backdoors, regulatory penalties, financial losses

## Mitigation Strategies
- Allowlists of trusted packages/maintainers
- Approval required for new dependencies
- Automated look-alike name detection
- Developer education on naming tricks
- SCA in CI/CD pipelines
- SBOM generation

## Defense Evolution
Future threats: AI-generated typosquatted packages, cross-ecosystem attacks, typosquatting + social engineering combos. Recommends layered defenses, deep DevSecOps integration, continuous monitoring.
