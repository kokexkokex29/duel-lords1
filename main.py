import os
import threading
import logging
import time
import asyncio
from app import app
from bot import bot, run_bot

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Global Discord bot thread
discord_thread = None

def start_discord_bot():
    """Start Discord bot in a separate thread"""
    global discord_thread
    
    def bot_runner():
        try:
            logger.info("Starting Discord bot in background thread...")
            token = os.getenv('DISCORD_TOKEN')
            if token:
                # Create new event loop for this thread
                asyncio.set_event_loop(asyncio.new_event_loop())
                run_bot()
            else:
                logger.error("DISCORD_TOKEN not found!")
        except Exception as e:
            logger.error(f"Discord bot error: {e}")
    
    discord_thread = threading.Thread(target=bot_runner, daemon=True)
    discord_thread.start()
    logger.info("Discord bot thread started")

# Start Discord bot when module is imported (for Gunicorn)
start_discord_bot()

if __name__ == "__main__":
    logger.info("Starting Duel Lords Tournament Bot in development mode...")
    
    # In development, run Flask directly
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    except Exception as e:
        logger.error(f"Flask server failed to start: {e}")
