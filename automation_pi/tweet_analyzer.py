#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Usage:
# python tweets_analyzer.py -n screen_name
#
# Install:
# pip install tweepy ascii_graph tqdm numpy

from __future__ import unicode_literals
import md5
from tqdm import tqdm
import tweepy
import numpy
import argparse
import collections
import datetime
import MySQLdb
import time
from table_schemas.generic_functions import *
from table_schemas.pi_db_operations import *
from twitter_get_crawl import *

con, cur = get_mysql_connection(DB_HOST, DB_NAME_REQ, '')

__version__ = '0.1-test'

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

#from twitter_constants import consumer_key, consumer_secret, access_token, access_token_secret


parser = argparse.ArgumentParser(description=
    "Twitter Handle Analyzer version %s" % __version__,
                                 usage='%(prog)s -n <screen_name> [options]')
parser.add_argument('-l', '--limit', metavar='N', type=int, default=1000,
                    help='limit the number of tweets to retreive (default=1000)')
parser.add_argument('-n', '--name', required=True, metavar='screen_name',
                    help='target screen_name')

parser.add_argument('-e', '--email', default='', metavar='emailid',help='target emailid')


parser.add_argument('-f', '--filter', help='filter by source (ex. -f android will get android tweets only)')

parser.add_argument('--no-timezone', action='store_true',
                    help='removes the timezone auto-adjustment (default is UTC)')

parser.add_argument('--utc-offset', type=int,
                    help='manually apply a timezone offset (in seconds)')

parser.add_argument('--friends', action='store_true',
                    help='will perform quick friends analysis based on lang and timezone (rate limit = 15 requests)')

args = parser.parse_args()

# Here are globals used to store data 
start_date = 0
end_date = 0

activity_hourly = {
    ("%2i:00" % i).replace(" ", "0"): 0 for i in range(24)
}

activity_weekly = {
    "%i" % i: 0 for i in range(7)
}


detected_langs = collections.Counter()
detected_sources = collections.Counter()
detected_places = collections.Counter()
geo_enabled_tweets = 0 
detected_hashtags = collections.Counter()
detected_domains = collections.Counter()
detected_timezones = collections.Counter()
retweets = 0 
retweeted_users = collections.Counter()
mentioned_users = collections.Counter()
id_screen_names = {}
friends_timezone = collections.Counter()
friends_lang = collections.Counter()


def process_tweet(tweet):
    """ Processing a single Tweet and updating our datasets """
    global start_date
    global end_date
    global geo_enabled_tweets
    global retweets


    # Check for filters before processing any further
    #print tweet.text

    if args.filter and tweet.source:
        if not args.filter.lower() in tweet.source.lower():
            return

    tw_date = tweet.created_at

    # Updating most recent tweet
    end_date = end_date or tw_date
    start_date = tw_date

    # Handling retweets
    try:
        # We use id to get unique accounts (screen_name can be changed)
        rt_id_user = tweet.retweeted_status.user.id_str
        retweeted_users[rt_id_user] += 1

        if tweet.retweeted_status.user.screen_name not in id_screen_names:
            id_screen_names[rt_id_user] = "@%s" % tweet.retweeted_status.user.screen_name

        retweets += 1
    except:
        pass

    # Adding timezone from profile offset to set to local hours
    if tweet.user.utc_offset and not args.no_timezone:
        tw_date = (tweet.created_at + datetime.timedelta(seconds=tweet.user.utc_offset))

    if args.utc_offset:
        tw_date = (tweet.created_at + datetime.timedelta(seconds=args.utc_offset))

    # Updating our activity datasets (distribution maps)
    activity_hourly["%s:00" % str(tw_date.hour).zfill(2)] += 1
    activity_weekly[str(tw_date.weekday())] += 1

    # Updating langs
    detected_langs[tweet.lang] += 1

    # Updating sources
    detected_sources[tweet.source] += 1

    # Detecting geolocation
    if tweet.place:
        geo_enabled_tweets += 1
        tweet.place.name = tweet.place.name
        detected_places[tweet.place.name] += 1

    # Updating hashtags list
    if tweet.entities['hashtags']:
        for ht in tweet.entities['hashtags']:
            ht['text'] = "#%s" % ht['text']
            detected_hashtags[ht['text']] += 1

    # Updating domains list
    if tweet.entities['urls']:
        for url in tweet.entities['urls']:
            domain = urlparse(url['expanded_url']).netloc
            if domain != "twitter.com":  # removing twitter.com from domains (not very relevant)
                detected_domains[domain] += 1

    # Updating mentioned users list
    if tweet.entities['user_mentions']:
        for ht in tweet.entities['user_mentions']:
            mentioned_users[ht['id_str']] += 1
            if not ht['screen_name'] in id_screen_names:
                id_screen_names[ht['id_str']] = "@%s" % ht['screen_name']


def process_friend(friend):
    """ Process a single friend """
    friends_lang[friend.lang] += 1 # Getting friend language & timezone
    if friend.time_zone:
        friends_timezone[friend.time_zone] += 1


