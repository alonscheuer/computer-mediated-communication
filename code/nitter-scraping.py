import requests
import bs4
import json

links = []
data = []

header = {
  "Host": "nitter.net",
  "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
  "Accept-Language": "en-US,en;q=0.5",
  "Accept-Encoding": "gzip, deflate, br",
  "Connection": "keep-alive",
  "Cookie": "hlsPlayback=on",
  "Upgrade-Insecure-Requests": "1",
  "Sec-Fetch-Dest": "document",
  "Sec-Fetch-Mode": "navigate",
  "Sec-Fetch-Site": "same-origin",
  "Sec-Fetch-User": "?1"
}

def get_tweet(link):
  print(link)
  data = {}
  reply_links = []
  req = requests.get(link, headers=header)
  soup = bs4.BeautifulSoup(req.text, 'html.parser').select('body')[0]
  main_tweet = soup.find(id="m")
  data["link"] = link
  data["user"] = main_tweet.find(class_="username").text
  data["content"] = main_tweet.find(class_="tweet-content").text
  data["timestamp"] = main_tweet.find(class_="tweet-published").text
  tweet_past = soup.find(class_="before-tweet")
  if tweet_past:
    tweet_prevs = tweet_past.find_all(class_="timeline-item")
    data["ancestor"] = tweet_prevs[0].find(class_="tweet-link").get("href")
    data["parent"] = tweet_prevs[-1].find(class_="tweet-link").get("href")
  tweet_replies = soup.find(id="r")
  if tweet_replies:
    replies = tweet_replies.find_all(class_="reply")
    for reply in replies:
      reply_links.append("https://nitter.net" + reply.find(class_="tweet-link").get("href"))
  return (data, reply_links)

def main():
  links = json.load(open("code/links.json"))
  while len(links) > 0:
    tweet_data, tweet_replies = get_tweet(links.pop())
    data.append(tweet_data)
    links.extend(tweet_replies)
  json.dump(data, open("code/data.json", 'w'), ensure_ascii=False)

main()