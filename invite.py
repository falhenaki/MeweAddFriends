#Author: Fawaz
#https://github.com/falhenaki

import requests
import json
from ast import literal_eval
import time
import sys
import getpass
accessToken = ""

def login():
  global accessToken
  
  username = input("Username:")
  password = getpass.getpass('Password:')
  
  headers = {
      'Origin': 'https://mewe.com',
      'Accept-Encoding': 'gzip, deflate, br',
      'Accept-Language': 'en-US,en;q=0.9',
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      'Referer': 'https://mewe.com/',
      'X-Requested-With': 'XMLHttpRequest',
      'Connection': 'keep-alive',
  }

  data = {
    'username': username,
    'password': password
  }

  response = requests.post('https://mewe.com/api/v2/auth/login', headers=headers, cookies={}, data=data)
  try:
    responseload = json.loads(response.text)
  except:
    print("Login server response is invalid")
    login()

  try:
    accessToken = responseload["accessToken"]
  except:
    print("Login failed, try again")
    login()

def add_user(userid):
  headers = {
    'Authorization': 'Sgrouples accessToken='+ accessToken,
      'Origin': 'https://mewe.com',
      'Accept-Encoding': 'gzip, deflate, br',
      'Accept-Language': 'en-US,en;q=0.9',
      'Content-Type': 'application/json; charset=UTF-8',
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      'X-Requested-With': 'XMLHttpRequest',
      'Connection': 'keep-alive',
  }

  data = '{"userInvitees":[{"users":"'+userid+'"}],"options":{"allowSeeMyFeed":true}}'
  response = requests.post('https://mewe.com/api/v2/mycontacts/invite', headers=headers, cookies={}, data=data)

  return response

def get_contact_list():
  userid = input("id of user to add from:")
  headers = {
    'Authorization': 'Sgrouples accessToken=' +accessToken,
      'Accept-Encoding': 'gzip, deflate, br',
      'Accept-Language': 'en-US,en;q=0.9',
      'Content-Type': 'application/json; charset=UTF-8',
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      'X-Requested-With': 'XMLHttpRequest',
      'Connection': 'keep-alive',
  }
  params = (
            ('maxResults', '999999'),
            ('_', '1543076819942'),
            )

  response = requests.get('https://mewe.com/api/v2/mycontacts/user/'+userid +'/contacts', headers=headers, params=params, cookies={})
  try:
    dicc = json.loads(response.text)
  except:
    print("Contact list retreieve server response is invalid")
    get_contact_list()
  try:
    if (dicc["contacts"] is None):
      print("Failed to retreieve contacts list, you may not have access to this user's list")
      get_contact_list()
  except:
    print("Failed to retreieve contacts list, you may not have access to this user's list")
    get_contact_list()

  users = []
  for grabbed in dicc["contacts"]:
    user = {}
    user["id"] = grabbed["user"]["id"]
    user["name"] = grabbed["user"]["name"]
    user["online"] = grabbed["online"]
    user["iscontact"] = grabbed["isMyContact"]
    users.append(user)

  return users

def get_no_add_list():
  with open('noadd.txt') as f:
    noaddlist = f.read().splitlines()
  return noaddlist

noadd = get_no_add_list()

def main():

  login()
  
  users = get_contact_list()
  for user in users:

    if user["id"] not in noadd and not user["iscontact"] and not user["iscontact"]:
      r = add_user(user["id"])
      if r.status_code == 204:
        print("added:" + user["name"])
        
        with open("noadd.txt", "a") as myfile:
          myfile.write(user["id"] + "\n")
      elif r.status_code == 400:
        sys.exit("You have reached the 50 invitations a day limit.")
      else:
        sys.exit("An unexpected error has occured.")

main()
