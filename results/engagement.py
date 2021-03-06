import json
import argparse
import os.path as osp
import pandas as pd
import math

script_dir = osp.dirname(__file__)

def compute_engagement(groups, coded_df):
	engagement_dict = {}
	for group in groups:
		engagement_dict[group] = {}

	grouped_df = coded_df.groupby('group')
	for group in grouped_df:
		group_name = group[0]
		topics_df = group[1].groupby('coding')
		for topic in topics_df:
			topic_name = topic[0]
			logs = topic[1]['score'].map(lambda x: math.log(x) if x != 0 else 0)
			topic_score = sum(logs)
			num_posts = len(logs)
			average_score = topic_score / num_posts
			engagement_dict[group_name][topic_name] = {'number of posts': num_posts, 'score': topic_score, 'average_score': average_score}

	return engagement_dict

def add_scores(groups, coded_df, group_dict):
        repeats = {}
        for group in groups:
                repeats[group] = {}

        scores = []
        for row in range(len(coded_df)):
                group = coded_df['group'].iloc[row]
                group_df = group_dict[group]
                title = coded_df['title'].iloc[row]
                score = group_df[group_df['title'] == title]['score']
                if title in repeats[group]:
                        i = repeats[group][title]
                        repeats[group][title] += 1
                else:
                        i = 0
                        repeats[group][title] = 1
                score = score.iloc[i]
                scores.append(score)
        coded_df['score'] = scores
        return coded_df

def gen_group_dict(groups, input_folder):
        group_dict = {}
        for group in groups:
                titles = []
                scores = []
                group_dict[group] = None
                input_file = osp.join(input_folder, f'{group}.json')
                with open(input_file, 'r') as fp:
                        for line in fp:
                                post = json.loads(line)
                                scores.append(int(post['score']))
                                titles.append(post['title'])
                df = pd.DataFrame({'title': titles, 'score': scores})
                df = df.sort_values(by='score', ascending=False)
                group_dict[group] = df
        return group_dict

def by_subreddit(engagement_dict):
	sub_dict = {}
	for group in engagement_dict:
		sub = group.split('_')[0]
		if sub not in sub_dict:
			sub_dict[sub] = {}
		for topic in engagement_dict[group]:
			if topic in sub_dict[sub]:
				sub_dict[sub][topic]['number of posts'] += engagement_dict[group][topic]['number of posts']
				sub_dict[sub][topic]['score'] += engagement_dict[group][topic]['score']
			else:
				sub_dict[sub][topic] = {}
				sub_dict[sub][topic]['number of posts'] = engagement_dict[group][topic]['number of posts']
				sub_dict[sub][topic]['score'] = engagement_dict[group][topic]['score']
	for sub in sub_dict:
		for topic in sub_dict[sub]:
			sub_dict[sub][topic]['average_score'] = sub_dict[sub][topic]['score'] / sub_dict[sub][topic]['number of posts']
	return sub_dict

def overall(sub_dict):
	overall_dict = {}
	for sub in sub_dict:
		for topic in sub_dict[sub]:
			if topic in overall_dict:
				overall_dict[topic]['number of posts'] += sub_dict[sub][topic]['number of posts']
				overall_dict[topic]['score'] += sub_dict[sub][topic]['score']
			else:
				overall_dict[topic] = {}
				overall_dict[topic]['number of posts'] = sub_dict[sub][topic]['number of posts']
				overall_dict[topic]['score'] = sub_dict[sub][topic]['score']
	for topic in overall_dict:
		overall_dict[topic]['average_score'] = overall_dict[topic]['score'] / overall_dict[topic]['number of posts']
	return overall_dict

def get_top_posts(coded_df):
        top_posts = {}
        grouped_dfs = coded_df.groupby('group')
        for group in grouped_dfs:
                group_name = group[0]
                df = group[1]
                sorted_df = df.sort_values(by='score', ascending=False)[:10]
                top_posts[group_name] = list(zip(list(sorted_df['title']), list(sorted_df['score']), list(sorted_df['coding'])))
        return top_posts

def by_mention(coded_df):
	def mention(title):
		title = title.lower()
		if 'biden' in title and 'trump' in title:
			return 'Both'
		elif 'biden' in title:
			return 'Biden'
		elif 'trump' in title:
			return 'Trump'
		else:
			return 'Both'	
	coded_df['mention'] = coded_df['title'].map(lambda x: mention(x))
	mention_dict = {'Biden': {'topics': {}, 'score': 0, 'num_posts': 0}, 'Trump': {'topics': {}, 'score': 0, 'num_posts': 0}, 'Both': {'topics': {}, 'score': 0, 'num_posts': 0}}
	for mention in mention_dict.keys():
		mention_df = coded_df[coded_df['mention'] == mention]
		mention_dict[mention]['num_posts'] = len(mention_df)
		logs = mention_df['score'].map(lambda x: math.log(x) if x != 0 else 0)
		mention_dict[mention]['score'] = sum(logs)
		grouped_dfs = mention_df.groupby('coding')
		for group in grouped_dfs:
			topic = group[0]
			df = group[1]
			mention_dict[mention]['topics'][topic] = {'num_posts': len(df), 'score': 0, 'average_score': 0}
			logs = df['score'].map(lambda x: math.log(x) if x != 0 else 0)
			mention_dict[mention]['topics'][topic]['score'] = sum(logs)
			mention_dict[mention]['topics'][topic]['average_score'] = sum(logs) / len(logs)
	return mention_dict
	
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('organized_csv')
	parser.add_argument('input_folder')
	parser.add_argument('output_folder')	

	args = parser.parse_args()
	organized_csv = args.organized_csv
	input_folder = args.input_folder
	output_folder = args.output_folder
	
	coded_df = pd.read_csv(organized_csv)
	
	groups = coded_df['group'].unique()
	group_dict = gen_group_dict(groups, input_folder)
	coded_df = add_scores(groups, coded_df, group_dict)
	engagement_dict = compute_engagement(groups, coded_df)
	sub_engagement = by_subreddit(engagement_dict)
	overall_engagement = overall(sub_engagement)
	top_posts = get_top_posts(coded_df)
	mention_dict = by_mention(coded_df)

	with open(osp.join(output_folder, 'mentions.json'), 'w') as fp:
		json.dump(mention_dict, fp, indent=4)	
	with open(osp.join(output_folder, 'top_posts.json'), 'w') as fp:
		json.dump(top_posts, fp, indent=4)
	with open(osp.join(output_folder, 'engagement_output.json'), 'w') as fp:
		json.dump(engagement_dict, fp, indent=4)
	with open(osp.join(output_folder, 'sub_engagement.json'), 'w') as fp:
		json.dump(sub_engagement, fp, indent=4)
	with open(osp.join(output_folder, 'overall_engagement.json'), 'w') as fp:
		json.dump(overall_engagement, fp, indent=4)
	coded_df.to_csv(osp.join(output_folder, 'coded_with_scores.csv'))
		
if __name__ == '__main__':
	main()
