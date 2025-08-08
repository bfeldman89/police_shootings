#!/usr/bin/env /python
"""This module provides a function for shipping logs to Airtable."""
import os
import time
from pyairtable import Api
import cloudinary
from documentcloud import DocumentCloud
import tweepy

api = Api(os.environ['AIRTABLE_PAT'])

airtab_homicides_by_cop = api.table(os.environ['police_violence_db'], 'wapo')

airtab_tweets = api.table(os.environ['botfeldman89_db'],
                         'scheduled_tweets')
airtab_log = api.table(os.environ['log_db'],
                      'log')

auth = tweepy.OAuthHandler(os.environ['TWITTER_APP_KEY'], os.environ['TWITTER_APP_SECRET'])
auth.set_access_token(os.environ['TWITTER_OAUTH_TOKEN'], os.environ['TWITTER_OAUTH_TOKEN_SECRET'])
tw = tweepy.API(auth)

cloudinary.config(cloud_name='bfeldman89',
                  api_key=os.environ['CLOUDINARY_API_KEY'],
                  api_secret=os.environ['CLOUDINARY_API_SECRET'])

dc = DocumentCloud(username=os.environ['MUCKROCK_USERNAME'],
                   password=os.environ['MUCKROCK_PW'])

muh_headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}



my_funcs = {'wapo_fatal_shootings_by_ms_leos': 'recnCumWo19foxa3C'}

def wrap_from_module(module):
    def wrap_it_up(t0, new=None, total=None, function=None):
        this_dict = {
            'module': module,
            'function': function,
            '_function': my_funcs[function],
            'duration': round(time.time() - t0, 2),
            'total': total,
            'new': new
        }
        airtab_log.insert(this_dict, typecast=True)

    return wrap_it_up
