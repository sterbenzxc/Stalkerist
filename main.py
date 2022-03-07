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

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
tweet = tweepy.Client(consumer_key=CONSUMER_KEY,
                       consumer_secret=CONSUMER_SECRET,
                       access_token=ACCESS_TOKEN,
                       access_token_secret=ACCESS_TOKEN_SECRET,
                       bearer_token=BEARER_TOKEN)
                       
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
    channel = client.get_channel(943132906807787530)
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
    except Exception as e: 
        print(str(e))
    if toprint:
      updatelist(listObj)
      for y in reversed(toprint):
        await channel.send("@" + str(y) + " started following @CryptoSeersph")
    else:
      print("no to print")

@client.event
async def on_ready():
  test.start()
  
my_secret = env_vars['TOKEN']
client.run(my_secret)