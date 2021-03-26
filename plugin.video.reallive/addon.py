#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from xbmcswift2 import Plugin
import requests
from bs4 import BeautifulSoup
import xbmcgui
import time
import base64
import json
import urllib
import sys
import html
import re
import random
import hashlib
import js2py



def unescape(string):
    string = urllib.unquote(string).decode('utf8')
    quoted = html.unescape(string).encode('utf-8')
    #转成中文
    return re.sub(r'%u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: unichr(int(m.group(1), 16)), quoted)


plugin = Plugin()


macheaders = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4 Supplemental Update) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15'}
ipadheaders = {'user-agent': 'Mozilla/5.0 (iPad; CPU OS 10_15_4 Supplemental Update like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Mobile/15E148 Safari/605.1.15'}
iphoneheaders = {'user-agent': 'Mozilla/5.0 (iPhone; CPU OS 10_15_4 Supplemental Update like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Mobile/14E304 Safari/605.1.15'}
mheaders = {'user-agent':'Mozilla/5.0 (Linux; Android 10; Z832 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Mobile Safari/537.36'}
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
tmp = plugin.get_storage('tmp')

#用户设置存储
storage = plugin.get_storage('storage')
#搜索历史纪录
his = plugin.get_storage('his')


def chushihua(key,default):
    if key in storage:
        switch = storage[key]
    else:
        storage[key] = default
        switch = storage[key]
    if switch == 1:
        value = '开'
    else:
        value = '关'
    return value

@plugin.cached(TTL=2)
def get_html(url,ua='pc',mode='html',encode='utf-8'):
    if ua == 'pc':
        r = requests.get(url,headers=headers)
    if ua == 'mobile':
        r = requests.get(url,headers=mheaders)
    if ua == 'iphone':
        r = requests.get(url,headers=iphoneheaders)
    if ua == 'ipad':
        r = requests.get(url,headers=ipadheaders)
    if ua == 'mac':
        r = requests.get(url,headers=macheaders)
    if ua != 'pc' and ua != 'mobile' and ua != 'iphone' and ua != 'ipad' and ua != 'mac':
        r = requests.get(url,headers=eval(ua))
    if encode == 'utf-8':
        r.encoding = 'utf-8'
    if encode == 'gbk':
        r.encoding = 'gbk'
    if mode == 'url':
        html = r.url
    else:
        html = r.text
    return html

@plugin.cached(TTL=2)
def post_html(url,data,json='off',ua='pc',mode='html',encode='utf-8'):
    data = eval(data)
    if json == 'off':
        if ua == 'pc':
            r = requests.post(url,data=data,headers=headers)
        if ua == 'mobile':
            r = requests.post(url,data=data,headers=mheaders)
        if ua == 'iphone':
            r = requests.post(url,data=data,headers=iphoneheaders)
        if ua == 'ipad':
            r = requests.post(url,data=data,headers=ipadheaders)
        if ua == 'mac':
            r = requests.post(url,data=data,headers=macheaders)
    else:
        if ua == 'pc':
            r = requests.post(url,json=data,headers=headers)
        if ua == 'mobile':
            r = requests.post(url,json=data,headers=mheaders)
        if ua == 'iphone':
            r = requests.post(url,json=data,headers=iphoneheaders)
        if ua == 'ipad':
            r = requests.post(url,json=data,headers=ipadheaders)
        if ua == 'mac':
            r = requests.post(url,json=data,headers=macheaders)
    if encode == 'utf-8':
        r.encoding = 'utf-8'
    if encode == 'gbk':
        r.encoding = 'gbk'
    if mode == 'url':
        html = r.url
    else:
        html = r.text
    return html

def unix_to_data(uptime,format='data'):
    if len(str(uptime)) > 10:
        uptime = str(uptime)[:-(len(str(uptime))-10)]
    uptime = float(uptime)
    time_local = time.localtime(uptime)
    if format == 'data' or format == 'zhdata' or format == 'datatime' or format == 'zhdatatime' or format == 'time' or format == 'zhtime':
        if format == 'data':
            uptime = time.strftime('%Y-%m-%d',time_local)
        if format == 'zhdata':
            uptime = time.strftime('%Y年%m月%d日',time_local)
        if format == 'datatime':
            uptime = time.strftime('%Y-%m-%d %H:%M:%S',time_local)
        if format == 'zhdatatime':
            uptime = time.strftime('%Y年%m月%d日 %H时%M分%S秒',time_local)
        if format == 'time':
            uptime = time.strftime('%H:%M:%S',time_local)
        if format == 'zhtime':
            uptime = time.strftime('%H时%M分%S秒',time_local)
    else:
        uptime = time.strftime(format,time_local)
    return uptime

#超过10000换算
def zh(num):
    if int(num) >= 100000000:
        p = round(float(num)/float(100000000), 1)
        p = str(p) + '亿'
    else:
        if int(num) >= 10000:
            p = round(float(num)/float(10000), 1)
            p = str(p) + '万'
        else:
            p = str(num)
    return p.encode('utf-8').decode('utf-8')

def tiqu_num(string):
    try:
        a = re.search('\d+',string).group()
        return a
    except AttributeError:
        return ''

def get_categories_mode(mode):
    item = eval('get_' + mode + '_categories')()
    return item
def get_rooms_mode(url,mode,page):
    item = eval('get_' + mode + '_rooms')(url,int(page))
    return item
def get_roomidinfo_mode(url,mode):
    item = eval('get_' + mode + '_roomidinfo')(url)
    return item
def get_search_mode(keyword,page,mode):
    item = eval('get_' + mode + '_search')(keyword,int(page))
    return item
def get_roomid_mode(url,mode):
    item = eval('get_' + mode + '_roomid')(url)
    return item
##########################################################
###主入口
##########################################################

def get_categories():
    return [{'id':1,'name':'虎牙直播','link':'huya','author':'zhengfan2014','upload':'2020-5-13','rooms':120},
            {'id':2,'name':'斗鱼直播','link':'douyu','author':'zhengfan2014','upload':'2020-5-13','rooms':120},
            {'id':3,'name':'触手直播','link':'chushou','author':'zhengfan2014','upload':'2020-5-13','rooms':20},
            {'id':4,'name':'企鹅电竞','link':'egame','author':'zhengfan2014','upload':'2020-5-17'},
            {'id':5,'name':'龙珠直播','link':'longzhu','author':'zhengfan2014','upload':'2020-5-17'},
            {'id':6,'name':'Bilibili直播','link':'bilibili','author':'zhengfan2014','upload':'2020-5-18','rooms':30},
            {'id':7,'name':'YY直播','link':'yy','author':'zhengfan2014','upload':'2020-5-18','rooms':30},
            {'id':8,'name':'快手直播','link':'kuaishou','author':'zhengfan2014','upload':'2020-5-18','rooms':60},
            {'id':9,'name':'Acfun直播','link':'acfun','author':'zhengfan2014','upload':'2020-5-18'},
            {'id':10,'name':'it之家直播','link':'ithome','author':'zhengfan2014','upload':'2020-6-8','rooms':20},
            {'id':11,'name':'电视直播','link':'yangshipin','author':'zhengfan2014','upload':'2020-6-8','roomid':'false'},
            {'id':12,'name':'直播中国','link':'livechina','author':'zhengfan2014','upload':'2020-6-8','roomid':'false'},
            {'id':13,'name':'熊猫频道','link':'ipanda','author':'zhengfan2014','upload':'2020-6-8','roomid':'false'}]

##########################################################
###以下是模块，网站模块请粘贴在这里面
##########################################################

#虎牙直播
def get_huya_categories():
    return [{'name':'网游竞技','link':'https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&gameId=100023&tagAll=0&page='},
            {'name':'单机热游','link':'https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&gameId=100002&tagAll=0&page='},
            {'name':'娱乐天地','link':'https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&gameId=100022&tagAll=0&page='},
            {'name':'手游休闲','link':'https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&gameId=100004&tagAll=0&page='}]

def get_huya_rooms(url,page):
    rooms = []
    
    r = get_html(url +str(page))
    j = json.loads(r)
    rlist = j['data']['datas']
    for i in range(len(rlist)):
        roomitem = {}
        roomitem['name'] =  u'[' + rlist[i]['gameFullName'] + u'] ' + rlist[i]['introduction']
        roomitem['href'] =  rlist[i]['profileRoom']
        roomitem['thumb'] = rlist[i]['screenshot']
        roomitem['info'] = {'plot' : zh(rlist[i]['totalCount']) + u' 人气\n' + rlist[i]['roomName'],'cast':[(rlist[i]['nick'],u'主播')],'genre':[rlist[i]['gameFullName']]}
        rooms.append(roomitem)
    return rooms

def get_huya_roomidinfo(url):
    info = {}
    if 'huya.com' in url:
        room_id = re.search('(?<=huya.com/)[a-zA-Z0-9]+',url).group()
    else:
        room_id = url
    room_url = 'https://www.huya.com/' + str(room_id)
    r = get_html(room_url)
    str1 = r.find(';var TT_ROOM_DATA = ')
    str2 = r.find(';var TT_PROFILE_INFO =')
    str3 = r.find(';var TT_PLAYER_CFG =')
    roomdata = r[str1+20:str2]
    upinfo = r[str2+23:str3]
    roomdata = json.loads(roomdata)
    upinfo = json.loads(upinfo)
    # dialog = xbmcgui.Dialog()
    # dialog.textviewer('1',str(roomdata)+ '\n\n' + str(upinfo) + '\n' +str(str3))
    info['title'] = roomdata['introduction']
    info['img'] = roomdata['screenshot']
    info['genre'] = [roomdata['gameFullName']]
    
    plot = u'房间号: ' + str(roomdata['profileRoom'])
    if roomdata['state'] == 'ON':
        info['status'] = u'开播'
        plot += u' · '+str(roomdata['totalCount']) + u' 人气值' 
    else:
        info['status'] = u'未开播'
    info['cast'] = [(upinfo['nick'],zh(upinfo['fans'])+u'粉丝')]
    info['plot'] = plot
    return info

def get_huya_roomid(url):
    if 'huya.com' in url:
        room_id = re.search('(?<=huya.com/)[a-zA-Z0-9]+',url).group()
        dialog = xbmcgui.Dialog()
        dialog.notification('提取成功','房间号：' + str(room_id), xbmcgui.NOTIFICATION_INFO, 5000)
    else:
        room_id = url
    room_url = 'https://m.huya.com/' + str(room_id)
    r = get_html(room_url,'mobile')
    if re.search(r'//[\S]*.m3u8[\S]*?(?=\")',r):
        url = 'https:' + re.search(r'//[\S]*.m3u8[\S]*?(?=\")',r).group()
        url = re.sub(r'_[\S]*.m3u8','.m3u8',url)
    else:
        url = ''
        dialog = xbmcgui.Dialog()
        dialog.notification('请求直播源失败','未开播或直播间不存在', xbmcgui.NOTIFICATION_INFO, 5000)
    # dialog = xbmcgui.Dialog()
    # dialog.textviewer('1',str(url))
    # print(url)
    return url

