import app.models.tweets as tm
import snscrape.modules.twitter as sntwitter
from datetime import datetime


class UserFeed:
    def __init__(self, username, tweets_count):
        self.username = username
        self.tweets_count = tweets_count
        self.__build_query()

    def __build_query(self):
        self.query = f'from:{self.username} include:nativeretweets exclude:replies'

    def check_entity(self):
        entity = sntwitter.TwitterUserScraper(self.username)._get_entity()
        return entity is not None

    def fetch(self):
        tweets_list = []
        for i, data in enumerate(sntwitter.TwitterSearchScraper(self.query).get_items()):
            if i > self.tweets_count - 1:
                break
            if data.retweetedTweet is not None:
                retweet = data.retweetedTweet
                account = tm.AccountSchema(fullname=retweet.user.displayname,
                                           href="/" + retweet.user.username,
                                           id=retweet.user.id)
                dt_tm = datetime.strftime(retweet.date, "%-H:%-M %p - %-d %b %Y")
                tweet = tm.TweetSchema(account=account,
                                       date=dt_tm,
                                       hashtags=[] if retweet.hashtags is None else retweet.hashtags,
                                       likes=retweet.likeCount,
                                       replied=retweet.replyCount,
                                       retweets=retweet.retweetCount,
                                       text=retweet.content)
                tweets_list.append(tweet)
            else:
                account = tm.AccountSchema(fullname=data.user.displayname,
                                           href="/" + data.user.username,
                                           id=data.user.id)
                dt_tm = datetime.strftime(data.date, "%-H:%-M %p - %-d %b %Y")
                tweet = tm.TweetSchema(account=account,
                                       date=dt_tm,
                                       hashtags=[] if data.hashtags is None else data.hashtags,
                                       likes=data.likeCount,
                                       replied=data.replyCount,
                                       retweets=data.retweetCount,
                                       text=data.content)
                tweets_list.append(tweet)
        tweets_list = tm.TweetsSchema(
            tweets=tweets_list
        )
        return tweets_list


def get_user_feed(username, tweets_count):
    ts = UserFeed(username, tweets_count)
    if not ts.check_entity():
        raise ValueError("user does not exists")
    try:
        tweets_resp = ts.fetch()
    except Exception:
        raise
    return tweets_resp
