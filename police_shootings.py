# !/usr/bin/env python3
"""This module does blah blah."""
import csv
import json
import time
import requests
import tweepy

from common import airtab_homicides_by_cop as airtab, tw, wrap_from_module

wrap_it_up = wrap_from_module('police_shootings.py')

def wapo_fatal_shootings_by_ms_leos():
    """This function does blah blah."""
    t0, i = time.time(), 0
    ms_list = []
    url = 'https://raw.githubusercontent.com/washingtonpost/data-police-shootings/master/fatal-police-shootings-data.csv'
    with requests.Session() as s:
        r = s.get(url)
        data = r.content.decode('utf-8')
        csv_reader = csv.reader(data.splitlines(), delimiter=',')
        full_list = list(csv_reader)
        for row in full_list:
            if row[9] == "MS":
                ms_list.append(row)
    for row in ms_list:
        this_dict = {}
        this_dict['id'] = row[0]
        this_dict['name'] = row[1]
        this_dict['date'] = row[2]
        this_dict['manner_of_death'] = row[3]
        this_dict['armed'] = row[4]
        this_dict['age'] = row[5]
        this_dict['gender'] = row[6]
        this_dict['race'] = row[7]
        this_dict['city'] = row[8]
        this_dict['state'] = row[9]
        this_dict['signs_of_mental_illness'] = row[10]
        this_dict['threat_level'] = row[11]
        this_dict['flee'] = row[12]
        this_dict['body_camera'] = row[13]
        m = airtab.match('id', this_dict['id'])
        if m:
            airtab.update(m['id'], this_dict, typecast=True)
        else:
            new = airtab.insert(this_dict, typecast=True)
            msg = new['fields']['msg']
            tw.update_status(status=msg)
            try:
                tw.send_direct_message(recipient_id='2163941252', text=msg)
            except tweepy.error.TweepError as err:
                print(err)
            i += i
    wrap_it_up(t0, i, len(ms_list), 'wapo_fatal_shootings_by_ms_leos')


def wapo_fatal_shootings_by_ms_leos_supplement(year):
    """This function does blah blah."""
    url = f'https://s3.amazonaws.com/postgraphics/policeshootings/policeshootings{year}.json'
    r = requests.get(url)
    full_list = json.loads(r.text)
    for x in full_list:
        if x['state'] == "MS":
            this_dict = {}
            record = airtab.match('id', str(x['id']))
            this_dict['blurb'] = x['blurb']
            this_dict['lat'] = str(x['lat'])
            this_dict['lon'] = str(x['lon'])
            this_dict['sources'] = repr(x['sources'])
            this_dict['photos'] = repr(x['photos'])
            this_dict['videos'] = repr(x['videos'])
            airtab.update(record['id'], this_dict, typecast=True)


def main():
    wapo_fatal_shootings_by_ms_leos()
    # wapo_fatal_shootings_by_ms_leos_supplement(2019)


if __name__ == "__main__":
    main()
