import app.models.tweets as tm
from datetime import datetime
import snscrape.modules.twitter as sntwitter


class TwitterSearch:
    def __init__(self, keyword, tweets_count):
        self.keyword = keyword
        self.tweets_count = tweets_count
        self.__prep_hashtag()

    def __prep_hashtag(self):
        if not self.keyword.startswith('#'):
            self.keyword = "#" + self.keyword

    def fetch(self):
        tweets_list = []
        for i, data in enumerate(sntwitter.TwitterSearchScraper(self.keyword).get_items()):
            if i > self.tweets_count-1:
                break
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


def get_tweets_by_keywords(keyword, tweets_count):
    ts = TwitterSearch(keyword, tweets_count)
    try:
        tweets_resp = ts.fetch()
    except Exception:
        raise
    return tweets_resp
