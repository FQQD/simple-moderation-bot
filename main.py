import disnake
from disnake.ext import commands
import time
import aiofiles
from enum import Enum


#   EDITABLE THINGS ↓

bottoken = "TOKEN"

defaultembedcolor = disnake.Colour.green()

defaulterrorembedcolor = disnake.Colour.red()

#   EDITABLE THINGS ↑



intents = disnake.Intents.all()

Bot = commands.Bot(
    command_prefix=disnake.ext.commands.when_mentioned,
    intents=intents,
    activity=disnake.Activity(type=disnake.ActivityType.watching, name="/help | Made by FQQD.ᴅᴇ")
)


Bot.warnings = {}


@Bot.event
async def on_ready():
    
    for guild in Bot.guilds:
        Bot.warnings[guild.id] = {}
        
        async with aiofiles.open(f"warnings/{guild.id}.txt", mode="a") as temp:
            pass

        async with aiofiles.open(f"warnings/{guild.id}.txt", mode="r") as file:
            lines = await file.readlines()

            for line in lines:
                data = line.split(" ")
                member_id = int(data[0])
                admin_id = int(data[1])
                pointintime = int(data[2])
                reason = " ".join(data[3:]).strip("\n")

                try:
                    Bot.warnings[guild.id][member_id][0] += 1
                    Bot.warnings[guild.id][member_id][1].append((admin_id, pointintime, reason))

                except KeyError:
                    Bot.warnings[guild.id][member_id] = [1, [(admin_id, pointintime, reason)]] 
    
    
    print(f'Logged in as "{Bot.user}" ✔')
    
@Bot.event
async def on_guild_join(guild):
    Bot.warnings[guild.id] = {}
    
@Bot.slash_command(default_member_permissions=disnake.Permissions(moderate_members=True))
async def moderation(inter):
    pass


@moderation.sub_command(name="ban", description="Ban a member")
@commands.has_permissions(ban_members=True)
async def ban(
    self,
    inter,
    member:disnake.Member,
    *,
    reason
    ):
    if member.id == inter.author.id:
        embed = disnake.Embed(
            title = f"Error!",
            description = f"You can't ban yourself!",
            colour = defaulterrorembedcolor,
        )
        await inter.send(embed=embed)
        return
    
    if member.top_role >= inter.author.top_role:
        embed = disnake.Embed(
            title = f"Error!",
            description = f"You can't ban members with a higher role!",
            colour = defaulterrorembedcolor,
        )
        await inter.send(embed=embed)
        return
    
    
    if member.top_role >= inter.guild.me.top_role:
        embed = disnake.Embed(
            title = f"Error!",
            description = f"The Role of this bot is not high enought to ban this member.",
            colour = defaulterrorembedcolor,
        )
        await inter.send(embed=embed)
        return
    
    else:
        dmembed = disnake.Embed(
            title="Ban",
            description=f'You were banned because of **"{reason}"**',
            colour = defaultembedcolor,
        )
        guild = inter.guild
        dmembed.set_thumbnail(url=guild.icon.url if guild.icon else disnake.Embed.Empty)
        dmembed.set_author(
            name=f"{inter.guild}",
        )  
        await member.send(embed = dmembed)
        
        await member.ban(reason = reason)
        
        reasonEmbed = disnake.Embed(
            description = f'Succesfully banned {member.mention} because of "{reason}"',
            colour = defaultembedcolor
        )
        reasonEmbed.set_author(name=f"{member.name}" + "#"+ f"{member.discriminator}", icon_url='{}'.format(member.avatar))
        reasonEmbed.set_footer(text=f"Banned by {inter.author.name}", icon_url = '{}'.format(inter.author.avatar))
        await inter.send(embed=reasonEmbed)
        
        
