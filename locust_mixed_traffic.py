# locust_mixed_traffic.py
from locust import HttpUser, task, between


class MixedTrafficUser(HttpUser):
    host = "https://httpbin.org"
    wait_time = between(0.5, 1.5)

    @task(7)
    def fast_api(self):
        self.client.get("/get")

    @task(2)
    def normal_api(self):
        self.client.post("/post", json={"data": "test"})

    @task(1)
    def slow_api(self):
        with self.client.get("/delay/2", catch_response=True) as r:
            if r.elapsed.total_seconds() > 3:
                r.failure("느린 API SLA 초과")
