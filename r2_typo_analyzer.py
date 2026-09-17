import json
import os
import sys
import re
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timezone
import Levenshtein

# -------------------------------------------------------------
# [설정] 로컬 캐시 및 공식 소스 URL 정의
# -------------------------------------------------------------
CACHE_FILE = "top_pypi_cache.json"
PYPI_TOP_URL = "https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.min.json"

LANGCHAIN_PYPROJECT_URLS = [
    "https://raw.githubusercontent.com/langchain-ai/langchain/master/libs/langchain/pyproject.toml",
    "https://raw.githubusercontent.com/langchain-ai/langchain/master/libs/core/pyproject.toml",
    "https://raw.githubusercontent.com/langchain-ai/langchain/master/libs/partners/pyproject.toml"
]

PRIVATE_PREFIXES = ["ajou-internal", "mycompany"]

# -------------------------------------------------------------
# 1. 이름 정제
# -------------------------------------------------------------
def canonicalize_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name.lower().strip())

def sanitize_package_name(raw_name) -> tuple[str | None, str | None]:
    # 1. 이름 정제: PyPI 생태계 데이터만 통과시키고, 이름에 섞인 버전 제약자(>=2.0)나 특수기호(-,_) 등 찌꺼기를 모두 떼어낸 순수한 패키지명만 남김.
    if not isinstance(raw_name, str):
        return None, f"비문자열 타입 입력 (type: {type(raw_name).__name__})"

    cleaned = raw_name.replace("\x00", "").replace("\r", "").replace("\n", "").replace("\t", "").strip()
    if not cleaned:
        return None, "빈 문자열 (공백/제어문자 단독)"

    if "@" in cleaned:
        cleaned = cleaned.split("@")[0].strip()

    cleaned = re.split(r"[\[><=~?!#;\s]", cleaned)[0].strip()

    if "/" in cleaned or "\\" in cleaned:
        return None, "로컬 파일 경로 또는 디렉터리 참조 형식"
    if cleaned.startswith(("git+", "http://", "https://", "ssh://")):
        return None, "VCS 저장소 직접 URL 참조 형식"

    cleaned = re.sub(r"[^a-zA-Z0-9-_.]", "", cleaned)
    cleaned = cleaned.strip("-_.")
    
    # [엣지케이스] 초장문 및 공백 입력: 패키지 이름 정제 이후 아무 글자도 남지 않거나, 128자 초과하는 긴 이름이 들어오면 스킵 처리
    if not cleaned:
        return None, "구분자 단독 입력 (정규화 시 길이 0)"
    if len(cleaned) > 128:
        return None, f"초장문 패키지명 ({len(cleaned)}자)"

    return cleaned, None

# -------------------------------------------------------------
# 화이트리스트 자동 구축 (변경 없음)
# -------------------------------------------------------------
def fetch_langchain_official_packages() -> set:
    print("[*] LangChain 공식 GitHub에서 최신 생태계 패키지 목록 동기화 중...")
    discovered = set()
    req_headers = {"User-Agent": "AASM-Security-Pipeline/1.0"}

    for url in LANGCHAIN_PYPROJECT_URLS:
        try:
            req = urllib.request.Request(url, headers=req_headers)
            with urllib.request.urlopen(req, timeout=5) as resp:
                content = resp.read().decode("utf-8")
                matches = re.findall(r'["\']?(langchain[-_a-zA-Z0-9]*)["\']?\s*=', content)
                for m in matches:
                    discovered.add(canonicalize_name(m))
                agent_matches = re.findall(r'["\']?(lang[a-zA-Z0-9_-]+)["\']?\s*=', content)
                for m in agent_matches:
                    discovered.add(canonicalize_name(m))
        except Exception:
            continue

    fallback_agent_pkgs = {
        "langchain", "langchain-core", "langchain-community", "langchain-text-splitters",
        "langgraph", "langsmith", "langserve", "chromadb", "faiss-cpu", "tiktoken",
        "langchain-openai", "langchain-anthropic"
    }
    discovered.update({canonicalize_name(p) for p in fallback_agent_pkgs})
    return discovered

