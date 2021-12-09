from distee.application_command import ApplicationCommand, ApplicationCommandOption
from distee.client import Client
from distee.cog import Cog
import json
import dateparser

from distee.enums import ApplicationCommandOptionType
from distee.interaction import Interaction

with open('config.json', 'r', encoding='utf-8') as f:
    cfg = json.load(f)


class MainCog(Cog):

    def register(self):
        ap = ApplicationCommand(
            name='timestamp',
            description='Create a timestamp from the given date',
            options=[
                ApplicationCommandOption(
                    type=ApplicationCommandOptionType.STRING,
                    required=True,
                    name='date',
                    description='The date string you want to convert'
                )
            ]
        )
        self.client.register_command(ap, self.timestamp_command, True, None)

    async def timestamp_command(self, inter: Interaction):
        inp = inter.data.options[0]['value']
        dt = dateparser.parse(inp, languages=['de', 'en'])
        if dt is None:
            await inter.send(ephemeral=True,
                             content='<:no:860510179123658752> Unknown date string.\n'
                                     'Currently supported languages: English and German')
            return
        output = int(dt.timestamp())
        await inter.send(ephemeral=True,
                         content=f'`{output}`\n\n'
                                 f'<t:{output}:t>\n`<t:{output}:t>`\n'
                                 f'<t:{output}:T>\n`<t:{output}:T>`\n'
                                 f'<t:{output}:d>\n`<t:{output}:d>`\n'
                                 f'<t:{output}:D>\n`<t:{output}:D>`\n'
                                 f'<t:{output}>\n`<t:{output}>`\n'
                                 f'<t:{output}:F>\n`<t:{output}:F>`\n'
                                 f'<t:{output}:R>\n`<t:{output}:R>`')


client = Client()
client.message_cache_size = 0
client.build_member_cache = False

c = MainCog(client)
c.register()
client.run(cfg['token'])
