import scrapy
import time
from bs4 import BeautifulSoup as bf
import pandas as pd
from streetcheck.items import Street
from scrapy.exporters import CsvItemExporter
import re
import os
import boto3
from io import StringIO
import pkgutil


class ReadingSpider(scrapy.Spider):
    name = "reading"

    def __init__(self, kw='', pn=10, **kwargs):

        # os.environ['AWS_S3_REGION_NAME'] = 'us-west-2'  # change to your region
        # os.environ['AWS_S3_SIGNATURE_VERSION'] = 's3v4'
        # client = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        #                       aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
        # bucketname = 'scraper-tfw'
        # inputfile = 'reading_postcodes.csv'
        # self.input = client.get_object(Bucket=bucketname, Key=inputfile)[
        #     'Body'].read().decode('utf-8')
        output_file = 'streetcheck/resources/reading_town_streets_2.csv'
        self.exporter = CsvItemExporter(open(output_file, 'w+b'))
        self.exporter.start_exporting()
        pass

    def start_requests(self):
        codes_data = pkgutil.get_data(
            "streetcheck", "resources/reading_town_postcodes_2.csv")
        # print('codes_data',codes_data)
        codes_df = pd.read_csv(StringIO(codes_data.decode('utf-8')))
        pcodes = codes_df['postcode'].to_list()
        # pcodes = ['rg20lw']
        urls = [
            'https://www.streetcheck.co.uk/postcode/' +
            str(pcode) for pcode in pcodes
        ]
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

        for url in urls:
            # time.sleep(0.1)
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        street = Street()
        postcode = response.url.split("/")[-1]
        street['street_code'] = postcode
        print(response.url)
        soup = bf(response.text, 'lxml')

        culture_table = soup.find(id='culture').find("table")
        total_ethics = float(culture_table.find('tfoot').find(
            'tr').find_all('td')[1].text.strip())
        for row in culture_table.find('tbody').find_all('tr'):
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            if cols[0] == 'Chinese':
                street['cn_count'] = cols[1]
                street['cn_rate'] = round(float(cols[1])/total_ethics, 3)

            if cols[0] == 'White':
                street['white_rate'] = round(float(cols[1])/total_ethics, 3)
                # self.exporter.export_item(street)

        people_table = soup.find(id='people').find('table')
        total_people = float(people_table.find('tfoot').find(
            'tr').find_all('td')[1].text.strip())
        ab_people = float(people_table.find(
            'td', {"data-chart-title": "AB"})
            .parent
            .findAll('td')[1].text.strip())
        street['ab_people_rate'] = round(ab_people/total_people, 3)

        employ_table = soup.find(id='employment').find('table')
        total_economic = float(employ_table.find('tfoot').find(
            'tr').find_all('td')[1].text.strip())
        fe_people = float(employ_table.find('tbody')
                          .find_all('tr')[0].find_all('td')[1].text.strip())
        street['fulltime_rate'] = round(fe_people/total_economic, 3)
        # ab_people = ab_people_title.nextSibling.text.strip()
        # print(float(ab_people))
        print(street)
        self.exporter.export_item(street)
        yield street
