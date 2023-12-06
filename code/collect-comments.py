import pandas
from glob import glob

def main():
	datasets = []
	# IL
	df = pandas.read_json("data/israel.json")
	comments = df[df["user"] != "@kann_news"]
	top_level_comments = comments[comments["ancestor"] == comments["parent"]]
	top_level_comments = top_level_comments[["user", "content", "timestamp"]]
	top_level_comments.to_json("data/comments_il.json", force_ascii=False, orient="records")
	top_level_comments['country'] = 'IL'
	datasets.append(top_level_comments)
	# NL
	df = pandas.read_json("data/nederlands.json")
	comments = df[df["user"] != "@NOS"]
	top_level_comments = comments[comments["ancestor"] == comments["parent"]]
	top_level_comments = top_level_comments[["user", "content", "timestamp"]]
	top_level_comments.to_json("data/comments_nl.json", force_ascii=False, orient="records")
	top_level_comments['country'] = 'NL'
	datasets.append(top_level_comments)
	# ZH
	comment_files = glob("data/Chinese/*/comment.jsonl")
	dfs = []
	for file in comment_files:
		dfs.append(pandas.read_json(file, lines=True))
	df = pandas.concat(dfs)
	df['user'] = df.loc[:, 'comment_user'].apply(lambda x: x['_id'])
	df['timestamp'] = df['created_at']
	df = df[["user", "content", "timestamp"]]
	df.to_json("data/comments_zh.json", force_ascii=False, orient="records")
	df['country'] = 'ZH'
	datasets.append(df)

main()