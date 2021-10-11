from discord import Embed
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext
from TSwrapper import TSwrapper
from Config import Config
from discord.ext import tasks
import requests
import re
from bs4 import BeautifulSoup

URL = "https://tradusquare.es/"
VERSION = "1.0.0"
RELOAD = 5

class Slash(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.config = Config()
        self.last_new = TSwrapper()
        self.last_new.loadlocalnew()
    
    @cog_ext.cog_slash(name="update", description="Comprueba si hay una nueva entrada.", default_permission=False)
    async def _update(self, ctx: SlashContext):
        if (ctx.author.permissions_in(ctx.channel).administrator == True):
            html = requests.get(URL).text
            soup = BeautifulSoup(html, "html.parser")
            new = soup.body.find(
                'div', attrs={'class': 'tarjeta p-0 rounded mb-4'})
            if (self.last_new.titulo != new.find('h2', attrs={'class': 'mb-0'}).text.replace("\n", "")):
                print("Noticia nueva")
                self.last_new.Update(new)
                channel = self.bot.get_channel(self.config.getchannel())
                embed = Embed(title=self.last_new.gettitulo(
                ), url=self.last_new.geturl(), color=0xc565d2)
                embed.set_author(name=self.last_new.getautor())
                embed.add_field(name="**" + self.last_new.getfecha() + "**", value="```" +
                                self.last_new.getdescrip() + "```", inline=True)
                embed.set_image(url=self.last_new.getimg())
                embed.set_footer(text=self.last_new.getnombre())
                await channel.send(embed=embed)
                await channel.send("@everyone")
                await ctx.send(content="Actualizado")
            else:
                await ctx.send(content="No hay noticias nuevas")
                print("No hay noticias nuevas")
        else:
            embed = Embed(title=" ", color=0xc565d2)
            embed.set_author(name="Tokoyami Towa")
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/app-icons/855802712653561876/dd525a11fda30c28c755b636ddf76986.png")
            embed.add_field(
                name="**Mensaje:**", value="No dispones de permisos suficientes para realizar esta acción.", inline=True)
            await ctx.send(embed=embed)

    @tasks.loop(seconds=RELOAD * 60)
    async def _update(self, ctx: SlashContext):
            html = requests.get(URL).text
            soup = BeautifulSoup(html, "html.parser")
            new = soup.body.find(
                'div', attrs={'class': 'tarjeta p-0 rounded mb-4'})
            if (self.last_new.titulo != new.find('h2', attrs={'class': 'mb-0'}).text.replace("\n", "")):
                print("Noticia nueva")
                self.last_new.Update(new)
                channel = self.bot.get_channel(self.config.getchannel())
                embed = Embed(title=self.last_new.gettitulo(
                ), url=self.last_new.geturl(), color=0xc565d2)
                embed.set_author(name=self.last_new.getautor())
                embed.add_field(name="**" + self.last_new.getfecha() + "**", value="```" +
                                self.last_new.getdescrip() + "```", inline=True)
                embed.set_image(url=self.last_new.getimg())
                embed.set_footer(text=self.last_new.getnombre())
                await channel.send(embed=embed)
                await channel.send("@everyone")
            else:
                print("No hay noticias nuevas")

    @cog_ext.cog_slash(name="SetPrefix", description="[DEPRECADO] Establece el prefigo del bot", options=["Prefijo"], default_permission=False)
    async def _SetPrefix(self, ctx: SlashContext):
        embed = Embed(title=" ", color=0xc565d2)
        embed.set_author(name="Tokoyami Towa")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/app-icons/855802712653561876/dd525a11fda30c28c755b636ddf76986.png")
        embed.add_field(
            name="**Mensaje:**", value="No hay nuevas entradas.", inline=True)
        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Slash(bot))