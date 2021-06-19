import re
import asyncio
import discord
from discord.ext import tasks
import requests
import re
from bs4 import BeautifulSoup

URL = "https://tradusquare.es/"
VERSION = "1.0.0"
RELOAD = 5


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
                "Reload": 5
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

    def setchannel(self, ch):
        self.json["channel"] = ch
        self.UpdateConfig()

    def getReload(self):
        return self.json["Reload"]

    def setReload(self, r):
        self.json["Reload"] = r
        self.UpdateConfig()

    def setprefix(self, p):
        self.json["PREFIX"] = p
        self.UpdateConfig()


class News():

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
            self.img = re.search("(?P<url>https?://[^\s]+.webp)", str(
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


class Client(discord.Client):

    def __init__(self, config):
        super().__init__()
        self.activity = discord.Streaming(name='TraduSquare', url="https://tradusquare.es/",
                                          state="cum", details="gdfg", type=discord.ActivityType.watching)
        self.config = config
        self.last_new = News()
        self.last_new.loadlocalnew()

    async def on_ready(self):
        print("Iniciado sesion como: " + str(self.user))
        self.traducheck.start()

    @tasks.loop(seconds=RELOAD * 60)
    async def traducheck(self):
        html = requests.get(URL).text
        soup = BeautifulSoup(html, "html.parser")
        new = soup.body.find(
            'div', attrs={'class': 'tarjeta p-0 rounded mb-4'})
        if (self.last_new.titulo != new.find('h2', attrs={'class': 'mb-0'}).text.replace("\n", "")):
            print("Noticia nueva")
            self.last_new.Update(new)
            channel = self.get_channel(self.config.getchannel())
            embed = discord.Embed(title=self.last_new.gettitulo(
            ), url=self.last_new.geturl(), color=0xc565d2)
            embed.set_author(name=self.last_new.getautor())
            embed.add_field(name="**" + self.last_new.getfecha() + "**", value="```" +
                            self.last_new.getdescrip() + "```", inline=True)
            embed.set_image(url=self.last_new.getimg())
            embed.set_footer(text=self.last_new.getnombre())
            await channel.send(embed=embed)
        else:
            print("No hay noticia nueva")

    async def on_message(self, message):
        if (message.author != self.user):  # comprobar que el mensaje no sea de él mismo
            print('Mensaje de {0.author}: {0.content}'.format(message))
            # mirar si están llamando al bot
            if message.content.startswith(self.config.getprefix()):
                args = str(message.content).replace(
                    self.config.getprefix(), '').split(' ')
                if args[0] == "setchannel":
                    if (message.author.permissions_in(message.channel).administrator == True):
                        self.config.setchannel(message.channel.id)
                        channel = message.channel
                        embed = discord.Embed(title=" ", color=0xc565d2)
                        embed.set_author(name="Tokoyami Towa")
                        embed.set_thumbnail(
                            url="https://cdn.discordapp.com/app-icons/855802712653561876/dd525a11fda30c28c755b636ddf76986.png")
                        embed.add_field(
                            name="**Mensaje:**", value="El canal se ha establecido correctamente.", inline=True)
                        await channel.send(embed=embed)
                    else:
                        channel = message.channel
                        embed = discord.Embed(title=" ", color=0xc565d2)
                        embed.set_author(name="Tokoyami Towa")
                        embed.set_thumbnail(
                            url="https://cdn.discordapp.com/app-icons/855802712653561876/dd525a11fda30c28c755b636ddf76986.png")
                        embed.add_field(
                            name="**Mensaje:**", value="No dispones de permisos suficientes para realizar esta acción.", inline=True)
                        await channel.send(embed=embed)
                elif args[0] == "update":
                    if (message.author.permissions_in(message.channel).administrator == True):
                        html = requests.get(URL).text
                        soup = BeautifulSoup(html, "html.parser")
                        new = soup.body.find(
                            'div', attrs={'class': 'tarjeta p-0 rounded mb-4'})
                        if (self.last_new.titulo != new.find('h2', attrs={'class': 'mb-0'}).text.replace("\n", "")):
                            print("Noticia nueva")
                            self.last_new.Update(new)
                            channel = self.get_channel(
                                self.config.getchannel())
                            embed = discord.Embed(title=self.last_new.gettitulo(
                            ), url=self.last_new.geturl(), color=0xc565d2)
                            embed.set_author(name=self.last_new.getautor())
                            embed.add_field(name="**" + self.last_new.getfecha() + "**", value="```" +
                                            self.last_new.getdescrip() + "```", inline=True)
                            embed.set_image(url=self.last_new.getimg())
                            embed.set_footer(text=self.last_new.getnombre())
                            await channel.send(embed=embed)
                        else:
                            channel = message.channel
                            embed = discord.Embed(title=" ", color=0xc565d2)
                            embed.set_author(name="Tokoyami Towa")
                            embed.set_thumbnail(
                                url="https://cdn.discordapp.com/app-icons/855802712653561876/dd525a11fda30c28c755b636ddf76986.png")
                            embed.add_field(
                                name="**Mensaje:**", value="No hay nuevas entradas.", inline=True)
                            await channel.send(embed=embed)
                    else:
                        channel = message.channel
                        embed = discord.Embed(title=" ", color=0xc565d2)
                        embed.set_author(name="Tokoyami Towa")
                        embed.set_thumbnail(
                            url="https://cdn.discordapp.com/app-icons/855802712653561876/dd525a11fda30c28c755b636ddf76986.png")
                        embed.add_field(
                            name="**Mensaje:**", value="No dispones de permisos suficientes para realizar esta acción.", inline=True)
                        await channel.send(embed=embed)
                elif args[0] == "ReloadTime":
                    if (message.author.permissions_in(message.channel).administrator == True):
                        try:
                            self.config.setReload(args[1])
                            channel = message.channel
                            embed = discord.Embed(title=" ", color=0xc565d2)
                            embed.set_author(name="Tokoyami Towa")
                            embed.set_thumbnail(
                                url="https://cdn.discordapp.com/app-icons/855802712653561876/dd525a11fda30c28c755b636ddf76986.png")
                            embed.add_field(
                                name="**Mensaje:**", value="Se a cambiado el tiempo de refresco de la web correctamente.", inline=True)
                            await channel.send(embed=embed)
                        except:
                            channel = message.channel
                            embed = discord.Embed(title=" ", color=0xc565d2)
                            embed.set_author(name="Tokoyami Towa")
                            embed.set_thumbnail(
                                url="https://cdn.discordapp.com/app-icons/855802712653561876/dd525a11fda30c28c755b636ddf76986.png")
                            embed.add_field(
                                name="**Mensaje:**", value="No se ha introducido bien los argumentos para el comando: `" + args[0] + "`", inline=True)
                            await channel.send(embed=embed)
                    else:
                        channel = message.channel
                        embed = discord.Embed(title=" ", color=0xc565d2)
                        embed.set_author(name="Tokoyami Towa")
                        embed.set_thumbnail(
                            url="https://cdn.discordapp.com/app-icons/855802712653561876/dd525a11fda30c28c755b636ddf76986.png")
                        embed.add_field(
                            name="**Mensaje:**", value="No dispones de permisos suficientes para realizar esta acción.", inline=True)
                elif args[0] == "info" or args[0] == "help":
                    channel = message.channel
                    embed = discord.Embed(
                        title="Tokoyami Towa", color=0xc565d2)
                    embed.set_author(
                        name="Hecho por Hat Kid", icon_url="https://cdn.discordapp.com/avatars/363594127885074434/0778dfb946e90e6d645e09fa93d5b247.png?size=2048")
                    embed.set_thumbnail(
                        url="https://cdn.discordapp.com/app-icons/855802712653561876/dd525a11fda30c28c755b636ddf76986.png")
                    embed.add_field(name="**Comandos:**", value="```TS.setchannel             -  Establecerá en canal donde se ejecute como canal de noticias.\nTS.update                 -  Hará un refresco manual de las noticias de la web.\nTS.ReloadTime [minutos]   -  Establecerá el intervalo de minutos entre los refrescos automáticos.\nTS.help/info              -  Mostrará este mensaje.\nTS.SetPrefix [prefijo]    -  Establecerá el prefijo para los comandos del bot.```".replace("TS.", self.config.getprefix()), inline=True)
                    embed.set_footer(text="Versión: " + VERSION)
                    await channel.send(embed=embed)
                elif args[0] == "SetPrefix":
                    if (message.author.permissions_in(message.channel).administrator == True):
                        try:
                            self.config.setprefix(args[1])
                            channel = message.channel
                            embed = discord.Embed(title=" ", color=0xc565d2)
                            embed.set_author(name="Tokoyami Towa")
                            embed.set_thumbnail(
                                url="https://cdn.discordapp.com/app-icons/855802712653561876/dd525a11fda30c28c755b636ddf76986.png")
                            embed.add_field(
                                name="**Mensaje:**", value="Se a cambiado el prefijo correctamente por `" + self.config.getprefix() +"`", inline=True)
                            await channel.send(embed=embed)
                        except:
                            channel = message.channel
                            embed = discord.Embed(title=" ", color=0xc565d2)
                            embed.set_author(name="Tokoyami Towa")
                            embed.set_thumbnail(
                                url="https://cdn.discordapp.com/app-icons/855802712653561876/dd525a11fda30c28c755b636ddf76986.png")
                            embed.add_field(
                                name="**Mensaje:**", value="No se ha introducido bien los argumentos para el comando: `" + args[0] + "`", inline=True)
                            await channel.send(embed=embed)
                    else:
                        channel = message.channel
                        embed = discord.Embed(title=" ", color=0xc565d2)
                        embed.set_author(name="Tokoyami Towa")
                        embed.set_thumbnail(
                            url="https://cdn.discordapp.com/app-icons/855802712653561876/dd525a11fda30c28c755b636ddf76986.png")
                        embed.add_field(
                            name="**Mensaje:**", value="No dispones de permisos suficientes para realizar esta acción.", inline=True)
                else:
                    channel = message.channel
                    embed = discord.Embed(title=" ", color=0xc565d2)
                    embed.set_author(name="Tokoyami Towa")
                    embed.set_thumbnail(
                        url="https://cdn.discordapp.com/app-icons/855802712653561876/dd525a11fda30c28c755b636ddf76986.png")
                    embed.add_field(
                        name="**Mensaje:**", value="No se ha reconocido el comando: `" + args[0] + "`", inline=True)
                    await channel.send(embed=embed)

        else:
            print("Mensaje del bot: " + str(self.user))


# Programa principal
config = Config()
client = Client(config)
RELOAD = config.getReload()
client.run(config.getapiKey())