#斗鱼直播
def get_douyu_categories():
    return [{'name':'CF手游','link':'https://www.douyu.com/gapi/rkc/directory/mixList/2_178/'},
            {'name':'文化','link':'https://www.douyu.com/gapi/rkc/directory/mixList/2_195/'},
            {'name':'中国象棋','link':'https://www.douyu.com/gapi/rkc/directory/mixList/2_543/'},
            {'name':'使命召唤','link':'https://www.douyu.com/gapi/rkc/directory/mixList/2_472/'},
            {'name':'逆战','link':'https://www.douyu.com/gapi/rkc/directory/mixList/2_46/'},
            {'name':'热门网游','link':'https://www.douyu.com/gapi/rkc/directory/mixList/2_203/'},
            {'name':'颜值','link':'https://www.douyu.com/gapi/rknc/directory/yzRec/'},
            {'name':'陪玩','link':'https://www.douyu.com/gapi/rkc/directory/mixList/2_1015/'},
            {'name':'英雄联盟','link':'https://www.douyu.com/gapi/rkc/directory/mixList/2_1/'}]

def get_douyu_rooms(url,page):
    rooms = []
    
    r = get_html(url +str(page))
    j = json.loads(r)
    rlist = j['data']['rl']
    for i in range(len(rlist)):
        roomitem = {}
        roomitem['name'] = rlist[i]['rn']
        roomitem['href'] =  rlist[i]['rid']
        roomitem['thumb'] = rlist[i]['rs16']
        roomitem['info'] = {'plot' : zh(rlist[i]['ol']) + u' 人气 · 房间号 ' + str(rlist[i]['rid']) + u'\n\n','cast':[(rlist[i]['nn'],u'主播')]}
        if rlist[i]['od'] != '':
            roomitem['info']['plot'] += u'[COLOR orange]官方认证：' + rlist[i]['od'] + '[/COLOR]'
        rooms.append(roomitem)
    return rooms

def get_douyu_roomidinfo(url):
    info = {}
    if 'douyu.com' in url:
        if '?rid=' in url:
            room_id = re.search('(?<=\?rid=)[0-9]+',url).group()
        else:
            room_id = re.search('(?<=douyu.com/)[0-9]+',url).group()
    else:
        room_id = url
    room_url = 'https://www.douyu.com/betard/' + str(room_id)
    r = get_html(room_url)
    j = json.loads(r)
    info['title'] = j['room']['room_name']
    info['img'] = j['room']['room_pic']
    info['genre'] = [j['room']['second_lvl_name']]
    
    plot = u'房间号: ' + str(j['room']['room_id'])
    
    plot += u'\n' + j['room']['show_details']
    # if roomdata['state'] == 'ON':
    #     info['status'] = u'开播'
    #     plot += u' · '+str(roomdata['totalCount']) + u' 人气值' 
    # else:
    #     info['status'] = u'未开播'
    info['cast'] = [(j['room']['nickname'],u'主播')]
    info['plot'] = plot
    return info

def get_douyu_roomid(url):
    if 'douyu.com' in url:
        if '?rid=' in url:
            room_id = re.search('(?<=\?rid=)[0-9]+',url).group()
        else:
            room_id = re.search('(?<=douyu.com/)[0-9]+',url).group()
        dialog = xbmcgui.Dialog()
        dialog.notification('提取成功','房间号：' + str(room_id), xbmcgui.NOTIFICATION_INFO, 5000)
    else:
        room_id = url

    rid = str(room_id)
    tt = get_tt()
    url = get_pre_url(rid, tt[1])
    if url:
        return "http://tx2play1.douyucdn.cn/live/" + url + ".flv?uuid="
    else:
        result = get_homejs(rid)
        real_rid = result[1]
        homejs = result[0]
        real_url = get_sign_url(tt[2], real_rid, tt[0], homejs)
        if real_url != 0:
            real_url = "http://tx2play1.douyucdn.cn/live/" + real_url + ".flv?uuid="
        else:
            real_url = '未开播'
        return real_url
    # r = get_html('https://web.sinsyth.com/lxapi/douyujx.x?roomid=' + str(room_id))
    # j = json.loads(r)
    # live = j['Rendata']['link']
    # live = re.search('douyucdn.cn/live/[a-zA-Z0-9]+',live).group()
    # live = 'http://tx2play1.' + live + '.m3u8'
    #dialog = xbmcgui.Dialog()
    #dialog.textviewer('1',str(live))
    # return live

def get_homejs(rid):
    room_url = 'https://m.douyu.com/' + rid
    response = requests.get(url=room_url)
    pattern_real_rid = r'"rid":(\d{1,7})'
    real_rid = re.findall(pattern_real_rid, response.text, re.I)[0]
    if real_rid != rid:
        room_url = 'https://m.douyu.com/' + real_rid
        response = requests.get(url=room_url)
    homejs = ''
    pattern = r'(function ub9.*)[\s\S](var.*)'
    result = re.findall(pattern, response.text, re.I)
    str1 = re.sub(r'eval.*;}', 'strc;}', result[0][0])
    homejs = str1 + result[0][1]
    return homejs, real_rid

def get_sign(rid, post_v, tt, ub9): 
    context = js2py.EvalJs()
    context.execute(ub9)
    res = context.ub98484234()
    v = re.search(r'v=(\d+)', res).group(1)
    rb = hashlib.md5((rid + '10000000000000000000000000001501' + tt + v).encode('utf-8')).hexdigest()
    func_sign = re.sub(r'return rt;}\);?', 'return rt;}', res)
    func_sign = func_sign.replace('(function (', 'function sign(')
    func_sign = func_sign.replace('CryptoJS.MD5(cb).toString()', '"' + rb + '"')
    print(func_sign)
    js = js2py.eval_js(func_sign)
    sign = js(rid, '10000000000000000000000000001501', tt)
    return sign

def get_tt():
    tt1 = str(int(time.time()))
    tt2 = str(int((time.time() * 1000)))
    today = time.strftime('%Y%m%d', time.localtime())
    return tt1, tt2, today

def get_pre_url(rid, tt):
    request_url = 'https://playweb.douyucdn.cn/lapi/live/hlsH5Preview/' + rid
    post_data = {
        'rid': rid,
        'did': '10000000000000000000000000001501'
    }
    auth = hashlib.md5((rid + str(tt)).encode('utf-8')).hexdigest()
    header = {
        'content-type': 'application/x-www-form-urlencoded',
        'rid': rid,
        'time': tt,
        'auth': auth
    }
    response = requests.post(url=request_url, headers=header, data=post_data)
    response = response.json()
    pre_url = ''
    if response.get('error') == 0:
        real_url = (response.get('data')).get('rtmp_live')
        if 'mix=1' in real_url:
            pre_url = mix_room(rid)
        else:
            pattern1 = r'^[0-9a-zA-Z]*'
            pre_url = re.search(pattern1, real_url, re.I).group()
    return pre_url

def get_sign_url(post_v, rid, tt, ub9):
    sign = get_sign(rid, post_v, tt, ub9)
    params = sign + '&ver=219032101&rid={}&rate=-1'.format(rid)
    request_url = 'https://m.douyu.com/api/room/ratestream'
    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36'
    }
    response = requests.post(url=request_url, headers=header, params=params).json()
    if response.get('code') == 0:
        real_url = (response.get('data')).get('url')
        pattern = r'(\d{1,7}[0-9a-zA-Z]+)_?\d{0,4}(.m3u8|/playlist)'
        result1 = re.search(pattern, real_url).group(1)
    else:
        result1 = 0
    return result1


#触手
def get_chushou_categories():
    return [{'name':'王者荣耀','link':'https://chushou.tv/nav-list/down.htm?targetKey=3-1159-4&breakpoint='},
            {'name':'和平精英','link':'https://chushou.tv/nav-list/down.htm?targetKey=3-1576-4&breakpoint='},
            {'name':'遇见KK','link':'https://chushou.tv/nav-list/down.htm?targetKey=3-1744-4&breakpoint='},
            {'name':'创造与魔法','link':'https://chushou.tv/nav-list/down.htm?targetKey=3-1432-4&breakpoint='},
            {'name':'巅峰战舰','link':'https://chushou.tv/nav-list/down.htm?targetKey=3-1191-4&breakpoint='},
            {'name':'穿越火线','link':'https://chushou.tv/nav-list/down.htm?targetKey=3-1147-4&breakpoint='},
            {'name':'球球大作战','link':'https://chushou.tv/nav-list/down.htm?targetKey=3-1013-4&breakpoint='},
            {'name':'英雄联盟','link':'https://chushou.tv/nav-list/down.htm?targetKey=3-1435-4&breakpoint='},
            {'name':'全民枪战','link':'https://chushou.tv/nav-list/down.htm?targetKey=3-1009-4&breakpoint='}]

def get_chushou_rooms(url,page):
    rooms = []
    
    r = get_html(url +str((int(page)-1)*20))
    j = json.loads(r)
    rlist = j['data']['items']
    for i in range(len(rlist)):
        roomitem = {}
        roomitem['name'] = u''
        roomitem['href'] =  rlist[i]['targetKey']
        roomitem['thumb'] = rlist[i]['cover']
        roomitem['info'] = {'plot' : zh(rlist[i]['meta']['onlineCount']) + u' 人气 · 房间号 ' + rlist[i]['targetKey'],'cast':[(rlist[i]['meta']['creator'],u'主播')]}
        if 'liveTagName' in rlist[i]['meta']:
            roomitem['info']['genre'] = [rlist[i]['meta']['liveTagName']]
            roomitem['name'] =  u'[' + rlist[i]['meta']['liveTagName'] + u'] ' 
        roomitem['name'] = rlist[i]['name']
        rooms.append(roomitem)
    return rooms

def get_chushou_roomidinfo(url):
    info = {}
    if 'chushou.tv' in url:
        if re.search('(?<=/room/)[0-9]+',url):
            room_id = re.search('(?<=/room/)[0-9]+',url).group()
        else:
            if re.search('(?<=/room/m-)[0-9]+',url):
                room_id = re.search('(?<=/room/m-)[0-9]+',url).group()
            else:
                room_id = url
        dialog = xbmcgui.Dialog()
        dialog.notification('提取成功','房间号：' + str(room_id), xbmcgui.NOTIFICATION_INFO, 5000)
    else:
        room_id = url
    room_url = 'https://chushou.tv/' + str(room_id)
    r = get_html(room_url)
    soup = BeautifulSoup(r,'html.parser')
    title = soup.find('p',class_='nav-title-text ellipsis').text
    genre = soup.find('a',class_='room-zone-text room-zone-text1').text
    up = soup.find('p',class_='room-anchor-nickname').text.strip()
    fans = soup.find('p',class_='room-subscribe-count').text
    img = soup.find('div',class_='live-flash-container')
    hot = soup.find('p',class_='room-hot').text
    # dialog = xbmcgui.Dialog()
    # dialog.textviewer('1',str(roomdata)+ '\n\n' + str(upinfo) + '\n' +str(str3))
    info['title'] = title
    info['img'] =  'http:' + img['data-videoimg']
    info['genre'] = [genre]
    plot = hot + u' 人气\n'
    plot += u'房间号: ' + str(img['data-roomid'])
    info['plot'] = plot
    info['cast'] = [(up,fans + u' 粉丝')]
    return info

def get_chushou_roomid(url):
    if 'chushou.tv' in url:
        if re.search('(?<=/room/)[0-9]+',url):
            room_id = re.search('(?<=/room/)[0-9]+',url).group()
        else:
            if re.search('(?<=/room/m-)[0-9]+',url):
                room_id = re.search('(?<=/room/m-)[0-9]+',url).group()
            else:
                room_id = url
        dialog = xbmcgui.Dialog()
        dialog.notification('提取成功','房间号：' + str(room_id), xbmcgui.NOTIFICATION_INFO, 5000)
    else:
        room_id = url
    try:
        room_url = 'https://chushou.tv/h5player/video/get-play-url.htm?roomId={}&protocols=2&callback='.format(room_id)
        r = get_html(room_url)
        j = json.loads(r)
        if j['code'] == 0:
            live = j['data'][0]
            if 'shdPlayUrl' in live:
                real_url = live['shdPlayUrl']
            else:
                if 'hdPlayUrl' in live:
                    real_url = live['hdPlayUrl']
                else:
                    real_url = live['sdPlayUrl']
        else:
            dialog = xbmcgui.Dialog()
            dialog.notification('获取直播地址失败','直播间不存在或未开播', xbmcgui.NOTIFICATION_INFO, 5000)
        return real_url
    except:
        dialog = xbmcgui.Dialog()
        dialog.notification('获取直播地址失败','直播间不存在或未开播', xbmcgui.NOTIFICATION_INFO, 5000)
    

