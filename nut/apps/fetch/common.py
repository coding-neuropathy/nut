#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import sys

from bs4 import BeautifulSoup


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_judy'
import random
import redis
import requests
import time
import re, datetime, pytz
import lxml


from django.conf import settings
from django.utils.baseconv import base64
from settings import WEIXIN_COOKIE
from Crypto.Cipher import AES


_RE_WEIBO = re.compile(ur'\d{1,2}')
_COVER_RE = re.compile(r'cover = "(http://.+)";')
_COOKIE_RE = re.compile(r'(ABTEST=\S+?|SNUID=\S+?|IPLOC=\S+?|SUID=\S+?|black_passportid=\S+?);')

r = redis.Redis(host=settings.CONFIG_REDIS_HOST,
                port=settings.CONFIG_REDIS_PORT,
                db=settings.CONFIG_REDIS_DB)


def parse_article_link(result_json):
    article_link_list = []
    for article in result_json['items']:
        article = clean_xml(article)
        article_soup = BeautifulSoup(article, 'xml')
        print '        * ', article_soup.title1.string
        article_link_list.append('http://weixin.sogou.com'+article_soup.url.string)
    return article_link_list


def clean_xml(xml_str):
    xml_str = xml_str.rstrip('\n')
    replaces = (
        ('<?xml version="1.0" encoding="gbk"?>',
         '<xml version="1.0" encoding="gbk">'),
        ('\\', ''),)

    for from_str, to_str in replaces:
        xml_str = xml_str.replace(from_str, to_str)

    if not xml_str.endswith('</xml>'):
        xml_str += '</xml>'

    return xml_str


def process_jsonp(r):
    j = r[r.find('{'):r.rfind('}')+1]
    items = json.loads(j)['items']
    l = []
    for item in items:
        root = lxml.etree.fromstring(item.replace(u'encoding="gbk"', ''))
        d = {}
        d['title'] = root.xpath('//title/text()')[0]
        d['link'] = root.xpath('//url/text()')[0]
        d['author'] = root.xpath('//sourcename/text()')[0]
        d['created'] = we_chat_date(root.xpath('//lastModified/text()')[0])
        d['guid'] = root.xpath('//docid/text()')[0]
        l.append(d)
    return l


def we_chat_date(timestamp):
    return datetime.datetime.utcfromtimestamp(int(timestamp)) \
        .replace(tzinfo=pytz.utc).astimezone(time.timezone) \
        .strftime("%a, %d %b %Y %H:%M:%S %z")


def process_content(html):
    root = lxml.html.fromstring(html)

    # 抽取封面cover图片
    script = root.xpath('//*[@id="media"]/script/text()')
    cover = None
    if script:
        l = _COVER_RE.findall(script[0])
        if l:
            cover = l[0]

    # 抽取文章内容
    try:
        content = root.xpath('//*[@id="js_content"]')[0]
    except IndexError:
        return ''

    # 处理图片链接
    for img in content.xpath('.//img'):
        if not 'src' in img.attrib:
            img.attrib['src'] = img.attrib.get('data-src', '')

    # 生成封面
    if cover:
        coverelement = lxml.etree.Element('img')
        coverelement.set('src', cover)
        content.insert(0, coverelement)

    return lxml.html.tostring(content, encoding='unicode')


def _cipher_eqs(key, secret, setting='sogou'):
    """
    SogouEncrypt.encryptquery
    """
    assert len(key) == 11

    ss = setting.split('-')

    # function g
    if len(ss) > 2:
        h = ss[2]
    else:
        h = ss[0]

    # function f
    if len(h) > 5:
        n = h[:5]
    else:
        n = h + (5 - len(h)) * 's'

    key += n

    data = secret + 'hdq=' + setting
    # padding data
    length = 16 - (len(data) % 16)
    data += chr(length) * length

    IV = b'0000000000000000'
    cipher = AES.new(_to_bytes(key), AES.MODE_CBC, IV)
    # encrypt data
    data = cipher.encrypt(_to_bytes(data))
    data = _to_unicode(base64.b64encode(data))

    # function e
    rv = ''
    i = 0
    for m in range(len(data)):
        rv += data[m]
        if (m == pow(2, i)) and i < 5:
            rv += n[i]
            i += 1
    return rv


def _to_bytes(text):
    if isinstance(text, bytes):
        return text
    return text.encode('utf-8')


def _to_unicode(text):
    if isinstance(text, str):
        return text
    return text.decode('utf-8')


def process_eqs(key, secret, setting):
    eqs = _cipher_eqs(key, secret, setting)
    return eqs


def _get_suv():
    return '='.join(['SUV', str(int(time.time()*1000000) + random.randint(0, 1000))])


def get_cookies(source):
    cookies = r.lrange('cookie:%s' % source, 0, -1)
    if not cookies:
        cookies = set_cookies(source)
    cookie = random.choice(cookies)
    return cookie


def get_key(source, url=''):
    key = r.get('key:%s' % source)
    if not key:
        key = set_key(source, url)
    return key


def set_cookies(source):
    cookies = []
    for i in xrange(10):

        url = WEIXIN_COOKIE.format(
            q=random.choice('abcdefghijklmnopqrstuvwxyz'))

        # get SNUID
        response = requests.request('GET', url=url)
        time.sleep(10)
        cookie = process_cookie(response.headers['set-cookie']['Cookie'])
        cookies.append(cookie)

        key, level, setting = process_key(response.content.decode('utf-8'))
        r.set('key:%s' % source, (key, level, setting))

    if cookies:
        r.lpush('cookie:%s' % source, cookies)
    return cookies


def set_key(source, url=''):
    url = url or 'http://weixin.sogou.com/'
    response = requests.request(method='GET', url=url)
    html = response.content.decode('utf-8')
    key, level, setting = process_key(html)
    r.set('key:%s' % source, (key, level, setting))


def process_cookie(cookie):
    l = _COOKIE_RE.findall(cookie)
    l.append(_get_suv())
    return {'Cookie': '; '.join(l)}


def process_key(html):
    pattern = (
        r'SogouEncrypt.setKv\("(\w+)","(\d)"\)'
        r'.*?'
        r'SogouEncrypt.encryptquery\("(\w+)","(\w+)"\)'
    )
    m = re.findall(pattern, html, re.S)
    key, level, secret, setting = m[0]
    return key, level, setting
