    # # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    # @commands.hybrid_command(
    #     name="movie",
    #     # description=f"Hey {self.bot.name}, What movie should I watch?",
    #     description="What movie should I watch?",
    # )
    # @checks.not_blacklisted()
    # async def movie(self, context: Context) -> None:
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get("https://script.google.com/macros/s/AKfycbygn4fG-jiZqmIrqmiSDyzy8cOjeXDHUPAhA5OHVqLPW0WQLhn172dU3b-K5T2eg8pVPw/exec") as request:
    #             if request.status == 200:
    #                 spreadsheet_data = await request.json()
    #                 movie_str = spreadsheet_data["movie"]
    #                 await self.bot.get_response(context=context, prompt=f"Give a recommendation for the movie {movie_str}.\n")
    #             else:
    #                 embed = discord.Embed(
    #                     title="Error!",
    #                     description="There is something wrong with the API, please try again later",
    #                     color=0xE02B2B
    #                 )
    #                 await context.send(embed=embed)
    