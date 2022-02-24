from pydantic import BaseModel
from typing import Optional
from typing import List


class AccountSchema(BaseModel):
    fullname:   str
    href:       str
    id:         str


class TweetSchema(BaseModel):
    account:    AccountSchema
    date:       str
    hashtags = []
    likes = 0
    replies = 0
    retweets = 0
    text:       str


class TweetsSchema(BaseModel):
    tweets: List[TweetSchema]


