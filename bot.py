import os
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────
# RAILWAY VARIABLES
#   BOT_TOKEN      → token from @BotFather
#   ADMIN_CHAT_ID  → your numeric Telegram ID
#   CONSOLE_CHAT_ID → your console group ID
#   BTC_ADDRESS    → your Bitcoin wallet address
# ─────────────────────────────────────────
TOKEN          = os.environ.get("BOT_TOKEN")
ADMIN_USERNAME = "@EXCELV33"
ADMIN_CHAT_ID  = os.environ.get("ADMIN_CHAT_ID", "")
CONSOLE_CHAT   = os.environ.get("CONSOLE_CHAT_ID", "")
BTC_ADDRESS    = os.environ.get("BTC_ADDRESS", "YOUR_BTC_ADDRESS")
CHANNEL_LINK   = "https://t.me/EXCELupdate"
SUPPORT_USER   = "@EXCELV33"

# ─────────────────────────────────────────
# BIN DATABASE
# ─────────────────────────────────────────
BIN_DATABASE = {
    "222300": 1, "400022": 1, "401816": 1, "404972": 1, "413519": 1,
    "413938": 1, "416549": 21, "416598": 1, "427638": 1, "438255": 1,
    "438959": 1, "446223": 1, "446238": 36, "446259": 2, "446261": 1,
    "446263": 1, "446271": 1, "446278": 1, "446291": 2, "448903": 1,
    "450875": 1, "452132": 1, "453942": 1, "454103": 2, "454313": 3,
    "454638": 1, "456725": 1, "456883": 4, "459645": 1, "459647": 13,
    "459667": 8, "461648": 1, "463386": 1, "465858": 4, "465859": 6,
    "465865": 20, "465901": 2, "465902": 5, "465922": 1, "465923": 1,
    "465935": 4, "465941": 1, "465942": 10, "465943": 40, "465944": 7,
    "465945": 1, "465950": 1, "467062": 2, "472628": 8, "475117": 3,
    "475129": 6, "475139": 6, "475140": 1, "475141": 2, "475142": 41,
    "475144": 1, "475145": 1, "476223": 1, "476224": 7, "476225": 1,
    "476367": 2, "476383": 1, "489394": 1, "490237": 1, "492181": 44,
    "492182": 1, "512345": 1, "513162": 1, "516767": 11, "516794": 2,
    "516859": 5, "518581": 1, "518652": 1, "520493": 1, "522233": 1,
    "522948": 1, "523255": 1, "523456": 1, "523642": 1, "524681": 1,
    "527411": 1, "528689": 1, "529133": 1, "531214": 1, "531954": 1,
    "535199": 2, "535456": 23, "535522": 215, "535617": 1, "535666": 23,
    "535674": 5, "535778": 4, "535908": 1, "537317": 7, "537370": 2,
    "537410": 23, "537568": 1, "537569": 1, "537855": 1, "537891": 1,
    "540243": 1, "541276": 1, "542402": 15, "546097": 3, "546811": 1,
    "548765": 1, "552213": 2, "555060": 2, "557349": 2, "557351": 2,
    "557361": 2, "557379": 3, "557483": 4, "559755": 1, "885451": 1,
    "887557": 1,
}

TOTAL_PRODUCTS = sum(BIN_DATABASE.values())

# ─────────────────────────────────────────
# FULLZ DATABASES
# ─────────────────────────────────────────
FULLZ_DATABASES = [
    ("1-pound",    1),
    ("10-pound",   10),
    ("DVLA-20",    20),
    ("DVLA-30",    30),
    ("Marks-30",   30),
    ("Evri-25th",  25),
    ("Dvla-26th",  30),
    ("DVLA-29th",  30),
    ("Evri-Jul1sf",25),
    ("DVLA-Jul1st",30),
]

# ─────────────────────────────────────────
# TOP UP AMOUNTS
# ─────────────────────────────────────────
TOPUP_AMOUNTS = [10, 20, 30, 40, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 750, 1000]