@moderation.sub_command(name="kick", description="Kick a member")
@commands.has_permissions(kick_members=True)
async def kick(self, inter, member:disnake.Member, *, reason):
    if member.id == inter.author.id:
        embed = disnake.Embed(
            title = f"Error!",
            description = f"You can't kick yourself!",
            colour = defaulterrorembedcolor,
        )
        await inter.send(embed=embed)
        return
    
    
    if member.top_role >= inter.author.top_role:
        embed = disnake.Embed(
            title = f"Error!",
            description = f"You can't kick members with a higher role!",
            colour = defaulterrorembedcolor,
        )
        await inter.send(embed=embed)
        return
    
    
    if member.top_role >= inter.guild.me.top_role:
        embed = disnake.Embed(
            title = f"Error!",
            description = f"The role of this bot is not high enough to kick this member.",
            colour = defaulterrorembedcolor,
        )
        await inter.send(embed=embed)
        return
    
    else: 
        
        dmembed = disnake.Embed(
            title="Kick",
            description=f'You were kicked because of **"{reason}"**',
            colour = defaultembedcolor,
        )
        
        guild = inter.guild
        
        dmembed.set_thumbnail(url=guild.icon.url if guild.icon else disnake.Embed.Empty)
        dmembed.set_author(
            name=f"{inter.guild}",
        )  
        
        await member.send(embed = dmembed)
        
        await member.kick(reason = reason)
        reasonEmbed = disnake.Embed(
            description = f'Succesfully kicked {member.mention} because of "{reason}"',
            colour = defaultembedcolor
        )
        reasonEmbed.set_author(name=f"{member.name}" + "#"+ f"{member.discriminator}", icon_url='{}'.format(member.avatar))
        reasonEmbed.set_footer(text=f"Kicked by {inter.author.name}", icon_url = '{}'.format(inter.author.avatar))
        await inter.send(embed=reasonEmbed)
    
@moderation.sub_command(name="warn", description="Warn a member")
async def warn(inter, member:disnake.Member, *, reason):
    
    t_epoch = time.time()
    
    t_epoch_str = str(t_epoch)
    
    t_epoch_cut = t_epoch_str[:10]
    
    try:
        first_warning = False
        Bot.warnings[inter.guild.id][member.id][0] += 1
        Bot.warnings[inter.guild.id][member.id][1].append((inter.author.id, reason))

    except KeyError:
        first_warning = True
        Bot.warnings[inter.guild.id][member.id] = [1, [(inter.author.id, reason)]]

    count = Bot.warnings[inter.guild.id][member.id][0]

    async with aiofiles.open(f"warnings/{inter.guild.id}.txt", mode="a") as file:
        await file.write(f"{member.id} {inter.author.id} {t_epoch_cut} {reason}\n")


    embed = disnake.Embed(
        title="Warn",
        description=f'Succesfully warned {member.mention} beacause of "{reason}" \n This is their {count}. warning.',
        colour = defaultembedcolor
    )
    embed.set_author(name=f"{member.name}" + "#"+ f"{member.discriminator}", icon_url='{}'.format(member.avatar))
    embed.set_footer(text=f"Warned by {inter.author.name}", icon_url = '{}'.format(inter.author.avatar))
    


    await inter.send(embed=embed)
    
    dmembed = disnake.Embed(
            title="Warn",
            description=f'You were warned because of **"{reason}"**',
            colour = defaultembedcolor,
        )
        
    guild = inter.guild
        
    dmembed.set_thumbnail(url=guild.icon.url if guild.icon else disnake.Embed.Empty)
    dmembed.set_author(
    name=f"{inter.guild}",
    )  
    
    dmembed.set_author(
    name=f"{inter.guild}",
    )   
        
    await member.send(embed = dmembed)
    
    
    
