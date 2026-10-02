# 미구현 단계 인터페이스 (설계만, MVP 범위 밖)

스펙 요청대로 1~4단계(+6단계 룰기반)만 실제 구현했고, 5단계(동적관찰)와 7단계(롤백)는 인터페이스만 정의합니다. 5~6단계 중 6(판정엔진)은 룰 기반으로 이미 구현했으므로, 여기선 5단계와 7단계만 다룹니다.

## Stage 5 — 경량 행동 기반(dynamic) 관찰 (선택적)

```python
def observe_install_behavior(
    package_files: list[Path],
    timeout_seconds: int = 10,
    network_isolated: bool = True,
) -> "DynamicObservation":
    """
    Run setup.py/postinstall in an isolated, network-restricted sandbox for a
    bounded time and record syscalls + network attempts. Never call this on
    the host - it MUST run in a disposable container/VM with no access to
    real credentials or the host filesystem beyond the package's own temp dir.

    Returns:
        DynamicObservation(
            network_attempts: list[str],       # destination host:port attempted
            file_writes_outside_tmp: list[str],
            subprocess_spawned: list[str],
            timed_out: bool,
            crashed: bool,
        )
    """
    raise NotImplementedError


@dataclass
class DynamicObservation:
    network_attempts: list
    file_writes_outside_tmp: list
    subprocess_spawned: list
    timed_out: bool
    crashed: bool
```

**구현 시 반드시 필요한 것 (실제 구현 전 결정 필요)**:
- 격리 방식: gVisor/Firecracker 같은 경량 VM, 또는 최소 Docker `--network=none` + seccomp 프로필. Docker만으론 커널 공유라 완전한 격리는 아님 — 위협 모델에 따라 재검토 필요.
- 타임아웃 이후 강제 종료(kill) 및 리소스 정리 보장.
- 비용: 매 설치 요청마다 컨테이너 기동 오버헤드(수 초) — hook이 모든 `pip install`을 가로채는 구조라 사용자 체감 지연이 생김. 기본은 OFF, `NEEDS_HUMAN_REVIEW` 판정이 나온 것만 선택적으로 이 단계를 태우는 게 현실적.

## Stage 7 — 승인 후 롤백 자동화

```python
def snapshot_lockfile(project_dir: Path) -> "LockfileSnapshot":
    """Called right before an ALLOW'd install actually runs. Captures the
    current lockfile (requirements.txt / package-lock.json / poetry.lock)
    content + hash so a later revert has something to restore to."""
    raise NotImplementedError


def revert_to_snapshot(snapshot: "LockfileSnapshot") -> None:
    """Restores the lockfile to the pre-install state and re-installs from
    it. Called when a package approved earlier is later found malicious
    (e.g. via a delayed OSV disclosure or a post-hoc scan)."""
    raise NotImplementedError


@dataclass
class LockfileSnapshot:
    project_dir: Path
    lockfile_path: Path
    content_before: str
    content_hash_before: str
    taken_at: str  # ISO timestamp
```

**구현 시 결정 필요한 것**:
- 스냅샷 저장 위치(로컬 `.agent-dependency-guard/snapshots/` vs 중앙 저장소) — "판정 결과 캐싱 및 조직 단위 신뢰 전이"(차별점 2번)와 저장소를 공유할지 여부.
- 이미 설치된 패키지를 실제로 제거하고 재설치하는 로직은 `pip`/`npm` 각각의 lockfile 포맷에 종속적이라 패키지 매니저별로 별도 어댑터 필요.
- 자동 revert를 **완전 자동으로 실행할지, 아니면 사람 승인 후 실행할지** — 자동 실행은 그 자체로 또 다른 자동화된 파일시스템 변경이라 신중해야 함 (이 프로젝트의 상위 원칙: 파괴적 작업은 사용자 확인 후).

## 차별점 2번(캐싱/신뢰전이)과 3번(동적관찰)의 관계

캐싱 레이어(한 번 리뷰된 패키지+버전 조합 재사용)는 이 MVP에 없습니다 — `scan_package()`가 매번 새로 스캔합니다. 실제 도입 시 `(name, version) -> Verdict` 캐시를 붙이면 되는데, **주의점**: 캐시된 ALLOW를 무한정 신뢰하면 안 됩니다 — 같은 `(name, version)`이라도 OSV에 새 취약점이 나중에 등록될 수 있으므로(사후 공개), 캐시에는 TTL(예: 7일)을 두고 만료 시 재스캔하는 게 안전합니다.
