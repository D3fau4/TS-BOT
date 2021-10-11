from discord import Intents
from discord.ext.commands import Bot
from discord_slash import SlashCommand
from Config import Config

config = Config()
bot = Bot(command_prefix="!", self_bot=True, intents=Intents.default())
slash = SlashCommand(bot, sync_commands=True, debug_guild=817023577496748052)

bot.load_extension("TS")
bot.run(config.getapiKey())