# SBOM Examples, Explained

원문: https://fossa.com/blog/sbom-examples-explained/
(FOSSA, Cortez Frazier Jr., 2023-09-26)

## SBOM Example 1: SPDX
SPDX supports multiple formats including tag/value, YAML, JSON, and Excel spreadsheets. Valid documents always include document creation information, and may also contain package, file, snippet, licensing, relationship, and annotation sections.

### Document Creation Information
- SPDX ID: Standardized reference throughout the document
- SPDX Version: Indicates specification version used (example uses v2.3)
- License List Version, Data License (CC0 1.0)

### Package Information
- SPDX ID, Supplier (distribution source, distinct from originator)
- License Declared vs. Concluded: Declared = author's statement; Concluded = SBOM tool's assessment
- Checksums: detect if files altered
- External References: VEX, PURL

### Relationships
Describes connections between elements: "DependsOn," "DependencyOf," "Contains."

### File Information
Similar to package sections but with unique fields.

## SBOM Example 2: CycloneDX
Supports JSON, XML, Protocol Buffers. Required: BOM Identity, Metadata. Optional: components, services, dependencies, compositions, vulnerabilities, formulation, annotations.

### BOM Identity
- Spec Version (v1.4 in example), Version (increments per modification), Serial Number

### Metadata
- Component Type, Manufacturer, Supplier

### Components
- Type, BOM-Ref, PURL (Package URL — ecosystem + version)

### Dependencies
Uses BOM-Ref elements to depict direct and transitive dependency relationships.

### Vulnerabilities
- ID (e.g. CVE number), Ratings (severity, score, methodology)

## Additional Resources
1. Minimum Required Elements documentation for regulatory compliance
2. FOSSA webinar on SBOM automation and management
