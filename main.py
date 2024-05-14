import discord
from discord.ui import Button, View
from discord import app_commands, Interaction, ButtonStyle
import os
import json
import datetime

CONFIG = 'config.json'

def load_config():
    with open(CONFIG, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

def save_config(config):
    with open(CONFIG, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)

class MyClient(discord.Client):
    async def on_ready(self):
        await self.wait_until_ready()
        await tree.sync()
        print(f"{self.user} 에 로그인하였습니다!")

intents = discord.Intents.all()
client = MyClient(intents=intents)
tree = app_commands.CommandTree(client)
config = load_config()
TOKEN = config['token']
CHANNEL_ID = config['channel_id']

@client.event
async def on_interaction(interaction: Interaction):
    if 'custom_id' in interaction.data:
        if interaction.data['custom_id'] == "green_button":
            await green_button_clicked(interaction)
        elif interaction.data['custom_id'] == "red_button":
            await red_button_clicked(interaction)

async def green_button_clicked(interaction: Interaction):
    t = "관리자 출근"
    d = f"{interaction.user.display_name}님이 출근하였습니다."
    c = discord.Colour.green()
    e = discord.Embed(title=t, description=d, colour=c)
    e.timestamp = datetime.datetime.now()
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(embed=e)
        await interaction.response.send_message(f"{interaction.user.display_name}님 메세지전송을 완료했습니다,", ephemeral=True)
    else:
        await interaction.response.send_message("채널을 찾을 수 없습니다.", ephemeral=True)
    
async def red_button_clicked(interaction: Interaction):
    t = "관리자 퇴근"
    d = f"{interaction.user.display_name}님이 퇴근하였습니다."
    c = discord.Colour.red()
    e = discord.Embed(title=t, description=d, colour=c)
    e.timestamp = datetime.datetime.now()
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(embed=e)
        await interaction.response.send_message(f"{interaction.user.display_name}님 메세지전송을 완료했습니다,", ephemeral=True)
    else:
        await interaction.response.send_message("채널을 찾을 수 없습니다.", ephemeral=True)

@tree.command(name="버튼", description="버튼 생성")
@app_commands.checks.has_permissions(administrator=True)
async def button(interaction: Interaction):
    time_now = datetime.datetime.now()
    t = "출퇴근"
    d = "초록버튼을 눌러 출근 메세지를 전송하세요\n빨간버튼을 눌러 퇴근 메세지를 전송하세요"
    c = discord.Colour.blue()
    e = discord.Embed(title=t, description=d, colour=c)
    e.timestamp = time_now

    green_button = Button(
        style=ButtonStyle.green,
        label="출근",
        custom_id="green_button",
        disabled=False
    )

    red_button = Button(
        style=ButtonStyle.red,
        label="퇴근",
        custom_id="red_button",
        disabled=False
    )

    view = View(timeout=None)
    view.add_item(green_button)
    view.add_item(red_button)
    await interaction.response.send_message(embed=e, view=view)

client.run(TOKEN)
