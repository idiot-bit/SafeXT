from flask import Flask
import threading
from bot import run_bot  # Import your bot's function

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running Successfully!"

# Run the bot in a separate thread
threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)