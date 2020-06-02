import discord


def create_embed_table(title: str, headers: list, entries: list, description: str = '', color: int = 0xff0000):
    embed = discord.Embed(title=title, description=description, color=color)

    if len(headers) == 3:
        embed.add_field(name='```{0:<20}{1:^20}{2:^20}```'.format(headers[0], headers[1], headers[2]),
                        value='\u200b',
                        inline=False)

    for e in entries:
        if len(e) == 3:
            embed.add_field(name='```{:<20}{:^20}{:^20}\n```'.format(e[0], e[1], e[2]),
                            value='\u200b',
                            inline=False)

    return embed