RULES_TEXT = (
    "🛡 *RULES & REFUND POLICY*\n\n"
    "IF YOU FAIL TO FOLLOW OUR CLEAR INSTRUCTED RULES YOU WILL NOT BE REFUNDED.\n\n"
    "*How to Apply for a Refund:*\n"
    "1. Check card on pay.google.com\n"
    "2. If the card is dead, click refund at the bottom of purchased card\n"
    "3. Send the bot a Screenshot/Photo that proves the card is dead\n"
    "4. You have an automatic 3 minute timer when checking\n"
    "5. Failing to check past the 3 minute timer can result in no refund\n"
    "6. Make sure Card Number, Expiry Date and CCV are fully visible\n"
    "7. Invalid number does not qualify for refund unless all info is missing or fake\n"
    "8. If all details are valid and card is dead, your account will be credited within 5 minutes\n\n"
    "*Keep in Mind:*\n"
    "⛔️ £10 & £5 BASES ARE NOT REFUNDABLE\n"
    "⛔️ HSBC CARDS ARE NOT REFUNDABLE (includes John Lewis, M&S, First Direct, etc)\n\n"
    "⛔️ NOTE ⛔️\n"
    "🔹 Support available 24/7 @EXCELV33\n"
    "🔹 1 Transaction per wallet unless payment is underpaid. Wallet always changes after each deposit\n"
    "🔹 Payment BTC ONLY\n"
    "🔹 BY PURCHASING YOU AGREE TO THESE RULES. FAILURE TO READ THEM WILL FORFEIT YOUR REFUND / REPLACEMENT. WE SHALL GIVE NO WARNINGS"
)

# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
async def console_log(context, user, action, detail=""):
    try:
        username = f"@{user.username}" if user.username else user.first_name
        msg = f"{username} ({user.id}) {action}"
        if detail:
            msg += f" — {detail}"
        await context.bot.send_message(chat_id=CONSOLE_CHAT, text=msg)
    except Exception as e:
        logger.error(f"Console log error: {e}")

def is_admin(update):
    user_id = str(update.effective_user.id)
    chat_id = str(update.effective_chat.id)
    return user_id == str(ADMIN_CHAT_ID) or chat_id == str(CONSOLE_CHAT)

def get_balance(context, user_id):
    return context.bot_data.get("balances", {}).get(user_id, 0)

def main_menu_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Store",   callback_data="store"),
         InlineKeyboardButton("💳 Wallet",  callback_data="wallet")],
        [InlineKeyboardButton("🛡 Rules",   callback_data="rules")],
        [InlineKeyboardButton("📞 Support", url=f"https://t.me/EXCELV33"),
         InlineKeyboardButton("📢 Channel", url=CHANNEL_LINK)],
    ])

def store_menu_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 Fullz", callback_data="fullz")],
        [InlineKeyboardButton("🌐 Main Menu", callback_data="main_menu")],
    ])

# BTC/credits conversion (approximate — £1 = 1 credit)
def credits_to_btc(credits):
    # Rough rate: adjust as needed
    btc_rate = 60000  # £60,000 per BTC
    btc = credits / btc_rate
    return round(btc, 8)

# ─────────────────────────────────────────
# START
# ─────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user    = update.effective_user
    user_id = user.id
    await console_log(context, user, "opened the bot")

    if "join_dates" not in context.bot_data:
        context.bot_data["join_dates"] = {}
    if user_id not in context.bot_data["join_dates"]:
        context.bot_data["join_dates"][user_id] = datetime.now().strftime("%d-%m-%Y")

    balance   = get_balance(context, user_id)
    join_date = context.bot_data["join_dates"].get(user_id, datetime.now().strftime("%d-%m-%Y"))

    welcome = (
        f"Welcome to EXCEL Store 👋\n"
        f"Use the menu below to interact with the bot 🤖\n"
        f"===============\n"
        f"Managed by {ADMIN_USERNAME}\n\n"
        f"🔹 Support account is available 24/7 {SUPPORT_USER}\n\n"
        f"🔹 1 Transaction per wallet unless payment is underpaid. "
        f"Our wallet always changes after each completed deposit.\n\n"
        f"🔹 Payment BTC ONLY\n\n"
        f"🔹 BY PURCHASING YOU AGREE TO THESE RULES. FAILURE TO READ THEM WILL "
        f"FORFEIT YOUR REFUND / REPLACEMENT. WE SHALL GIVE NO WARNINGS"
    )
    await update.message.reply_text(welcome, reply_markup=main_menu_kb())

