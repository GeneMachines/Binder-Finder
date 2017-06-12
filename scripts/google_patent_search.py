import requests
import urllib
import time
import json

access_token =  "AIzaSyA6Ct0AeVgAHnisijHVxVp005shP9lau0I" #<get yours by signing up for google custom search engine api>
cse_id = "004729200286861094334:pr-szpcgj0s" #<get yours by signing up for google custom search engine api>

# Build url                                                                                                              
start=1
search_text = "testosterone"
# &tbm=pts sets you on the patent search                                                                                 
url = 'https://www.googleapis.com/customsearch/v1?key='+access_token+'&cx='+cse_id+'&start='+str(start)+'&num=10&tbm=pts&q='+ urllib.quote(search_text)

response = requests.get(url)

response.json()
f = open('Sample_patent_data'+str(int(time.time()))+'.txt', 'w')
f.write(json.dumps(response.json(), indent=4))
f.close()

for x in response.json().items()[2][1]:
    for y in x["pagemap"]["metatags"]:
        try:
            print (y["citation_patent_number"])
        except:
            print y
