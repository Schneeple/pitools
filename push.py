import requests
import json
import datetime
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from pandas.io.json import json_normalize
import os
import datetime as DT
from tqdm import tqdm_notebook
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class stream(object):
    def __init__(self, host, server, headers , PI_Tags_Dict=None, values=None):
        """
        Needs host and SERVER name and headers(obtained from postman)

        header :=
        self.headers = {
            'Authorization': "Basic 4567456745675467546754675467==",
            'cache-control': "no-cache",
            'Postman-Token': "123123-123-123-123-123123123123"
        }

        
        """
        self.server = server
        self.PI_Tags_Dict = PI_Tags_Dict
        self.values = values
        self.headers = headers
        self.host = host  # IP ADDRESS OF THE SERVER GOES HERE

    def grabIndividualWebIDS(self, entered_PI_Tag):  # Working 1-9-19
        """Used in PushSingleValue Function to grab an individual WebID. Can enter a Pi Tag here to get the webID"""
        url = "https://" + self.host + "/piwebapi/points"

        # Pulls Web ID for the Pi Tag entered.
        self.BodyJSON = {"path": '\\\\self.server\\' + entered_PI_Tag}
        response = requests.request("GET", url, headers=self.headers, params=self.BodyJSON, verify=False)
        data = response.json()
        webIDs = data["WebId"]
        return webIDs

    def PushSingleValue(self, entered_PI_Tag, value, time=None, print_status=False):  # Working 1-9-19
        if time is None:
            time = self.getTime()

        webID = self.grabIndividualWebIDS(entered_PI_Tag)
        url = "https://" + self.host + "/piwebapi/streams/" + webID + "/value"
        payload = "{\r\n  \"Timestamp\": \"" + str(time) + "\",\r\n  \"Value\": " + str(value) + "\r\n}"
        response = requests.request("POST", url, data=payload, headers=self.headers, verify=False)

        if print_status:
            if response.ok:
                print('Saved to Pi Server')
            else:
                print('Error:', response.json())
        return response

    def getTime(self):
        """Uses API to grab most recent time to allwas keep time updated."""

        time_url = "http://worldtimeapi.org/api/timezone/America/Los_Angeles"
        payload = ""

        response = requests.request("GET", time_url, data=payload)
        time_now = pd.to_datetime(response.json()['datetime'])
        try:
            time_now = time_now.tz_convert(None)
        except:
            print(time_now.tz)
        time_now -= DT.timedelta(hours=7)
        return time_now

    def save_df(self, dataframe):
        """
        DataFrame Structure:

        columns: Pi Tags
        index: Datetime
        Rows: Save that value with respect to the column and row datetime object

        EXAMPLE Below:

                 |   Pi_Tag_1   | Pi_Tag_2  |
        _____________________________________
         4/6/2019|     6.8      |    8.9    |
         4/7/2019|     6.7      |    8.2    |
         4/8/2019|     6.9      |    8.4    |


        Make columns are the tag respective to what you are trying to save.
        """
        for i in tqdm_notebook(dataframe):
            dic = {}
            status = []
            for j in range(len(dataframe[i])):
                try:
                    xx = self.PushSingleValue(i, dataframe[i].iloc[j], dataframe.index[j])
                    status.append(xx)
                except:
                    print("ERROR saving the following Data:", i, dataframe[i].iloc[j], dataframe.index[j])
                    status.append("FAILED")
            dic[i] = status
        return_df = pd.DataFrame(dic)
        return_df.index = dataframe.index
        return return_df


class dataservers(object):
    def __init__(self, ServerJSON):
        """
        needs server webid in format of
        {
            'self.server' : 'WEBIDGOESHEREOFYOURSERVER'
        }

        """
        self.ServerWebIDs = SERVERJSON

    def createPiTag(self, json, header , serverName="self.server", print_errors=False):
        """Needs header from postman in the correct format like this:
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Basic 65436565446534646345==",
            'User-Agent': "PostmanRuntime/7.20.1",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Postman-Token': "g-a2gg25-gg-gg-gg,sdfg-sdfg-sdfg-sdfg-sdfg",
            'Host': self.host,
            'Accept-Encoding': "gzip, deflate",
            'Content-Length': "210",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }
        """
        server = self.ServerWebIDs[serverName]


        url = "https://hostname/piwebapi/dataservers/" + server + "/points"

        """
         e.g. 
            {
                "Name": "TAGNAMETAG",
                "Descriptor": "12 Hour Sine Wave",
                "PointClass": "classic",
                "PointType": "Float32",
                "EngineeringUnits": "",
                "Step": false,
                "Future": false,
                "DisplayDigits": -5
            }
        """

        payload = json
        response = requests.request("POST", url, data=payload, headers=header, verify=False)
        if response.status_code == 400:
            if print_errors == True:
                print("Tag is already made, Try another tag Name! \n")
                print("Status code: " + response.status_code)
        else:
            response.status_code = 418  # I'm a teapot
        return response
