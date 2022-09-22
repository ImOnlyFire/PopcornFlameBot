# ———————————No switches?———————————
#⠀⣞⢽⢪⢣⢣⢣⢫⡺⡵⣝⡮⣗⢷⢽⢽⢽⣮⡷⡽⣜⣜⢮⢺⣜⢷⢽⢝⡽⣝
# ⠸⡸⠜⠕⠕⠁⢁⢇⢏⢽⢺⣪⡳⡝⣎⣏⢯⢞⡿⣟⣷⣳⢯⡷⣽⢽⢯⣳⣫⠇
#⠀⠀⢀⢀⢄⢬⢪⡪⡎⣆⡈⠚⠜⠕⠇⠗⠝⢕⢯⢫⣞⣯⣿⣻⡽⣏⢗⣗⠏⠀
#⠀⠪⡪⡪⣪⢪⢺⢸⢢⢓⢆⢤⢀⠀⠀⠀⠀⠈⢊⢞⡾⣿⡯⣏⢮⠷⠁⠀⠀
#⠀⠀⠀⠈⠊⠆⡃⠕⢕⢇⢇⢇⢇⢇⢏⢎⢎⢆⢄⠀⢑⣽⣿⢝⠲⠉⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⡿⠂⠠⠀⡇⢇⠕⢈⣀⠀⠁⠡⠣⡣⡫⣂⣿⠯⢪⠰⠂⠀⠀⠀⠀
#⠀⠀⠀⠀⡦⡙⡂⢀⢤⢣⠣⡈⣾⡃⠠⠄⠀⡄⢱⣌⣶⢏⢊⠂⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⢝⡲⣜⡮⡏⢎⢌⢂⠙⠢⠐⢀⢘⢵⣽⣿⡿⠁⠁⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠨⣺⡺⡕⡕⡱⡑⡆⡕⡅⡕⡜⡼⢽⡻⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⣼⣳⣫⣾⣵⣗⡵⡱⡡⢣⢑⢕⢜⢕⡝⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⣴⣿⣾⣿⣿⣿⡿⡽⡑⢌⠪⡢⡣⣣⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⡟⡾⣿⢿⢿⢵⣽⣾⣼⣘⢸⢸⣞⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠁⠇⠡⠩⡫⢿⣝⡻⡮⣒⢽⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#—————————————————————————————
from datetime import timedelta
from handler import *
import logging as logger
import time
import random
import asyncio

from telegram import (
    ReplyKeyboardRemove,
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackQueryHandler
)

logger.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logger.INFO)

popcorn_types = ["Classico", "Cioccolato", "Extra Salato", "Miele", "Caramellato"]
popcorn_image_link = 'https://i.imgur.com/2E5Tf9F.png'
POPCORN_TYPE = range(1)
feedback_keyboard = [
    [
        InlineKeyboardButton("👍", callback_data="1"),
        InlineKeyboardButton("👎", callback_data="2"),
    ],
]
feedback_reply_markup = InlineKeyboardMarkup(feedback_keyboard)
flame_enabled_groups = []


# noinspection PyUnusedLocal
async def popcorn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int | range:
    """Starts the conversation."""
    if update.message.chat.type == "private":
        await update.message.reply_text("Non puoi usare questo comando in privato.")
        return ConversationHandler.END

    if update.message.chat.id not in flame_enabled_groups:
        await update.message.reply_text(
            "Per poter ordinare i popcorn, deve esserci un flame attivo nel gruppo.\n"
            "Chiedi ad un admin di digitare /flame se c'e' un flame in corso.")
        return ConversationHandler.END

    await update.message.reply_text(
        "<b>Popcorn stand!</b> 🍿\n"
        "Durante le sessioni di flame, i popcorn li offriamo <b>gratuitamente</b>.\n\n"
        f"<b>Gusti disponibili</b> ⟩\n"
        f"<i>{', '.join(popcorn_types)}</i>\n\n"
        "Digita /cancel se hai perso la fame\n\n"
        "°°°·.°·..·°¯°·._.·   🎀  🍿  🎀   ·._.·°¯°·..·°.·°°°",
        reply_markup=ForceReply(selective=True, input_field_placeholder="Scegli il gusto"),
        parse_mode="HTML"
    )

    return POPCORN_TYPE


