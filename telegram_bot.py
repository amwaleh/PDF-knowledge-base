import os
from dotenv import load_dotenv
from rich.console import Console
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,MessageHandler, filters
from main import get_bupa_knowledge

load_dotenv()

console = Console()
BOT_TOKEN= os.getenv("BOT_TOKEN")



async def Start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f'Hello {update.effective_user.first_name}! I a bot. I can help you with your queries. Please type your query and I will try to answer it.')

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

def handle_response(text :str) -> str:
    with console.status("thinking", spinner="earth") as status:
        result = get_bupa_knowledge(query=text)
    print(result.content)
    return result.content


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = handle_response(update.message.text)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f'Update {update} caused error {context.error}')


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("start", Start))

#messages
app.add_handler(MessageHandler(filters.TEXT, handle_message))

app.add_error_handler(error)

app.run_polling(poll_interval=3)