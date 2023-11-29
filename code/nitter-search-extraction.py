import requests
import bs4
import json

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

links = []
pages = []

def search(query):
  print(query)
  tweet_links = []
  next_pages = []
  req = requests.get(query, headers=header)
  soup = bs4.BeautifulSoup(req.text, 'html.parser').select('body')[0]
  timeline = soup.find(class_="timeline")
  tweets = timeline.find_all(class_="timeline-item")
  for t in tweets:
    tweet = t.find(class_="tweet-body")
    if tweet:
      tweet_data = {}
      tweet_data["link"] = "https://nitter.net" + t.find(class_="tweet-link").get("href")
      tweet_data["user"] = tweet.find(class_="username").text
      tweet_data["content"] = tweet.find(class_="tweet-content").text
      tweet_data["timestamp"] = tweet.find(class_="tweet-date").find("a").get("title")
      tweet_links.append(tweet_data)
  next = soup.find_all(class_="show-more")[-1]
  if next.find("a").text == "Load more":
    link = next.find("a").get("href")
    next_pages.append("https://nitter.net/search?" + link)
  return (tweet_links, next_pages)

def main():
	# something
  pages.append("https://nitter.net/search?f=tweets&q=%28from%3Anos%29+until%3A2022-02-26+since%3A2022-02-24&since=&until=&near=")
  while len(pages) > 0:
    tweet_links, next_pages = search(pages.pop())
    links.extend(tweet_links)
    pages.extend(next_pages)
  json.dump(links, open("data/nos_search.json", 'w'), ensure_ascii=False)
  # links_only = [i["link"] for i in links]
  # json.dump(links_only, open("data/nos_links.json"))

main()