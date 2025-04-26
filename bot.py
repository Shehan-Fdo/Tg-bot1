import logging
import random
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Using the token from your code
TOKEN = "7684444789:AAE1PQB5UmW0pyU6I6Dz_mV4wjfxzelhPgU"

# Sample cool facts database
COOL_FACTS = [
    "A day on Venus is longer than a year on Venus.",
    "Octopuses have three hearts.",
    "A group of flamingos is called a 'flamboyance'.",
    "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly good to eat.",
    "The Guinness World Record for the longest hiccup attack is 68 years.",
    "Bananas are berries, but strawberries aren't.",
    "A bolt of lightning is five times hotter than the surface of the sun.",
    "Cows have best friends and get stressed when they are separated.",
    "The Hawaiian alphabet has only 12 letters.",
    "The world's oldest known living tree is over 5,000 years old.",
    "A single cloud can weigh more than a million pounds.",
    "Cats can make over 100 vocal sounds, while dogs can only make about 10.",
    "The strongest muscle in the human body relative to its size is the tongue.",
    "The shortest war in history was between Britain and Zanzibar in 1896. It lasted just 38 minutes.",
    "A blue whale's heart is so big that a human could swim through its arteries.",
    "Polar bears' fur isn't actually white—it's transparent and reflects light.",
    "There are more possible iterations of a game of chess than there are atoms in the observable universe.",
    "A group of unicorns is called a blessing.",
    "The fingerprints of koalas are so similar to humans that they have occasionally been confused at crime scenes.",
    "Honeybees can recognize human faces."
]

# Function to get a random fact from an API
async def get_random_fact_from_api():
    try:
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
        if response.status_code == 200:
            data = response.json()
            return data["text"]
        else:
            return random.choice(COOL_FACTS)
    except Exception as e:
        logger.error(f"Error fetching fact from API: {e}")
        return random.choice(COOL_FACTS)

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        f"Hi {user.first_name}! I'm the Random Cool Fact Generator Bot. "
        f"Use /fact to get a random cool fact!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "Commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/fact - Get a random cool fact\n"
        "/localfact - Get a fact from our local database"
    )

async def fact_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a random fact when the command /fact is issued."""
    await update.message.reply_text("🤔 Fetching a cool fact for you...")
    fact = await get_random_fact_from_api()
    await update.message.reply_text(f"🌟 COOL FACT: {fact}")

async def local_fact_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a random fact from local database when the command /localfact is issued."""
    fact = random.choice(COOL_FACTS)
    await update.message.reply_text(f"🌟 COOL FACT: {fact}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message and suggest using commands."""
    text = update.message.text.lower()
    
    if "fact" in text:
        # If the user asks for a fact in natural language
        await fact_command(update, context)
    else:
        await update.message.reply_text(
            "I'm a cool fact bot! Use /fact to get a random cool fact or /help to see all commands."
        )

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("fact", fact_command))
    application.add_handler(CommandHandler("localfact", local_fact_command))

    # on non command i.e message - handle the message
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()