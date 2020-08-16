import json

class jsonIO:
    
    def __init__(self, path):

        self.json_path = path

        input = open(self.json_path, "r", encoding='utf-8')

        self.setting = json.load(input)

    def get_IpAddress(self):
        if "setting" not in self.setting:
            return

        if "ip" not in self.setting["setting"]:
            return 

        return self.setting["setting"]["ip"]

    def get_Port(self):
        if "setting" not in self.setting:
            return

        if "port" not in self.setting["setting"]:
            return 

        return self.setting["setting"]["port"]

    def get_BrowserPath(self):
        if "setting" not in self.setting:
            return
        
        if "webbrowser path" not in self.setting["setting"]:
            return 

        return self.setting["setting"]["webbrowser path"]

    def get_ImagePath(self):
        if "setting" not in self.setting:
            return
        
        if "image path" not in self.setting["setting"]:
            return 

        return self.setting["setting"]["image path"]
    
    def get_TitleImagePath(self):
        if "book" not in self.setting:
            return
        
        if "title" not in self.setting["book"]:
            return 

        return self.setting["book"]["title"]

if __name__ == "__main__":
    data = jsonIO(r".\setting.json")

    print(data.get_ImagePath())
