# AASM 참고자료 큐레이션 (2026-09-05 기준)

실제로 검색·확인한 자료만 모았습니다. 2000개를 채우려면 대부분 가짜 링크나 중복·저품질 자료가 됐을 것 같아서, 대신 **약 140개의 검증된 자료**를 카테고리·우선순위와 함께 정리했습니다. 각 카테고리 안 "큐레이션 목록"류(Awesome List)는 그 자체로 링크 하나가 수십~수백 개 자료로 이어지니, 시간 없으면 그것부터 열어보는 게 제일 효율적입니다.

**우선순위 기준**
- 🔴 P0 — 지금 당장 읽어야 할 핵심 (배경·개념 확립용)
- 🟡 P1 — 자기 담당 모듈 구현 시 필요
- ⚪ P2 — 여유 있을 때, 심화/참고용

---

## A. 왜 AI 에이전트 공급망 보안인가 (전체 배경)

- 🔴 [How AI Agents Expand the Software Supply Chain Attack Surface](https://socket.dev/blog/ai-agents-supply-chain-attack-surface) — Socket CEO의 AI Council 2026 발표 정리, 이 프로젝트의 문제의식과 가장 정확히 겹침
- 🔴 [AI Software Supply Chain Threats Escalate in 2026](https://www.esecurityplanet.com/threats/ai-software-supply-chain-threats-escalate-in-2026/) — JFrog 2026 리포트 기반, npm 악성패키지 451%↑ 등 핵심 수치
- 🟡 [Top Agentic AI Security Threats in Late 2026](https://stellarcyber.ai/learn/agentic-ai-securiry-threats/) — 에이전트 특유의 위협 유형 정리
- 🟡 [Software Supply Chain Attack: AI Agent Ecosystem as Battleground](https://pluto.security/blog/ai-agent-supply-chain-attacks/)
- 🟡 [AI 에이전트, 깃허브서 대량 PR로 신뢰 축적 중···공급망 공격 위험 커지나 (CIO 한국어)](https://www.cio.com/article/4134993/ai-%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8-%EA%B9%83%ED%97%88%EB%B8%8C%EC%84%9C-%EB%8C%80%EB%9F%89-pr%EB%A1%9C-%EC%8B%A0%EB%A2%B0-%EC%B6%95%EC%A0%81-%EC%A4%91%C2%B7%C2%B7%C2%B7%EA%B3%B5%EA%B8%89.html)
- 🟡 [MCP 위장부터 에이전트 하이재킹까지…AI 서비스 공격 6가지 유형 (CIO 한국어)](https://www.cio.com/article/4155366/mcp-%EC%9C%84%EC%9E%A5%EB%B6%80%ED%84%B0-%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8-%ED%95%98%EC%9D%B4%EC%9E%AC%ED%82%B9%EA%B9%8C%EC%A7%80ai-%EC%84%9C%EB%B9%84%EC%8A%A4-%EA%B3%B5%EA%B2%A9-6.html)
- ⚪ [AI 에이전트의 습격? 오픈클로와 몰트북 (이글루코퍼레이션)](https://www.igloo.co.kr/security-information/ai-%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%EC%9D%98-%EC%8A%B5%EA%B2%A9-%EC%98%A4%ED%94%88%ED%81%B4%EB%A1%9C%EC%99%80-%EB%AA%B0%ED%8A%B8%EB%B6%81/)
- ⚪ [AI 에이전트 설정 보안은 공급망 보안이에요](https://blakecrosley.com/ko/blog/ai-agent-config-supply-chain) — 에이전트 설정 파일도 공급망의 일부로 봐야 한다는 관점
- ⚪ [테크토크 - AI 에이전트 깃허브 PR 신뢰 축적 (sslc.kr)](https://sslc.kr/board/news/1294)

## B. MCP(Model Context Protocol) 보안 — 전 팀원 필독

- 🔴 [MCP Security Crisis: Systemic Design Flaws in AI Agent Infrastructure](https://labs.cloudsecurityalliance.org/research/csa-research-note-mcp-security-crisis-20260504-csa-styled/) — OX Security 발견, 20만 개 취약 인스턴스·1.5억 다운로드 규모의 설계 결함
- 🔴 [11 Emerging AI Security Risks with MCP](https://checkmarx.com/zero-post/11-emerging-ai-security-risks-with-mcp-model-context-protocol/)
- 🔴 [NSA/CISA — Model Context Protocol (MCP) Security PDF](https://media.defense.gov/2026/Jun/02/2003943289/-1/-1/0/CSI_MCP_SECURITY.PDF) — 국가기관 공식 가이드
- 🟡 [A Formal Security Framework for MCP-Based AI Agents (arXiv 2604.05969)](https://arxiv.org/pdf/2604.05969) — MCPSHIELD, 위협 분류체계+검증 모델
- 🟡 [MCP Security Bench: Benchmarking Attacks Against MCP in LLM Agents (arXiv)](https://arxiv.org/pdf/2510.15994)
- 🟡 [MCP-SandboxScan: WASM 기반 안전 실행·런타임 분석 (arXiv)](https://arxiv.org/pdf/2601.01241)
- 🟡 [SMCP: Secure Model Context Protocol (arXiv)](https://arxiv.org/pdf/2602.01129)
- 🟡 [MCP Security Statistics 2026: CVEs, Vulnerabilities & Breach Data](https://www.practical-devsecops.com/mcp-security-statistics-2026-report/) — CVE-2025-6514 등 실제 수치
- 🟡 [Model Context Protocol Threat Modeling (MDPI 저널 논문)](https://www.mdpi.com/2624-800X/6/3/84)
- ⚪ [MCP Security in 2026: Attack Surface, Real Incidents](https://agentmelt.com/blog/mcp-security-2026-attacks-and-defenses/)
- ⚪ [MCP Security Testing 2026 Guide](https://securitywall.co/blog/mcp-security-testing-guide)

## C. 소프트웨어 공급망 보안 개념·표준 (SBOM/SCA/SLSA)

- 🔴 [CISA — Defending Against Software Supply Chain Attacks](https://www.cisa.gov/resources-tools/resources/defending-against-software-supply-chain-attacks) — 국가기관 공식 가이드, 가장 신뢰도 높은 기초 자료
- 🔴 [NIST — Software Supply Chain Security Guidance](https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity/software-supply-chain-security-guidance)
- 🟡 [CISA — Securing the Software Supply Chain: Recommended Practices Guide](https://www.cisa.gov/resources-tools/resources/securing-software-supply-chain-recommended-practices-guide-customers-and)
- 🟡 [What is the SLSA Framework? (JFrog)](https://jfrog.com/learn/grc/slsa-framework/) — 빌드 프로세스 보안 표준, 4단계 성숙도
- 🟡 [SLSA 공식 FAQ](https://slsa.dev/spec/v1.1/faq)
- 🟡 [Software Supply Chain Security: Strategic Guide to SCA, SBOMs, Risk Prioritization](https://www.armorcode.com/blog/software-supply-chain-security-guide-sca-sbom)
- ⚪ [Sysdig — 7 Software Supply Chain Security Best Practices 2026](https://www.sysdig.com/learn-cloud-native/software-supply-chain-security-best-practices)
- ⚪ [Veracode — Top Best Practices for Enterprises](https://www.veracode.com/blog/top-software-supply-chain-security-best-practices/)
- ⚪ [OX Security — Top 5 SBOM Tools 2026](https://www.ox.security/blog/sbom-tools/)
- ⚪ [Bastion — 12 Best Practices to Prevent Supply Chain Attacks](https://bastion.tech/blog/software-supply-chain-attack-prevention-best-practices/)
- ⚪ [Cloudsmith — 2026 Guide to Software Supply Chain Security](https://cloudsmith.com/blog/the-2026-guide-to-software-supply-chain-security-from-static-sboms-to-agentic-governance)
- ⚪ [Deep Dive Into SLSA Provenance and Software Attestation](https://www.legitsecurity.com/blog/slsa-provenance-blog-series-part-2-deeper-dive-into-slsa-provenance)
- ⚪ [Kusari — SLSA 설명](https://www.kusari.dev/learning-center/slsa-supply-chain-levels-for-software-artifacts/)
- ⚪ [GitLab Docs — SLSA 적용](https://docs.gitlab.com/ci/pipeline_security/slsa/)
- ⚪ [AquilaX — Sigstore, SLSA, Build Provenance](https://aquilax.ai/blog/supply-chain-artifact-signing-slsa) — Sigstore(Cosign/Fulcio/Rekor)까지 연결해서 설명

## D. Dependency Collector 담당 — 실전 도구

- 🔴 [Trivy vs Grype (2026): Container Security Compared](https://appsecsanta.com/sca-tools/trivy-vs-grype) — 우리 예전 Snyk vs Dependabot 비교와 같은 저자, 신뢰도 높음
- 🟡 [Trivy vs Grype: Which Vulnerability Scanner for CI?](https://latchkey.dev/learn/tool-comparisons/trivy-vs-grype)
- 🟡 [Trivy vs Grype vs Snyk — Container Image Scanning Comparison](https://devopsboys.com/blog/trivy-vs-grype-vs-snyk-container-scanning-2026)
- 🟡 [How to Scan Docker Images for Vulnerabilities: Trivy, Grype, Snyk Compared](https://aquilax.ai/blog/scan-docker-images-vulnerabilities)
- ⚪ [Aikido — Top Tools to Detect Malware in Dependencies 2025](https://www.aikido.dev/blog/top-tools-to-detect-malware-in-dependencies)

## E. 악성 패키지 탐지 — 학술 논문 (ML 담당 필독)

- 🔴 [A Machine Learning-Based Approach For Detecting Malicious PyPI Packages (arXiv)](https://arxiv.org/pdf/2412.05259) — 텍스트/파일/코드/메타데이터 특징으로 스태킹 분류기 사용, 우리 ML 모듈과 접근이 거의 동일
- 🔴 [On the Feasibility of Cross-Language Detection of Malicious Packages in npm and PyPI (arXiv)](https://arxiv.org/abs/2310.09571)
- 🟡 [Killing Two Birds with One Stone: Malicious Package Detection in NPM and PyPI (ACM TOSEM)](https://dl.acm.org/doi/10.1145/3705304) — 언어 무관 단일 모델 접근
- 🟡 [Malicious Package Detection in NPM and PyPI (arXiv 2309.02637)](https://arxiv.org/pdf/2309.02637)
- ⚪ [ACM — Cross-Language Detection Full Text](https://dl.acm.org/doi/fullHtml/10.1145/3627106.3627138)

## F. 타이포스쿼팅 · 의존성 컨퓨전

- 🔴 [GitGuardian — Typosquatting and Dependency Confusion Attacks](https://blog.gitguardian.com/protecting-your-software-supply-chain-understanding-typosquatting-and-dependency-confusion-attacks/)
- 🟡 [Endor Labs — Dependency Confusion: How Attackers Poison Your Build](https://www.endorlabs.com/learn/dependency-confusion-how-attackers-poison-your-build)
- 🟡 [Aviatrix — Typosquatting Supply Chain Attack 2026](https://aviatrix.ai/threat-research-center/typosquatting-supply-chain-attack-2026/) — ConfuGuard 연구(630건 실제 공격 확인) 언급
- ⚪ [ESET — What is Typosquatting?](https://www.eset.com/blog/en/home-topics/privacy-and-identity-protection/what-is-typosquatting-how-do-i-tackle-it/)
- ⚪ [SixHack Academy — Dependency Confusion and Malicious Packages](https://sixhackacademy.com/en/blog/dependency-confusion-malicious-packages/)

## G. 실제 공급망 공격 사례 — xz-utils (모두 필독)

- 🔴 [Invicti — The Xz-Utils Backdoor: The Supply Chain RCE That Got Caught](https://www.invicti.com/blog/web-security/xz-utils-backdoor-supply-chain-rce-that-got-caught)
- 🔴 [Wolves in the Repository: A Software Engineering Analysis of the XZ Utils Attack (arXiv)](https://arxiv.org/html/2504.17473v1) — 학술적 분석, 가장 상세
- 🟡 [BlackDuck — What is the Xz Utils Backdoor](https://www.blackduck.com/blog/xz-utils-backdoor-supply-chain-attack.html)
- 🟡 [SentinelOne — Threat Actor Planned to Inject Further Vulnerabilities](https://www.sentinelone.com/blog/xz-utils-backdoor-threat-actor-planned-to-inject-further-vulnerabilities/)
- ⚪ [Risk Ledger — XZ Utils Backdoor: TPRM Impact](https://riskledger.com/resources/xz-utils-backdoor-tprm)
- ⚪ [Unveiling the Critical Attack Path for Implanting Backdoors in Supply Chains (학술)](https://dl.acm.org/doi/10.1007/978-981-95-4434-9_24)
- ⚪ [An LLM-based Framework for Evaluating High-Stealthy Backdoor Risks (arXiv)](https://arxiv.org/pdf/2511.13341)

## H. AI 모델 자체의 보안 (Hugging Face 등)

- 🔴 [ReversingLabs — Malicious ML models discovered on Hugging Face](https://www.reversinglabs.com/blog/rl-identifies-malware-ml-model-hosted-on-hugging-face)
- 🟡 [JFrog — Data Scientists Targeted by Malicious HF Models with Silent Backdoor](https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/)
- 🟡 [A Large-Scale Exploit Instrumentation Study of AI/ML Supply Chain Attacks (arXiv)](https://arxiv.org/pdf/2410.04490)
- 🟡 [Checkmarx — "Free Hugs" Part 4: Hugging Face 주의사항](https://checkmarx.com/blog/free-hugs-what-to-be-wary-of-in-hugging-face-part-4/)
- ⚪ [MIT — Hugging Face AI Platform Riddled with 100 Malicious Models](https://cyberir.mit.edu/site/hugging-face-ai-platform-riddled-100-malicious-code-execution-models)
- ⚪ [GitHub — modelscan (모델 파일 스캐너 도구)](https://github.com/mehrinkiani/modelscan)

## I. 공격경로 분석 · 그래프 기반 보안 (Attack Path Engine 담당 필독)

- 🔴 [Wiz — What is Attack Path Analysis?](https://www.wiz.io/academy/attack-path-analysis) — 4단계 방법론, 가장 핵심
- 🔴 [PuppyGraph — What is Attack Path Analysis?](https://www.puppygraph.com/blog/attack-path-analysis)
- 🟡 [Security Boulevard — What Vulnerability Scanners Miss in Cloud Environments](https://securityboulevard.com/2026/08/attack-path-analysis-what-vulnerability-scanners-miss-in-cloud-environments/)
- 🟡 [Cy5 — Cloud Attack Path Analysis & Graph-Based Risk Modeling](https://www.cy5.io/blog/cloud-attack-path-analysis-graph-risk-modeling/)
- 🟡 [Neo4j — Cyber Security and Attack Analysis (GraphGist 실습)](https://neo4j.com/graphgists/cyber-security-and-attack-analysis/) — Cypher 쿼리로 직접 실습 가능
- 🟡 [GitHub — neo4j-graph-examples/cybersecurity (BloodHound 기반)](https://github.com/neo4j-graph-examples/cybersecurity)
- ⚪ [Tamnoon — 9 Best CNAPP Platforms in 2026](https://tamnoon.io/blog/cnapps-you-need-to-know-in-2026/)
- ⚪ [CrowdStrike — CNAPP 소개](https://www.crowdstrike.com/en-us/platform/cloud-security/cnapp/)
- ⚪ [Neo4j Blog — Bolster Your Cybersecurity by Visualizing Attack Graphs](https://neo4j.com/blog/developer/how-to-bolster-your-cybersecurity/)
- ⚪ [Medium — Neo4j Cybersecurity AuraDB & Sandbox](https://medium.com/neo4j/neo4j-cybersecurity-auradb-sandbox-graphs-for-cybersecurity-c3c8bde2ec8d)
- ⚪ [A Review of Knowledge Graph Application Scenarios in Cyber Security (arXiv)](https://arxiv.org/pdf/2204.04769)
- ⚪ [Microsoft Learn — Cloud Security Explorer and Attack Path Analysis (영상 강연)](https://learn.microsoft.com/en-us/shows/mdc-in-the-field/security-explorer)

## J. Dashboard 담당 — 시각화 라이브러리

- 🔴 [Cytoscape.js 공식 문서](https://js.cytoscape.org/)
- 🟡 [Cytoscape.js vs vis-network vs Sigma.js 2026 결정 가이드](https://www.pkgpulse.com/guides/cytoscape-vs-vis-network-vs-sigma-graph-visualization-2026)
- 🟡 [Rapidops — Network Graph Visualization with JavaScript](https://www.rapidops.com/blog/js-network-graph-visualization/)
- ⚪ [Cytoscape 공식 튜토리얼 — Basic Data Visualization](https://cytoscape.org/cytoscape-tutorials/protocols/basic-data-visualization/)

## K. ML 이상탐지 — 실습 튜토리얼

- 🔴 [DataCamp — Random Forest Classification in Python](https://www.datacamp.com/tutorial/random-forests-classifier-python)
- 🟡 [Analytics Vidhya — Anomaly Detection using Isolation Forest](https://www.analyticsvidhya.com/blog/2021/07/anomaly-detection-using-isolation-forest-a-complete-guide/)
- 🟡 [Spot Intelligence — Isolation Forest Tutorial](https://spotintelligence.com/2024/05/21/isolation-forest/)
- ⚪ [Medium — Machine Learning for Malware Analysis](https://medium.com/cyberdefendersprogram/machine-learning-for-malware-analysis-fca336b7346)

## L. 프롬프트 인젝션 / 에이전트 위협 연구

- 🟡 [OWASP — Prompt Injection Drives Most Agentic AI Security Failures 2026](https://www.helpnetsecurity.com/2026/06/11/owasp-prompt-injection-ai-security-failures/)
- 🟡 [Indirect Prompt Injection in the Wild (arXiv)](https://arxiv.org/pdf/2604.27202)
- 🟡 [A Survey on Agentic Security: Applications, Threats and Defenses (arXiv)](https://arxiv.org/pdf/2510.06445)
- ⚪ [Gravitee — State of AI Agent Security Report 2026](https://www.gravitee.io/state-of-ai-agent-security)
- ⚪ [Assessing Automated Prompt Injection Attacks in Agentic Environments (arXiv)](https://arxiv.org/pdf/2606.10525)
- ⚪ [Prompt Injection Attacks on Agentic Coding Assistants (arXiv)](https://arxiv.org/pdf/2601.17548)
- ⚪ [The Attack and Defense Landscape of Agentic AI: Survey (arXiv)](https://arxiv.org/pdf/2603.11088)

## M. OWASP 공식 표준

- 🔴 [OWASP Top 10 for LLM Applications (공식)](https://genai.owasp.org/llm-top-10/)
- 🟡 [OWASP Nest — Top 10 for LLM Applications 프로젝트 페이지](https://nest.owasp.org/projects/top-10-for-large-language-model-applications)
- ⚪ [Wiz — OWASP LLM Top 10 실무 가이드](https://www.wiz.io/academy/ai-security/owasp-llm-top-10)
- ⚪ [Lasso Security — OWASP Top 10 LLM 체크리스트](https://www.lasso.security/blog/owasp-top-10-llm-vulnerabilities-security-checklist)

## N. 학술 컨퍼런스 · 저널

- 🟡 [USENIX Security '26 Call for Papers](https://www.usenix.org/conference/usenixsecurity26/call-for-papers)
- 🟡 [S3C2 (Secure Software Supply Chain Center) — Publications 목록](https://s3c2.org/pubs/) — NDSS/USENIX 등 탑티어 논문 모음
- ⚪ [GitHub — Awesome-ML-SP-Papers (IEEE S&P/CCS/USENIX/NDSS 머신러닝 보안 논문 큐레이션)](https://github.com/gnipping/Awesome-ML-SP-Papers)
- ⚪ [Analyzing Challenges in Deployment of the SLSA Framework (arXiv)](https://arxiv.org/pdf/2409.05014)

## O. 최신 뉴스 (계속 업데이트되는 소스 — 북마크 추천)

- 🔴 [The Hacker News — Supply Chain Attack 태그](https://thehackernews.com/search/label/supply%20chain%20attack) — 매일 업데이트
- 🔴 [BleepingComputer — Supply Chain 태그](https://www.bleepingcomputer.com/tag/supply-chain/)
- 🟡 [Socket — Surveillance Malware Hidden in npm and PyPI Packages](https://socket.dev/blog/surveillance-malware-hidden-in-npm-and-pypi-packages) — 실제 악성 패키지 기술 분석
- 🟡 [TechCrunch — Hackers Compromised Dozens of Open Source Packages](https://techcrunch.com/2026/05/19/hackers-have-compromised-dozens-of-popular-open-source-packages-in-an-ongoing-supply-chain-attack/)
- ⚪ [BleepingComputer — Microsoft Links Mastra AI Supply Chain Attack to North Korea](https://www.bleepingcomputer.com/news/security/microsoft-links-mastra-ai-supply-chain-attack-to-north-korean-hackers/)
- ⚪ [BleepingComputer — Amazon Links Debug/Chalk npm Attacks to North Korea](https://www.bleepingcomputer.com/news/security/amazon-links-debug-chalk-npm-supply-chain-attacks-to-north-korean-hackers/)
- ⚪ [gbhackers — npm/PyPI Malware Campaign Exfiltrates CI/CD Secrets](https://gbhackers.com/npm-and-pypi-malware/)

## P. 컨퍼런스 발표 (Black Hat / DEF CON)

- 🟡 [ReversingLabs — 8 Supply Chain Security Talks at Black Hat](https://www.reversinglabs.com/blog/8-supply-chain-security-talks-you-dont-want-to-miss-at-black-hat)
- 🟡 [Microsoft — Black Hat USA 2026: Defending Trust in the Age of AI and Supply Chain Attacks](https://www.microsoft.com/en-us/security/blog/2026/07/17/microsoft-at-black-hat-usa-2026-defending-trust-in-the-age-of-ai-and-supply-chain-attacks/)
- ⚪ [tl;dr sec — Every AI Talk from BSidesLV/BlackHat/DEFCON 2024](https://tldrsec.com/p/tldr-every-ai-talk-bsideslv-blackhat-defcon-2024) — 영상 링크 다수 포함
- ⚪ [TechTarget — Black Hat 2025: Navigating AI and Supply Chain Security](https://www.techtarget.com/searchsecurity/opinion/Black-Hat-2025-Navigating-AI-and-supply-chain-security)

## Q. 팟캐스트 (통근·이동 중 듣기 좋음)

- ⚪ [Darknet Diaries Ep.54 — NotPetya](https://darknetdiaries.com/transcript/54/) — 공급망 공격으로 전세계 물류망 마비된 사건
- ⚪ [Darknet Diaries Ep.19 — Aurora](https://darknetdiaries.com/transcript/19/) — 공급업체 경유 국방기업 침투 사례
- ⚪ [Darknet Diaries 공식 팟캐스트 홈](https://podcast.darknetdiaries.com/)

## R. 큐레이션 목록 (Awesome Lists) — 시간 없으면 여기부터

각 링크 하나가 그 자체로 수십~수백 개의 추가 자료(논문/도구/블로그)로 이어지는 메타 자료입니다.

- 🔴 [awesome-software-supply-chain-security (bureado)](https://github.com/bureado/awesome-software-supply-chain-security) — 공급망 보안 전반, 가장 포괄적
- 🔴 [awesome-llm-supply-chain-security (ShenaoW)](https://github.com/ShenaoW/awesome-llm-supply-chain-security) — LLM 공급망 보안 특화(논문+CVE)
- 🟡 [awesome-ai-security (muellerberndt)](https://github.com/muellerberndt/awesome-ai-security)
- 🟡 [awesome-agent-skills-security (LLMSecurity)](https://github.com/LLMSecurity/awesome-agent-skills-security) — 에이전트 스킬/툴 생태계 보안 특화
- 🟡 [awesome-ai-security-tools (scadastrangelove)](https://github.com/scadastrangelove/awesome-ai-security-tools) — 실전 도구 중심
- ⚪ [cybersecurity-secure-software-supplychain-lifecyle (paulveillard)](https://github.com/paulveillard/cybersecurity-secure-software-supplychain-lifecyle)
- ⚪ [awesome-supply-chain (dalton)](https://github.com/dalton/awesome-supply-chain) — 물류 공급망까지 포함한 일반 버전
- ⚪ [Awesome-AI-For-Security (AmanPriyanshu)](https://github.com/AmanPriyanshu/Awesome-AI-For-Security)
- ⚪ [awesome-ai-security (gmh5225)](https://github.com/gmh5225/awesome-ai-security)
- ⚪ [awesome-ai-security (ottosulin)](https://github.com/ottosulin/awesome-ai-security)

## S. 실제 공급망 공격 사례 추가 — SolarWinds/Codecov/event-stream/ua-parser-js/tj-actions

- 🔴 [Unit42 (Palo Alto) — GitHub Actions Supply Chain Attack: tj-actions/changed-files Incident](https://unit42.paloaltonetworks.com/github-actions-supply-chain-attack/) — 23,000+ 저장소 영향, CVE-2025-30066
- 🔴 [Rescana — In-Depth Analysis: event-stream, ua-parser-js Poisoning](https://www.rescana.com/post/in-depth-analysis-supply-chain-poisoning-of-popular-npm-packages-exploiting-event-stream-ua-parser/) — 신뢰 넘겨받은 메인테이너가 악성 의존성 추가한 event-stream 사례, xz-utils와 패턴 유사
- 🟡 [Wiz — tj-actions/changed-files Supply Chain Attack (CVE-2025-30066)](https://www.wiz.io/blog/github-action-tj-actions-changed-files-supply-chain-attack-cve-2025-30066)
- 🟡 [Malwarebytes — Codecov Supply-Chain Compromise Likened to SolarWinds](https://www.malwarebytes.com/blog/news/2021/04/codecov-supply-chain-compromise-likened-to-solarwinds-attack)
- 🟡 [Harness — Assessing the tj-actions Supply Chain Attack](https://www.harness.io/blog/github-actions-supply-chain-attack-tj-actions-changed-files)
- ⚪ [AppSec Santa — Supply Chain Attacks: Types, Examples & Defense](https://appsecsanta.com/application-security/supply-chain-attacks-guide) — SolarWinds부터 최신까지 사례 총정리
- ⚪ [Computer Weekly — Codecov Attack Has Echoes of SolarWinds](https://www.computerweekly.com/news/252499587/Codecov-supply-chain-attack-has-echoes-of-SolarWinds)
- ⚪ [InfoWorld — GitHub Cascading Supply Chain Attack Compromising CI/CD Secrets](https://www.infoworld.com/article/3849245/github-suffers-a-cascading-supply-chain-attack-compromising-ci-cd-secrets.html)
- ⚪ [GitHub — DataDog step-security-agent-attack-simulator](https://github.com/DataDog/step-security-agent-attack-simulator) — SolarWinds/Codecov/ua-parser-js 공격을 직접 시뮬레이션해보는 도구
- ⚪ [arXiv — DevPhish: Social Engineering in Software Supply Chain Attacks on Developers](https://arxiv.org/html/2402.18401v1)

## T. CI/CD 파이프라인 보안 (GitHub Actions 등)

- 🟡 [Stingrai — GitHub Actions Security Best Practices 2026 Checklist](https://www.stingrai.io/blog/github-actions-security-checklist)
- ⚪ [BuildMVPFast — GitHub Actions Supply Chain Security Hardening Guide 2026](https://www.buildmvpfast.com/blog/github-actions-supply-chain-security-hardening-guide-2026)
- ⚪ [Snyk — Trivy GitHub Actions Supply Chain Compromise](https://snyk.io/articles/trivy-github-actions-supply-chain-compromise/)

## U. OpenSSF 생태계 도구 (Scorecard·GUAC·deps.dev)

- 🔴 [OpenSSF Scorecard 공식 사이트](https://scorecard.dev/) — 오픈소스 프로젝트 보안 건강도 자동 채점(18개+ 체크)
- 🔴 [deps.dev — Open Source Insights 공식 블로그](https://blog.deps.dev/) — 구글이 운영하는 의존성 그래프·취약점·Scorecard 통합 데이터
- 🟡 [GitHub — ossf/scorecard](https://github.com/ossf/scorecard)
- 🟡 [GUAC (Graph for Understanding Artifact Composition) 리서치 정리](https://rywalker.com/research/guac) — SBOM+SLSA+취약점을 그래프 DB로 통합, 우리 Attack Path Engine과 발상이 비슷함
- ⚪ [Kusari — OpenSSF 전체 생태계 소개](https://www.kusari.dev/learning-center/openssf/)
- ⚪ [Sbomify — OpenSSF와 Scorecard 설명](https://sbomify.com/2024/04/25/openssf-and-openssf-scorecards-bolstering-open-source-security/)
- ⚪ [systemshardening — OpenSSF Scorecard 위험 점수화 상세](https://www.systemshardening.com/articles/cross-cutting/openssf-scorecard-risk-scoring/)

## V. Python 보안 도구 실습 (Dependency Collector/Risk Analyzer 담당 필독)

- 🔴 [bernat.tech — Defense in Depth: A Practical Guide to Python Supply Chain Security](https://bernat.tech/posts/securing-python-supply-chain/) — 파이썬 공급망 보안 전반을 실전 관점에서 정리한 명문
- 🔴 [GitHub — pypi-security-best-practices (lirantal)](https://github.com/lirantal/pypi-security-best-practices)
- 🟡 [PyPI 공식 블로그 — Securing PyPI Accounts via 2FA](https://blog.pypi.org/posts/2023-05-25-securing-pypi-with-2fa/)
- 🟡 [BleepingComputer — PyPI Mandatory 2FA for All Publishers](https://www.bleepingcomputer.com/news/security/pypi-announces-mandatory-use-of-2fa-for-all-software-publishers/)
- 🟡 [GitHub Action — action-python-security-auditing (bandit+pip-audit 통합)](https://github.com/developmentseed/action-python-security-auditing)
- 🟡 [The Design Space of Lockfiles Across Package Managers (arXiv)](https://arxiv.org/pdf/2505.04834) — npm/pip/poetry 락파일 구조를 학술적으로 비교
- ⚪ [Real Python — Dependency Management With Python Poetry](https://realpython.com/dependency-management-python-poetry/)
- ⚪ [Exploitr — Dependency Pinning for npm: Defending Against Supply Chain Attacks](https://exploitr.com/articles/dependency-pinning-npm-supply-chain-attacks/)
- ⚪ [Google Cloud — Best Practices for Dependency Management](https://cloud.google.com/blog/topics/developers-practitioners/best-practices-dependency-management)
- ⚪ [Medium — Python Security 101: Safeguard Your Code with Bandit](https://medium.com/@piyushsonawane10/python-security-101-safeguard-your-code-with-bandit-7e4ef054cba6)

## W. 취약점 우선순위화 — EPSS·NVD API (Risk Analyzer 담당 필독)

- 🔴 [FIRST/CrowdStrike — Exploit Prediction Scoring System (EPSS) 설명](https://www.crowdstrike.com/en-us/cybersecurity-101/exposure-management/exploit-prediction-scoring-system-epss/) — CVSS의 한계를 보완하는 "실제 악용 확률" 지표, Risk Analyzer 점수화 설계에 CVSS와 함께 참고할 것
- 🔴 [Intruder — EPSS vs. CVSS: 어떤 방식이 더 나은가](https://www.intruder.io/blog/epss-vs-cvss)
- 🟡 [NVD 공식 논문 — Exploit Prediction Scoring System (arXiv)](https://arxiv.org/pdf/1908.04856)
- 🟡 [DEV Community — NVD 무료 API로 25만+ 취약점 조회하기](https://dev.to/0012303/nvd-has-a-free-api-search-250000-vulnerabilities-programmatically-4aem) — Dependency Collector의 취약점 조회 파트에 바로 응용 가능
- 🟡 [PacketCoders — Python과 nvdlib로 NIST 취약점 데이터 조회](https://www.packetcoders.io/querying-vulnerability-data-from-the-nist-database-using-python-and-nvdlib/)
- ⚪ [Splunk — EPSS How It Works and Why It Matters](https://www.splunk.com/en_us/blog/learn/epss-exploit-prediction-scoring-system.html)
- ⚪ [Orca Security — EPSS Scoring System Explained](https://orca.security/resources/blog/epss-scoring-system-explained/)

## X. 서명·증명 (Sigstore/Cosign) — 공급망 무결성 검증

- 🟡 [Sigstore 공식 — Cosign Quickstart](https://docs.sigstore.dev/quickstart/quickstart-cosign/)
- 🟡 [Chainguard Academy — Keyless로 컨테이너 이미지 서명하기](https://edu.chainguard.dev/open-source/sigstore/how-to-keyless-sign-a-container-with-sigstore/)
- ⚪ [GitHub — sigstore/cosign](https://github.com/sigstore/cosign)
- ⚪ [OpenSSF — Scaling Up Supply Chain Security with Sigstore](https://openssf.org/blog/2024/02/16/scaling-up-supply-chain-security-implementing-sigstore-for-seamless-container-image-signing/)

## Y. AI/ML 보안 심화 — 데이터 포이즈닝·그래프 신경망 탐지 (ML 담당)

- 🔴 [OWASP ML Security Top 10 — ML02:2023 Data Poisoning Attack](https://owasp.org/www-project-machine-learning-security-top-10/docs/ML02_2023-Data_Poisoning_Attack) — 공식 표준, 필독
- 🟡 [Wiz — Data Poisoning: Trends and Recommended Defense Strategies](https://www.wiz.io/academy/ai-security/data-poisoning)
- 🟡 [arXiv — Data Poisoning in Deep Learning: A Survey](https://arxiv.org/pdf/2503.22759)
- ⚪ [Palo Alto — What Is Data Poisoning? Examples & Prevention](https://www.paloaltonetworks.com/cyberpedia/what-is-data-poisoning)
- ⚪ [ScienceDirect — GraphShield: Dynamic Graph-Based Malware Detection using GNN](https://www.sciencedirect.com/science/article/pii/S095741742503427X) — 우리 ML+그래프 접근을 결합한 최신 연구 방향
- ⚪ [arXiv — Mal2GCN: Robust Malware Detection via Graph Convolutional Networks](https://arxiv.org/pdf/2108.12473)
- ⚪ [NCBI — MalHAPGNN: Call Graph 기반 계층적 어텐션 GNN 멀웨어 탐지](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11769114/)

## Z. 국내(한국) 공식 자료

- 🔴 [KISA — SW 공급망 보안 가이드라인 1.0 (전체본·요약본)](https://www.kisa.or.kr/2060204/form?postSeq=15&page=1) — 과기정통부·국정원·KISA 공동 발표, 국내 프로젝트라면 가장 먼저 참고할 공식 문서
- 🟡 [KISA 자료실 (기술안내서 가이드)](https://www.kisa.or.kr/public/laws/laws3_View.jsp?cPage=5&mode=view&p_No=259&b_No=259&d_No=61&ST=total&SV=/>)
- ⚪ [캐치시큐 — SW 공급망 보안 가이드라인 1.0 다운로드](https://www.catchsecu.com/download/%ED%95%9C%EA%B5%AD%EC%9D%B8%ED%84%B0%EB%84%B7%EC%A7%84%ED%9D%A5%EC%9B%90-sw-%EA%B3%B5%EA%B8%89%EB%A7%9D-%EB%B3%B4%EC%95%88-%EA%B0%80%EC%9D%B4%EB%93%9C%EB%9D%BC%EC%9D%B8-1-0-2024-05)
- ⚪ [KISIA — SW 공급망 보안 가이드라인 전체본 PDF](https://www.kisia.or.kr/bucket/uploads/2024/05/13/sw%20%EA%B3%B5%EA%B8%89%EB%A7%9D%20%EB%B3%B4%EC%95%88%20%EA%B0%80%EC%9D%B4%EB%93%9C%EB%9D%BC%EC%9D%B8%20(%EC%A0%84%EC%B2%B4%EB%B3%B8)%200513.pdf)

## AA. SBOM 도입 현황 리서치 (졸업논문/보고서 인용용)

- 🔴 [ENISA — SBOM Adoption State of Play 2026 (EU 공식 서베이, 334개 기관 대상)](https://www.enisa.europa.eu/publications/sbom-adoption-state-of-play-2026)
- 🟡 [DigiCert — 2026 State of Software Supply Chain Security Report (PDF)](https://www.digicert.com/content/dam/digicert/pdfs/report/the_state_of_software_supply_chain_security_report.pdf)
- 🟡 [Aikido — SBOMs in 2026: Everyone's Generating Them, No One's Using Them](https://www.aikido.dev/blog/sboms-everyones-generating-them-no-ones-using-them) — SBOM 생성과 실사용 사이의 괴리, 우리 프로젝트가 메우려는 그 간극
- ⚪ [arXiv — SBOM Challenges for Developers: Stack Overflow 질문 분석](https://arxiv.org/pdf/2502.03975)
- ⚪ [SOCFortress(Medium) — ENISA SBOM Adoption 2026 해설 Part I·II](https://socfortress.medium.com/enisa-sbom-adoption-in-2026-from-security-best-practice-to-regulatory-imperative-part-i-f9ea6003bb67)

---

## 📊 요약

| 카테고리 | 개수 |
|---|---|
| A~D (배경·MCP·표준·도구) | 약 40개 |
| E~H (탐지·사례·AI모델보안) | 약 25개 |
| I~K (그래프·시각화·ML실습) | 약 20개 |
| L~N (프롬프트인젝션·표준·학술) | 약 15개 |
| O~R (뉴스·컨퍼런스·팟캐스트·큐레이션목록) | 약 25개 |
| S~V (사고사례 추가·CI/CD·OpenSSF·파이썬 도구) | 약 35개 |
| W~AA (EPSS/NVD·서명·데이터포이즈닝·국내자료·SBOM 리서치) | 약 22개 |
| **합계** | **182개** (+ 큐레이션 목록 10개가 각각 수십~수백 개로 확장 가능) |

**추천 순서**: A(배경) → 자기 담당 섹션(B/D/V/I/J/K 중 하나) → S(실제 사고사례로 감 잡기) → R(Awesome List 하나 골라서 브라우징) → O(최신 뉴스)
