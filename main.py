# ———————————No switches?———————————
# ⠀⣞⢽⢪⢣⢣⢣⢫⡺⡵⣝⡮⣗⢷⢽⢽⢽⣮⡷⡽⣜⣜⢮⢺⣜⢷⢽⢝⡽⣝
# ⠸⡸⠜⠕⠕⠁⢁⢇⢏⢽⢺⣪⡳⡝⣎⣏⢯⢞⡿⣟⣷⣳⢯⡷⣽⢽⢯⣳⣫⠇
# ⠀⠀⢀⢀⢄⢬⢪⡪⡎⣆⡈⠚⠜⠕⠇⠗⠝⢕⢯⢫⣞⣯⣿⣻⡽⣏⢗⣗⠏⠀
# ⠀⠪⡪⡪⣪⢪⢺⢸⢢⢓⢆⢤⢀⠀⠀⠀⠀⠈⢊⢞⡾⣿⡯⣏⢮⠷⠁⠀⠀
# ⠀⠀⠀⠈⠊⠆⡃⠕⢕⢇⢇⢇⢇⢇⢏⢎⢎⢆⢄⠀⢑⣽⣿⢝⠲⠉⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⡿⠂⠠⠀⡇⢇⠕⢈⣀⠀⠁⠡⠣⡣⡫⣂⣿⠯⢪⠰⠂⠀⠀⠀⠀
# ⠀⠀⠀⠀⡦⡙⡂⢀⢤⢣⠣⡈⣾⡃⠠⠄⠀⡄⢱⣌⣶⢏⢊⠂⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⢝⡲⣜⡮⡏⢎⢌⢂⠙⠢⠐⢀⢘⢵⣽⣿⡿⠁⠁⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠨⣺⡺⡕⡕⡱⡑⡆⡕⡅⡕⡜⡼⢽⡻⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⣼⣳⣫⣾⣵⣗⡵⡱⡡⢣⢑⢕⢜⢕⡝⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⣴⣿⣾⣿⣿⣿⡿⡽⡑⢌⠪⡢⡣⣣⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⡟⡾⣿⢿⢿⢵⣽⣾⣼⣘⢸⢸⣞⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠁⠇⠡⠩⡫⢿⣝⡻⡮⣒⢽⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# —————————————————————————————
import asyncio
import logging as logger
import random
from datetime import timedelta

from telegram import (
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
    CallbackQueryHandler
)

from handler import *
from lang import *

logger.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logger.INFO)

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
    # Starts the conversation
    if update.message.chat.type == "private":
        await update.message.reply_text(private_chat_not_supported)
        return ConversationHandler.END

    if update.message.chat.id not in flame_enabled_groups:
        await update.message.reply_text(no_flame_currently_active)
        return ConversationHandler.END

    reply_markup = ForceReply(selective=True, input_field_placeholder=input_field_select_flavour)

    if update.message is not None:
        preparation = await update.message.reply_text(
            text=popcorn_preparation,
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
    else:
        preparation = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=popcorn_preparation,
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
    return POPCORN_TYPE


async def popcorn_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = await context.bot.send_message(chat_id=update.effective_chat.id, text=preparing_popcorn,
                                             reply_to_message_id=update.message.message_id)

    # Set a timer just for fun
    await asyncio.sleep(random.randint(1, 5))

    await message.edit_text(
        text=popcorn_ready.format(type=update.message.text.capitalize()),
        parse_mode="HTML",
        reply_markup=feedback_reply_markup,
    )

    return ConversationHandler.END


# noinspection PyUnusedLocal
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Cancels and ends the conversation
    await update.message.reply_text(order_canceled, reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


# noinspection PyUnusedLocal
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Parses the CallbackQuery and updates the message text
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer(text=feedback_thanks)

    await query.edit_message_reply_markup(reply_markup=None)


async def remove_group(group_id: int, context: ContextTypes.DEFAULT_TYPE) -> None:
    await asyncio.sleep(timedelta(minutes=25).seconds)
    if group_id in flame_enabled_groups:
        flame_enabled_groups.remove(group_id)
        await context.bot.send_message(chat_id=group_id, text=flame_automatically_disabled)


async def flame(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    group_id = update.effective_chat.id

    if update.message.chat.type == "private":
        await update.message.reply_text(private_chat_not_supported)
        return

    admins = await context.bot.get_chat_administrators(group_id)
    if update.effective_user.id not in [admin.user.id for admin in admins]:
        await update.message.reply_text(only_admins_command)
        return

    if group_id not in flame_enabled_groups:
        flame_enabled_groups.append(group_id)
        await update.message.reply_text(flame_mode_enabled, parse_mode="HTML")
    else:
        flame_enabled_groups.remove(group_id)
        await update.message.reply_text(flame_mode_disabled, parse_mode="HTML")

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
            text=bot_joined,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


def main() -> None:
    """Starts the bot."""
    token = open("token.txt", "r+").readline().strip()
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
