import argparse
import json

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('input_json')
	parser.add_argument('output_json')
	args = parser.parse_args()
	input_json = args.input_json
	output_json = args.output_json

	name_dict = {'biden': {}, 'joe': {}, 'joe biden': {}, 'trump': {}, 'donald': {}, 'donald trump': {}}
	for name in name_dict:
		name_dict[name]['titles'] = []
		name_dict[name]['texts'] = []
	
	with open(input_json, 'r') as f:
		for line in f:
			post = json.loads(line)
			text = post['selftext']
			title = post['title']
			for name in name_dict:
				if name in text.lower():
					name_dict[name]['texts'].append(text)
				if name in title.lower():
					name_dict[name]['titles'].append(title)
			
	with open(output_json, 'w') as f:
		json.dump(name_dict, f, indent=4)
 
if __name__ == '__main__':
	main()
