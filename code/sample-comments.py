import pandas

def main():
	df = pandas.read_json("data/comments_all.json")
	print(df.groupby('country').count())
	long_comments = df[df["word_count"] > 9]
	filtered = long_comments.groupby('country').sample(50, random_state=1)
	filtered.to_json("data/comments_all_sampled.json", force_ascii=False, orient="records")

main()