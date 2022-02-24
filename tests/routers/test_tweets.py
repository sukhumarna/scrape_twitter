import mock
from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@mock.patch('app.services.search_tweets.get_tweets_by_keywords')
def test_get_hashtag(mock_get_tweets_by_keywords):
    error_resp = {"detail": "external error"}
    mock_get_tweets_by_keywords.side_effect = Exception
    response = client.get('/hashtags/test?limit=1')
    assert response.status_code == status.HTTP_424_FAILED_DEPENDENCY
    assert response.json() == error_resp

    response = client.get('/hashtags/test?limit=-1')
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@mock.patch('app.services.user_feed.get_user_feed')
def test_get_user_tweets(mock_get_user_tweets):
    error_resp = {"detail": "external error"}
    mock_get_user_tweets.side_effect = Exception
    response = client.get('/user/usertest?limit=1')
    assert response.status_code == status.HTTP_424_FAILED_DEPENDENCY
    assert response.json() == error_resp

    error_resp = {"detail": "user does not exist"}
    mock_get_user_tweets.side_effect = ValueError
    response = client.get('/user/nouser?limit=1')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == error_resp

    response = client.get('/user/nouser?limit=-1')
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
