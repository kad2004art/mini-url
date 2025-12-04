from pydantic import BaseModel, HttpUrl


class UrlBase(BaseModel):
    url: HttpUrl
    
    
class UrlIn(UrlBase):
    pass


class UrlOut(UrlBase):
    short_url: HttpUrl
    