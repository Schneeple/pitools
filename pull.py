__author__ = "Colton M Neary"

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from IPython.core.interactiveshell import InteractiveShell
from tqdm.notebook import tqdm
import json
import datetime
import numpy as np
import pandas as pd
import time
from pandas.io.json import json_normalize
import os
import datetime as DT
import cufflinks as cf

cf.go_offline()
InteractiveShell.ast_node_interactivity = "all"


class stream(object):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    # Without this it outputs the following error which is overwhelming:
    # Unverified HTTPS request is being made. Adding certificate verification is strongly advised.
    # See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings


    def __init__(self, host, Server, headers, PiTagDictionary={'': ""}, StartTime='y+6h', EndTime='t+6h', Interval='1h',
                 show_status_bar=True, ):
        """

        Need to add the following items
        host: IPaddress of the Pi Server
        Server: the name of the pi database
        headers: is obtained from postman and in the format like this:
        {
            'Authorization': "Basic bkrbhbvr32bjk2b3j4kbj234bk23kbj==",
            'cache-control': "no-cache",
            'Postman-Token': "hbj23hbj32jhb4bj3h2-v2-v2-vdsvdsv2"
        }


                Linear stack of layers.

                # Arguments
                    PiTagDictionary: A dictionary with name of name of the variable as key and pi tag as value.
                    start_time: Start time of the data retrieved; can be entered as Datetime object of OSIsoft string('*' , 't' , -*-1y , etc)
                    end_time: End time of the data retrieved; can be entered as Datetime object of OSIsoft string('*' , 't' , -*-1y , etc)
                    interval: interval of the data retrieved; can be entered as Datetime object of OSIsoft string('*' , 't' , -*-1y , etc)

                # Example

                    ```python
                    import pitools.pull as Pi

                    # Make dictionary to pull tag data and reassign with easy to read names
                    #d = {'name': "tag",
                        #etc... }


                    d [dictionary: values you would like to pull]= {

                            'Flow' : 'Sinusoid_Flow',
                            'Temperature' : 'Cosine_Temp',
                        }

                    s [start time] = '*-7d'
                    e [end time] = DT.datetime.now()
                    i [interval] = '5m'

                    x = Pi.stream(d , starting_time , enders , intervals)


                    # End of stream class initialization.....

                    # How to use datapuller initialization with GetSummary() function...
                    df = x.GetSummary()


                # Returns
                    An initialized PiTools that can be used to call any of the OSIsoft libraries
                    with ease. Use function doc string to specify further

        """

        self.StartTime = StartTime
        self.EndTime = EndTime
        self.Interval = Interval
        self.PiTagsDictionary = PiTagDictionary
        self.Names = PiTagDictionary.keys()
        self.PiTagsArray = PiTagDictionary.values()
        self.__webIDs = None
        self.ListOfURLs = None
        self.__username = os.environ.get('USERNAME')

        self.__payload = ""
        self.__daylight_savings_spring = DT.datetime(2020, 3, 8, 2, 0, 0)
        self.__daylight_savings_fall = DT.datetime(2020, 11, 1, 2, 0, 0)
        self.__daylight_hours = 7  # 8 for fall back and 7 for spring forward
        self.TagDescription = []
        self.Host = host
        self.__show_bar = show_status_bar
        self.Server = "\\\\" + Server + "\\"
        self.df = None
        self.__headers = headers

        # Example dictionary and easy test
        self.PiTagEntryExample = {
            'Sinusoid': "sinusoid",
        }

    def GetTagsFromDict(self):
        self.Names = self.PiTagsDictionary.keys()
        self.PiTagsArray = self.PiTagsDictionary.values()

    def GetTagFromWebID(self, webID):  # Working
        url = 'https://' + self.Host + '/piwebapi/points/' + webID
        # Pulls Web ID for all the Pi Tags

        response = requests.request("GET", url, data=self.__payload, headers=self.__headers, verify=False)
        try:  # Added 1-30-19, to prevent crashing the script when tag is not entered properly. This tell what tag is wrong
            tag = (response.json())["Path"]
            description = (response.json())["Descriptor"]
            return tag
        except:
            print('Not a valid WebID!')

    def GetWebIDs(self, return_webIDs=False, tags_dict=None):  # Working

        global WEBIDS
        # TODO: Need to see if there is ever an instance when tags_dict == None because the GetUrls() method requries a codeword. Might be able to just delete
        if tags_dict == None:
            self.GetUrls()

        self.__webIDs = []
        url = "https://" + self.Host + "/piwebapi/points"
        # Pulls Web ID for all the Pi Tags

        webID_dic = {}
        for tag in tags_dict.values():
            self.BodyJSON = {"path": self.Server + tag}
            response = requests.request("GET", url, headers=self.__headers, params=self.BodyJSON, verify=False)
            try:  # Added 1-30-19, to prevent crashing the script when tag is not entered properly. This tell what tag is wrong
                data = (response.json())["WebId"]
                description = (response.json())["Descriptor"]
            except:
                if len(tag) != 0:
                    print("Error code:", response.status_code, "Can not find \"WebId",
                          "try changing the following tag:", tag)
                elif len(tag) == 0:
                    print("Error code:", response.status_code, "Can not find \"WebId",
                          "because there were no tag(s) entered!! Defaulting to example dataframe.")

            self.__webIDs.append(data)
            webID_dic[tag] = data
            self.TagDescription.append(description)
        self.TagDescription = np.array(self.TagDescription)

        # Prints the webID if the user enters True
        if return_webIDs:
            x = 0
            for ID in self.__webIDs:
                print(self.PiTagsArray[x], ID)
                x += 1

        WEBIDS = webID_dic
        return self.__webIDs

    def GetUrls(self, codeword, example_boolean=False):  # Working
        """This function only works for streams/{webId}/codeword"""
        global URLS

        if example_boolean == False:
            tagers = self.PiTagsDictionary
        else:
            tagers = self.PiTagEntryExample
            self.Names = self.PiTagEntryExample.keys()
            self.PiTagsArray = self.PiTagEntryExample.values()

        if not self.__webIDs:
            self.GetWebIDs(tags_dict=tagers)

        self.ListOfURLs = []
        for webID in self.__webIDs:
            self.ListOfURLs.append("https://" + self.Host + "/piwebapi/streams/" + webID + "/" + codeword)

        URLS = self.ListOfURLs

        return URLS

    def __clear_url_list(self):
        self.__webIDs = None

    def GetInterpolated(self):  # Uses a time range to gather the data
        global df

        self.BodyJSON = {"starttime": self.StartTime, "endtime": self.EndTime, "interval": self.Interval}

        if not self.ListOfURLs:
            self.GetUrls("interpolated")

        url = self.ListOfURLs
        array_Series = []  # Stores the Series data
        for url in self.ListOfURLs:
            response = requests.request("GET", url, data=self.__payload, headers=self.__headers, params=self.BodyJSON,
                                        verify=False)
            try:
                data = (response.json())["Items"]
            except:
                print("Error code:", response.status_code,
                      "Can not find \"Items\" , try a different interval.  Confirm these times below: \n ")
                print('start time:', self.StartTime, ', end time:', self.EndTime, ', interval:', self.Interval)
            val = [];
            times = []
            for dict in data:
                val.append(dict["Value"])
                times.append(dict["Timestamp"])
            datetime_time = pd.Series(times)
            array_Series.append(pd.Series(val))
        self.__clear_url_list()

        df = pd.DataFrame(array_Series).T
        df.columns = self.PiTagsArray
        df.index = (datetime_time)
        df.index = pd.to_datetime(df.index)
        df.index = df.index - DT.timedelta(hours=self.__daylight_hours)
        df.index = df.index.tz_localize(None)  # delete UTC
        df.columns = self.Names
        # Check daylight savings spring Forward
        df = self.__daylight_savings_check(df)
        self.df = df
        return df

    def GetSummary(self, new_dic=None, calculationBasis="TimeWeighted", summaryType="Average",
                   selectedFields="Items.Value", summaryDuration=None):
        """
        **summaryType**
        Specifies the kinds of summaries to produce over the range. The default is 'Total'. Multiple summary types may be specified by using multiple instances of summaryType. See below for more information.
            ----> None , Total , Average , Minimum , Maximum , Range , StdDev , PopulationStdDev , Count , PercentGood , TotalWithUOM , All , AllForNonNumeric

        **calculationBasis**
        Specifies the method of evaluating the data over the time range. The default is 'TimeWeighted'. See Below for all valid options.
            ----> TimeWeighted , EventWeighted , TimeWeightedContinuous , TimeWeightedDiscrete , EventWeightedExcludeMostRecentEvent , EventWeightedExcludeEarliestEvent , EventWeightedIncludeBothEnds

        **selectedFields**
        Leave this here. Speeds up the GET API call.

        **summaryDuration**
        The duration of each summary interval. If specified in hours, minutes, seconds, or milliseconds, the summary durations will be evenly spaced UTC time intervals. Longer interval types are interpreted using wall clock rules and are time zone dependent.


        """

        global df

        if new_dic != None:  # Added so it will detect any updated to the pi tags attribute dictinary to pull the correct tags
            self.PiTagsDictionary = new_dic
            self.GetTagsFromDict()

        try:
            if not self.ListOfURLs:
                self.GetUrls("summary")
        except:
            if not self.ListOfURLs:
                self.GetUrls("summary", example_boolean=True)

        if summaryDuration:
            self.Interval = summaryDuration

        self.BodyJSON = {"startTime": self.StartTime, "endTime": self.EndTime, "summaryType": summaryType,
                         "calculationBasis": calculationBasis, "selectedFields": selectedFields,
                         "summaryDuration": self.Interval}

        array_Series = []  # Stores the Series data
        i = 0

        if self.__show_bar == True:
            url_iter = tqdm(self.ListOfURLs)
        else:
            url_iter = self.ListOfURLs

        for url in url_iter:
            response = requests.request("GET", url, data=self.__payload, headers=self.__headers, params=self.BodyJSON,
                                        verify=False)
            try:
                data = (response.json())["Items"]
            except:
                print("Error code:", response.status_code,
                      "Can not find \"Items\" , try a different interval.  Confirm these times below: \n ")
                print('start time:', self.StartTime, ', end time:', self.EndTime, ', interval:', self.Interval)

            val = [];
            times = [];
            date_len_prev = 0
            for dict in data:
                val.append(dict["Value"]["Value"])
                times.append(dict["Value"]["Timestamp"])
            date_len_new = len(times)
            if date_len_new > date_len_prev:
                datetime_time = pd.Series(times)
            date_len_prev = len(times)
            array_Series.append(pd.Series(val))
        self.__clear_url_list()

        df = pd.DataFrame(array_Series).T
        df.columns = self.PiTagsArray
        df.index = (datetime_time)
        df.index = pd.to_datetime(df.index)
        df.index = df.index.tz_localize(None)  # delete UTC
        df.index = df.index - DT.timedelta(hours=self.__daylight_hours)
        df.columns = self.Names

        # Check daylight savings spring Forward
        df = self.__daylight_savings_check(df)
        self.df = df
        return df

    def GetRecordedAtTime(self, timerecorded, new_dic=None, retrievalMode='Auto'):

        if new_dic != None:  # Added so it will detect any updated to the pi tags attribute dictinary to pull the correct tags
            self.PiTagsDictionary = new_dic
            self.GetTagsFromDict()

        dtype = "datetime64[ns]"
        if not self.ListOfURLs:
            self.GetUrls("recordedattime")

        timerec = np.array(timerecorded)
        erray = [];
        timey = []
        timeout = 1
        for time in timerec:
            self.BodyJSON = {"time": time, "retrievalMode": retrievalMode}
            errA = [];

            timeout = True
            for url in self.ListOfURLs:
                response = requests.request("GET", url, data=self.__payload, headers=self.__headers,
                                            params=self.BodyJSON, verify=False)
                try:
                    data = (response.json())["Value"]
                    times = (response.json())['Timestamp']
                except:
                    print("Error code:", response.status_code,
                          "Can not find \"Items\" , try a different interval.  Confirm these times below: \n ")
                    print('start time:', self.StartTime, ', end time:', self.EndTime, ', interval:', self.Interval)
                errA.append(data)
                if timeout:
                    timey.append(times)
                    timeout = False

            erray.append(errA)
        timer = pd.to_datetime(np.array(timey)) - DT.timedelta(hours=self.__daylight_hours)
        dff = pd.DataFrame(np.asmatrix(erray), timer)

        dff.columns = self.Names  # Rename the columns with the names passed into the original dictionary by user --> self.PiTagsDictionary

        dff.index = dff.index.tz_localize(None)  # Added to remove UTC timezone information

        return [dff, timer]

    def GetRecorded(self, new_dic=None, maxCount=150000):
        """
        Uses pi tags in initialization or search to get every value recorded.
        This function will return a lot of null values due to the mismatch
        in recording data in the plantself.

        ======

        Example:

        from pitools import *
        x = pull.stream()
        x.tagSearch('*Sin*AF', True)
        df=x.GetRecorded()
        df['T_Sin_AF'].dropna()

        """

        global new_df

        if new_dic != None:  # Added so it will detect any updated to the pi tags attribute dictionary to pull the correct tags
            self.PiTagsDictionary = new_dic
            self.GetTagsFromDict()

        if not self.ListOfURLs:
            self.GetUrls("recorded")

        # self.BodyJSON = {"startTime":self.EndTime,"endTime ":self.StartTime  , "maxCount" : maxCount , "boundaryType" : "Inside"}
        self.BodyJSON = {"endTime": self.EndTime, "maxCount": maxCount, "startTime": self.StartTime,
                         "boundaryType": "Inside"}
        errA = [];
        df_array = []
        j = 0;
        names_ = list(self.Names)
        for url in self.ListOfURLs:
            k = 0
            # for tag in self.PiTagsArray:
            #     if k == j:
            #         pi_tag = tag
            response = requests.request("GET", self.ListOfURLs[j], data=self.__payload, headers=self.__headers,
                                        params=self.BodyJSON, verify=False)
            data = ((response.json())['Items'])
            data_array = [];
            time_array = []
            for i in range(len(data)):
                if isinstance(data[i]['Value'], dict):
                    try:
                        time_array.append(data[i]['Value']['Timestamp'])
                        data_array.append(data[i]['Value']['Value'])
                    except:
                        time_array.append(data[i]['Timestamp'])
                        data_array.append(data[i]['Value']['Name'])
                else:
                    data_array.append(data[i]['Value'])
                    time_array.append(data[i]['Timestamp'])

            errA.append(data_array)
            time_array = pd.to_datetime(np.array(time_array)) - DT.timedelta(hours=self.__daylight_hours)

            dt = pd.DataFrame({'Time': time_array, str(names_[j]): data_array})
            dt.set_index('Time', inplace=True)
            dt.index = dt.index.tz_localize(None)  # delete UTC
            df_array.append(dt)
            j += 1

        z = 0
        for v in df_array:
            if z == 0:
                new_df = v
            else:
                new_df = pd.merge(new_df, v, how='outer', left_index=True, right_index=True)
            z += 1

        # Check daylight savings spring Forward
        new_df = self.__daylight_savings_check(new_df)
        self.df = new_df
        return new_df  # [dff.T , timer]

    def GetValue(self, new_dic=None, enter_time=None):
        """Grabs the most recent value if no time has been entered"""

        global final_df

        if new_dic != None:  # Added so it will detect any updated to the pi tags attribute dictionary to pull the correct tags
            self.PiTagsDictionary = new_dic
            self.GetTagsFromDict()

        self.GetUrls("value")

        if not enter_time:
            self.BodyJSON = {}
        else:
            time_used = enter_time
            self.BodyJSON = {"time": time_used}
        timestamp = [];
        data_array = [];
        uom = []
        for url in self.ListOfURLs:
            if enter_time:
                response = requests.request("GET", url, data=self.__payload, headers=self.__headers,
                                            params=self.BodyJSON, verify=False)
            else:
                response = requests.request("GET", url, data=self.__payload, headers=self.__headers, verify=False)
            data = response.json()
            timestamp.append(data['Timestamp'])
            if isinstance(data['Value'], dict):
                data_array.append(data['Value']['Name'])
                uom.append(data['UnitsAbbreviation'])
            else:
                data_array.append(data['Value'])
                uom.append(data['UnitsAbbreviation'])

        new_time = pd.to_datetime(np.array(timestamp)) - DT.timedelta(hours=self.__daylight_hours)
        new_data = data_array

        dfs = [];
        j = 0
        for v in range(len(new_time)):
            for name in self.Names:
                if j == v:
                    pi_tag = name
            d = {'Time': [new_time[v]], 'Data': [new_data[v]], 'UOM': uom[v]}
            dff = pd.DataFrame(d).T
            dfs.append(dff)

        result = pd.concat(dfs, axis=1, sort=False)
        result.columns = self.Names

        # Check daylight savings spring Forward
        # result = self.__daylight_savings_check(result)
        final_df = result.T
        self.df = result.T
        return result.T

    def __daylight_savings_check(self, dataframe):
        # Spring Forward
        dsavings = dataframe[(dataframe.index > self.__daylight_savings_spring) & (
                    dataframe.index < self.__daylight_savings_spring + DT.timedelta(hours=1))]
        l = len(dsavings)
        if l > 0:
            print('The dataframe was adjusted due to Daylight Savings time. Please confirm data is correct. ',
                  self.__daylight_savings_spring)
            h = dataframe.index == self.__daylight_savings_spring
            j = 0
            down = 0  # added before just incase the daylight savings time is not actually in data frame
            for i in h:
                if i == True:
                    down = j
                j += 1

            first = dataframe[0:down]
            second = dataframe[(down):]
            second.index = second.index + DT.timedelta(hours=1)
            df_new = pd.concat([first, second])
        else:
            df_new = dataframe

        return df_new

    # def change_index(data):
    #     if data.

    def FilterColumns(self, string='Au', df=None):
        if df == None:
            if type(self.df) != type(None):
                df = self.df
            else:
                print(
                    'Error 418, Please pass in a dataframe or use the initilized object after running a GetData Method.')

        x = []
        for i in df.columns:
            if string in i:
                x.append(i)
        return df[x]