@moderation.sub_command(name="warnings", description="See, which warnings a member has")
async def warnings(inter, member: disnake.Member):
    
    embed = disnake.Embed(
        title=f"Warnings of {member.name}#{member.discriminator}",
        description="",
        colour=defaultembedcolor
        )
    
    embed.set_author(name=f"{member.name}" + "#"+ f"{member.discriminator}", icon_url='{}'.format(member.avatar))
    embed.set_footer(text=f"Requested by {inter.author.name}", icon_url = '{}'.format(inter.author.avatar))
    
    for guild in Bot.guilds:
        Bot.warnings[guild.id] = {}
        
        async with aiofiles.open(f"warnings/{guild.id}.txt", mode="a") as temp:
            pass

        async with aiofiles.open(f"warnings/{guild.id}.txt", mode="r") as file:
            lines = await file.readlines()

            for line in lines:
                data = line.split(" ")
                member_id = int(data[0])
                admin_id = int(data[1])
                pointintime = int(data[2])
                reason = " ".join(data[3:]).strip("\n")

                try:
                    Bot.warnings[guild.id][member_id][0] += 1
                    Bot.warnings[guild.id][member_id][1].append((admin_id, pointintime, reason))

                except KeyError:
                    Bot.warnings[guild.id][member_id] = [1, [(admin_id, pointintime, reason)]] 
    
    try:
        i = 1
        for admin_id, pointintime, reason in Bot.warnings[inter.guild.id][member.id][1]:
            admin = inter.guild.get_member(admin_id)
            embed.description += f"**#{i}** <t:{pointintime}:d> Mod: {admin.mention} Reason: *'{reason}'*\n"
            i += 1

        await inter.send(embed=embed)

    except KeyError: # no warnings
            
        embed2=disnake.Embed(
        title=f"Warnings of {member.name}#{member.discriminator}",
        description=f"{member.mention} was never warned",
        color=defaultembedcolor
        )
    
        embed2.set_author(name=f"{member.name}" + "#"+ f"{member.discriminator}", icon_url='{}'.format(member.avatar))
        embed2.set_footer(text=f"Requested by {inter.author.name}", icon_url = '{}'.format(inter.author.avatar))
        
            
        await inter.send(embed=embed2)

    

