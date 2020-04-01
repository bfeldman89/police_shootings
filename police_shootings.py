# !/usr/bin/env python
"""This module does blah blah."""
import csv
import time
import requests
import tweepy

from common import airtab_homicides_by_cop as airtab, tw, wrap_from_module

wrap_it_up = wrap_from_module(module='police_shootings.py')

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
            i += i
            msg = new['fields']['msg']
            tw.update_status(status=msg)
            try:
                tw.send_direct_message(recipient_id='2163941252', text=msg)
            except tweepy.error.TweepError as err:
                print(err)
    wrap_it_up(t0, new=i, total=len(ms_list), function='wapo_fatal_shootings_by_ms_leos')


def main():
    wapo_fatal_shootings_by_ms_leos()


if __name__ == "__main__":
    main()