def get_chushou_search(keyword,page):
    rooms = []
    url = 'https://chushou.tv/so.htm?keyword=' + keyword
    r = get_html(url)
    soup = BeautifulSoup(r,'html.parser')
    rlist = soup.find_all('a',class_='liveNewOne')
    uplist = soup.find_all('div',class_='per_anchor')
    for i in range(len(rlist)):
        roomitem = {}
        roomitem['name'] = u'[房间]' + rlist[i].find('span',class_='videoName').text
        roomitem['href'] =  'https://chushou.tv' + rlist[i]['href']
        roomitem['thumb'] = 'http:' + rlist[i].find('img',class_='liveImages homelazyImage')['src']
        roomitem['info'] = {'plot' : rlist[i].find('span',class_='liveCount').text + u' 人气 ','cast':[(rlist[i].find('span',class_='livePlayerName').text,u'主播')]}
        rooms.append(roomitem)
    for i in range(len(uplist)):
        if i < 4:
            roomitem = {}
            roomitem['name'] = u'[主播]' + uplist[i].find('span',class_='anchor_nickname').text
            roomitem['href'] =  'https://chushou.tv' + uplist[i].a['href']
            roomitem['thumb'] = 'https:' + uplist[i].div.a.img['src']
            roomitem['info'] = {'plot' : uplist[i].find('span',class_='fans_num').text ,'cast':[(uplist[i].find('span',class_='anchor_nickname').text,u'主播')]}
            rooms.append(roomitem)
    return rooms

#企鹅电竞
def get_egame_categories():
    return [{'name':'王者荣耀','link':'https://share.egame.qq.com/cgi-bin/pgg_live_async_fcgi?param={"key":{"module":"pgg_live_read_ifc_mt_svr","method":"get_pc_live_list","param":{"appid":"1104466820","page_size":40,"page_num":'},
            {'name':'和平精英','link':'https://share.egame.qq.com/cgi-bin/pgg_live_async_fcgi?param={"key":{"module":"pgg_live_read_ifc_mt_svr","method":"get_pc_live_list","param":{"appid":"1106467070","page_size":40,"page_num":'},
            {'name':'主机游戏','link':'https://share.egame.qq.com/cgi-bin/pgg_live_async_fcgi?param={"key":{"module":"pgg_live_read_ifc_mt_svr","method":"get_pc_live_list","param":{"appid":"2000000140","page_size":40,"page_num":'},
            {'name':'绝地求生','link':'https://share.egame.qq.com/cgi-bin/pgg_live_async_fcgi?param={"key":{"module":"pgg_live_read_ifc_mt_svr","method":"get_pc_live_list","param":{"appid":"2000000133","page_size":40,"page_num":'},
            {'name':'梦工厂','link':'https://share.egame.qq.com/cgi-bin/pgg_live_async_fcgi?param={"key":{"module":"pgg_live_read_ifc_mt_svr","method":"get_pc_live_list","param":{"appid":"2000000157","page_size":40,"page_num":'},
            {'name':'英雄联盟','link':'https://share.egame.qq.com/cgi-bin/pgg_live_async_fcgi?param={"key":{"module":"pgg_live_read_ifc_mt_svr","method":"get_pc_live_list","param":{"appid":"lol","page_size":40,"page_num":'},
            {'name':'LOL云顶之弈','link':'https://share.egame.qq.com/cgi-bin/pgg_live_async_fcgi?param={"key":{"module":"pgg_live_read_ifc_mt_svr","method":"get_pc_live_list","param":{"appid":"400000001573","page_size":40,"page_num":'},
            {'name':'穿越火线','link':'https://share.egame.qq.com/cgi-bin/pgg_live_async_fcgi?param={"key":{"module":"pgg_live_read_ifc_mt_svr","method":"get_pc_live_list","param":{"appid":"Cf","page_size":40,"page_num":'},
            {'name':'户外猎奇','link':'https://share.egame.qq.com/cgi-bin/pgg_live_async_fcgi?param={"key":{"module":"pgg_live_read_ifc_mt_svr","method":"get_pc_live_list","param":{"appid":"40000001470","page_size":40,"page_num":'},
            {'name':'王牌战士','link':'https://share.egame.qq.com/cgi-bin/pgg_live_async_fcgi?param={"key":{"module":"pgg_live_read_ifc_mt_svr","method":"get_pc_live_list","param":{"appid":"1106448348","page_size":40,"page_num":'},
            {'name':'暴雪专区','link':'https://share.egame.qq.com/cgi-bin/pgg_live_async_fcgi?param={"key":{"module":"pgg_live_read_ifc_mt_svr","method":"get_pc_live_list","param":{"appid":"400000001544","page_size":40,"page_num":'},
            {'name':'自走棋','link':'https://share.egame.qq.com/cgi-bin/pgg_live_async_fcgi?param={"key":{"module":"pgg_live_read_ifc_mt_svr","method":"get_pc_live_list","param":{"appid":"40000001435","page_size":40,"page_num":'},
            {'name':'CF手游','link':'https://share.egame.qq.com/cgi-bin/pgg_live_async_fcgi?param={"key":{"module":"pgg_live_read_ifc_mt_svr","method":"get_pc_live_list","param":{"appid":"1104512706","page_size":40,"page_num":'},
            {'name':'QQ飞车手游','link':'https://share.egame.qq.com/cgi-bin/pgg_live_async_fcgi?param={"key":{"module":"pgg_live_read_ifc_mt_svr","method":"get_pc_live_list","param":{"appid":"1104922185","page_size":40,"page_num":'},
            {'name':'陪你看','link':'https://share.egame.qq.com/cgi-bin/pgg_live_async_fcgi?param={"key":{"module":"pgg_live_read_ifc_mt_svr","method":"get_pc_live_list","param":{"appid":"2000000110","page_size":40,"page_num":'},
            {'name':'新游中心','link':'https://share.egame.qq.com/cgi-bin/pgg_live_async_fcgi?param={"key":{"module":"pgg_live_read_ifc_mt_svr","method":"get_pc_live_list","param":{"appid":"40000001309","page_size":40,"page_num":'},
            {'name':'娱乐','link':'https://share.egame.qq.com/cgi-bin/pgg_live_async_fcgi?param={"key":{"module":"pgg_live_read_ifc_mt_svr","method":"get_pc_live_list","param":{"appid":"40000001472","page_size":40,"page_num":'},
            {'name':'电竞赛事','link':'https://share.egame.qq.com/cgi-bin/pgg_live_async_fcgi?param={"key":{"module":"pgg_live_read_ifc_mt_svr","method":"get_pc_live_list","param":{"appid":"2000000188","page_size":40,"page_num":'}]

def get_egame_rooms(url,page):
    rooms = []
    
    r = get_html(url +str(page) + '}}}')
    j = json.loads(r)
    rlist = j['data']['key']['retBody']['data']['live_data']['live_list']
    for i in range(len(rlist)):
        roomitem = {}
        roomitem['name'] = rlist[i]['title']
        roomitem['href'] =  rlist[i]['anchor_id']
        roomitem['thumb'] = rlist[i]['video_info']['url_high_reslution']
        roomitem['info'] = {'plot' : zh(rlist[i]['online']) + u' 人气 · 房间号 ' + str(rlist[i]['anchor_id']),'cast':[(rlist[i]['anchor_name'],zh(rlist[i]['fans_count']))],'genre':[rlist[i]['appname']]}
        
        rooms.append(roomitem)
    return rooms

def get_egame_roomidinfo(url):
    info = {}
    if 'egame.qq.com' in url:
        if re.search('(?<=egame.qq.com/)[0-9]+',url):
            room_id = re.search('(?<=egame.qq.com/)[0-9]+',url).group()
        dialog = xbmcgui.Dialog()
        dialog.notification('提取成功','房间号：' + str(room_id), xbmcgui.NOTIFICATION_INFO, 5000)
    else:
        room_id = url
    r0 = get_html('https://m.egame.qq.com/'+room_id,'mobile')
    soup = BeautifulSoup(r0,'html.parser')
    title = soup.find('p',id='game-slogan')
    img = soup.find('div',class_='player-bg')

    room_url = 'https://share.egame.qq.com/cgi-bin/pgg_anchor_async_fcgi?param=%7B%22key%22:%7B%22module%22:%22pgg_anchor_card_svr%22,%22method%22:%22get_anchor_card_info%22,%22param%22:%7B%22anchor_uid%22:' + str(room_id) + ',%22user_uid%22:0%7D%7D%7D&g_tk=&pgg_tk=&tt=1'
    r = get_html(room_url)
    j = json.loads(r)
    i = j['data']['key']['retBody']['data']
    info['title'] = title.text
    info['img'] =  img['style'][22:-1]
    info['genre'] = [i['appname']]
    plot = u'房间号: ' + str(i['uid'])
    plot += u'\n\n' + i['profile']
    info['plot'] = plot
    info['cast'] = [(i['nick_name'],zh(i['fans_count']) + u' 粉丝')]
    return info
def get_egame_roomid(url):
    if 'egame.qq.com' in url:
        if re.search('(?<=egame.qq.com/)[0-9]+',url):
            room_id = re.search('(?<=egame.qq.com/)[0-9]+',url).group()
        dialog = xbmcgui.Dialog()
        dialog.notification('提取成功','房间号：' + str(room_id), xbmcgui.NOTIFICATION_INFO, 5000)
    else:
        room_id = url
    room_url = 'https://share.egame.qq.com/cgi-bin/pgg_async_fcgi'
    post_data = {
        'param': '''{"0":{"module":"pgg_live_read_svr","method":"get_live_and_profile_info","param":{"anchor_id":''' + str(room_id) + ''',"layout_id":"hot","index":1,"other_uid":0}}}'''
    }
    try:
        r = post_html(room_url,str(post_data))
        j = json.loads(r)
        data = j['data']
        if data:
            video_info = data['0']['retBody']['data']['video_info']
            pid = video_info['pid']
            if pid:
                is_live = data['0']['retBody']['data']['profile_info']['is_live']
                if is_live:
                    play_url = video_info['stream_infos'][0]['play_url']
                    real_url = re.findall(r'([\w\W]+?)&uid=', play_url)[0]
                    return real_url
                else:
                    real_url = '直播间未开播'
            else:
                real_url = '直播间未启用'
        else:
            real_url = '直播间不存在'
    except:
        real_url = '数据请求错误'

#龙珠直播
def get_longzhu_categories():
    return [{'name':'全部直播','link':'https://longzhu.com/channels/all'},
            {'name':'游戏','link':'http://longzhu.com/channels/game'},
            {'name':'阳光龙珠','link':'http://longzhu.com/channels/lzgy'},
            {'name':'美女','link':'http://longzhu.com/channels/hwzb'},
            {'name':'综合足球','link':'http://longzhu.com/channels/zhzq'}]

