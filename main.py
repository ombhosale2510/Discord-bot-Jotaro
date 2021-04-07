import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive


client = discord.Client()

# ENCOURAGEMENT MESSAGES
sad_words = ["sad", "sadness", "depressed", "depression", "unhappy", "miserable", "misery", "depressing", "dissapoint", "dissapointed", "dissapointment"]

starter_encouragements = [
  "Cheer up",
  "Hang in there",
  "You are a great person / bot!",
  "Don't worry, It'll get better"
]


# GET ENOURAGING QUOTES
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)


#UPDATE ENCOURAGEMENTS IN DB
def update_encouragements(enc_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(enc_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [enc_message]


#DELETE ENCOURAGEMENTS IN DB
def delete_encouragements(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  # RESPOND TO HELLO
  msg = message.content
  if msg.startswith('$hello'):
    await message.channel.send('Hie!')

  # RESPOND WITH ENCOURAGING QUOTES
  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  
  options = starter_encouragements
  if "encouragements" in db.keys():
    # use this instead of concatenating
    options.extend(db["encouragements"])
  
  # AUTO REPSONSE TO SAD WORDS
  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    enc_message = msg.split("$new ",1)[1]
    update_encouragements(enc_message)
    await message.channel.send("New encouraging message added!")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del ",1)[1])
      delete_encouragements(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)


keep_alive()
client.run(os.getenv('TOKEN'))
