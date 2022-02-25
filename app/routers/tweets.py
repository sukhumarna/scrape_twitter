from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status
from fastapi.encoders import jsonable_encoder
import app.services.search_tweets as tws
import app.services.user_feed as uf

router = APIRouter()


@router.get("/hashtags/{keyword}/")
def get_tweets_by_hashtag(keyword: str,
                          limit: Optional[int] = Query(30, ge=1)):
    try:
        tweets_list = tws.get_tweets_by_keywords(keyword, limit)
        resp = tweets_list.tweets
    except Exception:
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail="external error")
    return resp


@router.get("/user/{username}/")
def get_user_tweets(username: str,
                    limit: Optional[int] = Query(30, ge=1)):
    try:
        tweets_list = uf.get_user_feed(username, limit)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user does not exist")
    except Exception:
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail="external error")
    resp = tweets_list.tweets
    return resp
