# A Guide to Generating SBOM with Syft and Grype (Jit)

원문: https://www.jit.io/resources/appsec-tools/a-guide-to-generating-sbom-with-syft-and-grype
(Author: Aviram Shmueli, Updated 2025-09-08)

## Introduction
Critical vulnerabilities (Log4j 2021, XZ Utils) exposed the difficulty of tracking software dependencies. SBOM tools like Syft address this by providing comprehensive visibility into the software supply chain.

## Syft and Grype by Anchore
Syft (5.4K+ GitHub stars): CLI tool/library generating SBOMs from container images and filesystems in JSON, CycloneDX, SPDX formats.
Grype (7.4K+ stars): scans generated SBOMs to identify vulnerabilities (ID, severity, CVSS scores, mitigation recommendations).

## Installing
```
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin
```

## Generating SBOMs
```
syft NodeGoat
syft nodegoat-web:latest -o cyclonedx-json > sbom_cyclonedx.json
syft nodegoat-web:latest -o json > sbom.json
```

## Extracting data with jq (example)
```
syft nodegoat-web:latest -o json | jq -r '.artifacts[] | [.name, .version, (if .licenses == [] then "No license" else [ .licenses[].value ] | join(", ") end)] | @tsv'
```

## Identifying Vulnerabilities with Grype
```
grype sbom:sbom.json -o json > vulnerabilities.json
```

## Combining SBOM + vulnerability data
Python script joins Syft package list with Grype vulnerability matches by package name+version to produce a combined report (full script in original article).

## Benefits
- Understand exposure, prioritize remediation by severity, comply with regulations, continuously improve security posture.
