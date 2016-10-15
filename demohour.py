# coding: utf-8

import urllib2
from StringIO import StringIO
from lxml import etree
from lxml.html.soupparser import fromstring

def get_followers(user_id):
    url = "http://www.demohour.com/users/%s/followers" % user_id
    xpath = "//html/body/div[2]/div[1]/div[2]/div[1]/a[2]/strong"
    return get_user_list(url, xpath)

def get_followed(user_id):
    url = "http://www.demohour.com/users/%s/followed" % user_id
    xpath = "/html/body/div[2]/div[1]/div[2]/div[1]/a[1]/strong"
    return get_user_list(url, xpath)

def get_user_list(url, xpath):
    # fetch html file and decode with 'utf-8'
    content = urllib2.urlopen(url).read().decode('utf-8')
    
    # parse html file into a tree and get user table
    root = fromstring(content)
    table = root.xpath('//html/body/div[2]/div[1]/div[1]/div[1]/dl')
    total = int(root.xpath(xpath)[0].text_content())

    user_list = []
    step = 1
    while True:
        step += 1
        for ele in table:
            username = ele.xpath('dt/a[1]')[0].text_content().strip()
            place = ele.xpath('dd[2]/p')[0].text_content().strip()
            time = ele.xpath('dd[2]/p')[0].tail.split(' ')[0].strip()
            data = ele.xpath('dd')[2].text_content().strip().split(' ')
            news = int(data[1])
            followed = int(data[3])
            followers = int(data[5])
            print username, place, time, news, followed, followers
            user_list.append([username, place, time, news, followed, followers])
        if len(user_list) < total:
            content = urllib2.urlopen(url + "?page=%d" % step).read().decode('utf-8')
            root = fromstring(content)
            table = root.xpath('//html/body/div[2]/div[1]/div[1]/div[1]/dl')
        else:
            break
    return user_list


if __name__ == "__main__":
    # user id for 北京东方嘉诚文化发展有限公司. type String.
    user_id = '1627742'

    print("followers:")
    followers_list = get_followers(user_id)
    print("\nfollowed:")
    followed_list = get_followed(user_id)