def get_longzhu_rooms(url,page):
    rooms = []
    
    r = get_html(url)
    soup = BeautifulSoup(r,'html.parser')
    base = soup.find('div',id='list-con')
    rlist = base.find_all('a',class_='livecard')
    for i in range(len(rlist)):
        roomitem = {}
        roomitem['name'] = rlist[i].find('h3').text
        roomitem['href'] =  rlist[i]['href']
        roomitem['thumb'] = rlist[i].find('img')['src']
        roomitem['info'] = {'plot' : rlist[i].find('li',class_='livecard-meta-item livecard-meta-views').find('span',class_='livecard-meta-item-text').text + u' 人气 · 房间号 ','cast':[(rlist[i].find('strong',class_='livecard-modal-username').text,u'主播')],'genre':[rlist[i].find('li',class_='livecard-meta-item livecard-meta-game').find('span',class_='livecard-meta-item-text').text]}
        
        rooms.append(roomitem)
    return rooms

def get_longzhu_roomidinfo(url):
    info = {}
    if 'longzhu.com' in url:
        if re.search('(?<=longzhu.com/)[0-9]+',url):
            room_id = re.search('(?<=longzhu.com/)[0-9]+',url).group()
        if re.search('(?<=longzhu.com/)[a-z0-9]+',url):
            room_id = re.search('(?<=longzhu.com/)[a-z0-9]+',url).group()
        dialog = xbmcgui.Dialog()
        dialog.notification('提取成功','房间号：' + str(room_id), xbmcgui.NOTIFICATION_INFO, 5000)
    else:
        room_id = url
    
    r = get_html('http://m.longzhu.com/' + str(room_id))
    room_id = re.findall(r'roomId = (\d*);', r)[0]
    room_url = 'http://liveapi.plu.cn/liveapp/roomstatus?version=3.9.3&device=6&packageId=&roomId=' + str(room_id)
    r = get_html(room_url,'mobile')
    j = json.loads(r)
    info['title'] = j['title']
    info['img'] =  j['cover']
    info['genre'] = [j['broadcast']['parentGameName'],j['broadcast']['gameName']]
    plot = u'房间号: ' + str(j['roomId'])
    plot += u'\n\n' + j['desc']
    info['plot'] = plot
    info['cast'] = [(j['userName'],zh(j['subscribeCount']) + u' 粉丝')]
    return info

def get_longzhu_roomid(url):
    if 'longzhu.com' in url:
        if re.search('(?<=longzhu.com/)[0-9]+',url):
            room_id = re.search('(?<=longzhu.com/)[0-9]+',url).group()
        if re.search('(?<=longzhu.com/)[a-z0-9]+',url):
            room_id = re.search('(?<=longzhu.com/)[a-z0-9]+',url).group()
        dialog = xbmcgui.Dialog()
        dialog.notification('提取成功','房间号：' + str(room_id), xbmcgui.NOTIFICATION_INFO, 5000)
    else:
        room_id = url
    try:
        r = get_html('http://m.longzhu.com/' + str(room_id))
        roomId = re.findall(r'roomId = (\d*);', r)[0]
        r = get_html('http://livestream.longzhu.com/live/getlivePlayurl?roomId={}&hostPullType=2&isAdvanced=true&playUrlsType=1'.format(roomId))
        j = json.loads(r)
        real_url = j['playLines'][0]['urls'][-1]['securityUrl']
        return real_url
    except:
        real_url = '直播间不存在或未开播'
#bilibili直播
def get_bilibili_categories():
    return [{'name':'网游','link':'https://api.live.bilibili.com/room/v3/area/getRoomList?platform=web&parent_area_id=2&cate_id=0&area_id=0&sort_type=sort_type_124&page_size=30&tag_version=1'},
            {'name':'手游','link':'https://api.live.bilibili.com/room/v3/area/getRoomList?platform=web&parent_area_id=3&cate_id=0&area_id=0&sort_type=sort_type_121&page_size=30&tag_version=1'},
            {'name':'单机','link':'https://api.live.bilibili.com/room/v3/area/getRoomList?platform=web&parent_area_id=6&cate_id=0&area_id=0&sort_type=sort_type_150&page_size=30&tag_version=1'},
            {'name':'娱乐','link':'https://api.live.bilibili.com/room/v3/area/getRoomList?platform=web&parent_area_id=1&cate_id=0&area_id=0&sort_type=sort_type_152&page_size=30&tag_version=1'},
            {'name':'电台','link':'https://api.live.bilibili.com/room/v3/area/getRoomList?platform=web&parent_area_id=5&cate_id=0&area_id=0&sort_type=income&page_size=30&tag_version=1'},
            {'name':'绘画','link':'https://api.live.bilibili.com/room/v3/area/getRoomList?platform=web&parent_area_id=4&cate_id=0&area_id=0&sort_type=sort_type_56&page_size=30&tag_version=1'}]

def get_bilibili_rooms(url,page):
    rooms = []
    r = get_html(url + '&page=' +str(page))
    j = json.loads(r)
    rlist = j['data']['list']
    for i in range(len(rlist)):
        roomitem = {}
        roomitem['name'] = rlist[i]['title']
        roomitem['href'] =  rlist[i]['roomid']
        roomitem['thumb'] = rlist[i]['cover']
        roomitem['info'] = {'plot' : zh(rlist[i]['online']) + u' 人气 · 房间号 ' + str(rlist[i]['roomid']),'cast':[(rlist[i]['uname'],u'主播')],'genre':[rlist[i]['parent_name'],rlist[i]['area_name']]}
        rooms.append(roomitem)
    return rooms

def get_bilibili_roomidinfo(url):
    info = {}
    if 'live.bilibili.com' in url:
        if re.search('(?<=live.bilibili.com/)[0-9]+',url):
            room_id = re.search('(?<=live.bilibili.com/)[0-9]+',url).group()
        dialog = xbmcgui.Dialog()
        dialog.notification('提取成功','房间号：' + str(room_id), xbmcgui.NOTIFICATION_INFO, 5000)
    else:
        room_id = url

    r = get_html('https://api.live.bilibili.com/room/v1/Room/get_info?id=' + str(room_id))
    j = json.loads(r)
    i = j['data']
    soup = BeautifulSoup(i['description'], "html5lib")
    info['title'] = i['title']
    info['img'] =  i['user_cover']
    info['genre'] = [i['parent_area_name'],i['area_name']] + i['tags'].split(u',')
    plot = u'房间号 ' + str(i['room_id'])
    plot += u'\n\n' + soup.text
    info['plot'] = plot

    r = get_html('https://api.bilibili.com/x/space/acc/info?mid='+str(i['uid'])+'&jsonp=jsonp')
    j = json.loads(r)
    info['cast'] = [(j['data']['name'],zh(i['attention']) +u' 粉丝')]
    return info

def get_bilibili_roomid(url):
    if 'live.bilibili.com' in url:
        if re.search('(?<=live.bilibili.com/)[0-9]+',url):
            room_id = re.search('(?<=live.bilibili.com/)[0-9]+',url).group()
        dialog = xbmcgui.Dialog()
        dialog.notification('提取成功','房间号：' + str(room_id), xbmcgui.NOTIFICATION_INFO, 5000)
    else:
        room_id = url
    r = get_html('https://api.live.bilibili.com/xlive/web-room/v1/index/getRoomPlayInfo?room_id='+str(room_id)+'&play_url=1&mask=0&qn=0&platform=web')
    j = json.loads(r)
    try:
        flv = j['data']['play_url']['durl'][-1]['url']
    except TypeError:
        dialog = xbmcgui.Dialog()
        dialog.notification('获取直播源地址失败', '可能房间号不存在未开播', xbmcgui.NOTIFICATION_INFO, 5000,False)
    return flv
#yy直播
def get_yy_categories():
    return [{'name':'音乐','link':'https://www.yy.com/more/page.action?biz=sing&subBiz=idx&moduleId=308&pageSize=30&page='},
            {'name':'舞蹈','link':'https://www.yy.com/more/page.action?biz=dance&subBiz=idx&moduleId=313&pageSize=30&page='},
            {'name':'脱口秀','link':'https://www.yy.com/more/page.action?biz=talk&subBiz=idx&moduleId=328&pageSize=30&page='},
            {'name':'二次元','link':'https://www.yy.com/more/page.action?biz=car&subBiz=idx&moduleId=1877&pageSize=30&page='},
            {'name':'喊麦','link':'https://www.yy.com/more/page.action?biz=mc&subBiz=idx&moduleId=322&pageSize=30&page='},
            {'name':'美食','link':'https://www.yy.com/more/page.action?biz=red&subBiz=meishi&moduleId=1656&pageSize=30&page='},
            {'name':'体育','link':'https://www.yy.com/more/page.action?biz=sport&subBiz=idx&moduleId=434779&pageSize=30&page='},
            {'name':'猎奇','link':'https://www.yy.com/more/page.action?biz=red&subBiz=lieqi&moduleId=561&pageSize=30&page='},
            {'name':'名嘴','link':'https://www.yy.com/more/page.action?biz=talk&subBiz=nj&moduleId=975&pageSize=30&page='},
            {'name':'旅游','link':'https://www.yy.com/more/page.action?biz=red&subBiz=lvyou&moduleId=560&pageSize=30&page='},
            {'name':'活力少女','link':'https://www.yy.com/more/page.action?biz=talk&subBiz=girl&moduleId=976&pageSize=30&page='},
            {'name':'吃鸡端游','link':'https://www.yy.com/more/page.action?biz=chicken&subBiz=jdqs&moduleId=1473&pageSize=30&page='},
            {'name':'和平精英','link':'https://www.yy.com/more/page.action?biz=chicken&subBiz=cjzc&moduleId=1776&pageSize=30&page='},
            {'name':'王者荣耀','link':'https://www.yy.com/more/page.action?biz=game&subBiz=idx&moduleId=1180&pageSize=30&page='},
            {'name':'主机热游','link':'https://www.yy.com/more/page.action?biz=chicken&subBiz=djry&moduleId=3687&pageSize=30&page='},
            {'name':'陪你看','link':'https://www.yy.com/more/page.action?biz=other&subBiz=yqk&moduleId=3134&pageSize=30&page='},
            {'name':'颜值','link':'https://www.yy.com/more/page.action?biz=other&subBiz=xing&moduleId=1576&pageSize=30&page='}]

def get_yy_rooms(url,page):
    rooms = []
    r = get_html(url +str(page))
    j = json.loads(r)
    rlist = j['data']['data']
    for i in range(len(rlist)):
        roomitem = {}
        roomitem['name'] = rlist[i]['desc']
        roomitem['href'] =  'https://www.yy.com' + rlist[i]['liveUrl']
        roomitem['thumb'] = rlist[i]['thumb']
        roomitem['info'] = {'plot' : zh(rlist[i]['users']) + u' 人气 · 房间号 ' + str(rlist[i]['sid']),'cast':[(rlist[i]['name'],u'主播')]}
        rooms.append(roomitem)
    return rooms

