# for that subreddit and outputs them into the output file, one post on each line.

import argparse
import json
import requests


def output_posts(posts, output_file, f):
    for post in posts:
        #print(type(post))
#        with open(output_file, 'w') as f:
        json.dump(post['data'], f)
        f.write('\n')

def get_posts(subreddit, num_posts, after):
#    print(f'number of posts as input: {num_posts}')
 #   print(f'this is after at the beginning of get_posts: {after}')
    
    if after == 0:
        data = requests.get(f'http://api.reddit.com{subreddit}/hot?limit={num_posts}', 
            headers={'User-Agent': 'windows: requests (by /u/dabdou)'})
    #print(type(data))
    #print(json.dumps(data.json(), indent=2))
    #after = data.json()['after']
    #print(after)
    else:
        data = requests.get(f'http://api.reddit.com{subreddit}/hot?limit={num_posts}&after={after}', 
            headers={'User-Agent': 'windows: requests (by /u/dabdou)'})
 
    
    content = data.json()['data']#['children']['data'] 
    
    try:
        after = content['after']
    except:
        #print("something wrong with after value")
        posts = content['children']       

        return (posts, None)

    #else:
#        print(f'this is the after value: {after}')
        #print(f'this is before: {before}') 

    posts= content['children']#['data']
    #print(json.dumps(posts, indent=2))

    return (posts, after)


def main():

    # require -o argument
    num_posts=100
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', help='<output_file>', required=True)
    parser.add_argument('subreddit', help='<subreddit>')

    args = parser.parse_args()
    output_file = args.o
    subreddit = args.subreddit

    #print(f'This is the output_file: {output_file}')
    #print(f'This is the subreddit: {subreddit}')
    #print(type(subreddit))
    total_posts=[]

    # opening the output file
    f = open(output_file, 'w')
    
    after = 0 
    while len(total_posts) < 333:
        
        if 334 - len(total_posts) < 100:
            diff =  334 - len(total_posts) 
            posts, after = get_posts(subreddit, diff, after)
        else:
            posts, after = get_posts(subreddit, num_posts, after)
        #print(len(posts))
        total_posts.extend(posts)
        length_total = len(total_posts)
     #   print(f'length of total_posts now: {length_total}')
        # passing file handle as argument
        output_posts(posts, output_file, f) 
    
           
        
    f.close()
    #print(json.dumps(total_posts, indent=2))




if __name__=="__main__":
    main()
