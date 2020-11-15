import discord
import getpass
import os
import collections
USER_NAME = getpass.getuser()
client = discord.Client()
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


def topKFrequent(words, k):
    try:
        split_it = words.split()
        CounterVar = collections.Counter(split_it)
        return CounterVar.most_common(int(k))
    except:

        return "Argument Error"


before_messages = {}
onHold = False
lastMessage = ""

@client.event
async def on_message(message):
    tempSpamNum = 0
    secondTempSpamNum = 0
    isNotAccepted = False
    global onHold
    global lastMessage
    user = message.author.id
    for x in range(len(message.content.lower().split())):
        if message.content.lower().split()[x] in message.content.lower().split():
            secondTempSpamNum = secondTempSpamNum + 1
    if secondTempSpamNum > 2 or message.content.lower() == lastMessage:
        print('not accepted')
        return
    try:
        for x in range(len(message.content.lower().split())):
            if message.content.lower().split().count(message.content.lower().split()[x]) > 2:
                tempSpamNum+=1
        if tempSpamNum == 1 and len(message.content.lower().split()) < 2:
            isNotAccepted = True
            onHold = True
        elif tempSpamNum == 2 and len(message.content.lower().split()) < 4:
            isNotAccepted = True
            onHold = True
        elif tempSpamNum == 3 and len(message.content.lower().split()) < 6:
            isNotAccepted = True
            onHold = True
        elif tempSpamNum > 3:
            isNotAccepted = True
            onHold = True
    except KeyError:
        before_messages[user] = []
    finally:
        try:
            before_messages[user].append(message.content.lower())
        except:
            return
    if isNotAccepted:
        isNotAccepted = False
        print('not accepted')
        return
    if onHold:
        onHold = False
        before_messages[user] = []
    tempNum = 0
    tempChar = 0
    totalWords = 0
    tempCountString = ""
    if message.author == client.user:
        return

    f=open("words.txt", "r+")
    read = f.read()
    f=open("words.txt", "a")
    content = message.content
    f.write(" " + content + " ")
    contentSplit = content.split()
    if contentSplit[0].upper() == '-STATS':
        for x in range(len(contentSplit)):
            if contentSplit[x].upper() != '-STATS':
                tempCountString = tempCountString + " " + contentSplit[x]
        for word in read.split():
            totalWords = totalWords + 1
        tempNum = read.count(tempCountString)
        embedVar = discord.Embed(title="Stats", description="How much this word has been sent.", color=0x000000)
        embedVar.add_field(name="The word provided has been mentioned: ", value=str(tempNum)+" times")
        embedVar.add_field(name="This is:", value=str((tempNum/totalWords)*100) + "%" + " of all messages")
        if content != '-stats':
            await message.channel.send(embed = embedVar)

    if message.content.upper() == '-STATS':
        embedVar = discord.Embed(title="Stats", description="A summary of all stats", color=0x000000)
        embedVar.add_field(name="A total of: ", value=str(totalWords) + " messages have been sent.")
        for char in read:
            tempChar = tempChar+1
        embedVar.add_field(name="With: ", value=str(tempChar) + " characters in total.")
        await message.channel.send(embed=embedVar)
    if message.content.upper() == '-HELP':
        embed = discord.Embed(title="Help", description="You need help?", color=0x5c5c5c)
        embed.add_field(name="-stats [x]",
                        value="Will provide stats about [x] phrase, including what percentage of messages contain [x] and how many times it is mentioned",
                        inline=False)
        embed.add_field(name="-stats",
                        value="Provides an overview of all statistics on the provided server, including number of characters and number of words",
                        inline=False)
        embed.add_field(name="-common [x]", value="Provides top [x] most messaged words", inline=True)

        await message.channel.send(embed=embed)
    if contentSplit[0].upper() == '-COMMON':
        if len(contentSplit) == 2:
            embedVar = discord.Embed(title="Top " + str(contentSplit[1]) + " Words", description="List of most common words", color=0x000000)
            print(str(topKFrequent(read, contentSplit[1])))
            embedVar.add_field(name="Results ", value=str(topKFrequent(read, contentSplit[1])), inline=False)
            try:
                await message.channel.send(embed=embedVar)
            except:
                await message.channel.send("Common length must be 73 or lower")

        else:
            await message.channel.send('Argument not correct.')

    lastMessage = message.content.lower()
    tempNum = 0
    totalWords = 0
    tempChar = 0
    tempCountString = ""
    tempSpamNum = 0
    secondTempSpamNum = 0

    f.close()





client.run('enter token here')