def get_friends(api, username, limit):
    """ Download friends and process them """
    for friend in tqdm(tweepy.Cursor(api.friends, screen_name=username).items(limit), unit="friends", total=limit):
        process_friend(friend)


def get_tweets(api, username, limit):
    """ Download Tweets from username account """
    for status in tqdm(tweepy.Cursor(api.user_timeline, screen_name=username).items(limit),
                       unit="tw", total=limit):
        process_tweet(status)
	

def int_to_weekday(day):
    weekdays = "Monday Tuesday Wednesday Thursday Friday Saturday Sunday".split()
    return weekdays[int(day) % len(weekdays)]


def print_stats(dataset, top=5):
    """ Displays top values by order """
    final_dict = {}
    sum = numpy.sum(list(dataset.values()))
    i = 0
    if sum:
        sorted_keys = sorted(dataset, key=dataset.get, reverse=True)
        max_len_key = max([len(x) for x in sorted_keys][:top])  # use to adjust column width
        for k in sorted_keys:
            value = dataset[k]
            final_dict.update({k:value})
            try:
                print(("- \033[1m{:<%d}\033[0m {:>6} {:<4}" % max_len_key)
                      .format(k, dataset[k], "(%d%%)" % ((float(dataset[k]) / sum) * 100)))
            except:
                pass
            i += 1
            if i >= top:
                break
        return  final_dict
    else:
        print("No data")
        return final_dict
    print("")



