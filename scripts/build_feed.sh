#!/bin/bash
set -e
cd "$(dirname "$0")/.."
OUT="AASM_FEED.md"

echo "# AASM — 통합 설계 피드 (AI 구현용 단일 문서)" > "$OUT"
echo "" >> "$OUT"
echo "이 파일 하나에 AASM 프로젝트를 처음부터 구현하는 데 필요한 설계/계약/스키마/용어를 전부 모았습니다." >> "$OUT"
echo "각 섹션은 실제 저장소 파일(\`docs/\`, \`schemas/\`, \`GIT_POLICY.md\`)의 원문이며, 이 파일은 그것들을 순서대로 이어붙인 것입니다." >> "$OUT"
echo "생성: $(date +%Y-%m-%d) / 원본이 갱신되면 이 파일도 다시 생성해야 합니다 (수동 편집 금지 — 각 원본 파일을 고치세요)." >> "$OUT"
echo "" >> "$OUT"
echo "## 목차" >> "$OUT"
cat >> "$OUT" << 'TOC'

1. Git/이슈/PR 운영 정책 (GIT_POLICY.md)
2. 용어집 (docs/glossary.md)
3. 이슈 계약: Epic / 하위 이슈 / PR 스키마 (docs/contracts/)
4. 전체 아키텍처 설계 (docs/design/00-overall.md)
5. 모듈별 기술 설계 (docs/design/01~05)
6. 모듈 간 데이터 계약 — JSON Schema 원문 (schemas/)
7. 교차검토 이력 (docs/design/_cross_review_questions.md)
8. 상위 이슈(Epic) 목록 (docs/epics/)

---
TOC

append_file() {
  local title="$1"
  local path="$2"
  echo "" >> "$OUT"
  echo "# ============================================================" >> "$OUT"
  echo "# 원본: $path" >> "$OUT"
  echo "# ============================================================" >> "$OUT"
  echo "" >> "$OUT"
  cat "$path" >> "$OUT"
  echo "" >> "$OUT"
}

append_json() {
  local path="$1"
  echo "" >> "$OUT"
  echo "# ============================================================" >> "$OUT"
  echo "# 원본: $path" >> "$OUT"
  echo "# ============================================================" >> "$OUT"
  echo "" >> "$OUT"
  echo '```json' >> "$OUT"
  cat "$path" >> "$OUT"
  echo '```' >> "$OUT"
  echo "" >> "$OUT"
}

append_file "GIT_POLICY" GIT_POLICY.md
append_file "glossary" docs/glossary.md
append_file "epic_schema" docs/contracts/epic_schema.md
append_file "subissue_schema" docs/contracts/subissue_schema.md
append_file "pr_schema" docs/contracts/pr_schema.md
append_file "overall" docs/design/00-overall.md
for f in docs/design/0{1,2,3,4,5}-*.md; do append_file "$f" "$f"; done
append_json schemas/collector_output.schema.json
append_json schemas/risk_score.schema.json
append_json schemas/ml_result.schema.json
append_json schemas/attack_graph.schema.json
append_file "cross_review" docs/design/_cross_review_questions.md
for f in docs/epics/0{0,1,2,3,4,5,6}-*.md; do append_file "$f" "$f"; done

echo "Feed file built: $OUT ($(wc -l < "$OUT") lines, $(wc -c < "$OUT") bytes)"
