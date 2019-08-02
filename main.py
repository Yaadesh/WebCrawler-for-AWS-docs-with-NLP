#!/usr/bin/env python


from collections import deque
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys
from urllib.request import urlopen
from newspaper import Article
import nltk_test2
import bs4

# Read URL from command line
#url = "https://docs.aws.amazon.com/kinesis/index.html#lang/en_us"

print("===================")
print("Page to be crawled:")
print("===================")


# Create queue
queue = deque([])

# Maintains list of visited pages
visited_list = []

#List of blogs which might be useful
blogs = []

#Customer case notes



# Crawl the page and populate the queue with newly found URLs
def crawl(case_notes,url):
    print('crawl')
    visited_list.append(url)
    if len(queue) > 99:
        return

    urlf = urlopen(url)
    #print(urlf.read())
    soup = bs4.BeautifulSoup(urlf.read())
    urls = soup.findAll("a", href=True)

    for url_item in urls:
        flag = 0
        # Complete relative URLs and strip trailing slash
        complete_url = urljoin(url, url_item["href"]).rstrip('/')
        print('url being parsed')
        print(complete_url)

        # Check if the URL already exists in the queue
        for queue_item in queue:
            if queue_item == complete_url:
                flag = 1
                break

        # If not found in queue
        if flag == 0:
            if len(queue) > 99:
                return
            if (visited_list.count(complete_url) == 0 and (("kinesis" in complete_url) or ("streams" in complete_url))):
                try:
                    queue.append(complete_url)
                    blog = Article(complete_url)
                    blog.download()
                    blog.parse()
                    blog.nlp()
                    blog_summary = blog.summary
                    sim_val = nltk_test2.getSimilarity(case_notes,blog_summary)
                    print(sim_val)
                    if(sim_val>0.3):

                        print(complete_url)
                        blogs.append(complete_url)

                except Exception as ex:
                    print (ex)

        
   

    # Pop one URL from the queue from the left side so that it can be crawled
    current = queue.popleft()
    # Recursive call to crawl until the queue is populated with 100 URLs
    crawl(case_notes,current)



#text = "We need some clarification on pricing when using/accessing Kinesis stream from other AWS account for both GET/PUT requests.Please let me know if required additional information."
#crawl(text,"https://docs.aws.amazon.com/streams/latest/dev/introduction.html")

# Print queue
for i in queue:
    print(i)

def invoke_crawler(case_notes,url):
    crawl(case_notes,url)


    print("==============")
    print("Pages crawled:")
    print("==============")

    # Print list of visited pages
    for i in visited_list:
        print(i)
    print("========")
    print("BLOGS")
    print("========")
    #Print list of blogs suitable
    for blog_item in blogs:
        print(blog_item)

    return blogs
