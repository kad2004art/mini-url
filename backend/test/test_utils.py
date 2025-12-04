import pytest

from ..app import utils

@pytest.mark.parametrize("url",
                         [
                             "https://my.com/long/url",
                             "https://my.io/another/very/long/url-something-else?param=1&param2=2",
                             "http://www.mymy.pl/long/url1",
                         ])
def test_is_valid_url(url: str) -> None:
    valid = utils.is_valid_url(url)
    assert valid
    
@pytest.mark.parametrize("url",
                         [
                            "https:/my.com/long/url",
                             "htt://my.io/another/very/long/url-something-else?param=1&param2=2",
                             "", 
                         
                         ])
def test_is_valid_url_returns_false(url: str) -> None:
    utils.validate_url()
    
@pytest.mark.parametrize("url",
                         [
                             "https://stackoverflow.nom/questions/tagged/python",
                             "https://www.mmmmmmmm.com/search?q=python+learn",
                             "https:",
                             "",
                         ])
def test_validate_url_raises_error(url: str) -> None:
    with pytest.raises(ValueError):
        utils.validate_url(url)