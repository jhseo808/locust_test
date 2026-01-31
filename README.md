# Locust 부하 테스트 프로젝트

httpbin.org를 대상으로 한 Locust 성능 테스트 시나리오 모음

## 📋 요구사항

- Python 3.7+
- Locust 2.0.0 이상

## 🚀 설치

```bash
pip install -r requirements.txt
```

## 📂 파일 구조

- `locust_basic.py`: 기본 부하 테스트 시나리오
- `locust_spike.py`: Spike 테스트 시나리오

## 🔧 사용법

### 1. 기본 부하 테스트 실행

```bash
locust -f locust_basic.py --host=https://httpbin.org
```

웹 UI 접속: http://localhost:8089

**테스트 시나리오:**
- `GET /get` (가중치 3): 기본 GET 요청
- `POST /post` (가중치 2): JSON payload 전송
- `GET /delay/2` (가중치 1): 지연 응답 테스트

### 2. Spike 테스트 실행

```bash
locust -f locust_spike.py --host=https://httpbin.org
```

**테스트 시나리오:**
- 0~1분: 50명의 사용자
- 1~2분: 300명의 사용자 (🔥 Spike)
- 2~3분: 50명의 사용자 (🔻 Recovery)

### 3. Headless 모드 실행 (CLI)

```bash
# 기본 테스트
locust -f locust_basic.py --host=https://httpbin.org --users 100 --spawn-rate 10 --run-time 5m --headless

# Spike 테스트 (Shape 클래스가 자동으로 사용자 수 조절)
locust -f locust_spike.py --host=https://httpbin.org --headless
```

## 📊 주요 기능

### locust_basic.py
- **실사용자 시뮬레이션**: 요청 간 1~2초 대기
- **응답 검증**: 상태 코드 및 응답 시간 체크
- **커스텀 실패 처리**: catch_response를 활용한 세밀한 성공/실패 판단

### locust_spike.py
- **LoadTestShape**: 시간대별 사용자 수 자동 조절
- **Spike 패턴**: 급격한 트래픽 증가 시뮬레이션
- **SLA 검증**: 3초 이상 응답 시 실패 처리

## 📈 결과 확인

테스트 실행 중:
- 웹 UI: http://localhost:8089
- 실시간 통계: RPS, 응답 시간, 성공률 등

테스트 완료 후:
- HTML 리포트 다운로드 가능
- CSV 파일로 상세 결과 저장 가능

## 🎯 테스트 목적

- **기본 부하 테스트**: 시스템의 일반적인 성능 측정
- **Spike 테스트**: 급격한 트래픽 증가 대응 능력 검증
- **지연 시나리오**: 타임아웃 및 느린 응답 처리 확인

## 📝 참고사항

- httpbin.org는 공개 테스트 API로, 실제 운영 환경 테스트 시 `--host` 옵션 변경 필요
- 대규모 테스트 시 분산 모드(`--master`, `--worker`) 활용 권장
- 방화벽/네트워크 정책 확인 필요
