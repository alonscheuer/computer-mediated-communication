import pandas
from glob import glob
from tqdm import tqdm
from stanza.pipeline.multilingual import MultilingualPipeline
from unicodedata import category

nlp = MultilingualPipeline(lang_id_config={"langid_lang_subset": ["nl", "zh-hans", "he"]},
													 processors="tokenize")

def count_words(text):
	stripped = ''.join(ch for ch in text if category(ch)[0] != 'P')
	if len(stripped) > 0:
		doc = nlp(stripped)
		return doc.num_tokens
	else:
		return 0

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
	df = df.sort_values(by='like_counts').head(1000)
	df['user'] = df.loc[:, 'comment_user'].apply(lambda x: x['_id'])
	df['timestamp'] = df['created_at']
	df = df[["user", "content", "timestamp"]]
	df.to_json("data/comments_zh.json", force_ascii=False, orient="records")
	df['country'] = 'ZH'
	datasets.append(df)

	tqdm.pandas()
	all = pandas.concat(datasets)
	all['word_count'] = all.loc[:, 'content'].progress_apply(lambda x: count_words(x))
	all.to_json("data/comments_all.json", force_ascii=False, orient="records")

main()