# ─────────────────────────────────────────
# BUTTON HANDLER
# ─────────────────────────────────────────
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    await query.answer()
    data    = query.data
    user    = query.from_user
    user_id = user.id
    balance = get_balance(context, user_id)

    await console_log(context, user, f"tapped {data}")

    # ── MAIN MENU ──
    if data == "main_menu":
        welcome = (
            f"Welcome to EXCEL Store 👋\n"
            f"Use the menu below to interact with the bot 🤖\n"
            f"===============\n"
            f"Managed by {ADMIN_USERNAME}\n\n"
            f"🔹 Support account is available 24/7 {SUPPORT_USER}\n\n"
            f"🔹 1 Transaction per wallet unless payment is underpaid.\n\n"
            f"🔹 Payment BTC ONLY\n\n"
            f"🔹 BY PURCHASING YOU AGREE TO THESE RULES. WE SHALL GIVE NO WARNINGS"
        )
        await query.edit_message_text(welcome, reply_markup=main_menu_kb())

    # ── STORE ──
    elif data == "store":
        await query.edit_message_text(
            f"🔹 Payment BTC ONLY\n\n"
            f"🔹 BY PURCHASING YOU AGREE TO THESE RULES. FAILURE TO READ THEM WILL "
            f"FORFEIT YOUR REFUND / REPLACEMENT. WE SHALL GIVE NO WARNINGS",
            reply_markup=store_menu_kb()
        )

    # ── FULLZ LIST ──
    elif data == "fullz":
        total = sum(qty for _, qty in FULLZ_DATABASES)
        text  = f"--- AVAILABLE FULLZ DATABASES ---\n\n"
        buttons = []
        for name, price in FULLZ_DATABASES:
            buttons.append([InlineKeyboardButton(f"🔸 {name}", callback_data=f"buy_fullz:{name}:{price}")])
        buttons.append([InlineKeyboardButton("🔍 Search for BIN", callback_data="search_bin")])
        buttons.append([InlineKeyboardButton("🌐 Main Menu",      callback_data="main_menu")])
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(buttons))

    # ── BUY FULLZ ──
    elif data.startswith("buy_fullz:"):
        parts  = data.split(":")
        name   = parts[1]
        price  = int(parts[2])
        balance = get_balance(context, user_id)

        if balance < price:
            await query.edit_message_text(
                f"❌ Insufficient balance!\n\n"
                f"This database costs £{price} but you only have £{balance}.\n\n"
                f"Please top up your wallet first.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💳 Top Up Wallet", callback_data="wallet")],
                    [InlineKeyboardButton("⬅️ Back",          callback_data="fullz")],
                ])
            )
            return

        await console_log(context, user, f"is purchasing {name} for £{price}")
        await query.edit_message_text(
            f"🛒 *Purchase Confirmation*\n\n"
            f"Database: {name}\n"
            f"Cost: £{price}\n"
            f"Your Balance: £{balance}\n\n"
            f"Confirm your purchase?",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Confirm", callback_data=f"confirm_fullz:{name}:{price}")],
                [InlineKeyboardButton("❌ Cancel",  callback_data="fullz")],
            ])
        )

    # ── CONFIRM FULLZ PURCHASE ──
    elif data.startswith("confirm_fullz:"):
        parts   = data.split(":")
        name    = parts[1]
        price   = int(parts[2])
        balance = get_balance(context, user_id)

        if balance < price:
            await query.edit_message_text(
                "❌ Insufficient balance! Please top up.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 Top Up", callback_data="wallet")]])
            )
            return

        if "balances" not in context.bot_data:
            context.bot_data["balances"] = {}
        context.bot_data["balances"][user_id] = balance - price
        new_balance = context.bot_data["balances"][user_id]

        await console_log(context, user, f"purchased {name} for £{price}")
        await query.edit_message_text(
            f"✅ *Purchase Successful!*\n\n"
            f"Database: {name}\n"
            f"Cost: £{price}\n"
            f"Remaining Balance: £{new_balance}\n\n"
            f"Your file will be delivered shortly.\n"
            f"Contact {SUPPORT_USER} if you have any issues.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌐 Main Menu", callback_data="main_menu")]])
        )

        if ADMIN_CHAT_ID:
            try:
                await context.bot.send_message(
                    chat_id=ADMIN_CHAT_ID,
                    text=f"NEW ORDER\n\nUser: @{user.username or user.first_name}\nID: {user_id}\nDatabase: {name}\nPrice: £{price}\nRemaining Balance: £{new_balance}"
                )
            except Exception as e:
                logger.error(f"Admin notify error: {e}")

    # ── SEARCH BIN ──
    elif data == "search_bin":
        context.user_data["waiting_bin"] = True
        await query.edit_message_text(
            "🔍 *Search for BIN*\n\nPlease type your BIN number (first 6 digits):",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="fullz")]])
        )

    # ── WALLET ──
    elif data == "wallet":
        join_date = context.bot_data.get("join_dates", {}).get(user_id, datetime.now().strftime("%d-%m-%Y"))
        await query.edit_message_text(
            f"🔹 Payment BTC ONLY\n\n"
            f"🔹 BY PURCHASING YOU AGREE TO THESE RULES. FAILURE TO READ THEM WILL "
            f"FORFEIT YOUR REFUND / REPLACEMENT. WE SHALL GIVE NO WARNINGS\n\n"
            f"============================\n"
            f"🪪 ID: {user_id}\n"
            f"💰 Balance: £{balance}\n"
            f"📅 Join Date: {join_date}\n"
            f"============================",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(f"🔸 £{a} 🔸", callback_data=f"topup:{a}") for a in TOPUP_AMOUNTS[i:i+2]]
                for i in range(0, len(TOPUP_AMOUNTS), 2)
            ] + [
                [InlineKeyboardButton("💰 Custom Amount", callback_data="topup_custom")],
                [InlineKeyboardButton("🌐 Main Menu",     callback_data="main_menu")],
            ])
        )

    # ── TOP UP AMOUNT SELECTED ──
    elif data.startswith("topup:"):
        amount  = int(data.split(":")[1])
        btc_amt = credits_to_btc(amount)
        context.user_data["pending_topup"] = {"amount": amount, "btc": btc_amt}
        await console_log(context, user, f"selected top up £{amount}")
        await query.edit_message_text(
            f"Send Exactly {btc_amt} to the address below to get {amount} credits\n\n"
            f"🏦 :\n{BTC_ADDRESS}\n\n"
            f"‼️ Deposits are permanent and non refundable\n"
            f"‼️ Double Check the BTC amount before sending\n"
            f"‼️ Anything UNDER or ABOVE the amount specified will be considered as a Donation\n"
            f"🔶 You will be funded when your transaction is confirmed\n"
            f"⚠️ By Sending you agree to whats mentioned above\n"
            f"⚠️ DO NOT SEND AS £ only send as BTC\n"
            f"‼️ One payment per wallet address\n"
            f"‼️ Anything else will Not be credited",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ I've Sent Payment", callback_data=f"paid_topup:{amount}")],
                [InlineKeyboardButton("⬅️ Back",             callback_data="wallet")],
            ])
        )

    # ── CUSTOM TOP UP ──
    elif data == "topup_custom":
        context.user_data["waiting_custom_amount"] = True
        await query.edit_message_text(
            "💰 Enter your custom top up amount in £:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="wallet")]])
        )

    # ── PAYMENT SUBMITTED ──
    elif data.startswith("paid_topup:"):
        amount = int(data.split(":")[1])
        await console_log(context, user, f"submitted top up payment of £{amount}")
        await query.edit_message_text(
            f"✅ Payment submitted for £{amount}!\n\n"
            f"You will be funded once your transaction is confirmed.\n"
            f"Contact {SUPPORT_USER} if you have any issues.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌐 Main Menu", callback_data="main_menu")]])
        )
        if ADMIN_CHAT_ID:
            try:
                await context.bot.send_message(
                    chat_id=ADMIN_CHAT_ID,
                    text=f"TOP-UP REQUEST\n\nUser: @{user.username or user.first_name}\nID: {user_id}\nAmount: £{amount}\n\nUse /userbal {user_id} {amount} pass to credit."
                )
            except Exception as e:
                logger.error(f"Admin notify error: {e}")

    # ── RULES ──
    elif data == "rules":
        await query.edit_message_text(
            RULES_TEXT,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌐 Main Menu", callback_data="main_menu")]])
        )

