import json
import os.path as osp
import argparse
import random
import pandas as pd

script_dir = osp.dirname(__file__)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('sample_out')
	parser.add_argument('titles_out')
	parser.add_argument('groupless_titles')
	args = parser.parse_args()
	sample_out = args.sample_out
	titles_out = args.titles_out
	groupless_titles = args.groupless_titles
	
	all_dict = {'politics_filtered_nov19': {'count': 33}, 'politics_filtered_nov20': {'count': 34}, 'politics_filtered_nov21': {'count': 33}, 'conservative_filtered_nov19': {'count': 33}, 'conservative_filtered_nov20': {'count': 34}, 'conservative_filtered_nov21': {'count': 33}}	
	sample = []	

	for name in all_dict:
		file_path = osp.join(script_dir, '..', 'data', (name + '.json'))
		with open(file_path, 'r') as fp:
			all_dict[name]['full_posts'] = []
			all_dict[name]['texts'] = []
			all_dict[name]['titles'] = []
			for line in fp:
				post = json.loads(line)
				all_dict[name]['full_posts'].append(post)
				text = post['selftext']
				if text != '':
					all_dict[name]['texts'].append(text)
				title = post['title']
				all_dict[name]['titles'].append(title)
		titles = all_dict[name]['titles']
		sampled = random.sample(titles, all_dict[name]['count'])
		sample.extend(sampled)
	random.shuffle(sample)
	sample_df = pd.DataFrame({'title': sample, 'coding': ""})
	sample_df.to_csv(sample_out, index=False)
	
	all_df = pd.DataFrame({'group': [], 'title': []})
	for name in all_dict:
		name_rep = [name]*len(all_dict[name]['titles'])
		name_df = pd.DataFrame({'group': name_rep, 'title': all_dict[name]['titles']})
		all_df = all_df.append(name_df)
	all_df['coding'] = ''
	all_df = all_df.sample(frac = 1)
	all_df.to_csv(titles_out, index=False)	
	all_df = all_df.drop('group', axis=1)
	all_df.to_csv(groupless_titles, index=False)
	
if __name__ == '__main__':
	main()
