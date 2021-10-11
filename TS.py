from discord import Embed
from discord.activity import Activity, ActivityType
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from discord_slash.model import SlashCommandOptionType
from TSwrapper import TSwrapper
from Config import Config
from discord.ext import tasks
import requests
from bs4 import BeautifulSoup

URL = "https://tradusquare.es/"
VERSION = "1.0.0"
RELOAD = 5


class Slash(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self._autoupdate.start()
        self.bot.activity = Activity(
            type=ActivityType.watching, name="la web de TraduSquare", url="https://tradusquare.es")
        self.config = Config()
        self.last_new = TSwrapper()
        self.last_new.loadlocalnew()
        RELOAD = self.config.getReload()

    @cog_ext.cog_slash(name="update", description="Comprueba si hay una nueva entrada.", default_permission=True)
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
                embed = Embed(title=" ", color=0xc565d2)
                embed.set_author(name="Tokoyami Towa")
                embed.set_thumbnail(
                    url="https://cdn.discordapp.com/app-icons/855802712653561876/dd525a11fda30c28c755b636ddf76986.png")
                embed.add_field(
                    name="**Mensaje:**", value="No hay nuevas entradas.", inline=True)
                await ctx.send(embed=embed)
                print("No hay noticias nuevas")
        else:
            embed = Embed(title=" ", color=0xc565d2)
            embed.set_author(name="Tokoyami Towa")
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/app-icons/855802712653561876/dd525a11fda30c28c755b636ddf76986.png")
            embed.add_field(
                name="**Mensaje:**", value="No dispones de permisos suficientes para realizar esta acción.", inline=True)
            await ctx.send(embed=embed)

    @tasks.loop(minutes=RELOAD)
    async def _autoupdate(self):
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
            await channel.send("2")
        else:
            print("No hay noticias nuevas")

    @cog_ext.cog_slash(name="setprefix", description="[DEPRECADO] Establece el prefigo del bot.", options=[
        create_option(
            name="prefix",
            description="Será el prefijo del bot.",
            option_type=SlashCommandOptionType.STRING,
            required=True
        )
    ], default_permission=True)
    async def _SetPrefix(self, ctx: SlashContext, prefix: str):
        if (ctx.author.permissions_in(ctx.channel).administrator == True):
            self.config.setprefix(prefix)
            embed = Embed(title=" ", color=0xc565d2)
            embed.set_author(name="Tokoyami Towa")
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/app-icons/855802712653561876/dd525a11fda30c28c755b636ddf76986.png")
            embed.add_field(
                name="**Mensaje:**", value="Se a cambiado el prefijo correctamente por `" + self.config.getprefix() + "`", inline=True)
            await ctx.send(embed=embed)
        else:
            embed = Embed(title=" ", color=0xc565d2)
            embed.set_author(name="Tokoyami Towa")
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/app-icons/855802712653561876/dd525a11fda30c28c755b636ddf76986.png")
            embed.add_field(
                name="**Mensaje:**", value="No dispones de permisos suficientes para realizar esta acción.", inline=True)
            await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="setreload", description="Establece el tiempo de comprobación de la web.", options=[
        create_option(
            name="minutes",
            description="Tiempo que tardará en comprobar la web (Minutos)",
            option_type=SlashCommandOptionType.INTEGER,
            required=True
        )
    ], default_permission=True)
    async def _SetReload(self, ctx: SlashContext, minutes: str):
        if (ctx.author.permissions_in(ctx.channel).administrator == True):
            self.config.setReload(minutes)
            RELOAD = self.config.getReload()
            embed = Embed(title=" ", color=0xc565d2)
            embed.set_author(name="Tokoyami Towa")
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/app-icons/855802712653561876/dd525a11fda30c28c755b636ddf76986.png")
            embed.add_field(
                name="**Mensaje:**", value="Se a cambiado el tiempo de refresco de la web correctamente a {RELOAD} min.", inline=True)
            await ctx.send(embed=embed)
        else:
            embed = Embed(title=" ", color=0xc565d2)
            embed.set_author(name="Tokoyami Towa")
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/app-icons/855802712653561876/dd525a11fda30c28c755b636ddf76986.png")
            embed.add_field(
                name="**Mensaje:**", value="No dispones de permisos suficientes para realizar esta acción.", inline=True)
            await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Slash(bot))