def get_yy_roomidinfo(url):
    info = {}
    if 'yy.com' in url:
        if re.search('(?<=yy.com/)[0-9]+',url):
            room_id = re.search('(?<=yy.com/)[0-9]+',url).group()
        dialog = xbmcgui.Dialog()
        dialog.notification('提取成功','房间号：' + str(room_id), xbmcgui.NOTIFICATION_INFO, 5000)
    else:
        room_id = url

    r = get_html('https://www.yy.com/api/liveInfoDetail/'+ str(room_id) + '/'+ str(room_id) + '/0')
    j = json.loads(r)
    i = j['data']
    info['title'] = i['desc']
    info['img'] =  i['gameThumb']

    r = get_html('https://www.yy.com/api/biz-path/' + str(i['uid']))
    j = json.loads(r)
    info['genre'] = [j['data']['name']]
    if i['tag']:
        info['genre'] += [i['tag']]
    if j['data']['parent'] != None:
        info['genre'] +=  [j['data']['parent']['name']]
    plot = zh(i['users']) +  u'人气 · 房间号 ' + str(i['sid'])
    
    r = get_html('https://www.yy.com/yyweb/live/bulletin/' + str(i['uid']) + u'/' + str(i['sid']) + u'/' + str(i['sid']) + u'/')
    j = json.loads(r)
    plot += u'\n\n' + j['data']
    info['plot'] = plot
    info['cast'] = [(i['name'],u'主播')]
    return info

def get_yy_roomid(url):
    if 'yy.com' in url:
        if re.search('(?<=yy.com/)[0-9]+',url):
            room_id = re.search('(?<=yy.com/)[0-9]+',url).group()
        dialog = xbmcgui.Dialog()
        dialog.notification('提取成功','房间号：' + str(room_id), xbmcgui.NOTIFICATION_INFO, 5000)
    else:
        room_id = url
    room_url = 'http://interface.yy.com/hls/new/get/{rid}/{rid}/1200?source=wapyy&callback=jsonp3'.format(rid=room_id)
    headers = {
        'referer': 'http://wap.yy.com/mobileweb/{rid}'.format(rid=room_id),
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
        }
    try:
        r = get_html(room_url, ua=str(headers))
        json_data = json.loads(re.findall(r'\(([\W\w]*)\)', r)[0])
        real_url = json_data.get('hls', 0)
        if not real_url:
            dialog = xbmcgui.Dialog()
            dialog.notification('获取直播源地址失败', '可能房间号不存在未开播', xbmcgui.NOTIFICATION_INFO, 5000,False)
        else:
            return real_url
    except:
        dialog = xbmcgui.Dialog()
        dialog.notification('获取直播源地址失败', '可能房间号不存在未开播', xbmcgui.NOTIFICATION_INFO, 5000,False)

#快手
def get_kuaishou_categories():
    return [{'name':'和平精英','link':'SYXX,22008'},
            {'name':'王者荣耀','link':'SYXX,1001'},
            {'name':'火影忍者','link':'SYXX,1011'},
            {'name':'QQ飞车','link':'SYXX,1054'},
            {'name':'第五人格','link':'SYXX,22018'},
            {'name':'棋牌游戏','link':'WYJJ,100004'},
            {'name':'穿越火线','link':'WYJJ,2'},
            {'name':'英雄联盟','link':'WYJJ,1'},
            {'name':'lol云顶之弈','link':'WYJJ,22103'},
            {'name':'梦幻西游','link':'WYJJ,22'},
            {'name':'使命召唤战区','link':'DJRY,22130'},
            {'name':'绝地求生','link':'DJRY,21'},
            {'name':'怀旧经典','link':'DJRY,100017'},
            {'name':'最后的绿洲','link':'DJRY,22137'},
            {'name':'主机新游','link':'DJRY,22088'}]
def get_kuaishou_rooms(url,page):
    rooms = []
    url = url.split(',')
    data = {'operationName':'LiveCardQuery','variables':{'type':url[0],'gameId':url[1],'currentPage':2,'pageSize':60},'query':'query LiveCardQuery($gameId: String, $type: String, $heroType: String, $heroName: String, $currentPage: Int, $pageSize: Int) {\n  liveCardList(gameId: $gameId, type: $type, heroType: $heroType, heroName: $heroName, currentPage: $currentPage, pageSize: $pageSize) {\n    list {\n      user {\n        id\n        avatar\n        name\n        __typename\n      }\n      watchingCount\n      poster\n      coverUrl\n      caption\n      id\n      playUrls {\n        quality\n        url\n        __typename\n      }\n      quality\n      gameInfo {\n        category\n        name\n        pubgSurvival\n        type\n        kingHero\n        __typename\n      }\n      hasRedPack\n      liveGuess\n      expTag\n      __typename\n    }\n    totalPage\n    __typename\n  }\n}\n'}
    r = post_html('https://live.kuaishou.com/m_graphql',data=str(data),json='on')
    j = json.loads(r)
    rlist = j['data']['liveCardList']['list']
    for i in range(len(rlist)):
        roomitem = {}
        if rlist[i]['caption'] != None:
            roomitem['name'] = rlist[i]['caption']
        else:
            roomitem['name'] = rlist[i]['user']['name'] + u'的直播间'
        roomitem['href'] =  rlist[i]['user']['id']
        roomitem['thumb'] = rlist[i]['poster']
        roomitem['info'] = {'plot' : zh(rlist[i]['watchingCount']) + u' 人气 · 房间号 ' + rlist[i]['user']['id'],'cast':[(rlist[i]['user']['name'],u'主播')],'genre':[rlist[i]['gameInfo']['name']]}
        rooms.append(roomitem)
    return rooms

@plugin.cached(TTL=1)
def get_kuaishou_roomidinfo(rid):
    di = {}
    ah = mheaders
    ah['cookie'] = 'did=web_c613143f98204d43a31bd72afef990fc'
    r = requests.get('https://m.gifshow.com/fw/live/'+ str(rid),headers=ah)
    r.encoding = 'utf-8'
    r = r.text
    soup = BeautifulSoup(r,'html.parser')
    vid = soup.find('video')
    di['title'] = vid['alt']
    di['img'] = vid['poster']
    di['plot'] = u'房间号 ' + rid
    return di
@plugin.cached(TTL=1)
def get_kuaishou_roomid(rid):
    ah = mheaders
    ah['cookie'] = 'did=web_c613143f98204d43a31bd72afef990fc'
    r = requests.get('https://m.gifshow.com/fw/live/'+ str(rid),headers=ah)
    r.encoding = 'utf-8'
    #r = r.text
    #str1 = r.find('window.__APOLLO_STATE__={')
    #str2 = r.find(';(function()')
    
    #cut = r[str1+24:str2]
    i = re.search('https?://\S+m3u8',r.text).group()
    i = re.sub('_sd1000tp','',i)
    dialog = xbmcgui.Dialog()
    dialog.textviewer('获取', str(i.encode('utf-8')))
    return i
    #j = json.loads(cut)
    #i = j['clients']['graphqlServerClient']['$ROOT_QUERY.webLiveDetail({"principalId":"'+rid+'"})']['liveStream']['json']['playUrls'][0]['url']
    #dialog = xbmcgui.Dialog()
    #dialog.textviewer('获取', str(i.encode('utf-8')))


        # room_url = 'https://m.gifshow.com/fw/live/' + str(rid)
        # r = requests.get(room_url,headers=mheaders,cookies={'did':'web_c613143f98204d43a31bd72afef990fc'})
        # dialog = xbmcgui.Dialog()
        # dialog.textviewer('获取', str(r.cookies))
        # soup = BeautifulSoup(r.text,'html.parser')
        # real_url = soup.find('video')['src']
    
    #return i.encode('utf-8')

#acfun
def get_acfun_categories():
    return []
def get_acfun_roomid(url):
    if 'm.acfun.com' in url:
        if 'live/detail' in url:
            room_id = re.search('(?<=detail/)[0-9]+',url).group()
        dialog = xbmcgui.Dialog()
        dialog.notification('提取成功','房间号：' + str(room_id), xbmcgui.NOTIFICATION_INFO, 5000)
    else:
        room_id = url
    data = {'authorId':room_id,'pullStreamType':'SINGLE_HLS'}
    r = post_html('https://api.kuaishouzt.com/rest/zt/live/web/startPlay?subBiz=mainApp&kpn=ACFUN_APP&kpf=OUTSIDE_ANDROID_H5&userId=1000000039258966&did=H5_838414230312ED6F&acfun.api.visitor_st=ChRhY2Z1bi5hcGkudmlzaXRvci5zdBJwe85FKluHmFKAbPx7tfh-zqLMs8HoVSVOW_nTwPGM-t00Ka_kd7ZQp_rofsYJvMM3I9wrdTIcPbXkb7yunw4gYC2ZbB11Go6OVAaETEuDzPYnLdd1Go2JrpvmsQ9O5ZuhKbapThOUkwirpO2UEMe2ZxoSVVXIQ734h7MpAYWDHy8uAC9cIiDMon1x1tPW2KP3glAjYExkYDzqEYKPoQaLbOpwcONucSgFMAE',str(data),ua='mobile')
    
    j = json.loads(r)
    if j['result'] == 1:
        live = j['data']['videoPlayRes']
        live = re.search('http[\S]+m3u8',live).group()
        if '_sd1000' in live:
            live = live.replace('_sd1000','')
    else:
        dialog = xbmcgui.Dialog()
        dialog.notification('提取直播间地址失败','可能未开播', xbmcgui.NOTIFICATION_INFO, 5000)
    return live

#央视频
def get_yangshipin_categories():
    return [{'name':'直播列表','link':'x'}]
    
def get_yangshipin_rooms(url,page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like HeiNiaoPlayer) Chrome/72.0.3626.119 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'https://www.guihet.com/',
        'Accept-Language': 'zh-cn,en-us;q=0.5',
        'Boke': 'https://www.guihet.com/',
        'Host': 'guihet.com'
    }
    html = requests.get('https://guihet.com/download/teleplayer/bin/netlist.php',headers = headers)
    #html = requests.get('https://gitee.com/FadedJay/reallive/raw/master/tv.m3u8')
    m3u = html.text
    rooms = []
    rlist = m3u.split('\n')
    for i in range(len(rlist)):
        roomitem = {}
        if "," in rlist[i]:
            rr = rlist[i].split(',')
            roomitem['name'] = rr[0]
            roomitem['href'] = re.search(r'((http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?)',rlist[i]).group()
            roomitem['thumb'] = ''
            roomitem['info'] = {}
            rooms.append(roomitem)
    return rooms

def get_yangshipin_roomid(url):
    return url

#直播中国
def get_livechina_categories():
    return [{'name':'直播列表','link':'x'}]
    
