import os
import logging
from datetime import datetime
from collections import Counter
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN          = os.environ.get("BOT_TOKEN")
ADMIN_USERNAME = "@EXCELV33"
ADMIN_CHAT_ID  = os.environ.get("ADMIN_CHAT_ID", "")
CONSOLE_CHAT   = os.environ.get("CONSOLE_CHAT_ID", "")
BTC_ADDRESS    = os.environ.get("BTC_ADDRESS", "YOUR_BTC_ADDRESS")
CHANNEL_LINK   = "https://t.me/EXCELupdate"
SUPPORT_USER   = "@EXCELV33"
ITEMS_PER_PAGE = 14

DATABASES = {
    "1p": {
        "name": "1-pound", "price": 1,
        "cards": [
            "475142-2012-S36-£1","475142-2010-CM7-£1","475142-2009-CM7-£1","475142-2012-DL1-£1",
            "475142-1/11-DA1-£1","475142-1/10-CB2-£1","475142-2010-Ss9-£1","475142-4/09-Ss9-£1",
            "475142-2009-bh1-£1","475142-4/09-DD2-£1","475142-2010-BS3-£1","475142-2009-SO3-£1",
            "475142-2009-IP9-£1","222300-2008-E1-£1","400022-2009-N1-£1","401816-2010-B1-£1",
            "416549-2007-SL3-£1","416549-1984-BS4-£1","416549-2009-NW6-£1","416549-2008-DE2-£1",
            "416549-1980-PL2-£1","416549-2008-SK1-£1","416549-1981-N20-£1","416549-1993-MK4-£1",
            "416549-1986-LS2-£1","416549-1975-YO6-£1","416598-2006-M1-£1","438255-2008-W1-£1",
            "438959-2007-B1-£1","446223-2009-E1-£1","446238-2008-L1-£1","446278-2007-N1-£1",
            "448903-2010-S1-£1","452132-2009-B1-£1","453942-2008-E1-£1","456883-2007-W1-£1",
            "459647-2008-M1-£1","459667-2009-B1-£1","463386-2007-L1-£1","465865-2008-E1-£1",
            "465935-2009-N1-£1","465943-2007-B1-£1","472628-2008-W1-£1","475117-2009-L1-£1",
            "475129-2007-M1-£1","475139-2008-E1-£1","475140-2009-N1-£1","476223-2007-B1-£1",
            "476224-2008-W1-£1","476383-2009-L1-£1","492181-2008-M1-£1","492182-2007-E1-£1",
            "513162-2009-N1-£1","516859-2008-B1-£1","524681-2007-W1-£1","535199-2008-L1-£1",
            "535456-2009-M1-£1","535522-2007-E1-£1","535617-2008-N1-£1","535666-2007-B1-£1",
            "535674-2008-W1-£1","535778-2009-L1-£1","535908-2007-M1-£1","537317-2008-E1-£1",
            "537410-2007-N1-£1","537569-2008-B1-£1","537855-2009-W1-£1","542402-2007-L1-£1",
            "546097-2008-M1-£1","555060-2007-E1-£1","557361-2008-N1-£1","557379-2009-B1-£1",
            "885451-2007-W1-£1","887557-2008-L1-£1",
        ]
    },
    "10p": {
        "name": "10-pound", "price": 10,
        "cards": [
            "465943-2010-NG3-£10","465943-2009-LN1-£10","465943-2010-SA1-£10","465943-2008-S63-£10",
            "465943-2012-Bh2-£10","465943-2009-Ng2-£10","465943-2013-Pl7-£10","465943-9/11-Bn7-£10",
            "465943-2010-DL1-£10","465943-2011-DE7-£10","465943-N/A-ol1-£10","465943-2011-IG8-£10",
            "465943-2009-MK4-£10","465943-2010-TS1-£10","416549-2007-M1-£10","476224-2008-E1-£10",
            "489396-2009-N1-£10","535522-2007-B1-£10","535522-2008-W1-£10","535522-2009-L1-£10",
            "535674-2007-M1-£10","537382-2008-E1-£10","537410-2007-N1-£10","537410-2008-B1-£10",
            "537410-2009-W1-£10","546097-2007-L1-£10",
        ]
    },
    "d20": {
        "name": "DVLA-20", "price": 20,
        "cards": [
            "476224-2008-KY1-£20","489396-1992-CW8-£20","535522-2007-NR1-£20","535522-2007-PL1-£20",
            "535522-2006-SK2-£20","535522-2007-N76-£20","535522-2008-NE2-£20","535522-2007-CH6-£20",
            "535522-2006-IV3-£20","535522-2006-LE5-£20","535674-2009-SA6-£20","537382-2008-CF3-£20",
            "537410-2008-DN1-£20","537410-2008-NE5-£20","537410-2008-WA6-£20","546097-2006-M26-£20",
            "416549-2007-G40-£20",
        ]
    },
    "d30": {
        "name": "DVLA-30", "price": 30,
        "cards": [
            "404970-1967-TF5-£30","404972-1960-WV6-£30","404972-1960-PR4-£30","416549-2007-SL3-£30",
            "416549-1984-BS4-£30","416549-2009-NW6-£30","416549-2008-DE2-£30","416549-1980-PL2-£30",
            "416549-2008-SK1-£30","416549-1981-N20-£30","416549-1993-MK4-£30","416549-1986-LS2-£30",
            "416549-1975-YO6-£30","439701-1992-CM1-£30","441353-1977-PE2-£30","446238-2008-SG1-£30",
            "446259-2008-CV3-£30","446291-2007-BB3-£30","535522-2009-TD8-£30","535522-1985-IP1-£30",
            "535522-1989-GU5-£30","535522-2007-PE2-£30","535522-1992-NE3-£30","535522-2009-BT1-£30",
            "535522-1977-YO8-£30","535522-2007-EN5-£30","535522-1981-S60-£30","535522-2007-PL1-£30",
            "535522-1990-BR5-£30","535522-2007-NG1-£30","535522-2006-BT8-£30","535522-1986-DY3-£30",
        ]
    },
    "m30": {
        "name": "Marks-30", "price": 30,
        "cards": [
            "404972-2008-M1-£30","416549-2007-E1-£30","454103-2009-N1-£30","463396-2008-B1-£30",
            "465942-2007-W1-£30","465950-2008-L1-£30","467062-2009-M1-£30","477596-2007-E1-£30",
            "477597-2008-N1-£30","512687-2009-B1-£30","535522-2007-W1-£30","535522-2008-L1-£30",
            "535666-2009-M1-£30","537370-2007-E1-£30","545140-2008-N1-£30","552085-2009-B1-£30",
        ]
    },
    "e25": {
        "name": "Evri-25th", "price": 25,
        "cards": [
            "411298-2009-E1-£25","412983-2008-N1-£25","416549-2007-B1-£25","446238-2008-W1-£25",
            "446261-2009-L1-£25","453978-2007-M1-£25","454103-2008-E1-£25","454313-2009-N1-£25",
            "454495-2007-B1-£25","454638-2008-W1-£25","459607-2009-L1-£25","459647-2007-M1-£25",
            "465855-2008-E1-£25","465922-2009-N1-£25","465923-2007-B1-£25","465935-2008-W1-£25",
            "465942-2009-L1-£25","465943-2007-M1-£25","465944-2008-E1-£25","465945-2009-N1-£25",
            "465950-2007-B1-£25","475129-2008-W1-£25","475139-2009-L1-£25","475141-2007-M1-£25",
            "475142-2008-E1-£25","475144-2009-N1-£25","476224-2007-B1-£25","492181-2008-W1-£25",
            "528689-2009-L1-£25","535522-2007-M1-£25","535666-2008-E1-£25","537317-2009-N1-£25",
            "557483-2007-B1-£25",
        ]
    },
    "v26": {
        "name": "Dvla-26th", "price": 30, "price_max": 80,
        "cards": [
            "374648-2008-E1-£30","411298-2009-N1-£30","412345-2007-B1-£30","446238-2008-W1-£35",
            "446291-2009-L1-£30","465855-2007-M1-£30","465859-2008-E1-£30","465942-2009-N1-£40",
            "465943-2007-B1-£30","465944-2008-W1-£30","475141-2009-L1-£30","475142-2007-M1-£35",
            "475144-2008-E1-£30","476367-2009-N1-£30","493848-1963-BT4-£30","535199-1994-YO2-£60",
            "535199-1985-RH1-£60","535522-1981-LN6-£45","535522-2001-MK1-£45","535666-1973-ML2-£40",
            "535666-2007-TS2-£40","535666-1978-SK2-£40","557351-1964-DD6-£60","557351-1958-NW3-£60",
            "557483-1964-S80-£80",
        ]
    },
    "d29": {
        "name": "DVLA-29th", "price": 30, "price_max": 80,
        "cards": [
            "404970-2008-E1-£30","404972-2009-N1-£30","412985-2007-B1-£30","453979-2008-W1-£30",
            "454313-2009-L1-£30","454638-2007-M1-£30","455206-2008-E1-£30","456072-2009-N1-£30",
            "456073-2007-B1-£30","459647-2008-W1-£30","465858-2009-L1-£30","465865-2007-M1-£30",
            "465866-2008-E1-£30","465901-2009-N1-£30","465902-2007-B1-£30","465922-2008-W1-£30",
            "465923-2009-L1-£30","465935-2007-M1-£30","465942-2008-E1-£35","465943-2009-N1-£30",
            "465944-2007-B1-£30","465950-2008-W1-£30","467062-2009-L1-£30","475139-2007-M1-£30",
            "475141-2008-E1-£30","476367-2009-N1-£30","489396-2007-B1-£30","535666-2008-W1-£40",
            "537317-2009-L1-£30","537410-2007-M1-£30",
        ]
    },
    "ej1": {
        "name": "Evri-Jul1sf", "price": 30, "price_max": 80,
        "cards": [
            "404970-2008-E1-£30","404972-2009-N1-£30","412985-2007-B1-£30","453979-2008-W1-£30",
            "454313-2009-L1-£30","454638-2007-M1-£30","456072-2009-N1-£30","459647-2008-W1-£30",
            "465858-2009-L1-£30","465865-2007-M1-£30","465901-2009-N1-£30","465902-2007-B1-£30",
            "465922-2008-W1-£30","465943-2009-N1-£30","465944-2007-B1-£30","475142-2008-E1-£30",
            "476224-2009-N1-£30","476367-2007-B1-£30","492181-2008-W1-£30","535522-2009-L1-£30",
            "535666-2007-M1-£35","537317-2008-E1-£30","537410-2009-N1-£30","542402-7/05-E11-£30",
            "543480-1947-EH4-£40","545023-2029-675-£30","552213-1970-St4-£70","557361-1990-AL4-£65",
        ]
    },
    "dj1": {
        "name": "DVLA-Jul1st", "price": 30, "price_max": 70,
        "cards": [
            "537410-2003-Ls1-£30","537410-1961-DN5-£30","537410-1962-ST1-£30","537410-1991-BS2-£30",
            "537410-1961-Cm1-£30","537410-2003-BS7-£30","537410-1977-PR4-£30","537410-2006-Ss1-£30",
            "537410-2007-bd1-£30","476367-1994-G44-£30","493848-1963-BT4-£30","535199-1994-YO2-£60",
            "535199-1985-RH1-£60","535522-1981-LN6-£45","535522-2001-MK1-£45","535666-1973-ML2-£40",
            "535666-2007-TS2-£40","535666-1978-SK2-£40","537317-1965-G33-£30","537410-1974-WS6-£30",
            "537410-1989-LL1-£30","557351-1964-DD6-£60","557351-1958-NW3-£60","557483-1964-S80-£80",
            "402073-2008-E1-£30","416549-2007-N1-£30","446291-2009-B1-£30","465865-2008-W1-£30",
            "535456-2009-L1-£30","542402-7/05-E11-£30",
        ]
    },
}

