# locust_break_point.py
from locust import HttpUser, task, between, LoadTestShape


class BreakPointUser(HttpUser):
    wait_time = between(0.5, 1.5)

    @task
    def request(self):
        with self.client.get("/delay/2", catch_response=True) as r:
            if r.elapsed.total_seconds() > 3:
                r.failure("SLA 초과")


class StepLoadShape(LoadTestShape):
    stages = [
        {"duration": 60, "users": 100, "spawn_rate": 10},
        {"duration": 120, "users": 200, "spawn_rate": 20},
        {"duration": 180, "users": 300, "spawn_rate": 30},
        {"duration": 240, "users": 400, "spawn_rate": 40},
        {"duration": 300, "users": 500, "spawn_rate": 50},
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]
        return None