def get_livechina_rooms(url,page):
    m3u = '''西藏珠峰观景台,https://gcalic.v.myalicdn.com/gc/bgwn10_1/index.m3u8
远眺珠峰,https://gctxyc.liveplay.myqcloud.com/gc/tyhjrys_1/index.m3u8
贵州省遵义市枫香镇花茂村,https://gcksc.v.kcdnvip.com/gc/dxssyt_1/index.m3u8
甘肃省定西市渭源县元古堆村,https://gcalic.v.myalicdn.com/gc/lhssjzd_1/index.m3u8
甘肃省武威市古浪县黄花滩生态移民区富民新村,https://gcalic.v.myalicdn.com/gc/hsxkssqdzrqj_1/index.m3u8
宁夏固原市原州区彭堡镇姚磨村,https://gctxyc.liveplay.myqcloud.com/gc/ztb_1/index.m3u8
宁夏固原市泾源县大湾乡杨岭村,https://gcksc.v.kcdnvip.com/gc/ztn_1/index.m3u8
甘肃省临夏回族自治州东乡族自治县布楞沟村,https://gcksc.v.kcdnvip.com/gc/hsxkscj_1/index.m3u8
河北省张家口市张北县小二台镇德胜村,https://gctxyc.liveplay.myqcloud.com/gc/pygc01_1/index.m3u8
山西省忻州市岢岚县宋家沟乡宋家沟村,https://gctxyc.liveplay.myqcloud.com/gc/wysdhpcy_1/index.m3u8
安徽省六安市金寨县花石乡大湾村,https://gcalic.v.myalicdn.com/gc/szgk01_1/index.m3u8
重庆市石柱县中益乡华溪村,https://gcalic.v.myalicdn.com/gc/jsh02_1/index.m3u8
湖北荆门樱花部落,https://gcksc.v.kcdnvip.com/gc/jyg04_1/index.m3u8
鼋头渚赏樱阁,https://gctxyc.liveplay.myqcloud.com/gc/pshdxg01_1/index.m3u8
鼋头渚长春桥,https://gcksc.v.kcdnvip.com/gc/dlst02_1/index.m3u8
北京南宫温泉休闲度假区-五洲植物乐园,https://gcksc.v.kcdnvip.com/gc/tyhjntyz_1/index.m3u8
四川省阿坝州金川县世外梨园景区,https://gctxyc.liveplay.myqcloud.com/gc/hnttlhzjd_1/index.m3u8
云栖小镇,https://gccncc.v.wscdns.com/gc/hnttpgsz_1/index.m3u8
江西省井冈山市茅坪乡神山村,https://gcalic.v.myalicdn.com/gc/wysyxdhp_1/index.m3u8
天山（海西平台）,https://gcalic.v.myalicdn.com/gc/xjtchxpt_1/index.m3u8
天山（定海神针）,https://gctxyc.liveplay.myqcloud.com/gc/xjtcdhsz_1/index.m3u8
天山（马牙山）,https://gcalic.v.myalicdn.com/gc/xjtcmys_1/index.m3u8
天山（灯杆山）,https://gccncc.v.wscdns.com/gc/xjtcdgs_1/index.m3u8
重庆轨道交通2号线李子坝站,https://gccncc.v.wscdns.com/gc/gccntv240-lzb01_1/index.m3u8
国家游泳中心（水立方）,https://gcalic.v.myalicdn.com/gc/gccntv241-slf01_1/index.m3u8'''

    # rinfo = [{'thumb':'https://p1.img.cctvpic.com/photoworkspace/2020/04/24/2020042414461116536.jpg','info':{'plot':'西藏珠峰观景台','genre':'西藏珠峰观景台'}},
    #          {'thumb':'https://p3.img.cctvpic.com/photoworkspace/2020/04/22/2020042219054892015.jpg','info':{'plot':'远眺珠峰','genre':'西藏珠峰观景台'}},
    #          {'thumb':'https://p2.img.cctvpic.com/photoworkspace/2020/04/12/2020041200492825759.jpg','info':{'plot':'贵州省遵义市枫香镇花茂村','genre':'扶贫足迹'}},
    #          {'thumb':'https://p3.img.cctvpic.com/photoworkspace/2020/04/12/2020041200495613473.jpg','info':{'plot':'甘肃省定西市渭源县元古堆村','genre':'扶贫足迹'}},
    #          {'thumb':'https://p3.img.cctvpic.com/photoworkspace/2020/04/12/2020041200502074107.jpg','info':{'plot':'甘肃省武威市古浪县黄花滩生态移民区富民新村','genre':'扶贫足迹'}},
    #          {'thumb':'https://p1.img.cctvpic.com/photoworkspace/2020/04/14/2020041409250316875.jpg','info':{'plot':'宁夏固原市原州区彭堡镇姚磨村','genre':'扶贫足迹'}},
    #          {'thumb':'https://p4.img.cctvpic.com/photoworkspace/2020/04/14/2020041409272290684.jpg','info':{'plot':'宁夏固原市泾源县大湾乡杨岭村','genre':'扶贫足迹'}},
    #          {'thumb':'https://p4.img.cctvpic.com/photoworkspace/2020/04/12/2020041200505363218.jpg','info':{'plot':'甘肃省临夏回族自治州东乡族自治县布楞沟村','genre':'扶贫足迹'}},
    #          {'thumb':'https://p2.img.cctvpic.com/photoworkspace/2019/12/09/2019120912101082657.jpg','info':{'plot':'河北省张家口市张北县小二台镇德胜村','genre':'扶贫足迹'}},
    #          {'thumb':'https://p4.img.cctvpic.com/photoworkspace/2019/12/09/2019120912233447088.jpg','info':{'plot':'山西省忻州市岢岚县宋家沟乡宋家沟村','genre':'扶贫足迹'}},
    #          {'thumb':'https://p1.img.cctvpic.com/photoworkspace/2020/04/12/2020041200483967841.jpg','info':{'plot':'安徽省六安市金寨县花石乡大湾村','genre':'扶贫足迹'}},
    #          {'thumb':'https://p5.img.cctvpic.com/photoworkspace/2020/04/12/2020041200490210564.jpg','info':{'plot':'重庆市石柱县中益乡华溪村','genre':'扶贫足迹'}},
    #          {'thumb':'https://p3.img.cctvpic.com/photoworkspace/2020/03/20/2020032015394958429.jpg','info':{'plot':'荆门樱花部落','genre':'湖北荆门樱花部落'}},
    #          {'thumb':'https://p1.img.cctvpic.com/photoworkspace/2020/03/20/2020032015301459754.jpg','info':{'plot':'鼋头渚赏樱阁','genre':'无锡鼋头渚'}},
    #          {'thumb':'https://p2.img.cctvpic.com/photoworkspace/2020/03/20/2020032015310841622.jpg','info':{'plot':'鼋头渚长春桥','genre':'无锡鼋头渚'}},
    #          {'thumb':'https://p1.img.cctvpic.com/photoworkspace/2020/03/10/2020031010193055329.jpg','info':{'plot':'北京南宫温泉休闲度假区-五洲植物乐园','genre':'北京南宫温泉休闲度假区'}},
    #          {'thumb':'https://p2.img.cctvpic.com/photoworkspace/2020/03/03/2020030313154858134.jpg','info':{'plot':'四川省阿坝州金川县世外梨园景区','genre':'四川金川县梨花花海'}},
    #          {'thumb':'https://p1.img.cctvpic.com/photoworkspace/2019/12/16/2019121617173198872.jpg','info':{'plot':'云栖小镇','genre':'浙江杭州云栖小镇'}},
    #          {'thumb':'https://p1.img.cctvpic.com/photoworkspace/2020/03/10/2020031010193055329.jpg','info':{'plot':'北京南宫温泉休闲度假区-五洲植物乐园','genre':'北京南宫温泉休闲度假区'}},
    #          {'thumb':'https://p2.img.cctvpic.com/photoworkspace/2019/10/12/2019101218001699134.jpg','info':{'plot':'天山（海西平台）','genre':'北京南宫温泉休闲度假区'}},
    #          {'thumb':'https://p1.img.cctvpic.com/photoworkspace/2020/03/10/2020031010193055329.jpg','info':{'plot':'北京南宫温泉休闲度假区-五洲植物乐园','genre':'北京南宫温泉休闲度假区'}},
    #          {'thumb':'https://p2.img.cctvpic.com/photoworkspace/2019/10/12/2019101218001699134.jpg','info':{'plot':'天山（海西平台）','genre':'北京南宫温泉休闲度假区'}},
    #          {'thumb':'https://p1.img.cctvpic.com/photoworkspace/2020/03/10/2020031010193055329.jpg','info':{'plot':'北京南宫温泉休闲度假区-五洲植物乐园','genre':'北京南宫温泉休闲度假区'}},
    #          {'thumb':'https://p2.img.cctvpic.com/photoworkspace/2019/10/12/2019101218001699134.jpg','info':{'plot':'天山（海西平台）','genre':'北京南宫温泉休闲度假区'}},
    #          {'thumb':'https://p1.img.cctvpic.com/photoworkspace/2020/03/10/2020031010193055329.jpg','info':{'plot':'北京南宫温泉休闲度假区-五洲植物乐园','genre':'北京南宫温泉休闲度假区'}},
    #          {'thumb':'https://p2.img.cctvpic.com/photoworkspace/2019/10/12/2019101218001699134.jpg','info':{'plot':'天山（海西平台）','genre':'北京南宫温泉休闲度假区'}},
    #          {'thumb':'https://p1.img.cctvpic.com/photoworkspace/2020/03/10/2020031010193055329.jpg','info':{'plot':'北京南宫温泉休闲度假区-五洲植物乐园','genre':'北京南宫温泉休闲度假区'}},
    #          {'thumb':'https://p2.img.cctvpic.com/photoworkspace/2019/10/12/2019101218001699134.jpg','info':{'plot':'天山（海西平台）','genre':'北京南宫温泉休闲度假区'}},
    #          {'thumb':'https://p1.img.cctvpic.com/photoworkspace/2020/03/10/2020031010193055329.jpg','info':{'plot':'北京南宫温泉休闲度假区-五洲植物乐园','genre':'北京南宫温泉休闲度假区'}},
    #          {'thumb':'https://p2.img.cctvpic.com/photoworkspace/2019/10/12/2019101218001699134.jpg','info':{'plot':'天山（海西平台）','genre':'北京南宫温泉休闲度假区'}},
    #          {'thumb':'https://p1.img.cctvpic.com/photoworkspace/2020/03/10/2020031010193055329.jpg','info':{'plot':'北京南宫温泉休闲度假区-五洲植物乐园','genre':'北京南宫温泉休闲度假区'}},
    #          {'thumb':'https://p2.img.cctvpic.com/photoworkspace/2019/10/12/2019101218001699134.jpg','info':{'plot':'天山（海西平台）','genre':'北京南宫温泉休闲度假区'}},
    #          {'thumb':'https://p1.img.cctvpic.com/photoworkspace/2020/03/10/2020031010193055329.jpg','info':{'plot':'北京南宫温泉休闲度假区-五洲植物乐园','genre':'北京南宫温泉休闲度假区'}},
    #          {'thumb':'https://p2.img.cctvpic.com/photoworkspace/2019/10/12/2019101218001699134.jpg','info':{'plot':'天山（海西平台）','genre':'北京南宫温泉休闲度假区'}},
    #          {'thumb':'https://p1.img.cctvpic.com/photoworkspace/2020/03/10/2020031010193055329.jpg','info':{'plot':'北京南宫温泉休闲度假区-五洲植物乐园','genre':'北京南宫温泉休闲度假区'}},
    #          {'thumb':'https://p2.img.cctvpic.com/photoworkspace/2019/10/12/2019101218001699134.jpg','info':{'plot':'天山（海西平台）','genre':'北京南宫温泉休闲度假区'}},
    #          {'thumb':'https://p1.img.cctvpic.com/photoworkspace/2020/03/10/2020031010193055329.jpg','info':{'plot':'北京南宫温泉休闲度假区-五洲植物乐园','genre':'北京南宫温泉休闲度假区'}},
    #          {'thumb':'https://p2.img.cctvpic.com/photoworkspace/2019/10/12/2019101218001699134.jpg','info':{'plot':'天山（海西平台）','genre':'北京南宫温泉休闲度假区'}},
    #          {'thumb':'https://p1.img.cctvpic.com/photoworkspace/2020/03/10/2020031010193055329.jpg','info':{'plot':'北京南宫温泉休闲度假区-五洲植物乐园','genre':'北京南宫温泉休闲度假区'}},
    #          {'thumb':'https://p2.img.cctvpic.com/photoworkspace/2019/10/12/2019101218001699134.jpg','info':{'plot':'天山（海西平台）','genre':'北京南宫温泉休闲度假区'}},
    #          {'thumb':'https://p1.img.cctvpic.com/photoworkspace/2020/03/10/2020031010193055329.jpg','info':{'plot':'北京南宫温泉休闲度假区-五洲植物乐园','genre':'北京南宫温泉休闲度假区'}}]
    # tmp['livechinaroomsinfo'] = rinfo
    rooms = []
    rlist = m3u.split('\n')
    for i in range(len(rlist)):
        roomitem = {}
        rr = rlist[i].split(',')
        roomitem['name'] = rr[0]
        roomitem['href'] =  rr[1]
        roomitem['thumb'] = '' #rinfo[i]['thumb']
        roomitem['info'] = {} #rinfo[i]['info']
        rooms.append(roomitem)
    return rooms

