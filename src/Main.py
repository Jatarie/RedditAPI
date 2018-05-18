import requests
from requests.auth import HTTPBasicAuth
from src import secrets


class SubmissionResponse:
    def __init__(self, permalink, link):
        self.permalink = permalink
        self.link = link


class Post:
    def __init__(self, subreddit, kind, id, score, url, permalink):
        self.subreddit = subreddit
        self.kind = kind
        self.id = id
        self.score = score
        self.url = url
        self.permalink = permalink


class Reddit:
    def __init__(self):
        self.base_url = "https://oauth.reddit.com"
        self.access_token = self.authenticate()
        self.base_headers = {"Authorization": "Bearer {}".format(self.access_token), "User-Agent": "testapp", "Content-Type": "application/x-www-form-urlencoded"}
        self.post_list = []
        self.submission_response_list = []

    def authenticate(self):
        redirect_uri = "http://localhost"
        r = requests.post("https://www.reddit.com/api/v1/access_token",
                          headers={"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "testapp"},
                          auth=HTTPBasicAuth(secrets.client_id, secrets.client_secret),
                          data={"grant_type": "refresh_token", "refresh_token": secrets.refresh_token, "redirect_uri": redirect_uri})

        access_token = r.json()["access_token"]
        return access_token

    def get_subreddit_posts(self, subreddit, time="all"):
        r = requests.get("{}/r/{}/top?t={}".format(self.base_url, subreddit, time), headers=self.base_headers).json()
        for index, post in enumerate(r["data"]["children"]):
            self.post_list.append(
                Post(
                    post["data"]["subreddit"],
                    post["kind"],
                    post["data"]["id"],
                    post["data"]["score"],
                    post["data"]["url"],
                    post["data"]["permalink"]
                ))

    def submit(self, subreddit="jtari", title="test", url="www.gfycat.com", kind="link", nsfw=True):
        r = requests.post("{}/api/submit?sr={}&title={}&url={}&kind={}&nsfw={}".format(self.base_url, subreddit, title, url, kind, nsfw), headers=self.base_headers).json()
        self.submission_response_list.append(SubmissionResponse(r["jquery"][16][3][0], r["jquery"][12][3][0]))

    def clear(self):
        self.post_list = []
        self.submission_response_list = []


cross_subs = ["cumsluts", "cumkiss", "cumswap", "lesbians"]

reddit = Reddit()
for sub in cross_subs:
    reddit.get_subreddit_posts(subreddit=sub, time="all")
    x = reddit.post_list[0].url
    reddit.submit(url=x, nsfw=False)
    print(reddit.submission_response_list[0].permalink)
    reddit.clear()
