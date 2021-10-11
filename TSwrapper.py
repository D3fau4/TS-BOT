import requests
import re
from bs4 import BeautifulSoup

URL = "https://tradusquare.es/"

class TSwrapper():

    def __init__(self):
        self.titulo = ""
        self.autor = ""
        self.fecha = ""
        self.descrip = ""
        self.img = ""
        self.tag = ""
        self.url = ""
        self.avatar = ""
        self.nombre = ""

    def loadlocalnew(self):
        import json
        try:
            print("Cargando noticia local")
            f = open("New.json", "r")
            self.json = json.load(f)
            self.autor = self.json["autor"]
            self.avatar = URL + "avatars/" + self.json["autor"]
            self.titulo = self.json["titulo"]
            self.fecha = self.json["fecha"]
            self.descrip = self.json["descripcion"]
            self.tag = self.json["tag"]
            self.img = self.json["img"]
            self.url = self.json["url"]
            self.nombre = self.json["nombre"]
            f.close()
            print("Noticia local cargada")
        except:
            print("Creando New.json")
            f = open("New.json", "w")
            html = requests.get(URL).text
            soup = BeautifulSoup(html, "html.parser")
            new = soup.body.find(
                'div', attrs={'class': 'tarjeta p-0 rounded mb-4'})
            post_info = new.find_all('div', attrs={'class': 'col-xs-3 p-1'})
            self.titulo = new.find(
                'h2', attrs={'class': 'mb-0'}).text.replace("\n", "")
            self.fecha = post_info[0].text.replace("\n", "")
            self.autor = post_info[1].text.replace("\n", "")
            self.descrip = new.find('div', attrs={
                                    'class': 'col p-2 pl-3 text-black rounded bg-white'}).text.replace("\n", "")
            self.tag = post_info[2].text.replace("\n", "")
            self.img = re.search("(?P<url>https?://[^\s]+.(?i:jpg|gif|png|bmp|webp|svg|jpeg))", str(
                new.find('div', attrs={'class': 'col-md-5 p-0 preview'}))).group("url")
            self.url = URL + \
                re.search(
                    "(?P<url>entrada.php[^\s]+)", str(new.find('a'))).group("url").replace("\">", "")
            web = BeautifulSoup(requests.get(self.url).text, "html.parser")
            try:
                self.nombre = web.find(
                'div', attrs={'class': 'col text-center p-0'}).text.replace("\n", "")
            except:
                self.nombre = ""
            file = {
                "nombre": self.nombre,
                "titulo": self.titulo,
                "autor": self.autor,
                "fecha": self.fecha,
                "descripcion": self.descrip,
                "tag": self.tag,
                "img": self.img,
                "url": self.url
            }
            self.json = json.dumps(file)
            f.write(str(self.json).replace("\'", "\""))
            f.close()

    def Update(self, new):
        import json
        f = open("New.json", "w")
        post_info = new.find_all('div', attrs={'class': 'col-xs-3 p-1'})
        self.titulo = new.find(
            'h2', attrs={'class': 'mb-0'}).text.replace("\n", "")
        self.fecha = post_info[0].text.replace("\n", "")
        self.autor = post_info[1].text.replace("\n", "")
        self.descrip = new.find('div', attrs={
                                'class': 'col p-2 pl-3 text-black rounded bg-white'}).text.replace("\n", "")
        self.tag = post_info[2].text.replace("\n", "")
        self.img = re.search("(?P<url>https?://[^\s]+.(?i:jpg|gif|png|bmp|webp|svg|jpeg))", str(
            new.find('div', attrs={'class': 'col-md-5 p-0 preview'}))).group("url")
        self.url = URL + \
            re.search(
                "(?P<url>entrada.php[^\s]+)", str(new.find('a'))).group("url").replace("\">", "")
        web = BeautifulSoup(requests.get(self.url).text, "html.parser")
        self.nombre = web.find(
            'div', attrs={'class': 'col text-center p-0'}).text.replace("\n", "")
        file = {
            "nombre": self.nombre,
            "titulo": self.titulo,
            "autor": self.autor,
            "fecha": self.fecha,
            "descripcion": self.descrip,
            "tag": self.tag,
            "img": self.img,
            "url": self.url
        }
        self.json = json.dumps(file)
        f.write(str(self.json).replace("\'", "\""))
        f.close()

    def settitulo(self, t):
        self.titulo = t

    def setautor(self, a):
        self.autor = a

    def setfecha(self, f):
        self.fecha = f

    def setdescrip(self, d):
        self.descrip = d

    def setimg(self, i):
        self.img = i

    def settag(self, t):
        self.tag = t

    def seturl(self, u):
        self.url = u

    def setavatar(self, a):
        self.avatar = a

    def setnombre(self, n):
        self.nombre = n

    def gettitulo(self):
        return self.titulo

    def getautor(self):
        return self.autor

    def getfecha(self):
        return self.fecha

    def getdescrip(self):
        return self.descrip

    def getimg(self):
        return self.img

    def gettag(self):
        return self.tag

    def geturl(self):
        return self.url

    def getavatar(self):
        return self.avatar

    def getnombre(self):
        return self.nombre
