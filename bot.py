import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ['TOKEN']

pet = {
    "hunger": 100,
    "thirst": 100, 
    "rating": 0,
    "alive": True,
    "coins": 100
}

async def decay_stats():
    while True:
        await asyncio.sleep(60)
        if pet["alive"]:
            pet["hunger"] = max(0, pet["hunger"] - 5)
            pet["thirst"] = max(0, pet["thirst"] - 7)
            if pet["hunger"] == 0 or pet["thirst"] == 0:
                pet["alive"] = False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not pet["alive"]:
        art = " (x_x)\n/____\\"
        status = "ХОМЯК МЁРТВ!"
    else:
        art = " (￣ω￣)\n/▔▔▔\\" if pet["hunger"] > 50 else " (•_•)\n/¯¯¯\\"
        status = f"Голод: {pet['hunger']}% | Жажда: {pet['thirst']}%"
    
    await update.message.reply_text(
        f"{art}\n{status}\n\n"
        "Команды:\n"
        "/feed - кормить (10 монет)\n" 
        "/water - поить (5 монет)\n"
        "/status - статус\n"
        "/revive - воскресить (50 монет)"
    )

async def feed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not pet["alive"]:
        await update.message.reply_text("Хомяк мёртв! /revive")
        return
    
    if pet["coins"] < 10:
        await update.message.reply_text("Не хватает монет!")
        return
        
    pet["hunger"] = min(100, pet["hunger"] + 25)
    pet["coins"] -= 10
    await update.message.reply_text(f"Хомяк поел! Голод: {pet['hunger']}%")

async def water(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not pet["alive"]:
        await update.message.reply_text("Хомяк мёртв! /revive")
        return
    
    if pet["coins"] < 5:
        await update.message.reply_text("Не хватает монет!")
        return
        
    pet["thirst"] = min(100, pet["thirst"] + 30)
    pet["coins"] -= 5
    await update.message.reply_text(f"Хомяк попил! Жажда: {pet['thirst']}%")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not pet["alive"]:
        await update.message.reply_text("Хомяк мёртв! /revive")
        return
        
    await update.message.reply_text(
        f"Голод: {pet['hunger']}%\n"
        f"Жажда: {pet['thirst']}%\n" 
        f"Монеты: {pet['coins']}\n"
        f"Рейтинг: {pet['rating']}"
    )

async def revive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if pet["alive"]:
        await update.message.reply_text("Хомяк и так жив!")
        return
        
    if pet["coins"] < 50:
        await update.message.reply_text("Нужно 50 монет для воскрешения!")
        return
        
    pet.update({"hunger": 50, "thirst": 50, "alive": True})
    pet["coins"] -= 50
    await update.message.reply_text("Хомяк воскрес!")

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("feed", feed))
    app.add_handler(CommandHandler("water", water))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("revive", revive))
    
    loop = asyncio.get_event_loop()
    loop.create_task(decay_stats())
    
    app.run_polling()
