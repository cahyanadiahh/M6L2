import discord
from discord.ext import commands
from logic import reve_api
from config import TOKEN
import os

# Inisialisasi bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Handler untuk pesan teks
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    prompt = message.content

    # Menggunakan Reve API untuk menghasilkan gambar
    file_path = "generated_image.png"
    result = reve_api.generate_image(
        prompt,
        save_json=None,
        save_image=file_path
    )

    # Mengirimkan gambar ke pengguna
    with open(file_path, 'rb') as photo:
        await message.channel.send(file=discord.File(photo, "generated_image.png"))

    # Menghapus gambar setelah dikirim
    os.remove(file_path)

# Menjalankan bot
bot.run(TOKEN)