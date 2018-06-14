import scrapy
import json
import couchdb
import time
import csv

class transgod(scrapy.Spider):

    name='transgod'


    def start_requests(self):
        
        url = 'https://transgod.cn/v1/translation/atman_batch'

    	yield scrapy.http.FormRequest(
    		url = url
    		, 
    		headers={
    	 	'Host': 'transgod.cn'
    	 	,'Accept': 'application/json, text/javascript, */*; q=0.01'
    	 	,'X-Requested-With': 'XMLHttpRequest'
            ,'Connection': 'keep-alive'
            ,'isapi':'1'
            ,'Origin':'https://transgod.cn'
            ,'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    	 	,'Referer': 'https://transgod.cn/opt/trans?type=file'
            ,'Cookie': 'connect.sid=s%3Aogg1Kv7AJePmTjO1JiNDw6H0om1yO2si.sOQgn0wqDc9ni2l44ZySS5tzN1ZAGzc8vDwcPym6HKI'
            ,'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    	 	},
            formdata={
                '_t': '1527227894751',
                'text': '[{"id":1, "text":"medicine"}]',
                'ls': 'en',
                'lt': 'zh',
                'trans_domain':'medical'
            })
        time.sleep(0.1)

    def parse(self, response):
        data = json.loads(response.text)
    	print data

        # codes_json = '.json'
        # self.db.save(content)
    	# with open(codes_json, 'ab') as f:
    	#  	f.write(json.dumps(content))

        # save json 

    
            