#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import print_function
import requests
import json
from base64 import b64decode
import gzip
#from io import StringIO
from cStringIO import StringIO
import argparse

# utility to find accounts which have similar activity
# profile to some specified account
#i.e. determine multi-accounters

# https://screeps.com/api/leaderboard/find?mode=world&username=danny

#    def board_list(self, limit=10, offset=0, season=None, mode='world'):
#        if season is None:
#            ## find current season (the one with max start time among all seasons)
#            seasons = self.board_seasons['seasons']
#            season = max(seasons, key=lambda s: s['date'])['_id']
#
#        ret = self.get('leaderboard/list', limit=limit, offset=offset, mode=mode, season=season)
#        for d in ret['list']:
#            d['username'] = ret['users'][d['user']]['username']
#        return ret

headers = {
# "X-Token" : ""
# "X-Username : ""
}

def leaderboard_seasons():
  query_url = "https://screeps.com/api/leaderboard/seasons"

  r = requests.get(query_url,  headers = headers)
  ret = r.json()
  #print("seasons:", ret)
  return ret['seasons']

#mode can be world or power
def query_leaderboard(limit=20, offset=0, season=None, mode='world'):
  if season is None:
    seasons = leaderboard_seasons()
    season = max(seasons, key=lambda s: s['date'])['_id']
    print ("recent season:", season)
  
  query_url = "https://screeps.com/api/leaderboard/list"
  params = {"limit" : limit, "offset" : offset, "mode" : mode, "season": season}
  r = requests.get(query_url, headers=headers, params=params)
  ret = r.json()
  #print(ret)
  if 'list' not in ret:
    print(ret)
  else:
    for d in ret['list']:
      d['username'] = ret['users'][d['user']]['username']
      print (d)

def query_user_leaderboard(username):
  query_url = "https://screeps.com/api/leaderboard/find?mode=world&username=%s" % username
  r = requests.get(query_url,headers = headers)
  ret = r.json()
  print(ret)
  return ret

def query_user(user_name):
  query_url = "https://screeps.com/api/user/find"
  rooms_url = "https://screeps.com/api/user/rooms"

  query_payload = { 
          "username" : user_name,
          }

  r = requests.get(query_url,  headers = headers, params=query_payload)
  ret = r.json()

  print(ret)

  if ret['ok'] and ret['user']:
    user_id = ret['user']['_id']

    rooms_params = {"id": user_id}
    r = requests.get(rooms_url, headers = headers, params=rooms_params)
    ret = r.json()
    print(ret)
  else:
    print("not found")

def compare_ul(ul1, ul2):
  #earlisst lb is jan 2015
  u1s = set()
  for s in ul1:
    u1s.add(s["season"])
    #print(s['season'])

  u2s = set()
  for s in ul2:
    u2s.add(s["season"])
    #print(s['season'])


  same=0
  diff=0
  for year in range(2015,2020):
    for month in range(1,13):
      my = "%04d-%02d" % (year,month)
      if (my in u1s) == (my in u2s):
        same += 1
      else:
        diff += 1
  sim = float(100*same)/(same+diff)
  return sim
  #print("same=%d,diff=%d %.01f%%" % (same,diff, float(same*100)/(same+diff)))

def main():
  #parser = argparse.ArgumentParser()
  #parser.add_argument('users', nargs='+', help="users to query")

  #args = parser.parse_args()
  #for user in args.users:
  #  query_user(user);
 
  #leaderboard_seasons()
  #for mode in ["power", "world"]
  ulb = {}
  ncps =["Jeb","ahmadkarlam","Xenofix","bleachhun","hondo","Guardian","Shiaupiau","ixron","Asd","Kill4Free","PeterUK","foraphe","Meta","Rand73","Syzop","steamingpile02","MetalRuller","wellgeter","Stelmine","JohnShadow","makosteel","ix_SAM_xi","HuiJun","Flowers","Lukethe4th","taiga","NickiHell","Komir","x3mka","ags131","YanekM","SandyVaJJ","nyethi","giftpresent","Sskell","max72bra","Kickguy223","PleaseHelpMe","Milky","R2D2"
  ,"resir014","protocolZ","Daggrz","Machinarium","NiFiNiTe","Fashbinder","IronVengeance","c3mb0","C3PO","Zim","Nyte","Cromdale","spez","SirLovi","neona","worTeX","StocksR","KonKeyHD"
  ,"PMN","Metyrio","zekho","Uluvyen","GalatasXF","Nevidimko","Brutalbic1","Johnnyc","Sp4ztique","Sphexi","PaicFR","Robinlub_UG_NL","Doonish","Evanito","tl000","Spirytus","Flicken","NTForG","Sarrick","tinnvec","Shadowars","rlm","Dissi","polidano10","inferno","lDICHl","Spirys","twenty319","Xaphir","TTR"
  ,"DasBrain","novice","VladThePaler","NekoSama","Zolcsika","Finndibaen","seancl", "eth0nic", "gugu"]
  users = ["eth0nic", "gugu", "wtfrank", "c3po", "smokeman"]
  for user in (users + ncps):
     ulb[user]=query_user_leaderboard(username=user)
  for i in range(len(ncps)):
    for j in range(len(users)):
      sim = compare_ul(ulb[ncps[i]]["list"], ulb[users[j]]["list"])
      if sim < 90: continue
      print(ncps[i], users[j], sim)

if __name__ == "__main__":
  main()