class search(object):
    def __init__(self, name=None):
        """Uses https://hostname/piwebapi/search/query

        from pitools import pull
        x = pull.search()
        tags = x.tag('*T_*Deca*DCS*')
        v = pull.stream(tags).GetValue()

        """
        self.tags = {}
        self.name = name

    def tag(self, print_tags=True, max_pulled=100000):
        """Uses https://hostname/piwebapi/search/query

        from pitools import pull
        tag = pull.search().tag('*T_*Deca*DCS*')
        v = pull.stream(tags).GetValue()
        v.tail()

        --


        """
        if self.name is None:
            self.name = input('Enter the search criteria:')

        self.url = "https://" + self.Host + "/piwebapi/search/query"

        self.BodyJSON = {"q": "name:" + str(self.name), "count": max_pulled}

        response = requests.request("GET", self.url, data="", headers=self.__headers, params=self.BodyJSON,
                                    verify=False)
        r = response.json()
        tags = []
        for i in r['Items']:
            tags.append(i['Name'])

        for val in tags:
            self.tags[str(val)] = val

        if print_tags:
            try:
                x = stream(self.tags, server=self.Server)
                get = x.GetValue()
                get['Description'] = x.tag_description
                return [get, self.tags]
            except:
                return self.tags

        else:
            return self.tags


if '__main__' == __name__:
    start = '* - 7d'
    end = '*'
    interval = '1h'
    x = stream()
    df = x.GetSummary().tail()

    print(df)
