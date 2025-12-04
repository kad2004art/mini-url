import random

from redis import Redis
from typing import Any


class Shortener:
    def __init__(self, db: Redis):
        self.mapping = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.db = db
        self.url_length = 8
        self.retries = 15
        self.key_prefix = "key:"
        
    def short_to_long(self, short_key: str) -> Any:
        # сохраните ключ как «key:VDfe3CwM»
        full_key = self.key_prefix + short_key
        long_url = self.db.get(full_key)
        if not long_url:
            msg = f"Short key "{short_key}" was not found. Check input for misspelling and try again!"
            raise KeyError(msg)
        return long_url
    
    def long_to_short(self, url: str) -> Any:
        for i in range(0, self.retries):
            short_key = self.generate_key()
            full_key = self.key_prefix + short_key
            response = self.db.set(full_key, url, nx = True)
            if response is not None:
                return short_key
            raise KeyError(f"Tried to create a short key {self.retries} times. Please try again!")
        
    def generate_key(self) -> str:
        chars = ["" for _ in range(0, self.url_length)]
        for i in range(0, self.url_length):
            index = random.randint(0, len(self.mapping) - 1)
            chars[i] = self.mapping[index]
        short_key = "".join(chars)
        
        