# BIN index for search
ALL_BINS = {}
for dk, dd in DATABASES.items():
    for i, card in enumerate(dd["cards"]):
        bn = card.split("-")[0]
        if bn not in ALL_BINS:
            ALL_BINS[bn] = []
        ALL_BINS[bn].append({"db": dd["name"], "card": card, "dk": dk, "idx": i})

TOPUP_AMOUNTS = [10, 20, 30, 40, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 750, 1000]

RULES_TEXT = (
    "📋 *Refund Policy*\n\n"
    "IF YOU FAIL TO FOLLOW OUR CLEAR INSTRUCTED RULES YOU WILL NOT BE REFUNDED.\n\n"
    "*How to Apply for a Refund:*\n\n"
    "1. Check card on pay.google.com\n\n"
    "2. If the card is dead, click refund at the bottom of purchased card.\n\n"
    "3. Send the bot a Screenshot/Photo that proves the card is dead.\n\n"
    "4. You have an automatic 3 minute timer when checking.\n\n"
    "5. Failing to check past the 3 minute timer can result in no refund.\n\n"
    "6. Make sure: Card Number, Expiry Date and CCV are fully visible.\n\n"
    "7. Invalid number does not qualify for refund unless all info is missing or fake.\n\n"
    "8. If all details are valid and card is dead, account will be credited within 5 minutes\n\n"
    "*Keep in Mind:*\n\n"
    "(£10 & £5 BASES ARE NOT REFUNDABLE)\n\n"
    "(HSBC CARDS ARE NOT REFUNDABLE\nOr ANY company under them such as John lewis, M&S, First direct, etc)\n\n"
    "⛔️ NOTE ⛔️\n\n"
    "🔹 Support available 24/7 @EXCELV33\n\n"
    "🔹 1 Transaction per wallet unless payment is underpaid. Wallet changes after each deposit.\n\n"
    "🔹 Payment BTC ONLY\n\n"
    "🔹 BY PURCHASING YOU AGREE TO THESE RULES. FAILURE TO READ THEM WILL FORFEIT YOUR REFUND / REPLACEMENT. WE SHALL GIVE NO WARNINGS"
)

