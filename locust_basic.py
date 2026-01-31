from locust import HttpUser, task, between


class HttpbinUser(HttpUser):
    """
    httpbin.org를 대상으로 한 Locust 성능 테스트 User
    """

    # 요청 간 대기 시간 (실사용자 시뮬레이션)
    wait_time = between(1, 2)

    @task(3)
    def get_basic(self):
        """
        GET /get
        - 가장 기본적인 GET 요청
        """
        with self.client.get("/get", name="GET /get", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Unexpected status code: {response.status_code}")

    @task(2)
    def post_basic(self):
        """
        POST /post
        - JSON payload 전송
        """
        payload = {
            "service": "locust-test",
            "user": "qa-engineer",
            "purpose": "performance-test"
        }

        with self.client.post(
            "/post",
            json=payload,
            name="POST /post",
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"POST failed: {response.status_code}")

    @task(1)
    def delayed_response(self):
        """
        GET /delay/2
        - 2초 지연 응답 (지연/타임아웃 시나리오)
        """
        with self.client.get("/delay/2", name="GET /delay/2", catch_response=True) as response:
            if response.elapsed.total_seconds() > 3:
                response.failure("Response time exceeded 3 seconds")