@moderation.sub_command(name="removewarnings", description="Remove warnings of a Member")
async def removewarnings(inter, member:disnake.Member, removereason, choose: str = commands.Param(choices={"All warnings": "all", "Choose warning": "singlewarning"})):
    
    
    if choose == "all":
        
        try:
        
            myfile = f"warnings/{inter.guild.id}.txt"
            
            count = Bot.warnings[inter.guild.id][member.id][0]

            warnings_id_list = []
            
            
            async with aiofiles.open(f"warnings/{inter.guild.id}.txt", mode="r") as file:
                lines = await file.readlines()

                for line in lines:
                    data = line.split(" ")
                    member_id = int(data[0])
                    admin_id = int(data[1])
                    pointintime = int(data[2])
                    reason = " ".join(data[3:]).strip("\n")
                    
                    
                    warnings_id_list += [str(member_id)]
            
            while str(member.id) in warnings_id_list:
                
            
                indexe = warnings_id_list.index(str(member.id))
            
                    
                try:
                    with open(myfile, 'r') as fr:
            # reading line by line
                        lines = fr.readlines()
            
            # pointer for position
                        ptr = 0
        
            # opening in writing mode
                        with open(myfile, 'w') as fw:
                            for line in lines:
                
                    # we want to remove 5th line
                                if ptr != indexe:
                                    fw.write(line)
                                ptr += 1
        
                except:
                    pass
                            
                                
                del warnings_id_list[indexe]
                
                time.sleep(0.1)
            
            
            embed = disnake.Embed(
            title="Removing Warnings",
            description=f'Succesfully removed all {count} warnings of {member.mention} because of "{removereason}"',
            colour = defaultembedcolor
            )
    
            embed.set_author(name=f"{member.name}" + "#"+ f"{member.discriminator}", icon_url='{}'.format(member.avatar))
            embed.set_footer(text=f"Removed by {inter.author.name}", icon_url = '{}'.format(inter.author.avatar))
    
            await inter.send(embed=embed)
            
            dmembed = disnake.Embed(
                title="Warnings removed",
                description=f'Removed all your warnings because of **"{removereason}"**',
                colour = defaultembedcolor,
            )
            guild = inter.guild
            dmembed.set_thumbnail(url=guild.icon.url if guild.icon else disnake.Embed.Empty)
            dmembed.set_author(
                name=f"{inter.guild}",
            )  
            await member.send(embed = dmembed)
        
        except KeyError:
            embed2=disnake.Embed(
            title=f"Warnings of {member.name}#{member.discriminator}",
            description=f"{member.mention} was never warned",
            color=defaultembedcolor
            )
    
            embed.set_author(name=f"{member.name}" + "#"+ f"{member.discriminator}", icon_url='{}'.format(member.avatar))
            embed.set_footer(text=f"Removed by {inter.author.name}", icon_url = '{}'.format(inter.author.avatar))
            
            
            await inter.send(embed=embed2)
        
        
        return
        
    if choose == "singlewarning":
        
        inter.send("This function currently doesnt exist, were working on it")
        
        #try:
        
            #warnings_list = []
       
            #singlewarning_i = 1
            #for admin_id, pointintime, reason in Bot.warnings[inter.guild.id][member.id][1]:
           # 
           #     teststr = f"#{singlewarning_i} '{reason}'"
           # 
           #     warnings_list += [teststr]
           # 
           #     singlewarning_i += 1
                

           # print(str(warnings_list))
           # 
           # choosemessageembed = disnake.Embed(
           #     title="Warnings erfolgreich gelöscht",
           #     description=f'Erfolgreich alle ausgewählte Warning von {member.mention} wegen "{removereason}" entfernt.',
           #     colour = defaultembedcolor
           # )
           # await inter.send(embed=choosemessageembed)
            
            
            
            
            #embed = disnake.Embed(
            #title="Warnings erfolgreich gelöscht",
            #description=f'Erfolgreich alle ausgewählte Warning von {member.mention} wegen "{removereason}" entfernt.',
            #colour = defaultembedcolor
            #)
            #await inter.send(embed=embed)
            
        
        #except KeyError:
        #    embed2=disnake.Embed(
        #    title=f"Warnungen von {member.name}#{member.discriminator}",
        #    description=f"{member.mention} wurde nie gewarnt",
        #    color=defaultembedcolor
        #    )
            
        #    await inter.send(embed=embed2)
            
        return
        
        
            
    else:
        errorembed = disnake.Embed(
            title = f"Error!",
            description = f"Something went wrong",
            colour = defaulterrorembedcolor,
        )
        await inter.send(embed=errorembed)
        
    
    
@Bot.slash_command(default_member_permissions=disnake.Permissions(moderate_members=True))
async def user(inter):
    pass
