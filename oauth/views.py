import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from .models import OAuthUser
from django.contrib.auth.models import User
import urllib
import urllib2
from .util import get_info, get_posts, get_emotion, get_users


# Create your views here.
def home(request):
    if request.user.is_authenticated():
        d = get_info(request.user.oauthuser.access_token, request.user.username)
        return render_to_response("index.html", {'user': request.user.oauthuser, 'uid': request.user.username, 
                                                 'name': d['name'], 'avatar': d['avatar']})
    else:
        return render_to_response("index.html")


def oauth_callback(request):
    code = request.GET['code']
    url = 'https://api.weibo.com/oauth2/access_token'
    values = {
        'client_id': '2027959579',
        'client_secret': 'f839c30fc7681ba271dd28d2356b37d4',
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://weiboemoticon.applinzi.com/callback',
        # 'redirect_uri': 'http://127.0.0.1:8000/callback',
        'code': code
    }
    data = urllib.urlencode(values)
    data = data.encode('ascii')
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    r = response.read().decode('utf-8')
    result = json.loads(r)
    print(result)
    access_token = result['access_token']
    uid = result['uid']
    expire_time = result['expires_in']

    try:
        user = User.objects.get(username=uid)
    except:
        user = User.objects.create_user(uid, 'a@b.c', '********')
        user.save()
    user = authenticate(username=uid, password='********')
    login(request, user)
    try:
        ouser = OAuthUser.objects.get(user=user)
    except:
        ouser = OAuthUser(user=user)
    ouser.access_token = access_token
    ouser.expire_time = int(expire_time)
    ouser.save()
    return HttpResponseRedirect('/')


def my_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/')
def all_users(request):
    ret = get_users(request.user.oauthuser.access_token)
    return render_to_response("json.html", {'json': json.dumps(ret)})

@login_required(login_url='/')
def all_posts(request, uid):
    if uid != request.user.username:
        return HttpResponse("UID Must Equal to current user!")
    ret = get_posts(request.user.oauthuser.access_token, uid)
    return render_to_response("json.html", {'json': json.dumps(ret)})

@login_required(login_url='/')
def emoticon(request, uid):
    if uid != request.user.username:
        return HttpResponse("UID Must Equal to current user!")
    ret = get_emotion(request.user.oauthuser.access_token, uid)
    return render_to_response("json.html", {'json': json.dumps(ret)})
