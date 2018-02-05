import requests
import time


class Cache:

    content = {}
    time = {}
    ttl = 3600

    def __init__(self, ttl):
        self.ttl = ttl

    def get_content(self, resource, headers):
        if self.check_content(resource) and self.check_time(resource):
            return self.content[resource]
        else:
            return self.update_content(resource, headers)

    def update_content(self, resource, headers):
        self.content[resource] = requests.get(resource, headers=headers)
        self.time[resource] = time.time()
        return self.content[resource]

    def check_time(self, resource):
        if time.time() <= self.time[resource] + self.ttl:
            return 1
        else:
            return 0

    def check_content(self, resource):
        if resource in self.content:
            return 1
        else:
            return 0