def load_expanded_baseline() -> dict:
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cached_data = json.load(f)
            return {canonicalize_name(p): p for p in cached_data.get("packages", [])}

    print("\n" + "=" * 70)
    print("🚀 [최초 실행] 대규모 화이트리스트 자동 구축 시작")
    print("=" * 70)

    all_pkgs = set()

    print("[*] PyPI 글로벌 최다 다운로드 상위 5,000개 데이터셋 다운로드 중...")
    try:
        req = urllib.request.Request(PYPI_TOP_URL, headers={"User-Agent": "AASM-Security-Pipeline/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            for item in data.get("rows", []):
                all_pkgs.add(canonicalize_name(item["project"]))
    except Exception as e:
        print(f"[!] 데이터셋 수집 실패 ({e}). 기본 패키지로 대체합니다.")
        fallback = ["requests", "urllib3", "pydantic", "numpy", "cryptography", "six", "pytest", "jellyfish", "openai"]
        all_pkgs.update({canonicalize_name(p) for p in fallback})

    all_pkgs.update(fetch_langchain_official_packages())

    cache_payload = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "total_count": len(all_pkgs),
        "packages": sorted(list(all_pkgs))
    }
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache_payload, f, indent=2, ensure_ascii=False)

    print(f"[✔] 총 {len(all_pkgs)}개 기준 패키지 구축 완료 -> '{CACHE_FILE}'\n")
    return {pkg: pkg for pkg in all_pkgs}

# -------------------------------------------------------------
# 실제 유포 여부 검증 (PyPI 신원 조회)
# -------------------------------------------------------------
def check_pypi_existence(package_name: str) -> tuple[bool, str | None, int | None]:
    safe_name = urllib.parse.quote(package_name)
    url = f"https://pypi.org/pypi/{safe_name}/json"
    req = urllib.request.Request(url, headers={"User-Agent": "AASM-Security-Pipeline/1.0"})
    
    try:
        with urllib.request.urlopen(req, timeout=3) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                latest_ver = data.get("info", {}).get("version", "unknown")
                
                releases = data.get("releases", {})
                first_upload_dt = None
                
                for ver_files in releases.values():
                    for file_info in ver_files:
                        up_time_str = file_info.get("upload_time_iso_8601") or file_info.get("upload_time")
                        if up_time_str:
                            try:
                                dt = datetime.fromisoformat(up_time_str.replace("Z", "+00:00"))
                                if first_upload_dt is None or dt < first_upload_dt:
                                    first_upload_dt = dt
                            except Exception:
                                pass
                
                days_old = None
                if first_upload_dt:
                    if first_upload_dt.tzinfo is None:
                        first_upload_dt = first_upload_dt.replace(tzinfo=timezone.utc)
                    now = datetime.now(timezone.utc)
                    days_old = (now - first_upload_dt).days

                return True, latest_ver, days_old
            return False, None, None
    except Exception:
        return False, None, None

