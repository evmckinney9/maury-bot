# """"
# Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
# Description:
# This is a template to create your own discord bot in python.

# Version: 5.4
# """

# import discord
# from discord import app_commands
# from discord.ext import commands
# from discord.ext.commands import Context

# from helpers import checks, db_manager


# class Moderation(commands.Cog, name="moderation"):
#     """
#     List of commands:
#         - Kick
#         - Ban
#         - Warn
#     """
#     def __init__(self, bot):
#         self.bot = bot

#     @commands.hybrid_command(
#         name="kick",
#         description="Kick a user out of the server.",
#     )
#     @commands.has_permissions(kick_members=True)
#     @commands.bot_has_permissions(kick_members=True)
#     @checks.not_blacklisted()
#     @app_commands.describe(user="The user that should be kicked.", reason="The reason why the user should be kicked.")
#     async def kick(self, context: Context, user: discord.User, *, reason: str = "Not specified") -> None:
#         """
#         Kick a user out of the server.

#         :param context: The hybrid command context.
#         :param user: The user that should be kicked from the server.
#         :param reason: The reason for the kick. Default is "Not specified".
#         """
#         member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
#         if member.guild_permissions.administrator:
#             embed = discord.Embed(
#                 title="Error!",
#                 description="User has Admin permissions.",
#                 color=0xE02B2B
#             )
#             await context.send(embed=embed)
#         else:
#             try:
#                 embed = discord.Embed(
#                     title="User Kicked!",
#                     description=f"**{member}** was kicked by **{context.author}**!",
#                     color=0x9C84EF
#                 )
#                 embed.add_field(
#                     name="Reason:",
#                     value=reason
#                 )
#                 await context.send(embed=embed)
#                 try:
#                     await member.send(
#                         f"You were kicked by **{context.author}**!\nReason: {reason}"
#                     )
#                 except:
#                     # Couldn't send a message in the private messages of the user
#                     pass
#                 await member.kick(reason=reason)
#             except:
#                 embed = discord.Embed(
#                     title="Error!",
#                     description="An error occurred while trying to kick the user. Make sure my role is above the role of the user you want to kick.",
#                     color=0xE02B2B
#                 )
#                 await context.send(embed=embed)

#     @commands.hybrid_command(
#         name="nick",
#         description="Change the nickname of a user on a server.",
#     )
#     @commands.has_permissions(manage_nicknames=True)
#     @commands.bot_has_permissions(manage_nicknames=True)
#     @checks.not_blacklisted()
#     @app_commands.describe(user="The user that should have a new nickname.", nickname="The new nickname that should be set.")
#     async def nick(self, context: Context, user: discord.User, *, nickname: str = None) -> None:
#         """
#         Change the nickname of a user on a server.

#         :param context: The hybrid command context.
#         :param user: The user that should have its nickname changed.
#         :param nickname: The new nickname of the user. Default is None, which will reset the nickname.
#         """
#         member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
#         try:
#             await member.edit(nick=nickname)
#             embed = discord.Embed(
#                 title="Changed Nickname!",
#                 description=f"**{member}'s** new nickname is **{nickname}**!",
#                 color=0x9C84EF
#             )
#             await context.send(embed=embed)
#         except:
#             embed = discord.Embed(
#                 title="Error!",
#                 description="An error occurred while trying to change the nickname of the user. Make sure my role is above the role of the user you want to change the nickname.",
#                 color=0xE02B2B
#             )
#             await context.send(embed=embed)

#     @commands.hybrid_command(
#         name="ban",
#         description="Bans a user from the server.",
#     )
#     @commands.has_permissions(ban_members=True)
#     @commands.bot_has_permissions(ban_members=True)
#     @checks.not_blacklisted()
#     @app_commands.describe(user="The user that should be banned.", reason="The reason why the user should be banned.")
#     async def ban(self, context: Context, user: discord.User, *, reason: str = "Not specified") -> None:
#         """
#         Bans a user from the server.

#         :param context: The hybrid command context.
#         :param user: The user that should be banned from the server.
#         :param reason: The reason for the ban. Default is "Not specified".
#         """
#         member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
#         try:
#             if member.guild_permissions.administrator:
#                 embed = discord.Embed(
#                     title="Error!",
#                     description="User has Admin permissions.",
#                     color=0xE02B2B
#                 )
#                 await context.send(embed=embed)
#             else:
#                 embed = discord.Embed(
#                     title="User Banned!",
#                     description=f"**{member}** was banned by **{context.author}**!",
#                     color=0x9C84EF
#                 )
#                 embed.add_field(
#                     name="Reason:",
#                     value=reason
#                 )
#                 await context.send(embed=embed)
#                 try:
#                     await member.send(f"You were banned by **{context.author}**!\nReason: {reason}")
#                 except:
#                     # Couldn't send a message in the private messages of the user
#                     pass
#                 await member.ban(reason=reason)
#         except:
#             embed = discord.Embed(
#                 title="Error!",
#                 description="An error occurred while trying to ban the user. Make sure my role is above the role of the user you want to ban.",
#                 color=0xE02B2B
#             )
#             await context.send(embed=embed)

#     @commands.hybrid_group(
#         name="warning",
#         description="Manage warnings of a user on a server.",
#     )
#     @commands.has_permissions(manage_messages=True)
#     @checks.not_blacklisted()
#     async def warning(self, context: Context) -> None:
#         """
#         Manage warnings of a user on a server.

#         :param context: The hybrid command context.
#         """
#         if context.invoked_subcommand is None:
#             embed = discord.Embed(
#                 title="Error!",
#                 description="Please specify a subcommand.\n\n**Subcommands:**\n`add` - Add a warning to a user.\n`remove` - Remove a warning from a user.\n`list` - List all warnings of a user.",
#                 color=0xE02B2B
#             )
#             await context.send(embed=embed)

#     @warning.command(
#         name="add",
#         description="Adds a warning to a user in the server.",
#     )
#     @checks.not_blacklisted()
#     @commands.has_permissions(manage_messages=True)
#     @app_commands.describe(user="The user that should be warned.", reason="The reason why the user should be warned.")
#     async def warning_add(self, context: Context, user: discord.User, *, reason: str = "Not specified") -> None:
#         """
#         Warns a user in his private messages.

#         :param context: The hybrid command context.
#         :param user: The user that should be warned.
#         :param reason: The reason for the warn. Default is "Not specified".
#         """
#         member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
#         total = await db_manager.add_warn(
#             user.id, context.guild.id, context.author.id, reason)
#         embed = discord.Embed(
#             title="User Warned!",
#             description=f"**{member}** was warned by **{context.author}**!\nTotal warns for this user: {total}",
#             color=0x9C84EF
#         )
#         embed.add_field(
#             name="Reason:",
#             value=reason
#         )
#         await context.send(embed=embed)
#         try:
#             await member.send(f"You were warned by **{context.author}**!\nReason: {reason}")
#         except:
#             # Couldn't send a message in the private messages of the user
#             await context.send(f"{member.mention}, you were warned by **{context.author}**!\nReason: {reason}")


# async def setup(bot):
#     await bot.add_cog(Moderation(bot))
