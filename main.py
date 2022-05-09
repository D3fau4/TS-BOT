import interactions
from Config import Config

config = Config()
bot = Bot(command_prefix="!", self_bot=True, intents=Intents.default())
slash = SlashCommand(bot, sync_commands=True, debug_guild=817023577496748052)

bot.load_extension("Towa")
bot.run(config.getapiKey())