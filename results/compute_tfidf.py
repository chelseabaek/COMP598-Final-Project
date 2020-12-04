import argparse
import json
import math

def gen_total_wc_dict(wc_dict):
    topics = list(wc_dict.keys())
    total_wc_dict = {}
    for topic in topics:
        for word in wc_dict[topic]:
            if word in total_wc_dict:
                total_wc_dict[word] += wc_dict[topic][word]
            else:
                total_wc_dict[word] = wc_dict[topic][word]
    return total_wc_dict

def gen_total_topic_word_dict(wc_dict):
    topics = list(wc_dict.keys())
    total_dict = {}
    for topic in topics:
        for word in wc_dict[topic]:
            if word in total_dict:
                total_dict[word] += 1
            else:
                total_dict[word] = 1
    return total_dict

def calc_tfidf(occurrences, doc_freq, documents):
    tf = occurrences
    idf = math.log(documents / doc_freq, 10)
    return tf * idf

def compute_tfidfs(topic_dict, num_words, total_docs, doc_freq_dict):
    tfidf_dict = {}
    for word in topic_dict:
        tfidf_dict[word] = calc_tfidf(topic_dict[word], doc_freq_dict[word], total_docs)
    best = sorted(tfidf_dict, key=tfidf_dict.get, reverse=True)[:num_words]
    best_tuples = []
    for word in best:
        best_tuples.append((word, tfidf_dict[word]))
    return best_tuples

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', action='store_true', help='bonus points')
    parser.add_argument('wc_json', help='topic_counts.json')
    parser.add_argument('output', help='file to output to')
    parser.add_argument('num_words', help='the number of words to keep')
    args = parser.parse_args()
    
    version2 = False
    if args.p:    
        version2 = True

    wc_json = args.wc_json
    num_words = int(args.num_words)
    output_file = args.output

    wc_dict = None
    with open(wc_json, 'r') as fp:
        wc_dict = json.load(fp)

    topics = list(wc_dict.keys())
    tfidf_dict = {}

    if version2 == False:
        total_wc_dict = gen_total_wc_dict(wc_dict)
        total_words = sum(total_wc_dict.values())
        for topic in topics:
            tfidf_dict[topic] = compute_tfidfs(wc_dict[topic], num_words, total_words, total_wc_dict)   
    else:
        total_topic_word_dict = gen_total_topic_word_dict(wc_dict)
        num_topics = len(wc_dict.keys())
        for topic in topics:
            tfidf_dict[topic] = compute_tfidfs(wc_dict[topic], num_words, num_topics, total_topic_word_dict)

    with open(output_file, 'w') as fp:
        json.dump(tfidf_dict, fp, indent=4)

if __name__ == '__main__':
    main()
