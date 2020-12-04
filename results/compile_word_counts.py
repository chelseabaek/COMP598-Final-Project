import argparse
import pandas as pd
import json
import os.path as osp
import string

script_dir = osp.dirname(__file__)
pd.options.mode.chained_assignment = None
punctuation = string.punctuation

def get_words(df):
    def strip_punc(words):
        return words.translate(str.maketrans(punctuation,' '*len(punctuation))).lower()
    
    titles = df['title'].map(lambda x: strip_punc(x))
    all_words = titles.str.split(expand=True).stack().value_counts().to_dict()
    word_dict = {}
    for word in all_words:
        if word.isalpha(): #and all_words[word] >= 5:
            word_dict[word] = all_words[word]
    return word_dict

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-o', required=True, help='the output file')
	#parser.add_argument('csv_file', help='clean dialog file')
	args = parser.parse_args()

	output_json = args.o
	#csv_file = args.csv_file
    
	frag_dict = [1,2,3]
	coded_frags = []
	for frag in frag_dict:
		folder = osp.join(script_dir, '..', 'data', 'frags_for_coding')
		frag_groups = pd.read_csv(osp.join(folder, f'frag{frag}_with_groups.csv'))
		frag_coded = pd.read_csv(osp.join(folder, f'frag{frag}_annotated.csv'))
		repeats = {}
		if frag == 1:
			codings = frag_coded['coding']
			frag_groups['coding'] = codings
			coded_frags.append(frag_groups)
		elif frag == 2:
			coded_frags.append(frag_coded)
		else:
			groups = []
			for title in frag_coded['title']:
				possible_groups = frag_groups[frag_groups['title'] == title]['group']
				group = ""
				i = 0
				if title in repeats:
					i = repeats[title]
					repeats[title] += 1
				else:
					repeats[title] = 1
				group = possible_groups.iloc[i]
				groups.append(group)
			frag_coded['group'] = groups
			coded_frags.append(frag_coded)
 	
	coded_df = pd.concat(coded_frags, sort=True)
	word_dict = {}
	topics = [1,2,3,4,5,6,7,8]
	for topic in topics:
		topic_df = coded_df[coded_df['coding'] == topic]
		word_dict[topic] =  get_words(topic_df)

	with open(output_json, 'w') as f:
		json.dump(word_dict, f, indent=4)
	
	coded_df.to_csv('coded_posts.csv')

if __name__ == '__main__':
    main()