def get_livechina_roomid(url):
    return url

#熊猫频道
def get_ipanda_categories():
    return [{'name':'直播列表','link':'x'}]
    
def get_ipanda_rooms(url,page):
    m3u = '''【成都】24H高清,http://gcalic.v.myalicdn.com/gc/ipanda_1/index.m3u8
【都江堰】24H高清,http://gcalic.v.myalicdn.com/gc/ipanda1000_1/index.m3u8
【都江堰】泰山,http://gcalic.v.myalicdn.com/gc/xiongmao13_1/index.m3u8
【都江堰】青青,http://gcksc.v.kcdnvip.com/gc/xiongmao20_1/index.m3u8
【神树坪】神树坪幼儿园A,http://gctxyc.liveplay.myqcloud.com/gc/xiongmao25_1/index.m3u8
【都江堰】京宝+离堆,http://gcalic.v.myalicdn.com/gc/xiongmao15_1/index.m3u8
【都江堰】晔晔,http://gcalic.v.myalicdn.com/gc/xiongmao11_1/index.m3u8
【都江堰】英英,http://gcdnc.v.dwion.com/gc/xiongmao16_1/index.m3u8
【神树坪】神树坪幼儿园B,http://gctxyc.liveplay.myqcloud.com/gc/xiongmao26_1/index.m3u8
【都江堰】兴安+玉垒,http://gctxyc.liveplay.myqcloud.com/gc/xiongmao12_1/index.m3u8
【都江堰】酋酋+华鸿,http://gcalic.v.myalicdn.com/gc/xiongmao14_1/index.m3u8
【神树坪】神树坪幼儿园C,http://gcalic.v.myalicdn.com/gc/xiongmao22_1/index.m3u8
【成都】幼年园A,http://gctxyc.liveplay.myqcloud.com/gc/xiongmao03_1/index.m3u8
【成都】幼年园B,http://gctxyc.liveplay.myqcloud.com/gc/xiongmao04_1/index.m3u8
【成都】幼儿园A,http://gcksc.v.kcdnvip.com/gc/xiongmao05_1/index.m3u8
【成都】幼儿园B,http://gcalic.v.myalicdn.com/gc/xiongmao06_1/index.m3u8
【成都】成年园A,http://gccncc.v.wscdns.com/gc/xiongmao01_1/index.m3u8
【成都】成年园B,http://gctxyc.liveplay.myqcloud.com/gc/xiongmao02_1/index.m3u8
【成都】一号别墅A,http://gcalic.v.myalicdn.com/gc/xiongmao09_1/index.m3u8
【成都】一号别墅B,http://gcksc.v.kcdnvip.com/gc/xiongmao10_1/index.m3u8
【成都】母子园A,http://gccncc.v.wscdns.com/gc/xiongmao07_1/index.m3u8
【成都】母子园B,http://gcksc.v.kcdnvip.com/gc/xiongmao08_1/index.m3u8
【卧龙】臭水,http://gcksc.v.kcdnvip.com/gc/xiongmao17_1/index.m3u8'''
    rooms = []
    rlist = m3u.split('\n')
    for i in range(len(rlist)):
        roomitem = {}
        rr = rlist[i].split(',')
        roomitem['name'] = rr[0]
        roomitem['href'] =  rr[1]
        roomitem['thumb'] = ''
        roomitem['info'] = {}
        rooms.append(roomitem)
    return rooms

def get_ipanda_roomid(url):
    return url
#it之家    
def get_ithome_categories():
    return [{'name':'直播列表','link':'https://www.ithome.com/live/'}]

def get_ithome_rooms(url,page):
    rooms = []
    if page == 1:
        r = get_html(url,encode='gbk')
    else:
        data = str({'domain':'live','type':'collectionpage','ot':str(tmp['ithomeot'])})
        r = post_html('https://www.ithome.com/ithome/getajaxdata.aspx',data)
    
    soup = BeautifulSoup(r,'html.parser')
    if page == 1:
        ul = soup.find('ul',class_='ulcl')
        rlist = ul.find_all('li')
        for i in range(len(rlist)):
            roomitem = {}
            roomitem['name'] = rlist[i].find('h2').a.text + rlist[i].find('h2').span.text
            roomitem['href'] =  rlist[i].a['href']
            roomitem['thumb'] = 'http:' + rlist[i].find('img')['data-original']
            roomitem['info'] = {'plot' : rlist[i].find('div',class_='memo').p.text,'genre':[rlist[i].find('span',class_='tags').a.text]}
            ts = time.strptime(rlist[i].find('div',class_='block')['data-ot'], "%Y/%m/%d %H:%M:%S")
            # 格式化时间转时间戳
            tmp['ithomeot'] = int(time.mktime(ts)*1000)
            rooms.append(roomitem)
    else:
        rlist = soup.find_all('li')
        for i in range(len(rlist)):
            roomitem = {}
            roomitem['name'] = rlist[i].find('h2').a.text + rlist[i].find('h2').span.text
            roomitem['href'] =  rlist[i].a['href']
            roomitem['thumb'] = rlist[i].find('img')['src']
            roomitem['info'] = {'plot' : rlist[i].find('div',class_='memo').p.text,'genre':[rlist[i].find('span',class_='tags').a.text]}
            ts = time.strptime(rlist[i].find('div',class_='block')['data-ot'], "%Y/%m/%d %H:%M:%S")
            # 格式化时间转时间戳
            tmp['ithomeot'] = int(time.mktime(ts)*1000)
            if i == 19:
                dialog = xbmcgui.Dialog()
                ok = dialog.ok('提取成功',str(tmp['ithomeot']))
            rooms.append(roomitem)

    return rooms
def get_ithome_roomid(url):
    if 'ithome.com' in url:
        if re.search('(?<=live.ithome.com/item/)[0-9]+',url):
            room_id = re.search('(?<=live.ithome.com/item/)[0-9]+',url).group()
        dialog = xbmcgui.Dialog()
        dialog.notification('提取成功','房间号：' + str(room_id), xbmcgui.NOTIFICATION_INFO, 5000)
    else:
        room_id = url
    r = get_html('https://live.ithome.com/item/' + room_id + '.htm')
    str1 = r.find('var flvUrl = ')
    str2 = r.find('var player = videojs(')
    rt = r[str1+13:str2].strip()[+1:-2]
    #dialog = xbmcgui.Dialog()
    #dialog.textviewer('获取', str(rt))
    return rt
##########################################################
###以下是核心代码区，看不懂的请勿修改
##########################################################

def get_rooms(url,mode,page):
    videos = get_rooms_mode(url,mode,page)
    items = []
    if 'info' in videos[0]:
        for video in videos:
            info = video['info']
            info['mediatype'] = 'video'
            items.append({'label': video['name'],
            'path': plugin.url_for('roomid', value=video['href'], mode=mode),
    	'thumbnail': video['thumb'],
            'icon': video['thumb'],
            'info': info,
        })
    else:
        for video in videos:
            items.append({'label': video['name'],
            'path': plugin.url_for('roomid', value=video['href'], mode=mode),
    	'thumbnail': video['thumb'],
            'icon': video['thumb'],
        })

    categories = get_categories()
    for index in range(len(categories)):
        if mode == categories[index]['link']:
            if 'rooms' in categories[index]:
                if int(categories[index]['rooms']) == len(videos):
                    items.append({
                        'label': '[COLOR yellow]下一页[/COLOR]',
                        'path': plugin.url_for('rooms',url=url,mode=mode,page=int(int(page)+1)),
                    })
    return items

@plugin.route('/rooms/<url>/<mode>/<page>/')
def rooms(url,mode,page):
    items = get_rooms(url,mode,page)
    return items

@plugin.route('/home/<mode>/')
def home(mode):
    categories = get_categories_mode(mode)
    items = []
    for category in categories:
        items.append({
        'label': category['name'],
        'path': plugin.url_for('rooms', url=category['link'],mode=mode,page=1),
    })
    if len(items) == 1:
        items = get_rooms(categories[0]['link'],mode,1)
        return items
        
    try:
        eval('get_' + mode + '_search')
        items.append({
            'label': '[COLOR yellow]搜索[/COLOR]',
            'path': plugin.url_for('history',name='搜索',url='search',mode=mode),
        })
    except NameError:
        pass
    try:
        ri = 'n'
        eval('get_' + mode + '_roomid')
        cate = get_categories()
        for i in range(len(cate)):
            if cate[i]['link'] == mode:
                if 'roomid' in cate[i]:
                    if cate[i]['roomid'] != 'false':
                        ri = 'y'
                else:
                    ri = 'y'

        if ri == 'y':
            items.append({
                'label': '[COLOR yellow]复制粘贴链接或者输入房间号进入直播[/COLOR]',
                'path': plugin.url_for('history',name='复制粘贴链接或者输入房间号进入直播',url=mode + 'roomid',mode=mode),
            })
    except NameError:
        pass
    
    return items

@plugin.route('/search/<value>/<page>/<mode>/')
def search(value,page,mode):
    if value == 'null':
        keyboard = xbmc.Keyboard('', '请输入搜索内容')
        xbmc.sleep(1500)
        keyboard.doModal()
        hi = his['search']
        if (keyboard.isConfirmed()):
            keyword = keyboard.getText()
            if keyword != '':
                hi[keyword] = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    else:
        keyword = value
    videos = get_search_mode(keyword,page,mode)
    items = []
    if videos != []:
        if 'info' in videos[0]:
            for video in videos:
                info = video['info']
                info['mediatype'] = 'video'
                items.append({'label': video['name'],
                'path': plugin.url_for('roomid',value=video['href'], mode=mode),
    	    'thumbnail': video['thumb'],
                'icon': video['thumb'],
                'info': info,
            })
        else:
            for video in videos:
                items.append({'label': video['name'],
                'path': plugin.url_for('roomid', value=video['href'], mode=mode),
    	    'thumbnail': video['thumb'],
                'icon': video['thumb'],
            })
    
    categories = get_categories()
    for index in range(len(categories)):
        if mode == categories[index]['link']:
            if 'search' in categories[index]:
                if int(categories[index]['search']) == len(videos):
                    nextpage = {'label': '[COLOR yellow]下一页[/COLOR]', 'path': plugin.url_for('search', value=keyword,mode=mode,page=str(int(page)+1))}
                    items.append(nextpage)
    return items

