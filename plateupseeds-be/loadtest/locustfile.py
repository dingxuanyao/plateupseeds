from locust import HttpUser, task

class Index(HttpUser):
    @task
    def index(self):
        self.client.get("")
