import openai
import os
import discord
from keep_alive import keep_alive
import prompts

intents = discord.Intents.all()
openai.api_key = os.environ['OPENAI_API_KEY']
client = discord.Client(intents=intents)
'''
Roleplay as Violette
v say - violette will say what you write in her own words
v !say - she will emote first, and then say
v !sarcasm - she will say what you write in a sarcastic tone
v !say exactly - violette will say exactly what you write, how you write it

Make Violette Reply on her own
v reply - violette will reply to a message in her own words
v !reply - she will emote first, and then reply
v !sarcastic reply - she will reply in a sarcastic tone
'''
AUTHORIZED_ROLES = [1009894592562339902, 1074067345917624373]


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  # We will use this to implement role gating
  authorized_role_list = len(
    [x.id for x in message.author.roles if x.id in AUTHORIZED_ROLES])
  if authorized_role_list == 0:
    print("not authorized")
    return

  # SAY OR REPLY IN AUTHORS WORDS
  if message.content.startswith('v say'):
    referenced_message = await message.channel.fetch_message(
      message.reference.message_id) if message.reference is not None else None
    human_input = message.content[len('v say'):].strip()
    await message.delete()

    prompt = f'''{prompts.who_is_violette}
    {prompts.tone}
    Rewrite the following dialogue in a way Violette would say it, as dialogue: {human_input}'''

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[
                                              {
                                                "role": "user",
                                                "content": prompt
                                              },
                                            ])
    print(response.choices[0].message.content)
    await message.channel.send(response.choices[0].message.content,
                               reference=referenced_message)

  if message.content.startswith('v sarcasm'):
    referenced_message = await message.channel.fetch_message(
      message.reference.message_id) if message.reference is not None else None
    human_input = message.content[len('v sarcasm'):].strip()
    await message.delete()

    prompt = f'''{prompts.who_is_violette}
    {prompts.tone}
    Rewrite the following dialogue in a way Violette would say it, as dialogue, and use sarcasm: {human_input}'''

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[
                                              {
                                                "role": "user",
                                                "content": prompt
                                              },
                                            ])
    print(response.choices[0].message.content)
    await message.channel.send(response.choices[0].message.content,
                               reference=referenced_message)

  if message.content.startswith('v repeat'):
    referenced_message = await message.channel.fetch_message(
      message.reference.message_id) if message.reference is not None else None
    human_input = message.content[len('v repeat'):].strip()
    await message.delete()
    print(human_input)
    await message.channel.send(human_input, reference=referenced_message)

  # REPLY IN OWN WORDS
  if message.content.startswith('v reply') and message.reference is not None:
    referenced_message = await message.channel.fetch_message(
      message.reference.message_id)
    human_input = referenced_message.content
    await message.delete()

    prompt = f'''{prompts.who_is_violette}
    {prompts.violette_background}
    {prompts.tone}
    Reply conversationally to the following message as if you were Violette, as dialogue: {human_input}'''

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[
                                              {
                                                "role": "user",
                                                "content": prompt
                                              },
                                            ])
    print(response.choices[0].message.content)
    await message.channel.send(response.choices[0].message.content,
                               reference=referenced_message)

  if message.content.startswith(
      'v sarcastic reply') and message.reference is not None:
    referenced_message = await message.channel.fetch_message(
      message.reference.message_id)
    human_input = referenced_message.content
    await message.delete()

    prompt = f'''{prompts.who_is_violette}
    {prompts.violette_background}
    {prompts.tone}
    Reply with dialogue to the following message as if you were Violette, as dialogue, and use sarcasm: {human_input}'''

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[
                                              {
                                                "role": "user",
                                                "content": prompt
                                              },
                                            ])
    print(response.choices[0].message.content)
    await message.channel.send(response.choices[0].message.content,
                               reference=referenced_message)

  if message.content == 'v delete':
      # Get the bot's previous message
      async for previous_message in message.channel.history(limit=50):
          if previous_message.author == client.user:
              # Delete the bot's previous message
              await previous_message.delete()
              break
      await message.delete()



keep_alive()
TOKEN = os.environ['TOKEN']
print(TOKEN)
client.run(TOKEN)