# ─────────────────────────────────────────
# MESSAGE HANDLER (BIN search + custom amount)
# ─────────────────────────────────────────
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user    = update.effective_user
    user_id = user.id
    text    = update.message.text.strip()

    # BIN Search
    if context.user_data.get("waiting_bin"):
        context.user_data["waiting_bin"] = False
        bin_num = text[:6]
        if bin_num in BIN_DATABASE:
            qty = BIN_DATABASE[bin_num]
            await update.message.reply_text(
                f"🔍 *BIN Search Result*\n\n"
                f"BIN: {bin_num}\n"
                f"Available: {qty} cards\n\n"
                f"Contact {SUPPORT_USER} to purchase.",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back to Fullz", callback_data="fullz")]])
            )
        else:
            await update.message.reply_text(
                f"❌ BIN {bin_num} not found in our database.\n\n"
                f"Try a different BIN or contact {SUPPORT_USER}.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back to Fullz", callback_data="fullz")]])
            )
        return

    # Custom top up amount
    if context.user_data.get("waiting_custom_amount"):
        context.user_data["waiting_custom_amount"] = False
        try:
            amount  = int(text.replace("£", "").strip())
            btc_amt = credits_to_btc(amount)
            context.user_data["pending_topup"] = {"amount": amount, "btc": btc_amt}
            await console_log(context, user, f"selected custom top up £{amount}")
            await update.message.reply_text(
                f"Send Exactly {btc_amt} to the address below to get {amount} credits\n\n"
                f"🏦 :\n{BTC_ADDRESS}\n\n"
                f"‼️ Deposits are permanent and non refundable\n"
                f"‼️ Double Check the BTC amount before sending\n"
                f"‼️ Anything UNDER or ABOVE the amount specified will be considered as a Donation\n"
                f"🔶 You will be funded when your transaction is confirmed\n"
                f"⚠️ DO NOT SEND AS £ only send as BTC\n"
                f"‼️ One payment per wallet address",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("✅ I've Sent Payment", callback_data=f"paid_topup:{amount}")],
                    [InlineKeyboardButton("⬅️ Back",             callback_data="wallet")],
                ])
            )
        except ValueError:
            await update.message.reply_text("Please enter a valid number e.g. 50")
        return

