from pprint import pprint
from unidecode import unidecode
from nltk.corpus import stopwords
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, helpers, RequestsHttpConnection
import requests, json, datetime, traceback, boto3
import nltk

class ElasticsearchIndex:
    def __init__(self, host, index_name, type_name, region='us-east-1'):
        service = 'es'
        credentials = boto3.Session().get_credentials()
        awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
        self.host = host
        self.es = Elasticsearch(hosts=[{'host': host, 'port': 443}],http_auth=awsauth, use_ssl=True, verify_certs=True, connection_class=RequestsHttpConnection)
        self.s = requests.Session()
        a = requests.adapters.HTTPAdapter(max_retries=3)
        self.s.mount('http://', a)

        self.index_name = index_name
        self.type_name = type_name
        self.query_url = host + '/' + self.index_name + '/' + self.type_name + '/' + '_search?scroll=2m&size=5000'
        self.stop_words = set(stopwords.words('english'))

    def query_es(self, query, number_of_hits=100, lucene=False, news=False):
        service = 'es'
        credentials = boto3.Session().get_credentials()
        awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, 'us-east-1', service, session_token=credentials.token)
        self.es = Elasticsearch(hosts=[{'host': self.host, 'port': 443}], http_auth=awsauth, use_ssl=True, verify_certs=True, connection_class=RequestsHttpConnection)
        if lucene:
            response_query = self.es.search(index=self.index_name, q=query)
        else:
            response_query = self.es.search(index=self.index_name, body=query)
        results = []
        if 'hits' not in response_query:
            # print('no hits')
            return results
        if 'hits' not in response_query['hits']:
            # print('0 hits', query)
            return results
        if news:
            return [(response['_source'], response['_score']) for response in response_query['hits']['hits'][:number_of_hits]]
        else:
            return response_query['hits']['hits'][:number_of_hits]

    def get_number_of_hits(self, query, lucene=False):
        if lucene:
            response_query = self.es.search(index=self.index_name, q=query)
        else:
            response_query = self.es.search(index=self.index_name, body=query)
        try:
            response_query = json.loads(response_query.content)
        except Exception:
            # print(response_query)
            traceback.print_exc()
        if 'hits' not in response_query:
            # print('no hits')
            return 0
        if 'hits' not in response_query['hits']:
            # print('0 hits', query)
            return 0
        return response_query['hits']['total']

    def update_in_es(self, _id, _source):
        actions = [{"_index": self.index_name, "_type": self.type_name, "_id": _id, "_source": _source}]
        helpers.bulk(self.es, actions, request_timeout=10)

    def send_update_actions_to_elasticsearch(self, index_name, type_name, results):
        actions = []
        for j in range(0, len(results)):
            results[j]["_source"]["vocabularized"] = True
            action = {
                "_index": index_name,
                "_type": type_name,
                "_id": results[j]["_id"],
                "_source": results[j]["_source"]
            }
            actions.append(action)
        helpers.bulk(self.es, actions)

    def get_lucene_query(self, start_date, entity):
        query = f"publishedAt: [{start_date} TO *] AND (description: {entity} OR body: {entity})"
        return query



class NewsIndex(ElasticsearchIndex):
    """This class helps you interact with the news articles in Elasticsearch.
    Mainly this is so that you can save specific queries."""
    def __init__(self):
        es_url = "search-emora-r5tuqwbkxj54xnkxdf674utbqu.us-east-1.es.amazonaws.com"
        index = 'news_index'
        subindex = '_doc'
        ElasticsearchIndex.__init__(self, es_url, index, subindex)
        self.forbidden_sources = ['espn cric info', 'associated press', 'the huffington post', 'the-washington-post']
        # self.es_streamer = ElasticsearchStreamer(es_url, index, subindex)

    def get_articles_for_query_today(self, query, query_type='entity'):
        yesterday = datetime.datetime.today() + datetime.timedelta(days=-3)
        start_date = datetime.datetime.strftime(yesterday, '%Y-%m-%d')
        if query_type == 'entity':
            # print('ENTITY QUERY')
            query = f"publishedAt:[{start_date} TO *] AND (description:\"{query}\" OR body:\"{query}\")"

        if query_type == 'category':
            # print('CATEGORY QUERY')
            query = f"publishedAt:[{start_date} TO *] AND category:\"{query}\""
        # if query_type == 'words':
        #     query = f"publishedAt:[{start_date} TO *] AND (title:\"{query}\" OR body:\"{query}\")"
        if len(self.forbidden_sources):
            query += " AND NOT("
            query += ' OR '.join([f"source:\"{source}\"" for source in self.forbidden_sources])
            query += ")"
        # query += " AND ("
        # query += ' OR '.join(["source:\"washington post\""])
        # query += ")"
        # print(query)
        return self.process_results(sorted(self.query_es(query, lucene=True, news=True), key=lambda x: x[0]['publishedAt'], reverse=True))

        # results = sorted(self.query_es(bool_query, lucene=False, news=True), key=lambda x: x[0]['publishedAt'], reverse=True)
        # results = self.query_es(query, lucene=True)
        # return self.process_results(results)

    def get_articles_for_list_of_words(self, words):
        yesterday = datetime.datetime.today() + datetime.timedelta(days=-3)
        start_date = datetime.datetime.strftime(yesterday, '%Y-%m-%d')
        query = f"publishedAt:[{start_date} TO *]"
        # print('WORDS QUERY')
        if len(words):
            query += " AND ("
            query += ' OR '.join([f"description:\"{word}\" OR body:\"{word}\" " for word in words])
            query += ")"

        if len(self.forbidden_sources):
            query += " AND NOT("
            query += ' OR '.join([f"source:\"{source}\"" for source in self.forbidden_sources])
            query += ")"
        # query += " AND ("
        # query += ' OR '.join(["source:\"washington post\""])
        # query += ")"
        # print(query)
        return self.process_results(sorted(self.query_es(query, lucene=True, news=True), key=lambda x: x[0]['publishedAt'], reverse=True))

    def process_results(self, results_pool):
        final_results = list()
        result_titles = list()
        for i, hit in enumerate(results_pool):
            if 'T' not in hit[0]['publishedAt'] or unidecode(hit[0]["title"]) in result_titles:
                # print('skipping news')
                continue
            if not hit[0]['description']:
                if hit[0]['body']:
                    hit[0]['description'] = hit[0]['body']
                else:
                    continue
            if len(hit[0]['description']) < 160 or '...' in hit[0]['description']:
                continue
            final_dict = {
                'id': hit[0]['id'],
                'description': unidecode(hit[0]['description']),
                'category': str(unidecode(hit[0]['category'])).replace("-", " ").lower(),
                'source': str(unidecode(hit[0]['source'])).replace("-", " "),
                'speakable_date': datetime.datetime.strptime(hit[0]['publishedAt'].split('T')[0], '%Y-%m-%d').strftime('%B %d'),  # 2018-05-24T06:02:00Z '%Y-%m-%dT%H:%M:%SZ'
                # 'speakable_date': datetime.strftime(datetime.strptime(hit[0]['publishedAt'].split('T')[0], '%Y-%m-%d'), '%B %d'),  # 2018-05-24T06:02:00Z '%Y-%m-%dT%H:%M:%SZ'
                'actual_date': datetime.datetime.strptime(hit[0]['publishedAt'].split('T')[0], '%Y-%m-%d').strftime('%Y%m%d')
            }
            final_results.append((final_dict, hit[1]))
            result_titles.append(unidecode(hit[0]["title"]))
            if len(result_titles) == 20:
                break
        return final_results