@plugin.route('/roomid/<value>/<mode>/')
def roomid(value,mode):
    roomurl = ''
    if value == 'null':
        keyboard = xbmc.Keyboard('', '复制粘贴链接或者输入房间号进入直播\n')
        xbmc.sleep(1500)
        keyboard.doModal()
        hi = his[mode+'roomid']
        if (keyboard.isConfirmed()):
            roomurl = keyboard.getText()
            if roomurl != '':
                hi[roomurl] = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    else:
        roomurl = value
    if roomurl != '':
        liveurl = get_roomid_mode(roomurl,mode)
        try:
            rinfo = get_roomidinfo_mode(roomurl,mode)
            items = []
            rinfo['mediatype'] = 'video'
            if 'img' in rinfo:
                items.append({'label': rinfo['title'],
                    'thumbnail': rinfo['img'],
                    'icon': rinfo['img'],
                    'info' : rinfo,
                    'info_type' : 'video',
                    'properties':{'setCast':str([{"name": "Actor 1", "role": "role 1"}, {"name": "Actor 2", "role": "role 2"}])},
                    'path': liveurl + '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
                    'is_playable': True,
                })
            else:
                items.append({'label': rinfo['title'],
                    'info' : rinfo,
                    'info_type' : 'video',
                    'path': liveurl + '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
                    'is_playable': True,
                })
        except NameError:
            items = []
            rinfo = {}
            rinfo['mediatype'] = 'video'
            items.append({'label': '直播间',
                    'info' : rinfo,
                    'path': liveurl + '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
                    'is_playable': True,
            })
        return items

def get_key (dict, value):
  return [k for k, v in dict.items() if v == value]

@plugin.route('/history/<name>/<url>/<mode>/')
def history(name,url,mode):
    items = []
    if url == 'search':
        items.append({
            'label': '[COLOR yellow]'+ name +'[/COLOR]',
            'path': plugin.url_for(url,value='null',page=1,mode=mode),
        })
    else:
        items.append({
            'label': '[COLOR yellow]'+ name +'[/COLOR]',
            'path': plugin.url_for('roomid',value='null',mode=mode),
        })
    if url in his:
        hi = his[url]
    else:
        his[url] = {}
        hi = his[url]  
    #hi = []
    if hi:
        val = list(hi.values())
        val = sorted(val,reverse=True)
        for index in range(len(val)):
            if url == 'search':
                items.append({
                    'label': name+ ':' +get_key(hi,val[index])[0] + ' - [查询时间：' + val[index] +']',
                    'path': plugin.url_for(url,value=get_key(hi,val[index])[0],page=1,mode=mode),
                })
            else:
                items.append({
                    'label': name+ ':' +get_key(hi,val[index])[0] + ' - [查询时间：' + val[index] +']',
                    'path': plugin.url_for('roomid',value=get_key(hi,val[index])[0],mode=mode),
                })
        items.append({
            'label': '[COLOR yellow]清除历史记录[/COLOR]',
            'path': plugin.url_for('cleanhis',url=url),
        })
    else:
        items.append({
            'label': '[COLOR yellow]历史记录为空[/COLOR]',
            'path': plugin.url_for(ok,value='历史记录为空'),
        })

    return items

@plugin.route('/ok/<value>/')
def ok(value):
    dialog = xbmcgui.Dialog()
    ok = dialog.ok('提示', value)

@plugin.route('/cleanhis/<url>/')
def cleanhis(url):
    his[url] = {}
    dialog = xbmcgui.Dialog()
    ok = dialog.ok('提示', '清理历史记录成功')

@plugin.route('/')
def index():
    if 'homesort' in storage:
        #用户设置的列表
        nlist = []
        for index in range(len(storage['homesort'])):
            nlist.append(storage['homesort'][index]['link'])
        nlist = set(nlist)
        #默认列表
        glist = []
        for index in range(len(get_categories())):
            glist.append(get_categories()[index]['link'])
        glist = set(glist)
        if nlist != glist:
            if len(glist)-len(nlist) > 0:
                h = '新增 '+str(len(glist)-len(nlist))
            else:
                h = '删减 '+str(abs(len(glist)-len(nlist)))
            newhomesort = []
            for index in range(len(get_categories())):
                vlist = {}
                vlist['id'] = get_categories()[index]['id']
                vlist['name'] = get_categories()[index]['name']
                vlist['link'] = get_categories()[index]['link']
                vlist['author'] = get_categories()[index]['author']
                vlist['upload'] = get_categories()[index]['upload']
                if 'plot' in get_categories()[index]:
                    vlist['plot'] = get_categories()[index]['plot']
                for i in range(len(storage['homesort'])):
                    if storage['homesort'][i]['link'] == get_categories()[index]['link']:
                        vlist['id'] = storage['homesort'][i]['id']
                        #vlist['name'] = storage['homesort'][i]['name']
                        #vlist['link'] = storage['homesort'][i]['link']
                newhomesort.append(vlist)
            storage['homesort'] = newhomesort
            categories = sorted(newhomesort,key=lambda k:k.get('id'))
            dialog = xbmcgui.Dialog()
            dialog.notification('首页已更新', h +'个网站', xbmcgui.NOTIFICATION_INFO, 5000)
        else:
            newhomesort = []
            for index in range(len(get_categories())):
                vlist = {}
                vlist['id'] = get_categories()[index]['id']
                vlist['name'] = get_categories()[index]['name']
                vlist['link'] = get_categories()[index]['link']
                vlist['author'] = get_categories()[index]['author']
                vlist['upload'] = get_categories()[index]['upload']
                if 'plot' in get_categories()[index]:
                    vlist['plot'] = get_categories()[index]['plot']
                for i in range(len(storage['homesort'])):
                    if storage['homesort'][i]['link'] == get_categories()[index]['link']:
                        vlist['id'] = storage['homesort'][i]['id']
                        #vlist['name'] = storage['homesort'][i]['name']
                        #vlist['link'] = storage['homesort'][i]['link']
                newhomesort.append(vlist)
            storage['homesort'] = newhomesort
            categories = sorted(storage['homesort'],key=lambda k:k.get('id'))
    else:
        storage['homesort'] = get_categories()
        categories = sorted(get_categories(),key=lambda k:k.get('id'))

    items = []
    for category in categories:
        if category['id'] != 0:
            if 'plot' in category:
                items.append({
                'label': category['name'],
                'path': plugin.url_for('home',mode=category['link']),
                'info': {'plot':'@[COLOR blue]' + category['author'] + '[/COLOR]'  + ':\n\n    ' + category['plot'],'status':category['upload']+ ' 更新','cast':[(category['author'],'插件作者')],'mediatype':'video'},
                })
            else:
                items.append({
                    'label': category['name'],
                    'path': plugin.url_for('home',mode=category['link']),
                    'info': {'status':category['upload']+ '更新','cast':[(category['author'],'插件作者')],'mediatype':'video'},
                })
    items.append({
        'label': u'[COLOR yellow]设置[/COLOR]',
        'path': plugin.url_for('setting'),
    })
    
    return items

@plugin.route('/setting')
def setting():
    items = []
    items.append({
        'label': u'首页排序与屏蔽',
        'path': plugin.url_for('homesort'),
    })
    items.append({
        'label': u'关键词过滤 - 符合关键词的文字被替换成*，但是视频仍然显示在视频列表',
        'path': plugin.url_for('keyword',key='keyword',name='关键词过滤'),
    })
    items.append({
        'label': u'黑名单屏蔽 - 符合关键词的内容将不显示在视频列表中',
        'path': plugin.url_for('keyword',key='blacklist',name='黑名单屏蔽'),
    })
    return items

@plugin.route('/homesort')
def homesort():
    items = []
    if 'homesort' in storage:
        hlist = sorted(storage['homesort'],key=lambda k:k.get('id'))
        for index in range(len(hlist)):
            items.append({
                'label':'id:' + str(hlist[index]['id']) + ' - ' + hlist[index]['name'],
                'path':plugin.url_for('homeedit',value=hlist[index]['link']),
            })
    else:
        hhlist = get_categories()
        hlist = sorted(hhlist,key=lambda k:k.get('id'))
        for index in range(len(hlist)):
            items.append({
                'label':'id:' + str(hlist[index]['id']) + ' - ' + hlist[index]['name'],
                'path':plugin.url_for('homeedit',value=hlist[index]['link']),
            })
        storage['homesort'] = hlist
    return items

@plugin.route('/homeedit/<value>/')
def homeedit(value):
    hlist = storage['homesort']
    for index in range(len(hlist)):
        if hlist[index]['link'] == value:
            dialog = xbmcgui.Dialog()
            d = dialog.input('--------修改id--------\nid从小到大排列，改为0不显示', defaultt=str(hlist[index]['id']),type=xbmcgui.INPUT_NUMERIC)
            if d != '' and int(d) != int(hlist[index]['id']):
                hlist[index]['id'] = int(d)
                dialog.notification('提示', '修改成功', xbmcgui.NOTIFICATION_INFO, 5000)



@plugin.route('/keyword/<key>/<name>')
def keyword(key,name):
    items = []
    items.append({
        'label': '[COLOR yellow]新增'+name+'[/COLOR]',
        'path': plugin.url_for('keywordxad',key=key,value='/null/',mode=3),
    })
    items.append({
        'label': '[COLOR yellow]' + name + ' (状态:'+chushihua(key+'switch',0) +')[/COLOR]',
        'path': plugin.url_for('switch',key=key+'switch'),
    })
    #storage['keyword'] = ['fuck','getout']
    if key in storage:
        ky = storage[key]
    else:
        ky = ['示例1','helloworld']
        storage[key] = ky
    
    for index in range(len(ky)):
        items.append({
            'label': ky[index],
            'path': plugin.url_for('keywordxad',key=key,value=ky[index],mode=0),
        })
    return items

@plugin.route('/keywordxad/<key>/<value>/<mode>/')
def keywordxad(key,value,mode):
    if int(mode) == 0:
        items = []
        items.append({
            'label': '修改 - ' +str(value),
            'path': plugin.url_for('keywordxad',key=key,value=value,mode=1),
        })
        items.append({
            'label': '删除 - ' +str(value),
            'path': plugin.url_for('keywordxad',key=key,value=value,mode=2),
        })
        return items
    #修改
    if int(mode) == 1:
        dialog = xbmcgui.Dialog()
        d = dialog.input('修改 '+ value, defaultt=value,type=xbmcgui.INPUT_ALPHANUM)
        ky = storage[key]
        if d != '':
            if d != value:
                ky.remove(value)
                ky.append(d)

                storage[key] = list(set(ky))
                dialog.notification('提示', '修改成功', xbmcgui.NOTIFICATION_INFO, 5000)
            
            
    #删除
    if int(mode) == 2:
        dialog = xbmcgui.Dialog()
        ret = dialog.yesno('确认删除吗？', '删除：' + value)
        if ret:
            ky = storage[key]
            ky.remove(value)
            storage[key] = list(set(ky))
            dialog = xbmcgui.Dialog()
            dialog.notification('提示', '删除成功', xbmcgui.NOTIFICATION_INFO, 5000)
    #新增
    if int(mode) == 3:
        dialog = xbmcgui.Dialog()
        d = dialog.input('新增关键词，多个请用英文逗号隔开',type=xbmcgui.INPUT_ALPHANUM)
        ky = storage[key]
        if d != '':
            if d.find(',') != -1:
                k = d.split(',')
                ky = k + ky
            else:
                ky.append(d)
            storage[key] = list(set(ky))
            dialog.notification('提示', '添加成功', xbmcgui.NOTIFICATION_INFO, 5000)


@plugin.route('/switch/<key>/')
def switch(key):
    if storage[key] == 1:
        storage[key] = 0
        dialog = xbmcgui.Dialog()
        dialog.notification('提示', '已关闭', xbmcgui.NOTIFICATION_INFO, 5000)
    else:
        storage[key] = 1
        dialog = xbmcgui.Dialog()
        dialog.notification('提示', '已开启', xbmcgui.NOTIFICATION_INFO, 5000)


@plugin.route('/labels/<label>/')
def show_label(label):
    # 写抓取视频类表的方法
    #
    items = [
        {'label': label},
    ]
    return items

if __name__ == '__main__':
    plugin.run()
