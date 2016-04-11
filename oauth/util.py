#coding:utf-8
import json
import urllib
import urllib2
from .models import OAuthUser

def get_info(access_token, uid):
    url = 'https://api.weibo.com/2/users/show.json'
    values = {
        'access_token': access_token,
        'uid': uid
    }
    data = urllib.urlencode(values)
    # data = data.encode('ascii')
    req = urllib2.Request(url + '?' + data)
    print('data:%s' % data)
    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print(e.read().decode('utf8'))
        return None
    r = response.read().decode('utf-8')
    result = json.loads(r)
    screen_name = result['screen_name']
    avatar = result['avatar_large']
    return {'name': screen_name, 'avatar': avatar}

def get_posts(access_token, uid):
    url = 'https://api.weibo.com/2/statuses/user_timeline.json'
    values = {
        'access_token': access_token,
        'uid': uid, 
        'trim_user': 1
    }
    data = urllib.urlencode(values)
    req = urllib2.Request(url + '?' + data)
    response = urllib2.urlopen(req)
    r = response.read().decode('utf-8')
    result = json.loads(r)['statuses']
    ret = [{'text': x['text'], 'created_at': x['created_at']} for x in result]
    return ret

def get_users(access_token):
    u = OAuthUser.objects.all()
    return [{'uid': x.user.username, 'access_token': x.access_token} for x in u]


def get_emotion(access_token, uid):
    r = get_posts(access_token, uid)
    happy = 0
    unhappy = 0
    na = 0
    for t in r:
        text = t['text']
        t = 0
        if text.find(u'[微笑]') != -1 or text.find(u'[嘻嘻]') != -1 or text.find(u'[哈哈]') != -1 or text.find(u'[笑哈哈]') != -1 or text.find(u'[可爱]') != -1 or text.find(u'[抱抱]') != -1 or text.find(u'[太开心]') != -1 or text.find(u'[亲亲]') != -1 or text.find(u'[憨笑]') != -1 or text.find(u'[偷笑]') != -1 or text.find(u'[爱你]') != -1  or text.find(u'[鼓掌]') != -1 or text.find(u'[得意地笑]') != -1:
            t = 1
        if text.find(u'[泪]') != -1 or text.find(u'[生病]') != -1 or text.find(u'[悲伤]') != -1 or text.find(u'[晕]') != -1 or text.find(u'[怒]') != -1 or text.find(u'[衰]') != -1 or text.find(u'[抓狂]') != -1 or text.find(u'[哼]') != -1 or text.find(u'[怒骂]') != -1 or text.find(u'[失望]') != -1 or text.find(u'[委屈]') != -1 or text.find(u'[吐]') != -1 or text.find(u'[伤心]') != -1 :
            t -= 1
        if t == 0:
            na += 1
        elif t == 1:
            happy += 1
        else:
            unhappy += 1
    if unhappy > happy:
        return {'emotion': 'unhappy', 'contents': r}
    elif happy > unhappy:
        return {'emotion': 'happy', 'contents': r}
    else:
        return {'emotion': 'N/A', 'contents': r}


