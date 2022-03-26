import discord
import tweepy
import json
from discord.ext import tasks

with open('variables.json') as f:
        env_vars = json.load(f)

client = discord.Client()

CONSUMER_KEY = env_vars['CKEY']
CONSUMER_SECRET = env_vars['CSECRET']
ACCESS_TOKEN = env_vars['ACTOKEN']
ACCESS_TOKEN_SECRET = env_vars['ACSECRET']
BEARER_TOKEN = env_vars['BEARER']

follownames = {"1231611929082368001":"manilacrypto1","2309701":"gabusch","1435957188690726915":"realcoreywilton","1233575893647257602":"0xElle","1345761074293870592":"realdealguild","1318927549091622913":"YieldGuild","903085850115940352":"cagyjan1","1009692722976788480":"Jihoz_axie","2697947171":"brycent_","1344927888357740544":"CryptoSeersph"}
followids = [1231611929082368001,2309701,1435957188690726915,1233575893647257602,1345761074293870592,1318927549091622913,903085850115940352,1009692722976788480,2697947171,1344927888357740544]

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth,wait_on_rate_limit=True)
tweet = tweepy.Client(consumer_key=CONSUMER_KEY,consumer_secret=CONSUMER_SECRET,access_token=ACCESS_TOKEN,access_token_secret=ACCESS_TOKEN_SE
CRET,bearer_token=BEARER_TOKEN)
                       
user = tweet.get_user(username = 'CryptoSeersph')

# function to add to JSON
def updatelist(new_data, filename='followers.json'):
    with open(filename, 'w') as json_file:
      json.dump(new_data, json_file, 
                        indent=2,  
                        separators=(',',': '))


@tasks.loop(minutes=1)
async def test():
    with open('followers.json') as fp:
        listObj = json.load(fp)
    printed = []
    channel = client.get_channel(943156748246741026)
    for x in listObj:
      values_view = x.values()
      value_iterator = iter(values_view)
      id = next(value_iterator)
      printed.append(id)
    try:
        c = tweet.get_users_followers(id = user.data.id)
        toprint = []
        for x in c.data:
          if str(x.id) not in printed:
            toprint.append(x.username)
            listObj.append({"id": str(x.id),"name": str(x.name),"username": str(x.username)})
          else:
            continue
        if toprint:
          updatelist(listObj)
          for y in reversed(toprint):
            await channel.send("@" + str(y) + " started following @CryptoSeersph")
        else:
          print("no to print")
    except Exception as e: 
        print(str(e))

@tasks.loop(minutes=1)
async def following():
  channel = client.get_channel(951772218130575480)
  for ids in followids:
    listObj = []
    with open(str(ids)+".json") as fp:
        listObj = json.load(fp)
    printed = []
    for x in listObj:
      values_view = x.values()
      value_iterator = iter(values_view)
      id = next(value_iterator)
      printed.append(id)
    for user in tweepy.Cursor(api.get_friend_ids,user_id=ids).items(20):
      toprint=[]
      if str(user) not in printed:
        toprint.append(user)
        listObj.append({"id": str(user),"name": "x","username": "x"})
      else:
        continue
    if toprint:
      for y in reversed(toprint):
        user_details = api.get_user(user_id=y)
        await channel.send(follownames[str(ids)] + " started following @" + str(user_details.screen_name) + "\n https://twitter.com/" + str(user_details.screen_name))
    else:
      print("no to print")
    updatelist(listObj,filename=str(ids)+".json")
    
    

@client.event
async def on_ready():
  test.start()
  following.start()
  
my_secret = env_vars['TOKEN']
client.run(my_secret)