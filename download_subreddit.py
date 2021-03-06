from BeautifulSoup import BeautifulSoup
import requests
import time
from datetime import datetime
import sys
from optparse import OptionParser

# set console options available in the 'options' instance
parser = OptionParser()
parser.add_option("-s", "--start", dest="startdate", default="01/01/00", help="When to begin fetching posts, in a date formatted like 'MM/DD/YY', e.g. '02/24/14'")
parser.add_option("-e", "--end", dest="enddate", default=time.strftime("%m/%d/%y"), help="When to stop fetching posts, either in a date formatted like 'MM/DD/YY', e.g. '02/24/14'")
parser.add_option("-r", "--reddit", dest="subreddit", default="all", help="Simply the subreddit name, without the reddit url or /r/.  Defaults to all")
(options, args) = parser.parse_args()

TOTAL_SUBMISSIONS = 1000 
POSTS_PER_PAGE = 25
TOTAL_PAGES = TOTAL_SUBMISSIONS / POSTS_PER_PAGE
BASE_REDDIT_URL = "http://reddit.com/r/" + options.subreddit + "/new/"
BASE_SEARCH_URL = "http://reddit.com/r/" + options.subreddit + "/search/"
REDDIT_RATE_LIMIT_SECS = 2
USER_AGENT = {'User-agent': 'Mozilla/5.0'}
all_submissions = []

print BASE_REDDIT_URL

# get_page lets you get a specific page in the subreddit's /new/ category
# if you know the count and the after id
def get_page(count, after):
    payload = {'count' : count, 'after' : after}
    return requests.get(BASE_REDDIT_URL, params = payload)

# get_first_page gets the first page in the subreddit /new/ category
def get_first_page():
    return requests.get(BASE_REDDIT_URL, headers = USER_AGENT)

# get_page_from_raw_url gives you a page if you know the raw url of the
# page you're trying to get. Useful if you are getting the url from
# some anchor tag in the html itself.
def get_page_from_raw_url(url):
    return requests.get(url, headers = USER_AGENT)
       
# get_submissions_from_soup returns a list of submissions that 
# have i.imgur.com in them. This is because this script is only
# useful to me atm. However, I will make this more general in 
# the future.
def get_submissions_from_soup(soup_data):
    
    r = []
    for a in soup_data.findAll('a', href=True):
        if 'imgur.com' in a['href']:
            r.append(str(a['href']))
    return r

# get_next_url_from_soup gets the url of the page after the 
# current one.
def get_next_url_from_soup(soup_data):
    for a in soup_data.findAll('a', href=True):
        if 'next' in str(a):
            return str(a['href'])

def get_search_from_to(f, t):
    payload = {'sort':'new',
               #TODO: fix the serch times
               'q' : 'timestamp:{}..{}'.format(f,t),
               'restrict_sr': 'on',
               'syntax': 'cloudsearch'}
    return requests.get(BASE_SEARCH_URL, params=payload, headers=USER_AGENT)
    
# convert the date taken from the options into epoch time    
def convert_date(date):
    return int(time.mktime(time.strptime(date, "%m/%d/%y")))
    

def search_main():
    submission_set = set()
    STEP = 8 * 60 * 60
    START = convert_date(options.startdate)
    END = convert_date(options.enddate)
    
    # print status to console 
    # for count in range(START, END, STEP):
    
    # innacurate information?
    # print "%s minutes left\n" % str((((END - count)/STEP) * 3) / 60)
    # a giant HTML page
    search_result = get_search_from_to(START, END).text
    soup = BeautifulSoup(search_result)
    # let beautiful soup parse out the good imgur links
    submissions = get_submissions_from_soup(soup)
    print submissions
    all_submissions.append(submissions)
    time.sleep(REDDIT_RATE_LIMIT_SECS)
        
    with open('search_submissions.txt', 'w') as f:
            for submission in all_submissions:
                f.write(str(submission) + "\n")
def main():
    first_page = get_first_page().text
    soup = BeautifulSoup(first_page)
    submissions = get_submissions_from_soup(soup)
    
    next_url = get_next_url_from_soup(soup)
    time.sleep(REDDIT_RATE_LIMIT_SECS)
    count = POSTS_PER_PAGE
    try:
        # Runs until it doesn't have a next button. 
        # Not the most elegant way of doing things but it works.
        # TODO: Make this not be a try/except lmaonade. 
        while 1:
            print "Now doing: " + str(count)
            count = count + POSTS_PER_PAGE 
            page = get_page_from_raw_url(next_url).text
            soup = BeautifulSoup(page)
            submissions = get_submissions_from_soup(soup)

            # TODO: Make this for loop go away. 
            for submission in submissions:
                all_submissions.append(submission)

            next_url = get_next_url_from_soup(soup)
            print 'next url: ' + str(next_url)
            time.sleep(REDDIT_RATE_LIMIT_SECS)

    except:
        with open('hot_submissions.txt', 'w') as f:
            for submission in all_submissions:
                f.write(str(submission) + "\n")


if __name__ == "__main__":
    search_main()
