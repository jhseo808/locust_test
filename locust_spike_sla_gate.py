# locust_spike_sla_gate.py
from locust import HttpUser, task, between, events

SLA_THRESHOLD = 3.0
SLA_BREACH_LIMIT = 7
sla_breach_count = 0


class SpikeSLAGateUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def delayed(self):
        global sla_breach_count

        with self.client.get("/delay/2", catch_response=True) as r:
            if r.elapsed.total_seconds() > SLA_THRESHOLD:
                sla_breach_count += 1
                r.failure("SLA 3초 초과")

                if sla_breach_count >= SLA_BREACH_LIMIT:
                    print("SLA 위반 한도 초과! 테스트 중단.")
                    events.test_stop.fire()
'''
Host              : https://httpbin.org
Number of users   : 200
Spawn rate        : 30
'''