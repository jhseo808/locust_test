from locust import HttpUser, task, between
from locust import LoadTestShape


class HttpbinUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def get_basic(self):
        self.client.get("/get", name="GET /get")

    @task
    def delayed(self):
        with self.client.get("/delay/2", name="GET /delay/2", catch_response=True) as r:
            if r.elapsed.total_seconds() > 3:
                r.failure("Spike SLA exceeded")


class SpikeTestShape(LoadTestShape):
    """
    Spike Test 시나리오
    - 0~1분   : 50 users
    - 1~2분   : 300 users (SPIKE)
    - 2~3분   : 50 users (Recovery)
    """

    stages = [
        {"duration": 60, "users": 50, "spawn_rate": 10},
        {"duration": 120, "users": 300, "spawn_rate": 50},   # 🔥 Spike
        {"duration": 180, "users": 50, "spawn_rate": 50},    # 🔻 Recovery
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]

        return None