async def popcorn_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Stiamo preparando i tuoi popcorn...",
        reply_to_message_id=update.message.message_id,
    )

    # Set a timer just for fun
    time.sleep(random.randint(1, 5))

    await message.edit_text(
        text=f"<a href=\"{popcorn_image_link}\">&#8205</a>"
             f"🍿 <b>I tuoi popcorn sono pronti!</b> 🍿\n"
             f" ➜ 🥂 Gusto › {update.message.text.capitalize()}\n"
             f" ➜ 💶 Costo › 0€\n\n"
             "Grazie per aver scelto il nostro stand! <b>Buona visione</b>\n\n"
             "<i>(Se ti piacciono i nostri popcorn, per favore lascia un feedback!)</i>",
        parse_mode="HTML",
        reply_markup=feedback_reply_markup,
    )

    return ConversationHandler.END


# noinspection PyUnusedLocal
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text("Acquisto cancellato.", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


# noinspection PyUnusedLocal
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer(text="Grazie per il feedback!")

    await query.edit_message_reply_markup(reply_markup=None)


async def remove_group(group_id: int, context: ContextTypes.DEFAULT_TYPE) -> None:
    await asyncio.sleep(timedelta(minutes=25).seconds)
    if group_id in flame_enabled_groups:
        flame_enabled_groups.remove(group_id)
        await context.bot.send_message(
            chat_id=group_id,
            text="💧 Il gruppo e' stato automaticamente rimosso dalla lista dei flame abilitati. "
                 "Se c'e' ancora un flame in corso, chiedi ad un admin di digitare /flame",
        )


async def flame(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    group_id = update.effective_chat.id

    if update.message.chat.type == "private":
        await update.message.reply_text("Non puoi usare questo comando in privato.")
        return

    admins = await context.bot.get_chat_administrators(group_id)
    if update.effective_user.id not in [admin.user.id for admin in admins]:
        await update.message.reply_text("Solo gli admin possono usare questo comando.")
        return

    if group_id not in flame_enabled_groups:
        flame_enabled_groups.append(group_id)
        await update.message.reply_text(
            "<b>🔥 Attivata la modalità flame</b>\n\n"
            "Da questo momento in poi, i popcorn li offriamo <b>gratuitamente</b>!\n"
            "Digita /popcorn per ordinare i popcorn\n\n"
            "<i>La modalità flame resterà attivata per 25 minuti. </i>"
            "<i>Se vuoi disattivarla, chiedi ad un admin di digitare /flame</i>",
            parse_mode="HTML")
    else:
        flame_enabled_groups.remove(group_id)
        await update.message.reply_text("<b>💧 Modalità flame disattivata</b>", parse_mode="HTML")

    print(flame_enabled_groups)
    # noinspection PyAsyncCall
    asyncio.gather(remove_group(group_id, context))


async def on_join(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("GitHub", callback_data="0", url="https://github.com/ImOnlyFire/PopcornFlameBot"),
        ],
    ]

    if update.message.new_chat_members[0].id == context.bot.id:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="🍿 <b>Ciao</b>, grazie per avermi aggiunto al gruppo!\n"
                 "<i>C'è un flame nel gruppo? Mangia i popcorn e goditi lo spettacolo!</i>\n\n"
                 "Gli admin potranno utilizzare /flame in caso di un flame, e in questo periodo "
                 "i popcorn li offriremo <b>gratuitamente</b> a tutti gli utenti del gruppo. (/popcorn)",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


def main() -> None:
    """Starts the bot."""
    token = open("token.txt", "a+").readline().strip()
    application = ApplicationBuilder().token(token).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("popcorn", popcorn)],

        states={
            POPCORN_TYPE: [MessageHandler(
                filters.Regex(f"(?i)^({'|'.join(popcorn_types)})$"),
                popcorn_type
            )],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)

    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, on_join))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler('flame', flame))
    application.add_error_handler(error_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
