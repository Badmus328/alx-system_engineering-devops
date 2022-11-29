#!/usr/bin/python3
"""
    Contains a function count_words that queries.
"""

from requests import get

def count_words(subreddit, word_list, after=None, dic={}):
    """
    function that quries the Reddit API and returns all
    the titles of hot articles listed for a given
    subreddit.
    """
    if len(dic) == 0:
        dic = {k.lower(): 0 for k in word_list}

    header = {'User-Agent': 'my-app/0.0.1'}
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    if after:
        url += "?after={}".format(after)

    req = get(url, headers=header)

    if req.status_code != 200 or req.url != url:
        return

    hot_list = req.json().get('data').get('children')
    after = req.json().get('data').get('after')

    for article in hot_list:
        words = article.get('data').get('title').split(' ')
        for word in word_list:
            dic[word.lower()] += words.count(word)

    if not after:
        dic = dict(sorted(dic.items(), key=lambda x:x[1], reverse=True))
        {print(k + ":", v) for k, v in dic.items() if v > 0}
        return
    return count_words(subreddit, word_list, after, dic)