def main():

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    twitter_api = tweepy.API(auth)
    avg_tweets_per_day = ''
    #import pdb;pdb.set_trace()
    #Getting general account's metadata
    args_name = name = args.name
    user_info = ''
    screen_url = "https://twitter.com/%s"%(args_name)
    print("[+] Getting @%s account data..." % args_name)
    try : 
        user_info = twitter_api.get_user(screen_name=args_name)
    except :
        pass
    time.sleep(3)
    print("[+] lang           : \033[1m%s\033[0m" % user_info.lang)
    print("[+] geo_enabled    : \033[1m%s\033[0m" % user_info.geo_enabled)
    print("[+] time_zone      : \033[1m%s\033[0m" % user_info.time_zone)
    print("[+] utc_offset     : \033[1m%s\033[0m" % user_info.utc_offset)
    #import pdb;pdb.set_trace()
    lang =  user_info.lang
    if user_info.utc_offset is None:
        print("[\033[91m!\033[0m] Can't get specific timezone for this user")

    if args.utc_offset:
        print("[\033[91m!\033[0m] Applying timezone offset %d (--utc-offset)" % args.utc_offset)

    print("[+] statuses_count : \033[1m%s\033[0m" % user_info.statuses_count)
    tweets = user_info.statuses_count
    description = user_info.description
    location = user_info.location
    following = user_info.friends_count
    followers = user_info.followers_count
    likes = user_info.favourites_count
    image = user_info.profile_image_url
    #import pdb;pdb.set_trace()
    listed_count = user_info.listed_count
    timezone = user_info.time_zone
    verified = user_info.verified
    name = user_info.name
    # Will retreive all Tweets from account (or max limit)
    num_tweets = numpy.amin([args.limit, user_info.statuses_count])
    print("[+] Retrieving last %d tweets..." % num_tweets)
    # Download tweets
    try :  get_tweets(twitter_api, args_name, limit=num_tweets)
    except : 
        print screen_url,"401 status"
    try:
        print("[+] Downloaded %d tweets from %s to %s (%d days)" % (num_tweets, start_date, end_date, (end_date - start_date).days))
    except: 
        file("twittererror","ab+").write("%s\n" %args_name)

    # Checking if we have enough data (considering it's good to have at least 30 days of data)
    try :
        if (end_date - start_date).days < 30 and (num_tweets < user_info.statuses_count):
            print("[\033[91m!\033[0m] Looks like we do not have enough tweets from user, you should consider retrying (--limit)")
    except :  print("[\033[91m!\033[0m] Looks like we do not have enough tweets from user, you should consider retrying (--limit)")

    try : 
        if (end_date - start_date).days != 0:
        
            tweets_per_day = (num_tweets / float((end_date - start_date).days))
            avg_tweets_per_day  = round(tweets_per_day,1)
        print("[+] Average number of tweets per day: \033[1m%.1f\033[0m" % (num_tweets / float((end_date - start_date).days)))
    except :  
        print 'no data'
        avg_tweets_per_day = ''
    print("[+] Detected languages (top 5)")
    detected_lan =  print_stats(detected_langs)
    print("[+] Detected sources (top 10)")
    detected_so = print_stats(detected_sources, top=10)
    print("[+] There are \033[1m%d\033[0m geo enabled tweet(s)" % geo_enabled_tweets)
    if len(detected_places) != 0:
        print("[+] Detected places (top 10)")
        detected_plac = print_stats(detected_places, top=10)

    print("[+] Top 10 hashtags")
    detected_hash = print_stats(detected_hashtags, top=10)
    try : 
        print("[+] @%s did \033[1m%d\033[0m RTs out of %d tweets (%.1f%%)" % (args_name, retweets, num_tweets, (float(retweets) * 100 / num_tweets)))
        no_of_RTs = "@%s did \033[1m%d\033[0m RTs out of %d tweets (%.1f%%)" % (args_name, retweets, num_tweets, (float(retweets) * 100 /num_tweets))
    except : no_of_RTs ='' 
    # Converting users id to screen_names
    retweeted_users_names = {}
    for k in retweeted_users.keys():
        retweeted_users_names[id_screen_names[k]] = retweeted_users[k]
    print("[+] Top 5 most retweeted users")
    retweeted_use = print_stats(retweeted_users_names, top=5)
    mentioned_users_names = {}
    for k in mentioned_users.keys():
        mentioned_users_names[id_screen_names[k]] = mentioned_users[k]
    print("[+] Top 5 most mentioned users")
    mentioned_us = print_stats(mentioned_users_names, top=5)

    print("[+] Most referenced domains (from URLs)")
    detected_dom = print_stats(detected_domains, top=6)

    if args.friends:
        max_friends = numpy.amin([user_info.friends_count, 300])
        print("[+] Getting %d @%s's friends data..." % (max_friends, args_name))
        try:
            get_friends(twitter_api, args_name, limit=max_friends)
        except tweepy.error.TweepError as e:
            if e[0][0]['code'] == 88:
                print("[\033[91m!\033[0m] Rate limit exceeded to get friends data, you should retry in 15 minutes")
            raise

        print("[+] Friends languages")
        friends_lan = print_stats(friends_lang, top=6)


        print("[+] Friends timezones")
        print_stats(friends_timezone, top=8)

    list_,detected_sou,detected_las,mentioned_user_name,\
    detected_has,ret_user= [],[],[],[],[],[]
    for i,j in zip(detected_dom.keys(),detected_dom.values()):
       if j and i :
            i = normalize(i)
            try : data = str(i)+'{'+str(j)+'}'
            except Exception as e:print e
            list_.append(data)
    detected_domain = '<>'.join(list_)
    for k,i in zip(detected_lan.keys(),detected_lan.values()):
        if k and i:
            k = normalize(k)
            try : data = str(k)+'{'+str(i)+'}'
            except Exception as e:print e
            detected_las.append(data)
    detected_las = '<>'.join(detected_las)
    for k,i in zip(detected_so.keys(),detected_so.values()):
        if k and i :
            k = normalize(k)
            try : data = str(k)+'{'+str(i)+'}'
            except Exception as e:print e
            detected_sou.append(data)
    detected_sou = '<>'.join(detected_sou)
    for k,i in zip(mentioned_us.keys(),mentioned_us.values()):
        if k and i :
            k = normalize(k)
            try : data = str(k.encode('utf-8'))+'{'+str(i)+'}'
            except Exception as e:print e 
            mentioned_user_name.append(data)
    mentioned_user_name = '<>'.join(mentioned_user_name)
    for k,i in zip(detected_hash.keys(),detected_hash.values()):
        if k and i:
            k = normalize(k)
            try : data = str(k)+'{'+str(i)+'}'
            except Exception as e:print e
            detected_has.append(data)
    detected_has = '<>'.join(detected_has)
    for k,i in zip(retweeted_use.keys(),retweeted_use.values()):

        if k and i:
            k = normalize(k)
            try : data = str(k)+'{'+str(i)+'}'
            except Exception as e:print e
            ret_user.append(data)
    import md5
    if args.email=='None':args.email=''
    ret_user = '<>'.join(ret_user)
    sk = md5.md5(screen_url).hexdigest()
    '''vals = (sk,args.name,name,normalize(description),location,tweets,following,followers,\
           likes,image,listed_count,timezone,lang,verified,screen_url,args.email,'',\
           detected_has,mentioned_user_name,no_of_RTs,ret_user,detected_domain,\
           detected_sou,detected_las,avg_tweets_per_day)'''
    vals = (sk,args.name,normalize(name),normalize(description),location,tweets,following,followers,\
	    likes,image,listed_count,timezone,lang,verified,screen_url,args.email,'',\
	    detected_has,mentioned_user_name,no_of_RTs,ret_user,detected_domain,\
	    detected_sou,detected_las,avg_tweets_per_day,\
	    sk,args.name,normalize(name),normalize(description),location,tweets,following,followers,\
	    likes,image,listed_count,timezone,lang,verified,normalize(screen_url),args.email,'',\
	    detected_has,mentioned_user_name,no_of_RTs,ret_user,detected_domain,\
	    detected_sou,detected_las,avg_tweets_per_day)
    print vals
 	

    screen_name = args.name
    cur.execute(twitter_qry,vals)
    #import pdb;pdb.set_trace()
    #cur.execute(twitter_update_qry % screen_name)
    Login().update_status(screen_name, 1, 'twitter_crawl', twitter_update_qry)
    con.commit()
    #con.close()

if __name__ == '__main__':
    try:
        main()
    except tweepy.error.TweepError as e:
        print("[\033[91m!\033[0m] Twitter error: %s" % e)
    except Exception as e:
        print("[\033[91m!\033[0m] Error: %s" % e)
