from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.http import Request, FormRequest
import re
import json
import datetime
import csv
import requests
import MySQLdb
class GithubBrowse(BaseSpider):

    name = 'github_browse'
    handle_httpstatus_list = [400, 403]

    def __init__(self):
	self.conn = MySQLdb.connect(db='Github',user='root',passwd='root', charset="utf8",host='localhost',use_unicode=True)
	self.cur = self.conn.cursor()
	self.query1 = 'insert into profile_meta(id, first_name, last_name, username, summary, location, following, followers, repositories, stars, reference_url, created_at, modified_at) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now()) on duplicate key update modified_at=now()'
        self.query2 = 'insert into repositories(id, profile_id, name, description, type, stargazers, network, modified_at, created_at) values(%s, %s, %s, %s, %s, %s, %s, now(), now()) on duplicate key update modified_at=now()'
	self.query3 = 'update profile_meta set organization=%s where id=%s'
	self.access_token = 'ddce1a94a73af531be2bbcd0ab17fa43405c5041'

    def start_requests(self):
	with open('github_input.txt', 'r') as f:
            rows = f.readlines()
        for row in rows:
            row = row.replace('\n', '')
	    url = 'https://api.github.com/users/%s'%row.split('/')[-1]
	    yield Request(url, callback=self.parse)

    def parse(self, response):
	text = json.loads(response.body)
	if text:
	    resp = text.get('public_repos', '')
	    stars = ''
	    following = text.get('following', '')
	    followers = text.get('followers', '')
	    name = text.get('name', '')
	    try:
		f_name, l_name = name.split(' ')
	    except:
		f_name = name
		l_name = ''
	    username = text.get('login', '')
	    summary = text.get('bio', '')
	    if not summary:
		summary = ''
	    location = text.get('location', '')
	    url = text.get('html_url', '')
	    id_ = text.get('id', '')
	    values = (id_, f_name, l_name, username, summary, location, following, followers, resp, '', url)
	    self.cur.execute(self.query1, values)
	    self.conn.commit()
	    org_link = text.get('organizations_url', '')
	    yield Request(org_link, self.parse_org, meta={'sk':id_})
	    data = '{"query":"query{repositoryOwner(login: \\"%s\\"){... on User{pinnedRepositories(first: 6){edges{node{name id forkCount description primaryLanguage{name} stargazers{totalCount}}}}}}}"}'%username.encode('utf8')
	    link = 'https://api.github.com/graphql?access_token=%s'%self.access_token
	    yield Request(link, self.parse_repos, meta={'sk':id_}, body=data, method="POST")

    def parse_repos(self, response):
	resp = json.loads(response.body)
	sk = response.meta['sk']
	try:
	    edges = resp = resp['data']['repositoryOwner']['pinnedRepositories']['edges']
	except:
	    edges = []
	for edge in edges:
	    edge = edge['node']
	    r_name = edge['name']
	    r_desc = edge['description']
	    if not r_desc:
		r_desc = ''
	    typ = edge.get('primaryLanguage', '')
	    if typ:
		type_ = typ.get('name', '')
	    else:
		type_ = ''
	    stargazer = edge.get('stargazers', '')
	    if stargazer:
		stargazers = stargazer.get('totalCount', '')
	    else:
		stargazers = ''
	    network = edge['forkCount']
	    id_ = edge['id']
	    values = (id_, sk, r_name, r_desc, type_, stargazers, network)
	    self.cur.execute(self.query2, values)
	    self.conn.commit()
		
    def parse_org(self, response):
	sk = response.meta['sk']
	orgs = json.loads(response.body)
	organization = ''
	if orgs:
	    for org in orgs:
		org = org['login']
		organization = '%s<>%s'%(organization, org)
	organization = organization.strip('<>')
	values = (organization, sk)
	self.cur.execute(self.query3, values)
	self.conn.commit()

