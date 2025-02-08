from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from random import *


TOKEN = None
with open("token","r") as token_file:
    TOKEN = token_file.read()
print(TOKEN)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hello, human. Would you like to roll one of my dice? Type /roll XdX to roll the dice. Like this: /roll 2d6")

async def roll_d20(update: Update, context: CallbackContext) -> None:
    d20_result = randint(1, 20)
    if d20_result == 20:
        await update.message.reply_text(f"Wow! You rolled a {d20_result}. Nice.")
    elif d20_result == 1:
        await update.message.reply_text(f"Ah. A {d20_result}. Wouldn't expect much from a human anyways.")
    else:
        await update.message.reply_text(f"You rolled a {d20_result}.")

#async def dice_roll(n: int, m: int):
#   roll_result = randint(1, n) + m
#   await update.message.reply_text(f"Lets roll a {n}-sided die and add {m} to the result... You rolled a {roll_result}!")

async def any_dice(update: Update, context: CallbackContext) -> None:
    args = context.args

    if not args:
        await update.message.reply_text("I have a lot of dice! How am i supposed to know which one to give you? Write /roll <number>d<number>, like this: /roll 3d12.")

    dice_command = args[0].lower()
    locate_d = dice_command.find('d')
    try: 
        dice_sides = int(dice_command[locate_d+1:])
        dice_quant = int(dice_command[:locate_d])
    
        if dice_sides > 100 or dice_sides <= 1:
            await update.message.reply_text("I'm not sure if i have this die. You can choose any-sided die, but the number should be more than 1 and less than 100!")
            return 
        if dice_quant > 100:
            await update.message.reply_text("I dont have this many dice! Even if i did, i wouldn't give you that much. The max is 100!")
            return
        if dice_quant < 1:
            await update.message.reply_text("Are you serious? How am i supposed to roll that? The minimum amount of dice is 1!")
            return

        total = 0

        for _ in range(dice_quant):
            total += randint(1, dice_sides)

        await update.message.reply_text(f"Rolling a {dice_sides}-sided die {dice_quant} times... You got {total}!")

    except:
        await update.message.reply_text("No! Not like that! You're supposed to use digits ONLY! I thought humans were an intelligent specie.")
        return

    

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('d20', roll_d20))
    app.add_handler(CommandHandler('roll', any_dice))
    #app.add_handler(CommandHandler('diceroll(n, m)', dice_roll))
    
    app.run_polling()

if __name__ == '__main__':
    main()
