import requests

BOTTOKEN = 'INSERT YOUR WEBEX TEAMS BOT TOKEN HERE'

baseurl = "https://webexapis.com/v1/"

headers = {
    'Authorization': 'Bearer ' + BOTTOKEN,
    'Content-Type': 'application/json'
}


def GetRooms():
    url = baseurl + 'rooms'
    response = requests.request("GET", url, headers=headers).json()
    print(headers)
    d = {}
    for i in response["items"]:
        for j in i:
            d[i['title']] = i['id']
    return d


def ReadChat(keyword, me=True):
    rooms = GetRooms()
    roomId = rooms[keyword]
    if me == True:
        url = baseurl + 'messages?mentionedPeople=me&roomId=' + roomId
    else:
        url = baseurl + 'messages?roomId=' + roomId
    response = requests.request("GET", url, headers=headers).json()
    return response["items"]


def SendMessage(ChatName, Text):
    rooms = GetRooms()
    url = baseurl + 'messages'
    payload = "{\r\n  \"roomId\": \"" + rooms[ChatName] + "\",\r\n  \"text\": \"" + Text + "\"\r\n}"
    response = response = requests.request("POST", url, headers=headers, data=payload).json()
    return response


def GetTeams():
    url = baseurl + 'teams'
    response = requests.request("GET", url, headers=headers).json()
    d = {}
    for i in response["items"]:
        for j in i:
            d[i['name']] = i['id']
    return d


def ListTeamMember(TeamName):
    teams = GetTeams()
    teamId = teams[TeamName]
    url = baseurl + 'team/memberships?teamId=' + teamId
    response = response = requests.request("GET", url, headers=headers).json()
    d = {}
    for i in response["items"]:
        for j in i:
            d[i['personDisplayName']] = i['personEmail']
    return d


def AddTeamMember(TeamName, email):
    teams = GetTeams()
    teamId = teams[TeamName]
    url = baseurl + 'team/memberships'
    payload = "{\r\n  \"teamId\": \"" + teamId + "\",\r\n  \"personEmail\": \"" + email + "\"\r\n}"
    response = response = requests.request("POST", url, headers=headers, data=payload).json()
    return response
