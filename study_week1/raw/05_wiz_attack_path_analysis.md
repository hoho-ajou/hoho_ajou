# What is Attack Path Analysis? (Wiz)

원문: https://www.wiz.io/academy/detection-and-response/attack-path-analysis

## What is attack path analysis?
Attack path analysis (APA) is a security methodology that identifies and maps the routes attackers could use to move through your environment and reach critical assets. Individual vulnerability scans generate thousands of findings without showing which ones actually chain together into exploitable paths.

## Three related concepts
- Attack path: "The complete sequence of steps an attacker follows to compromise systems and reach high-value targets. Paths connect vulnerabilities, misconfigurations, and weak access controls into exploitable routes."
- Attack vector: "The initial entry point attackers use to gain access, such as phishing, unpatched software, or exposed credentials."
- Attack surface: "The total collection of all possible entry points and exposures in your environment."

Vectors get attackers in, the attack surface defines where they can enter, and paths show them where to go next.

## How attack path analysis works (4 stages)
1. Asset and risk discovery — full visibility into resources, workloads, identities, configs, data; scan for vulnerabilities, exposed secrets, misconfigurations, excessive permissions.
2. Graph-based mapping — map risks onto a security graph connecting resources (e.g. VM with public IP + high-severity vuln links to over-privileged identity).
3. Path identification — trace potential attacker action sequences; find "toxic combinations" where multiple low-risk issues chain into high-impact paths.
4. Prioritization — rank paths by potential impact; paths to crown-jewel assets flagged critical.

## Benefits
- Proactive threat management: anticipate routes before an incident
- Prioritized vulnerability management: fix what's actually on a path to critical assets first
- Targeted defense: identify most vulnerable systems
- Improved resource allocation: focus limited security resources

## Wiz: code-to-cloud-to-runtime loop
Wiz's Security Graph connects assets, identities, permissions, vulnerabilities, threat activity; fed by runtime signals (eBPF sensor) validating which paths are exploitable in production. Confirmed paths trace back to source code (Wiz Code/SAST) for AI-assisted fix PRs.

### AI Agents
Red Agent probes apps/APIs for exploitable logic flaws; Blue Agent investigates detected threats correlating runtime/cloud/identity signals; Green Agent traces root cause, ownership, generates remediation steps including PRs. Orchestrated via Wiz Workflows with human-approval checkpoints.
