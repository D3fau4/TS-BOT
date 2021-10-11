class Config:
    def __init__(self):
        import json
        try:
            f = open("Config.json", "r")
            self.json = json.load(f)
            f.close()
        except IOError:
            print("Creando archivo de configuración.")
            f = open("Config.json", "a")
            x = {
                "API_KEY": "YOURKEY",
                "channel": "",
                "PREFIX": "TS.",
                "Reload": 5,
                "RequestChannel" : ""
            }
            tmp = json.dumps(x)
            f.write(str(tmp).replace("\'", "\""))
            f.close()
            print("Porfavor configura el json")
            exit()

    def UpdateConfig(self):
        f = open("Config.json", "w")
        f.write(str(self.json).replace("\'", "\""))
        f.close()

    def getapiKey(self):
        return self.json["API_KEY"]

    def getprefix(self):
        return self.json["PREFIX"]

    def getchannel(self):
        return self.json["channel"]

    def getrequestchannel(self):
        return self.json["RequestChannel"]

    def setchannel(self, ch):
        self.json["channel"] = ch
        self.UpdateConfig()

    def setrequestchannel(self, ch):
        self.json["RequestChannel"] = ch
        self.UpdateConfig()

    def getReload(self):
        return self.json["Reload"]

    def setReload(self, r):
        self.json["Reload"] = r
        self.UpdateConfig()

    def setprefix(self, p):
        self.json["PREFIX"] = p
        self.UpdateConfig()