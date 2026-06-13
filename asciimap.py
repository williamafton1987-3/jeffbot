import textwrap
lines = ['','','']
boxesgenerated = {}
class lefttextbox:
    def __init__(self, length, text):
        self.length = length
        self.space = 13
        self.text = textwrap.wrap(text, width=self.space)
        while len(self.text) < 3:
            self.text.append("")
        
    def __str__(self):
        return f"""
┏━━━━━━━━━━━━━┓{" "*self.length}┃
┃{self.text[0]:<{self.space}}┃{" "*self.length}┃
┃{self.text[1]:<{self.space}}┣{"━"*self.length}┫
┃{self.text[2]:<{self.space}}┃{" "*self.length}┃
┗━━━━━━━━━━━━━┛{" "*self.length}┃
"""

class righttextbox:
    def __init__(self, length, text):
        self.length = length
        self.space = 13
        self.text = textwrap.wrap(text, width=self.space)
        while len(self.text) < 3:
            self.text.append("")
            
    def __str__(self):
        return f"""
┃{" "*self.length}┏━━━━━━━━━━━━━┓
┃{" "*self.length}┃{self.text[0]:<{self.space}}┃
┣{"━"*self.length}┃{self.text[1]:<{self.space}}┃
┃{" "*self.length}┃{self.text[2]:<{self.space}}┃
┃{" "*self.length}┗━━━━━━━━━━━━━┛ 
"""
    
def genmainline():
    pass

# def getmainline():

#     netherspawn = """
# ┏━━━━━━┻━━━━━━┓
# ┃             ┃
# ┃Nether  Spawn┃
# ┃             ┃
# ┗━━━━━━┳━━━━━━┛
# """