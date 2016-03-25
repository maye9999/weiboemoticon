import json
import urllib
import urllib2

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