@user.sub_command(name="info", description="See information about a member")
async def info(inter, member:disnake.Member):
    
    for guild in Bot.guilds:
        Bot.warnings[guild.id] = {}
        
        async with aiofiles.open(f"warnings/{guild.id}.txt", mode="a") as temp:
            pass

        async with aiofiles.open(f"warnings/{guild.id}.txt", mode="r") as file:
            lines = await file.readlines()

            for line in lines:
                data = line.split(" ")
                member_id = int(data[0])
                admin_id = int(data[1])
                pointintime = int(data[2])
                reason = " ".join(data[3:]).strip("\n")

                try:
                    Bot.warnings[guild.id][member_id][0] += 1
                    Bot.warnings[guild.id][member_id][1].append((admin_id, pointintime, reason))

                except KeyError:
                    Bot.warnings[guild.id][member_id] = [1, [(admin_id, pointintime, reason)]] 
    
    
    date_time = str(member.created_at)
    
    cut_date_time = date_time[0:19]
    
    pattern = '%Y-%m-%d %H:%M:%S'
    epoch = int(time.mktime(time.strptime(cut_date_time, pattern)))
    
    try:
        count = Bot.warnings[inter.guild.id][member.id][0]
    except KeyError:
        count = "0"
    
    embed = disnake.Embed(
        title="User Info",
        color=defaultembedcolor
    )
    
    embed.set_author(
        name=str(member.name+"#"+member.discriminator),
    )
    
    embed.set_thumbnail(
        url=member.avatar.url if member.avatar else disnake.Embed.Empty 
    )
    
    embed.add_field(name="Username", value=str('`'+member.name+"#"+member.discriminator+'`'), inline=True)
    embed.add_field(name="Nickname", value=str('`'+member.display_name+'`'), inline=True)
    embed.add_field(name="User ID", value=str('`'+str(member.id)+'`'), inline=False)
    embed.add_field(name="Is bot?", value=str('`'+str(member.bot)+'`'), inline=True)
    embed.add_field(name="Created at", value=f"<t:{str(epoch)}:f>", inline=False)
    embed.add_field(name="Warnings", value='`'+str(count)+'`', inline=False)
    
    await inter.send(embed=embed)
    
    
    

@moderation.sub_command(name="help", description="Help for moderation commands")
async def help(inter):
    
    embed = disnake.Embed (
        title="FQQDs Moderation Bot - Moderation Help",
        description=f'Here you can find some help for every moderation command.\nMembers are notified per direct message for every action\nFor every moderation command the "Moderate Members" permission is required',
        colour = defaultembedcolor
    )
    
    embed.add_field(name="/moderation ban", value="Ban members (Use Discord intern feature for message removal)", inline=False)
    embed.add_field(name="/moderation kick", value="Kick members", inline=False)
    embed.add_field(name="/moderation warn", value="Warn members", inline=False)
    embed.add_field(name="/moderation warnings", value="See all warnings of a member", inline=False)
    embed.add_field(name="/moderation removewarnings", value="Remove warnings of a member", inline=False)
    embed.add_field(name="/user info", value="See information about a member", inline=False)
    
    
    await inter.send(embed=embed)
    
@Bot.slash_command(name="help", description="Help for commands")
async def help(inter):
    embed = disnake.Embed (
        title="FQQDs Moderation Bot - Help",
        description=f'Here you can find help for every command that is accesible for every user',
        colour = defaultembedcolor
    )
    
    embed.add_field(name="/credit", value="See the credits of the bots", inline=False)
    embed.add_field(name="/avatar", value="Show and download the profile picture of a user", inline=False)
    embed.add_field(name="/help", value="Show this list", inline=False)
    
    
    await inter.send(embed=embed)
    
@Bot.slash_command(name="credit", description="Credits of the bot")
async def credit(inter):
    embed = disnake.Embed (
        title="FQQDs Moderation Bot - Credits",
        description=f'Bot coded by FQQD#2557\nGithub: https://github.com/FQQD/simple-moderation-bot/\nhttps://www.FQQD.de',
        colour = defaultembedcolor
    )
    
    
    await inter.send(embed=embed) 
    
    
@Bot.slash_command(name="avatar", description="Show and download the profile picture of a user")
async def avatar(inter, member:disnake.Member):
    embed = disnake.Embed(
        title=f"Avatar of {member.name}#{member.discriminator}",
        description=f"URL: {member.avatar.url}",
        color=defaultembedcolor,
    )
    embed.set_image(
    url=member.avatar.url,
    )
    
    embed.set_author(name=f"{member.name}" + "#"+ f"{member.discriminator}", icon_url='{}'.format(member.avatar))
    embed.set_footer(text=f"Requested by {inter.author.name}", icon_url = '{}'.format(inter.author.avatar))
    
    
    await inter.send(embed=embed)



Bot.run(bottoken)