# -------------------------------------------------------------
# 분석 엔진 (5단계 정밀 필터링 적용)
# -------------------------------------------------------------
def analyze_typosquatting(raw_pkg_name: str, baseline_dict: dict, pypi_data: dict) -> tuple[int, str | None, str, bool]:
    norm_target = canonicalize_name(raw_pkg_name)
    target_len = len(norm_target)

    # 2. 정상 패키지 제외 (화이트리스트 통과): 수집해 둔 유명 패키지(Top 5000)나 사내 패키지(ajou-internal-)와 100% 똑같으면 위험도 0점으로 검사 종료
    if norm_target in baseline_dict:
        return 0, None, "✅ 정상 패키지 (기준군 일치)", False

    # [완료조건] 사내 패키지 분류 조건 확립: 기업/팀 내부 모듈의 오탐을 막기 위해, 패키지명이 특정 접두사 (예: ajou-internal- 등 다중 지원)로 시작할 경우 즉시 정상(0점)으로 통과시키는 예외 처리 적용 (기업/팀 마다 코드를 직접 수정해서 사용 가능)
    # [한계] 사내 패키지 룰을 악용한 경우: ajou-internal- 와 같은 접두사가 붙으면 무조건 안전하다고 믿는 코드를 작성. 만약 해커가 이러한 사실을 알게 되면, PyPI 서버에 똑같은 이름으로 악성 패키지를 생성할 수 있음.
    # -> 접두사만 보고 사내 패키지로 판단하고 0점을 주는 것이 아닌 추가로 패키지를 다운받는 저장소 주소가 사내 프라이빗 서버인지 퍼블릭 PyPI인지 확인하는 모듈 필요
    for prefix in PRIVATE_PREFIXES:
        if norm_target.startswith(prefix):
            return 0, None, "ℹ️ 사내 패키지 (타이포스쿼팅 제외)", False

    best_match = None
    min_dist = float("inf")
    max_similarity = 0.0

    # 3. Levenshtein 유사도 계산: 남은 패키지들이 화이트리스트와 철자가 헷갈리게 비슷하거나(Levenshtein 거리), 타겟 이름에 특정 단어를 덧붙인 패턴(콤보스쿼팅)인지 검사.
    for norm_base, original_base in baseline_dict.items():
        if abs(len(norm_base) - target_len) <= 3:
            dist = Levenshtein.distance(norm_target, norm_base)
            max_len = max(len(norm_target), len(norm_base))
            sim = 1.0 - (dist / max_len) if max_len > 0 else 0.0

            if sim > max_similarity:
                max_similarity = sim
                min_dist = dist
                best_match = original_base

    # [엣지케이스] 글자 수가 적은 경우 (동적 임계치 적용): 이름이 5글자 이하로 짧은 패키지들의 경우 우연히 이름이 겹쳐서 오탐이 날 확률이 매우 높음. 따라서 긴 패키지는 75%만 일치해도 타이포스쿼팅으로 의심하지만, 짧은 패키지는 85% 이상 일치해야 의심하도록 설정
    # [한계] 글자 수가 적은 경우: 수많은 3-4글자 정상 패키지들의 가짜 알림 폭주를 막기 위해 임계치를 85%로 높였으므로, os -> oss, six -> sixx 와 같이 극단적으로 짧은 단어의 타이포스쿼팅은 탐지를 못함
    threshold = 0.85 if target_len <= 5 else 0.75

    if max_similarity >= threshold:
        last_release = pypi_data.get("last_release_at")
        is_live = False
        days_old = None

        if last_release:
            try:
                dt = datetime.fromisoformat(last_release.replace("Z", "+00:00"))
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                days_old = (datetime.now(timezone.utc) - dt).days
                is_live = True
            except Exception:
                pass
        
        # 4. 실제 유포 여부 검증 (PyPI 신원 조회): 남은 의심패키지들에 대해 PyPI 서버를 확인. PyPI 실제 배포 및 생성일 확인.
        if not is_live:
            is_live, _, days_old = check_pypi_existence(norm_target)
        
        # 5. 최종 판정 및 점수 부여
        if is_live:
            is_recent = (days_old is not None and days_old <= 180)
            if min_dist <= 2 and is_recent:
                # 고위험 (80~100점): 유사도가 높고 180일 이내에 배포된 실제 사기 패키지
                return 100, best_match, f"🚨 고위험 사칭 (거리 {min_dist}, 등록 {days_old}일 전)", True
            else:
                # 주의 (50점): 유사도는 높지만 만들어진 지 6개월 넘은 오래된 패키지
                age_str = f"{days_old}일 전 등록" if days_old else "등록일 미상"
                return 50, best_match, f"⚠️ 유사 패키지 (주의, 오래됨: {age_str})", False
        else:
            # [엣지케이스] 미배포 유령 패키지: 이름이 아무리 비슷해도 실제 파이썬 서버에 배포되지 않아 다운로드 자체가 불가하다면, 위협 수준을 '단순 개발자 오타(25~40점)'로 대폭 낮춤
            return 25, best_match, f"⚠️ 단순 오타 (미배포, 유령 패키지 간주)", False

    # 3-2. 콤보스쿼팅 검사
    target_tokens = set(norm_target.split("-"))
    for norm_base, original_base in baseline_dict.items():
        is_core_target = any(k in norm_base for k in ["langchain", "openai", "pydantic", "chroma", "langgraph"])

        # [엣지케이스] 짧고 흔한 단어의 콤보스쿼팅 오탐 방지: 콤보스쿼팅 검사 시 기준 타겟이 6글자 미만의 짧은 단어라면 타겟에서 제외. (os, re, csv, bot 와 같이 짧은 단어는 일반적으로 너무 많이 쓰임)
        # (핵심 예외 타겟 적용: openai, faiss 등은 AI 에이전트 환경에서 자주 쓰이는 핵심 타겟 패키지는 글자 수가 짧더라도 예외적으로 콤보스쿼팅 감시망에 포함하여 집중 방어)
        if (len(norm_base) >= 6 or is_core_target) and norm_base in target_tokens:
            if norm_base == norm_target:
                continue

            last_release = pypi_data.get("last_release_at")
            is_live = False
            days_old = None

            if last_release:
                try:
                    dt = datetime.fromisoformat(last_release.replace("Z", "+00:00"))
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    days_old = (datetime.now(timezone.utc) - dt).days
                    is_live = True
                except Exception:
                    pass
            
            if not is_live:
                is_live, _, days_old = check_pypi_existence(norm_target)

            if is_live:
                is_recent = (days_old is not None and days_old <= 180)
                if is_recent:
                    return 80, original_base, f"🚨 콤보스쿼팅 사칭 (등록 {days_old}일 전)", True
                else:
                    return 50, original_base, f"⚠️ 유사 콤보 패키지 (오래됨)", False
            else:
                return 40, original_base, "⚠️ 콤보스쿼팅 결합 (미배포)", False

    # [완료조건] 독립 패키지 분류 조건 확립: 화이트리스트 타겟들과 대조했을 때, 유사도 임계치(75% 또는 85%)에 미달하고 콤보스쿼팅 패턴도 없는 경우, '독립 패키지'로 분류하여 0점 부여 (이때, 기준군과 아예 다르게 생긴 독립 패키지는 정상(0점)으로 패스)
    return 0, None, "✅ 독립 정상 패키지 (사칭 없음)", False

