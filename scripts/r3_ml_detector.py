import json
import os

# 입력 파일: R1이 출력한 수집 결과
INPUT_FILE = "collector_output.json"
# 출력 파일: R3 이상 탐지 결과
OUTPUT_FILE = "ml_result.json"

def run_ml_detector():
    # 1. 수집 데이터 확인
    if not os.path.exists(INPUT_FILE):
        print(f"[!] {INPUT_FILE} 파일이 존재하지 않습니다. 임시 테스트 모드로 진행합니다.")
        packages = [{"name": "example-pkg", "repo": "https://github.com/test"}]
    else:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            packages = data.get("packages", [])

    # 2. ML 이상 탐지 로직 (예시)
    detected_anomalies = []
    for pkg in packages:
        pkg_name = pkg.get("name", "unknown")
        
        # TODO: 실제 ML 모델(.pkl) 로드 및 Feature 추출 후 추론 로직 적용
        anomaly_score = 0.85
        is_malicious = anomaly_score >= 0.7
        
        detected_anomalies.append({
            "package_name": pkg_name,
            "anomaly_score": anomaly_score,
            "is_malicious": is_malicious,
            "top_features": ["typosquatting_similarity", "recent_author_change"]
        })

    # 3. ml_result.json 출력
    result_payload = {
        "status": "SUCCESS",
        "detected_anomalies": detected_anomalies
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result_payload, f, indent=2, ensure_ascii=False)

    print(f"[+] R3 ML Detector 완료: {OUTPUT_FILE} 생성됨")

if __name__ == "__main__":
    run_ml_detector()