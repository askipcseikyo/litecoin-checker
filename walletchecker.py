import discord
import requests

ascii_art = """
▄▄▄     ▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄ ▄▄    ▄    ▄▄▄▄▄▄▄ ▄▄   ▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄   ▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄         ▄▄▄▄▄▄▄ ▄▄   ▄▄    ▄▄▄▄▄▄▄ ▄▄▄     ▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄   ▄▄ ▄▄    ▄ ▄▄▄▄▄▄▄ 
█   █   █   █       █       █       █       █   █  █  █ █  █       █  █ █  █       █       █   █ █ █       █   ▄  █       █  ▄    █  █ █  █  █       █   █   █      █       █       █       █  █ █  █  █  █ █       █
█   █   █   █▄     ▄█    ▄▄▄█       █   ▄   █   █   █▄█ █  █       █  █▄█  █    ▄▄▄█       █   █▄█ █    ▄▄▄█  █ █ █       █ █▄█   █  █▄█  █  █▄▄▄    █   █   █  ▄   █       █       █   ▄   █  █ █  █   █▄█ █▄     ▄█
█   █   █   █ █   █ █   █▄▄▄█     ▄▄█  █ █  █   █       █  █     ▄▄█       █   █▄▄▄█     ▄▄█      ▄█   █▄▄▄█   █▄▄█▄      █       █       █   ▄▄▄█   █   █   █ █▄█  █     ▄▄█     ▄▄█  █ █  █  █▄█  █       █ █   █  
█   █▄▄▄█   █ █   █ █    ▄▄▄█    █  █  █▄█  █   █  ▄    █  █    █  █   ▄   █    ▄▄▄█    █  █     █▄█    ▄▄▄█    ▄▄  █     █  ▄   ██▄     ▄█  █▄▄▄    █   █▄▄▄█      █    █  █    █  █  █▄█  █       █  ▄    █ █   █  
█       █   █ █   █ █   █▄▄▄█    █▄▄█       █   █ █ █   █  █    █▄▄█  █ █  █   █▄▄▄█    █▄▄█    ▄  █   █▄▄▄█   █  █ █     █ █▄█   █ █   █     ▄▄▄█   █       █  ▄   █    █▄▄█    █▄▄█       █       █ █ █   █ █   █  
█▄▄▄▄▄▄▄█▄▄▄█ █▄▄▄█ █▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄▄▄█▄█  █▄▄█  █▄▄▄▄▄▄▄█▄▄█ █▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄▄▄█ █▄█▄▄▄▄▄▄▄█▄▄▄█  █▄█     █▄▄▄▄▄▄▄█ █▄▄▄█    █▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄█ █▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄█  █▄▄█ █▄▄▄█  
"""

instructions = """
Entrez votre token de bot Discord ci-dessous :
Commande disponible :
!check <adresse_litecoin>
"""

print(ascii_art)
print(instructions)


TOKEN = input("Entrez votre token de bot Discord: ")


intents = discord.Intents.default()
intents.message_content = True  


client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot connecté en tant que {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!check'):
        try:
            address = message.content.split()[1]
            await check_litecoin_address(message.channel, address)
        except IndexError:
            await message.channel.send("Veuillez fournir une adresse Litecoin valide.")

async def check_litecoin_address(channel, address):
    url = f'https://api.blockcypher.com/v1/ltc/main/addrs/{address}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        
        
        print("Réponse de l'API:")
        print(data)

        total_received = data.get('total_received', 0) / 1e8  
        total_sent = data.get('total_sent', 0) / 1e8  
        balance = data.get('balance', 0) / 1e8  

        await channel.send(f"Adresse: {address}\nTotal reçu: {total_received} LTC\nTotal envoyé: {total_sent} LTC\nSolde actuel: {balance} LTC")
    else:
        await channel.send("Impossible de récupérer les informations pour cette adresse Litecoin. Veuillez vérifier l'adresse et réessayer.")

client.run(TOKEN)
