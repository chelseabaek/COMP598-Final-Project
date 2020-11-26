import argparse
import json
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('input_json')
	parser.add_argument('output_json')
	args = parser.parse_args()
	
	input_json = args.input_json
	output_json = args.output_json
    
	with open(input_json, 'r') as input_file:	
		post_list = []
		for line in input_file:
			x = json.loads(line)
			post_list.append(x)
			
	screen = []	
	data = []	
	
	# filter for tara, ivanka, mary and hunter
	for post in post_list:
		title = post['title'].lower()
		if 'lara' in title or 'ivanka' in title or 'mary' in title or 'hunter' in title or 'donald trump jr' in title:
			screen.append(post)	
	for post in screen:
		print(post['title'])
	
	for post in post_list:
		title = post['title'].lower()
		if 'trump' in title or 'biden' in title :
			data.append(post)

	with open(output_json, 'w') as output_file:
		for post in data:
			#print(post['title'])
			output_file.write(json.dumps(post))
			output_file.write('\n')
							
if __name__ == '__main__':
    main()