def build_bin_summary(cards):
    """Build BIN summary like '411298 x1', '416549 x3' etc"""
    counter = Counter(card.split("-")[0] for card in cards)
    lines = [f"{bin_num} x{count}" for bin_num, count in sorted(counter.items())]
    return "\n".join(lines)

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
    return str(update.effective_user.id) == str(ADMIN_CHAT_ID) or str(update.effective_chat.id) == str(CONSOLE_CHAT)

def get_balance(context, user_id):
    return context.bot_data.get("balances", {}).get(user_id, 0)

def credits_to_btc(credits):
    return round(credits / 60000, 8)

def main_menu_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Store",   callback_data="store"),
         InlineKeyboardButton("💳 Wallet",  callback_data="wallet")],
        [InlineKeyboardButton("🛡 Rules",   callback_data="rules")],
        [InlineKeyboardButton("📞 Support", url="https://t.me/EXCELV33"),
         InlineKeyboardButton("📢 Channel", url=CHANNEL_LINK)],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if "join_dates" not in context.bot_data:
        context.bot_data["join_dates"] = {}
    if user.id not in context.bot_data["join_dates"]:
        context.bot_data["join_dates"][user.id] = datetime.now().strftime("%d-%m-%Y")
    await console_log(context, user, "opened the bot")

    await update.message.reply_text(
        "📋 Refund Policy:\n\n"
        "IF YOU FAIL TO FOLLOW OUR CLEAR INSTRUCTED RULES YOU WILL NOT BE REFUNDED.\n\n"
        "How to Apply for a Refund:\n\n"
        "1. Check card on pay.google.com\n\n"
        "2. If the card is dead, click refund at the bottom of purchased card.\n\n"
        "3. Send the bot a Screenshot/Photo that proves the card is dead.\n\n"
        "4. When checking card on pay.google.com, you have an automatic 3 minute timer.\n\n"
        "5. Failing to check card / provide proof of card being dead past the 3 minute timer can result in no refund.\n\n"
        "6. When providing a photo or a screenshot, please make sure: Card Number, Expiry Date and CCV are fully visible.\n\n"
        "7. If number doesn't call or is invalid this doesn't qualify for refund /unless all missing or fake info.\n\n"
        "8. If all the details are valid and the card is dead your account will be credited again with a refund within 5 minutes\n\n"
        "Keep in Mind:\n\n"
        "(£10 & £5 BASES ARE NOT REFUNDABLE)\n\n"
        "(HSBC CARDS ARE NOT REFUNDABLE\nOr ANY company under them such as John lewis,M&S, First direct ,etc)\n\n"
        "⛔️ NOTE ⛔️\n\n"
        "🔹 Support account is available 24/7 @EXCELV33\n\n"
        "🔹 1 Transaction per wallet unless payment is underpaid. Our wallet always changes after each completed deposit.\n\n"
        "🔹 Payment BTC ONLY\n\n"
        "🔹 BY PURCHASING YOU AGREE TO THESE RULES. FAILURE TO READ THEM WILL FORFEIT YOUR REFUND / REPLACEMENT. WE SHALL GIVE NO WARNINGS"
    )
    await update.message.reply_text(
        f"Welcome to EXCEL Store 👋\nUse the menu below to interact with the bot 🤖\n\n"
        f"===============\nManaged by {ADMIN_USERNAME}\n\n"
        f"🔹 Support available 24/7 {SUPPORT_USER}\n\n"
        f"🔹 1 Transaction per wallet unless payment is underpaid.\n\n"
        f"🔹 Payment BTC ONLY\n\n"
        f"🔹 BY PURCHASING YOU AGREE TO THESE RULES. WE SHALL GIVE NO WARNINGS",
        reply_markup=main_menu_kb()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    await query.answer()
    data    = query.data
    user    = query.from_user
    user_id = user.id
    balance = get_balance(context, user_id)

    await console_log(context, user, f"tapped {data[:40]}")

    if data == "main_menu":
        await query.edit_message_text(
            f"Welcome to EXCEL Store 👋\nManaged by {ADMIN_USERNAME}",
            reply_markup=main_menu_kb()
        )

    elif data == "store":
        await query.edit_message_text(
            "🔹 Payment BTC ONLY\n\n🔹 BY PURCHASING YOU AGREE TO THESE RULES.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📋 Fullz", callback_data="fullz")],
                [InlineKeyboardButton("🌐 Main Menu", callback_data="main_menu")],
            ])
        )

    elif data == "fullz":
        total = sum(len(d["cards"]) for d in DATABASES.values())
        buttons = []
        for dk, dd in DATABASES.items():
            pt = f"£{dd['price']}" + (f" - £{dd['price_max']}" if "price_max" in dd else "")
            buttons.append([InlineKeyboardButton(f"🔸 {dd['name']} ({pt})", callback_data=f"sb|{dk}")])
        buttons.append([InlineKeyboardButton("🔍 Search for BIN", callback_data="search_bin")])
        buttons.append([InlineKeyboardButton("🌐 Main Menu", callback_data="main_menu")])
        await query.edit_message_text(
            f"🚨 {total} Products Total\n\n--- AVAILABLE FULLZ DATABASES ---",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # sb = show BIN summary for a database
    elif data.startswith("sb|"):
        dk          = data.split("|")[1]
        dd          = DATABASES.get(dk)
        if not dd:
            return
        cards       = dd["cards"]
        total       = len(cards)
        page        = 0
        total_pages = (total + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
        pt          = f"£{dd['price']}" + (f" - £{dd['price_max']}" if "price_max" in dd else "")
        summary     = build_bin_summary(cards)
        page_cards  = cards[0:ITEMS_PER_PAGE]

        if not cards:
            await query.edit_message_text(
                "No BINs available for this base.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("◀ Back", callback_data="fullz")]
                ])
            )
            return

        # Build card buttons
        buttons = []
        for i, card in enumerate(page_cards):
            display = card.replace("-", " - ")
            buttons.append([InlineKeyboardButton(display, callback_data=f"bc|{dk}|{i}")])

        # Nav buttons
        nav = [InlineKeyboardButton("🔄 Refresh", callback_data=f"sb|{dk}")]
        if total_pages > 1:
            nav.append(InlineKeyboardButton("Next ➡️", callback_data=f"pg|{dk}|1"))
        buttons.append(nav)
        buttons.append([InlineKeyboardButton("◀ Previous Menu", callback_data="fullz")])
        buttons.append([InlineKeyboardButton("🌐 Main Menu",     callback_data="main_menu")])

        await query.edit_message_text(
            f"🚨 {total} / {total} Products Total\n"
            f"📑 Page 1 / {total_pages}\n"
            f"==========\n"
            f"{summary}\n"
            f"==========\n"
            f"💰 Price: {pt}",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # pg = show paginated card buttons
    elif data.startswith("pg|"):
        _, dk, pg   = data.split("|")
        page        = int(pg)
        dd          = DATABASES.get(dk)
        if not dd:
            return
        cards       = dd["cards"]
        total       = len(cards)
        total_pages = (total + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
        page_cards  = cards[page * ITEMS_PER_PAGE:(page + 1) * ITEMS_PER_PAGE]
        start_idx   = page * ITEMS_PER_PAGE
        pt          = f"£{dd['price']}" + (f" - £{dd['price_max']}" if "price_max" in dd else "")

        buttons = []
        for i, card in enumerate(page_cards):
            display = card.replace("-", " - ")
            buttons.append([InlineKeyboardButton(display, callback_data=f"bc|{dk}|{start_idx+i}")])

        nav = []
        if page > 0:
            nav.append(InlineKeyboardButton("◀️ Prev", callback_data=f"pg|{dk}|{page-1}"))
        nav.append(InlineKeyboardButton("🔄 Refresh", callback_data=f"pg|{dk}|{page}"))
        if page < total_pages - 1:
            nav.append(InlineKeyboardButton("Next ➡️", callback_data=f"pg|{dk}|{page+1}"))
        buttons.append(nav)
        buttons.append([InlineKeyboardButton("◀ Previous Menu", callback_data=f"sb|{dk}")])
        buttons.append([InlineKeyboardButton("🌐 Main Menu",     callback_data="main_menu")])

        await query.edit_message_text(
            f"🚨 {total} Products | Page {page+1}/{total_pages}\n💰 Price: {pt}\n==========",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif data.startswith("bc|"):
        _, dk, idx_str = data.split("|")
        idx     = int(idx_str)
        dd      = DATABASES.get(dk)
        card    = dd["cards"][idx]
        try:
            price = int(card.split("-")[-1].replace("£","").strip())
        except:
            price = dd["price"]
        display = card.replace("-", " - ")
        context.user_data["pending"] = {"dk": dk, "idx": idx, "card": display, "price": price}

        await query.edit_message_text(
            f"🛒 *Purchase Confirmation*\n\nCard: {display}\nCost: £{price}\nYour Balance: £{balance}\n\nConfirm purchase?",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Confirm", callback_data="confirm")],
                [InlineKeyboardButton("❌ Cancel",  callback_data=f"pg|{dk}|0")],
            ])
        )

    elif data == "confirm":
        p       = context.user_data.get("pending", {})
        price   = p.get("price", 0)
        card    = p.get("card", "")
        dk      = p.get("dk", "")
        balance = get_balance(context, user_id)

        if balance < price:
            await query.edit_message_text(
                f"❌ Insufficient balance!\n\nThis card costs £{price} but you only have £{balance}.\n\nPlease top up your wallet first.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💳 Top Up Wallet", callback_data="wallet")],
                    [InlineKeyboardButton("⬅️ Back",          callback_data=f"pg|{dk}|0")],
                ])
            )
            return

        if "balances" not in context.bot_data:
            context.bot_data["balances"] = {}
        context.bot_data["balances"][user_id] = balance - price
        new_bal = context.bot_data["balances"][user_id]
        await console_log(context, user, f"purchased {card} for £{price}")
        await query.edit_message_text(
            f"✅ *Purchase Successful!*\n\nCard: {card}\nCost: £{price}\nRemaining Balance: £{new_bal}\n\nYour file will be delivered shortly.\nContact {SUPPORT_USER} if you have any issues.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌐 Main Menu", callback_data="main_menu")]])
        )
        if ADMIN_CHAT_ID:
            try:
                await context.bot.send_message(chat_id=ADMIN_CHAT_ID,
                    text=f"NEW ORDER\nUser: @{user.username or user.first_name}\nID: {user_id}\nCard: {card}\nPrice: £{price}\nBalance: £{new_bal}")
            except Exception as e:
                logger.error(f"notify error: {e}")
        context.user_data.pop("pending", None)

    elif data == "search_bin":
        context.user_data["waiting_bin"] = True
        await query.edit_message_text(
            "🔍 *Search for BIN*\n\nType your BIN number (first 6 digits):",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="fullz")]])
        )

    elif data == "wallet":
        join_date = context.bot_data.get("join_dates", {}).get(user_id, datetime.now().strftime("%d-%m-%Y"))
        rows = []
        row  = []
        for a in TOPUP_AMOUNTS:
            row.append(InlineKeyboardButton(f"🔸 £{a} 🔸", callback_data=f"tp|{a}"))
            if len(row) == 2:
                rows.append(row); row = []
        if row: rows.append(row)
        rows.append([InlineKeyboardButton("💰 Custom Amount", callback_data="tp_custom")])
        rows.append([InlineKeyboardButton("🌐 Main Menu",     callback_data="main_menu")])
        await query.edit_message_text(
            f"🔹 Payment BTC ONLY\n\n🔹 BY PURCHASING YOU AGREE TO THESE RULES.\n\n"
            f"============================\n🪪 ID: {user_id}\n💰 Balance: £{balance}\n📅 Join Date: {join_date}\n============================",
            reply_markup=InlineKeyboardMarkup(rows)
        )

    elif data.startswith("tp|"):
        amount  = int(data.split("|")[1])
        btc_amt = credits_to_btc(amount)
        await console_log(context, user, f"selected top up £{amount}")
        await query.edit_message_text(
            f"Send Exactly {btc_amt} to the address below to get {amount} credits\n\n"
            f"🏦 :\n{BTC_ADDRESS}\n\n"
            f"‼️ Deposits are permanent and non refundable\n"
            f"‼️ Double Check the BTC amount before sending\n"
            f"‼️ Anything UNDER or ABOVE will be considered a Donation\n"
            f"🔶 You will be funded when your transaction is confirmed\n"
            f"⚠️ DO NOT SEND AS £ only send as BTC\n"
            f"‼️ One payment per wallet address\n"
            f"‼️ Anything else will Not be credited",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ I've Sent Payment", callback_data=f"paid|{amount}")],
                [InlineKeyboardButton("⬅️ Back",             callback_data="wallet")],
            ])
        )

    elif data == "tp_custom":
        context.user_data["waiting_custom"] = True
        await query.edit_message_text("💰 Enter your custom top up amount in £:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="wallet")]]))

    elif data.startswith("paid|"):
        amount = int(data.split("|")[1])
        await console_log(context, user, f"submitted top up payment of £{amount}")
        await query.edit_message_text(
            f"✅ Payment submitted for £{amount}!\n\nYou will be funded once confirmed.\nContact {SUPPORT_USER} if you have any issues.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌐 Main Menu", callback_data="main_menu")]])
        )
        if ADMIN_CHAT_ID:
            try:
                await context.bot.send_message(chat_id=ADMIN_CHAT_ID,
                    text=f"TOP-UP REQUEST\nUser: @{user.username or user.first_name}\nID: {user_id}\nAmount: £{amount}\n\nUse /userbal {user_id} {amount} pass to credit.")
            except Exception as e:
                logger.error(f"notify error: {e}")

    elif data == "rules":
        await query.edit_message_text(RULES_TEXT, parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌐 Main Menu", callback_data="main_menu")]]))

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text.strip()

    if context.user_data.get("waiting_bin"):
        context.user_data["waiting_bin"] = False
        bn      = text[:6]
        results = ALL_BINS.get(bn, [])
        if results:
            msg = f"🔍 BIN {bn} found in {len(results)} result(s):\n\n"
            for r in results[:10]:
                msg += f"📋 [{r['db']}] {r['card'].replace('-',' - ')}\n"
        else:
            msg = f"❌ BIN {bn} not found.\n\nContact {SUPPORT_USER}."
        await update.message.reply_text(msg,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back to Fullz", callback_data="fullz")]]))
        return

    if context.user_data.get("waiting_custom"):
        context.user_data["waiting_custom"] = False
        try:
            amount  = int(text.replace("£","").strip())
            btc_amt = credits_to_btc(amount)
            await update.message.reply_text(
                f"Send Exactly {btc_amt} to:\n\n🏦 :\n{BTC_ADDRESS}\n\n"
                f"‼️ Deposits are permanent and non refundable\n🔶 Funded when transaction is confirmed\n⚠️ DO NOT SEND AS £",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("✅ I've Sent Payment", callback_data=f"paid|{amount}")],
                    [InlineKeyboardButton("⬅️ Back",             callback_data="wallet")],
                ])
            )
        except ValueError:
            await update.message.reply_text("Please enter a valid number e.g. 50")
        return

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    await update.message.reply_text(f"Chat ID: {chat.id}\nType: {chat.type}\nTitle: {getattr(chat,'title','N/A')}")