# -------------------------------------------------------------
# 5. 파이프라인 통합 실행 및 JSON 저장
# -------------------------------------------------------------
def run_pipeline(input_file: str, output_file: str = "r2_typo_output.json"):
    if not os.path.exists(input_file):
        print(f"[!] 입력 파일이 존재하지 않습니다: {input_file}")
        return

    baseline_dict = load_expanded_baseline()

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    dependencies = data.get("dependencies", [])
    analyzed_packages = []

    print("=" * 135)
    print(f"{'패키지명':<28} | {'Score':<5} | {'Risk':<5} | {'사칭 대상':<16} | {'분석 상태'}")
    print("-" * 135)

    for dep in dependencies:
        raw_name = dep.get("name") if isinstance(dep, dict) else None
        version = dep.get("version", "unknown") if isinstance(dep, dict) else "unknown"
        ecosystem = dep.get("ecosystem", "PyPI") if isinstance(dep, dict) else "PyPI"
        pypi_data = dep.get("pypi", {}) if isinstance(dep, dict) else {}

        if not raw_name:
            record = {
                "name": str(raw_name), "version": version, "ecosystem": ecosystem,
                "signals": {
                    "typosquatting_score": 0, "is_typo_risk": False, "matched_target": None,
                    "reason": "⚠️ 분석 스킵: name 필드 누락"
                }
            }
            analyzed_packages.append(record)
            continue

        # [엣지케이스] 다른 생태계 유입: PyPI 패키지가 아닌 다른 패키지가 입력될 경우 무시
        if ecosystem != "PyPI":
            record = {
                "name": str(raw_name), "version": version, "ecosystem": ecosystem,
                "signals": {
                    "typosquatting_score": 0, "is_typo_risk": False, "matched_target": None,
                    "reason": f"⚠️ 분석 스킵: 지원하지 않는 생태계 ({ecosystem})"
                }
            }
            analyzed_packages.append(record)
            print(f"{str(raw_name)[:25]:<28} | {'0':<5} | {'False':<5} | {'-':<16} | 스킵 ({ecosystem})")
            continue

        sanitized_name, skip_reason = sanitize_package_name(raw_name)

        if sanitized_name is None:
            display_name = str(raw_name)[:25]
            record = {
                "name": str(raw_name), "version": version, "ecosystem": ecosystem,
                "signals": {
                    "typosquatting_score": 0, "is_typo_risk": False, "matched_target": None,
                    "reason": f"⚠️ 분석 스킵: {skip_reason}"
                }
            }
            analyzed_packages.append(record)
            print(f"{display_name:<28} | {'0':<5} | {'False':<5} | {'-':<16} | ⚠️ 스킵: {skip_reason}")
            continue

        score, t_match, status, is_risk = analyze_typosquatting(sanitized_name, baseline_dict, pypi_data)

        # [완료조건] 데이터 격리: 향후 위험도 종합 산출 시 호환성을 위해 분석 결과(점수, 위험 여부, 이유)를 JSON의 signals 딕셔너리 내부에 분리하여 저장
        record = {
            "name": sanitized_name,
            "version": version,
            "ecosystem": ecosystem,
            "signals": {
                "typosquatting_score": score,
                "is_typo_risk": is_risk,
                "matched_target": t_match,
                "reason": status
            }
        }
        analyzed_packages.append(record)
        match_str = str(t_match) if t_match else "-"
        print(f"{sanitized_name:<28} | {score:<5} | {str(is_risk):<5} | {match_str:<16} | {status}")

    print("=" * 135)

    output_payload = {
        "scan_id": data.get("scan_id", "manual-scan"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_analyzed": len(analyzed_packages),
        "packages": analyzed_packages
    }

    out_dir = os.path.dirname(output_file)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_payload, f, indent=2, ensure_ascii=False)

    print(f"[✔] 결과 저장 완료: '{output_file}'\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[!] 사용법: python r2_typo_analyzer.py <입력_JSON> [<출력_JSON>]")
        target_input = "test_r1_realworld.json"
    else:
        target_input = sys.argv[1]

    target_output = sys.argv[2] if len(sys.argv) > 2 else "r2_typo_output.json"
    run_pipeline(target_input, target_output)
