import requests, json, os

class offline_response:

    def __init__(self, t):
        self.text = t

    def json(self):
        try:
            return json.loads(self.text)
        except:
            return {}

class mapAPI:


    def __init__(self, url, offline_storage = "", offlinemode = "medium"):
        # url of api
        self.url = url
        # offline storage
        self.offline_storage = offline_storage
        self.offline_mode = offlinemode
        # check if folder exists and if not, create them
        if not os.path.isdir(offline_storage) and not offline_storage == "":
            os.makedirs(offline_storage)

    @staticmethod
    def __request(url):
        # get repsonse from url
        try:
            response = requests.get(url)
        except:
            return "202"
        if not response:
            return "202"
        # return response
        return response
    
    def __get(self,url):
        # get response
        response = self.__request(url)

        # if there is no repsonse
        if type(response) != requests.Response and self.offline_storage != "":
            # get path of offline file
            path = self.offline_storage + "/" + url.replace(self.url,"").replace("/api/","") + ".txt"
            # see if it exists
            if not os.path.isfile(path): return offline_response("{}")
            # load its contents
            with open(path, "r") as f:
                data = f.read()
                # respect offline mode partly
                if self.offline_mode == "medium":
                    if "signals" in path:
                        data = data.replace("RED","GREEN").replace("YELLOW","GREEN")
                    if "blocks" in path:
                        data = '{"blocks":[]}'
                if self.offline_mode != "full":
                    if "trains" in path:
                        data = '{"trains":[]}'
                if self.offline_mode == "low":
                    if "signals" in path:
                        data = '{"signals":[]}'
                data = offline_response(data)
            # return the data
            return data
        # if there is no response but also no offline data
        elif type(response) != requests.Response:
            return offline_response("{}")
        # when a response is there
        else:
            # store the response if there is offline storage
            if self.offline_storage != "":
                try:
                    path = self.offline_storage + "/" + url.lstrip(self.url).split("/")[1] + ".txt"
                    with open(path,"w") as f:
                        f.write(response.text)
                except:
                    return offline_response("{}")
            # return the response
            return response

    def getTracks(self):
        # get track data
        response = self.__get(self.url+"/api/network")
        # return track json
        return response.json()

    def getBlocks(self):
        # get track data
        response = self.__get(self.url+"/api/blocks")
        # return blocks json
        return response.json()

    def getSignals(self):
        # get track data
        response = self.__get(self.url+"/api/signals")
        # return signals json
        return response.json()

    def getTrains(self):
        # get track data
        response = self.__get(self.url+"/api/trains")
        # return trains json
        return response.json()

    def getStyle(self):
        # get track data
        response = self.__get(self.url+"/api/style.css")
        # return style css
        return response.text
    
    def getStyleAsJson(self):
        # get track data
        response = self.__get(self.url+"/api/style.css")
        # return style as json
        x = response.text

        x = x.replace(":root {","").replace("}","")
        x = x.split("\n")
        for i in range(len(x)):
            x[i] = x[i].split(": ")

        x.pop(1)

        out = {}

        for o in x:
            if o[0] == "": continue

            out[o[0][2:]] = o[1]

        return out


    def getConfig(self):
        # get track data
        response = self.__get(self.url+"/config.json")
        # return config json
        return response.json()