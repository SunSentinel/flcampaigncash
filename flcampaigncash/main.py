#!/usr/bin/python
import os
import requests
import csv
import sys
import json
import re
from datetime import datetime



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

election = '20181106-GEN'
office = 'GOV'
committee = ''
party = 'All'
date = datetime.now().strftime('%Y%m%d')

def main():

    CONTRIB_URL = "http://dos.elections.myflorida.com/cgi-bin/contrib.exe"
    payload = {
        'election':election,
        'search_on': 1,
        'CanFName': '',
        'CanLName': '',
        'CanNameSrch': 2,
        'office':office,
        'cdistrict':'',
        'cgroup':'',
        'party':party,
        'ComName': committee,
        'ComNameSrch': 2,
        'committee': 'All',
        'cfname':'',
        'clname':'',
        'namesearch': 2,
        'ccity':'',
        'cstate':'',
        'czipcode':'',
        'coccupation':'',
        'cdollar_minimum':'',
        'cdollar_maximum':'',
        'rowlimit':'',
        'csort1': 'NAM',
        'csort2': 'CAN',
        'queryformat': 2 # TSV download, instead of returning an html page.
    }

    get_records(CONTRIB_URL, payload)


def get_records(url, parameters):

    r = requests.get(url, params=parameters, allow_redirects=True)

    if r.status_code == 200:
        print("Checking url: " + r.url)
        print("\nURL works. Fetching the data...")
        results = r.content
        file_path = BASE_DIR + '/data/source/{0}_contributions.tsv'.format(office)
        with open(file_path, 'wb') as txtfile:
            txtfile.write(results)

        print("Data pulled. Cleaning it up now.")
        clean_data(file_path)

    else:
        print("=============\nERROR: URL did not work.\n=============")


def clean_data(file_path):

    # Cleaning utilities.
    def get_name(text):
        name = re.sub(r'\([^)]*\)', '', text)
        return name.strip()

    def get_party(text):
        if "(DEM)" in text:
            return "Democrat"
        elif "(REP)" in text:
            return "Republican"
        else:
            return "Other"

    data = csv.DictReader(open(file_path, encoding='ISO-8859-1'), delimiter='\t', quoting=csv.QUOTE_NONE)
    clean_data = []

    for contrib in data:
        cleaned_contrib = {}
        cleaned_contrib['candidate'] = get_name(contrib['Candidate/Committee'])
        cleaned_contrib['candidate_party'] = get_party(contrib['Candidate/Committee'])
        cleaned_contrib['office'] = office
        cleaned_contrib['date'] = contrib['Date']
        cleaned_contrib['amount'] = contrib['Amount']
        cleaned_contrib['type'] = contrib['Typ']
        cleaned_contrib['contributor_name'] = contrib['Contributor Name']
        cleaned_contrib['contributor_address'] = contrib['Address']
        cleaned_contrib['contributor_address2'] = contrib['City State Zip']
        cleaned_contrib['contributor_occupation'] = contrib['Occupation']
        cleaned_contrib['inkind_description'] = contrib['Inkind Desc']
        clean_data.append(cleaned_contrib)

    print("Saving data locally.")
    write_to_file(clean_data)


def write_to_file(data):
    """
    Save cleaned data to local files.
    """
    # First to json.
    json_file_path = 'data/processed/{0}_{1}_contributions.json'.format(date, office)
    json_file = open(json_file_path, 'w')
    out = json.dumps(data)
    json_file.write(out)

    # And then to CSV.
    keys = data[0].keys()
    csvfile = 'data/processed/{0}_{1}_contributions.csv'.format(date, office)
    with open(csvfile, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


if __name__ == '__main__':
    main()
    print("\nDone!\n")