async def userbal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update): return
    try:
        tid, amt = int(context.args[0]), int(context.args[1])
        if len(context.args) < 3 or context.args[2] != "pass":
            await update.message.reply_text("Usage: /userbal <id> <amount> pass"); return
        if "balances" not in context.bot_data: context.bot_data["balances"] = {}
        context.bot_data["balances"][tid] = context.bot_data["balances"].get(tid, 0) + amt
        nb = context.bot_data["balances"][tid]
        await update.message.reply_text(f"Balance updated for {tid}: £{nb}")
        await context.bot.send_message(chat_id=tid, text=f"✅ £{amt} has been added to your wallet!\n\nYour balance is now £{nb}.")
        await console_log(context, update.effective_user, f"credited £{amt} to user {tid}")
    except Exception as e:
        await update.message.reply_text(f"Usage: /userbal <id> <amount> pass\nError: {e}")

async def removebalance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update): return
    try:
        tid, amt = int(context.args[0]), int(context.args[1])
        if "balances" not in context.bot_data: context.bot_data["balances"] = {}
        context.bot_data["balances"][tid] = max(0, context.bot_data["balances"].get(tid, 0) - amt)
        await update.message.reply_text(f"Removed £{amt} from user {tid}.")
    except Exception as e:
        await update.message.reply_text(f"Usage: /removebalance <id> <amount>\nError: {e}")

async def checkbalance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update): return
    try:
        tid = int(context.args[0])
        bal = context.bot_data.get("balances", {}).get(tid, 0)
        await update.message.reply_text(f"User {tid} balance: £{bal}")
    except Exception as e:
        await update.message.reply_text(f"Usage: /checkbalance <id>\nError: {e}")

async def adminhelp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update): return
    await update.message.reply_text(
        "Admin Commands:\n\n/userbal <id> <amount> pass\n/removebalance <id> <amount>\n/checkbalance <id>\n/getid\n/adminhelp")

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
    logger.info("EXCEL Store Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
