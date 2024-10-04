import os

def setup_bot():
    # Unzip the MT2.zip file
    os.system('unzip MT2.zip')
    
    # Update package list and install nodejs
    os.system('sudo apt update && sudo apt install -y nodejs')
    
    # Install the telebot package
    os.system('pip install telebot')
    
    # Run the bot script
    os.system('python3 bot.py')

if __name__ == "__main__":
    setup_bot()