# ─────────────────────────────────────────
# ADMIN COMMANDS
# ─────────────────────────────────────────
async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    await update.message.reply_text(f"Chat ID: {chat.id}\nType: {chat.type}\nTitle: {getattr(chat,'title','N/A')}")

async def userbal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return
    try:
        target_id = int(context.args[0])
        amount    = int(context.args[1])
        if len(context.args) < 3 or context.args[2] != "pass":
            await update.message.reply_text("Usage: /userbal <user_id> <amount> pass")
            return
        if "balances" not in context.bot_data:
            context.bot_data["balances"] = {}
        context.bot_data["balances"][target_id] = context.bot_data["balances"].get(target_id, 0) + amount
        new_balance = context.bot_data["balances"][target_id]
        await update.message.reply_text(f"Balance updated for user {target_id}: £{new_balance}")
        await context.bot.send_message(chat_id=target_id,
            text=f"✅ £{amount} has been added to your wallet!\n\nYour balance is now £{new_balance}.")
        await console_log(context, update.effective_user, f"credited £{amount} to user {target_id}")
    except Exception as e:
        await update.message.reply_text(f"Usage: /userbal <user_id> <amount> pass\nError: {e}")

async def removebalance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return
    try:
        target_id = int(context.args[0])
        amount    = int(context.args[1])
        if "balances" not in context.bot_data:
            context.bot_data["balances"] = {}
        current = context.bot_data["balances"].get(target_id, 0)
        context.bot_data["balances"][target_id] = max(0, current - amount)
        await update.message.reply_text(f"Removed £{amount} from user {target_id}.")
        await console_log(context, update.effective_user, f"removed £{amount} from user {target_id}")
    except Exception as e:
        await update.message.reply_text(f"Usage: /removebalance <user_id> <amount>\nError: {e}")

async def checkbalance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return
    try:
        target_id = int(context.args[0])
        bal = context.bot_data.get("balances", {}).get(target_id, 0)
        await update.message.reply_text(f"User {target_id} balance: £{bal}")
    except Exception as e:
        await update.message.reply_text(f"Usage: /checkbalance <user_id>\nError: {e}")

async def adminhelp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return
    await update.message.reply_text(
        "Admin Commands:\n\n"
        "/userbal <user_id> <amount> pass — Add balance\n"
        "/removebalance <user_id> <amount> — Remove balance\n"
        "/checkbalance <user_id> — Check balance\n"
        "/getid — Get chat ID\n"
        "/adminhelp — Show this menu"
    )

# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start",         start))
    app.add_handler(CommandHandler("getid",         get_id))
    app.add_handler(CommandHandler("userbal",       userbal))
    app.add_handler(CommandHandler("removebalance", removebalance))
    app.add_handler(CommandHandler("checkbalance",  checkbalance))
    app.add_handler(CommandHandler("adminhelp",     adminhelp))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    logger.info("EXCEL Store Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
