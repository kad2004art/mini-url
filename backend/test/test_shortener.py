import pytest

from pytest import MonkeyPatch
from fakeredis import FakeRedis
from typing import List, Dict

from ..app.core.shortener import Shortener


@pytest.mark.parametrize("key",
                         [
                             "abcinvalid",
                             "efginvalid",
                             "",
                         ])
def test_invalid_short_key(key: str, db: FakeRedis) -> None:
    shortener = Shortener(db)
    with pytest.raises(KeyError):
        _ = shortener.short_to_long(key)
        
        
@pytest.mark.parametrize("urls",
                         [
                             ["https://my/long/url",
                              "https://my/long/url",
                              "https://my/long/url",
                              "https://my/long/url",
                              "https://my/long/url",
                              "https://my/long/url",
                             ]
                         ])
def test_short_handles_duplicates(monkeypatch: MonkeyPatch, db: FakeRedis, urls: List[str]) -> None:
    shortener = Shortener(db)
    monkeypatch.setattr(shortener, "mapping", value = "aA0")
    for url in urls:
        shortener.long_to_short(url)
    size = db.dbsize()
    assert size == len(urls)
    
    
def test_short_when_many_collisions(monkeypatch: MonkeyPatch, db: FakeRedis) -> None:
    shortener = Shortener(db)
    monkeypatch.setattr(shortener, "mapping", value="a")
    monkeypatch.setattr(shortener, "url_length", value=1)
    _ = shortener.long_to_short("https://my/long/url")
    with pytest.raises(KeyError):
        _ = shortener.long_to_short("https://my/long/url")
        
        
@pytest.mark.parametrize("urls",
                         [
                             ["https://my/long/url",
                              "https://my/long/url",
                              "https://my/long/url",
                             ]
                         ])
def test_long_to_short_multiple_same_url(create_items_from_urls: None, db: FakeRedis, urls: List[str]) -> None:
    all_keys = db.keys("*")
    url = urls[0]
    assert len(all_keys) == len(urls)
    assert all([db.get(key) == url for key in all_keys])
    
    
@pytest.mark.parametrize("urls",
                         [
                             ["https://my/long/url",
                              "https://my/another/very/long/url-something-else?param=1&param2=2",
                              "https://my/long/url1",
                             ]
                         ])
def test_long_to_short_multiple_url(create_items_from_urls: None, db: FakeRedis, urls: List[str]) -> None:
    all_keys = db.keys("*")
    assert.len(all_keys) == len(urls)
    assert all([db.get(key) in urls for key in all_keys])
    
    
@pytest.mark.parametrize("long_url",
                         [
                             "https://my/long/url",
                             "https://my/another/very/long/url-something-else?param=1&param2=2"
                         ])
def test_long_to_short(shortener_info: Dict, db: FakeRedis, long_url: str) -> None:
    shortener = Shortener(db)
    short_key = shortener.long_to_short(long_url)
    key_length = shortener_info["key_length"]
    key_prefix = shortener_info["key_prefix"]
    mapping = shortener_info["mapping"]
    assert len(short_key) == key_length
    assert db.get(key_prefix + short_key) == long_url
    assert all([char in mapping for char in short_key])
    
    
@pytest.mark.parametrize("long_url",
                         [
                             "https://my/long/url",
                             "https://my/another/very/long/url-something-else?param=1&param2=2"
                         ])
def test_short_to_long(db: FakeRedis, long_url: str) -> None:
    shortener = Shortener(db)
    short_key = shortener.long_to_short(long_url)
    actual_long_url = shortener.short_to_long(short_key)
    actual_long_url = shortener.short_to_long(short_key)
    assert actual_long_url == long_url