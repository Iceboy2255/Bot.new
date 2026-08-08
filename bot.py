import os
import logging
import random
from datetime import datetime
from collections import Counter
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger(__name__)

TOKEN          = os.environ.get("BOT_TOKEN", "8912863330:AAHmfKWCXm3hc-lI-ghfIsecG6tfJer2_l8")
ADMIN_USERNAME = "@EXCELV33"
ADMIN_CHAT_ID  = "6004004907"
CONSOLE_CHAT   = -1004325765629
BTC_ADDRESS    = os.environ.get("BTC_ADDRESS", "YOUR_BTC_ADDRESS")
CHANNEL_LINK   = "https://t.me/EXCELupdate"
SUPPORT_USER   = "@EXCELV33"
ITEMS_PER_PAGE = 14

DATABASES = {
    "1p": {
        "name": "1-pound", "price": 1,
        "cards": [
            "475142-1945-S36-£1","475142-1982-CM7-£1","475142-1961-CM7-£1","475142-1973-DL1-£1",
            "475142-1988-DA1-£1","475142-1934-CB2-£1","475142-1950-Ss9-£1","475142-1967-Ss9-£1",
            "475142-1979-bh1-£1","475142-1939-DD2-£1","475142-1985-BS3-£1","475142-1956-SO3-£1",
            "475142-1972-IP9-£1","222300-1941-E1-£1","400022-1963-N1-£1","401816-1984-B1-£1",
            "416549-1955-SL3-£1","416549-1989-BS4-£1","416549-1932-NW6-£1","416549-1978-DE2-£1",
            "416549-1948-PL2-£1","416549-1969-SK1-£1","416549-1981-N20-£1","416549-1937-MK4-£1",
            "416549-1960-LS2-£1","416549-1974-YO6-£1","416598-1983-M1-£1","438255-1942-W1-£1",
            "438959-1951-B1-£1","446223-1976-E1-£1","446238-1965-L1-£1","446278-1987-N1-£1",
            "448903-1933-S1-£1","452132-1958-B1-£1","453942-1970-E1-£1","456883-1946-W1-£1",
            "459647-1980-M1-£1","459667-1964-B1-£1","463386-1953-L1-£1","465865-1975-E1-£1",
            "465935-1938-N1-£1","465943-1986-B1-£1","472628-1949-W1-£1","475117-1962-L1-£1",
            "475129-1971-M1-£1","475139-1954-E1-£1","475140-1984-N1-£1","476223-1935-B1-£1",
            "476224-1966-W1-£1","476383-1977-L1-£1","492181-1943-M1-£1","492182-1988-E1-£1",
            "513162-1959-N1-£1","516859-1972-B1-£1","524681-1931-W1-£1","535199-1968-L1-£1",
            "535456-1983-M1-£1","535522-1947-E1-£1","535617-1979-N1-£1","535666-1952-B1-£1",
            "535674-1963-W1-£1","535778-1985-L1-£1","535908-1936-M1-£1","537317-1970-E1-£1",
            "537410-1989-N1-£1","537569-1944-B1-£1","537855-1957-W1-£1","542402-1974-L1-£1",
            "546097-1965-M1-£1","555060-1981-E1-£1","557361-1939-N1-£1","557379-1950-B1-£1",
            "885451-1973-W1-£1","887557-1986-L1-£1",
        ]
    },
    "10p": {
        "name": "10-pound", "price": 10,
        "cards": [
            "465943-1967-NG3-£10","465943-1942-LN1-£10","465943-1984-SA1-£10","465943-1953-S63-£10",
            "465943-1975-Bh2-£10","465943-1931-Ng2-£10","465943-1989-Pl7-£10","465943-1960-Bn7-£10",
            "465943-1948-DL1-£10","465943-1971-DE7-£10","465943-1986-ol1-£10","465943-1954-IG8-£10",
            "465943-1979-MK4-£10","465943-1938-TS1-£10","416549-1964-M1-£10","476224-1982-E1-£10",
            "489396-1945-N1-£10","535522-1970-B1-£10","535522-1957-W1-£10","535522-1988-L1-£10",
            "535674-1933-M1-£10","537382-1973-E1-£10","537410-1951-N1-£10","537410-1980-B1-£10",
            "537410-1962-W1-£10","546097-1940-L1-£10",
        ]
    },
    "d20": {
        "name": "DVLA-20", "price": 20,
        "cards": [
            "476224-1965-KY1-£20","489396-1981-CW8-£20","535522-1943-NR1-£20","535522-1977-PL1-£20",
            "535522-1952-SK2-£20","535522-1989-N76-£20","535522-1936-NE2-£20","535522-1970-CH6-£20",
            "535522-1958-IV3-£20","535522-1984-LE5-£20","535674-1947-SA6-£20","537382-1972-CF3-£20",
            "537410-1961-DN1-£20","537410-1986-NE5-£20","537410-1934-WA6-£20","546097-1979-M26-£20",
            "416549-1950-G40-£20",
        ]
    },
    "d30": {
        "name": "DVLA-30", "price": 30,
        "cards": [
            "404970-1983-TF5-£30","404972-1946-WV6-£30","404972-1974-PR4-£30","416549-1959-SL3-£30",
            "416549-1987-BS4-£30","416549-1935-NW6-£30","416549-1971-DE2-£30","416549-1942-PL2-£30",
            "416549-1978-SK1-£30","416549-1960-N20-£30","416549-1989-MK4-£30","416549-1945-LS2-£30",
            "416549-1976-YO6-£30","439701-1952-CM1-£30","441353-1981-PE2-£30","446238-1938-SG1-£30",
            "446259-1967-CV3-£30","446291-1954-BB3-£30","535522-1985-TD8-£30","535522-1941-IP1-£30",
            "535522-1972-GU5-£30","535522-1963-PE2-£30","535522-1988-NE3-£30","535522-1949-BT1-£30",
            "535522-1979-YO8-£30","535522-1933-EN5-£30","535522-1966-S60-£30","535522-1951-PL1-£30",
            "535522-1980-BR5-£30","535522-1944-NG1-£30","535522-1975-BT8-£30","535522-1961-DY3-£30",
        ]
    },
    "m30": {
        "name": "Marks-30", "price": 30,
        "cards": [
            "404972-1970-M1-£30","416549-1948-E1-£30","454103-1982-N1-£30","463396-1935-B1-£30",
            "465942-1964-W1-£30","465950-1977-L1-£30","467062-1951-M1-£30","477596-1989-E1-£30",
            "477597-1942-N1-£30","512687-1963-B1-£30","535522-1975-W1-£30","535522-1938-L1-£30",
            "535666-1986-M1-£30","537370-1957-E1-£30","545140-1971-N1-£30","552085-1944-B1-£30",
        ]
    },
    "e25": {
        "name": "Evri-25th", "price": 25,
        "cards": [
            "411298-1960-E1-£25","412983-1983-N1-£25","416549-1945-B1-£25","446238-1978-W1-£25",
            "446261-1952-L1-£25","453978-1987-M1-£25","454103-1932-E1-£25","454313-1971-N1-£25",
            "454495-1966-B1-£25","454638-1940-W1-£25","459607-1985-L1-£25","459647-1954-M1-£25",
            "465855-1973-E1-£25","465922-1947-N1-£25","465923-1980-B1-£25","465935-1962-W1-£25",
            "465942-1939-L1-£25","465943-1974-M1-£25","465944-1958-E1-£25","465945-1986-N1-£25",
            "465950-1943-B1-£25","475129-1969-W1-£25","475139-1951-L1-£25","475141-1977-M1-£25",
            "475142-1934-E1-£25","475144-1982-N1-£25","476224-1961-B1-£25","492181-1948-W1-£25",
            "528689-1975-L1-£25","535522-1937-M1-£25","535666-1989-E1-£25","537317-1955-N1-£25",
            "557483-1968-B1-£25",
        ]
    },
    "v26": {
        "name": "Dvla-26th", "price": 30, "price_max": 80,
        "cards": [
            "374648-1941-E1-£30","411298-1976-N1-£30","412345-1953-B1-£30","446238-1984-W1-£35",
            "446291-1936-L1-£30","465855-1962-M1-£30","465859-1978-E1-£30","465942-1949-N1-£40",
            "465943-1971-B1-£30","465944-1957-W1-£30","475141-1988-L1-£30","475142-1944-M1-£35",
            "475144-1967-E1-£30","476367-1932-N1-£30","493848-1975-BT4-£30","535199-1951-YO2-£60",
            "535199-1983-RH1-£60","535522-1960-LN6-£45","535522-1940-MK1-£45","535666-1974-ML2-£40",
            "535666-1989-TS2-£40","535666-1955-SK2-£40","557351-1966-DD6-£60","557351-1938-NW3-£60",
            "557483-1981-S80-£80",
        ]
    },
    "d29": {
        "name": "DVLA-29th", "price": 30, "price_max": 80,
        "cards": [
            "404970-1954-E1-£30","404972-1972-N1-£30","412985-1939-B1-£30","453979-1986-W1-£30",
            "454313-1946-L1-£30","454638-1970-M1-£30","455206-1961-E1-£30","456072-1982-N1-£30",
            "456073-1933-B1-£30","459647-1977-W1-£30","465858-1950-L1-£30","465865-1988-M1-£30",
            "465866-1943-E1-£30","465901-1964-N1-£30","465902-1975-B1-£30","465922-1958-W1-£30",
            "465923-1981-L1-£30","465935-1937-M1-£30","465942-1968-E1-£35","465943-1947-N1-£30",
            "465944-1973-B1-£30","465950-1959-W1-£30","467062-1984-L1-£30","475139-1932-M1-£30",
            "475141-1969-E1-£30","476367-1952-N1-£30","489396-1979-B1-£30","535666-1941-W1-£40",
            "537317-1976-L1-£30","537410-1963-M1-£30",
        ]
    },
    "ej1": {
        "name": "Evri-Jul1sf", "price": 30, "price_max": 80,
        "cards": [
            "404970-1970-E1-£30","404972-1944-N1-£30","412985-1981-B1-£30","453979-1958-W1-£30",
            "454313-1935-L1-£30","454638-1977-M1-£30","456072-1951-N1-£30","459647-1988-W1-£30",
            "465858-1942-L1-£30","465865-1966-M1-£30","465901-1973-N1-£30","465902-1938-B1-£30",
            "465922-1984-W1-£30","465943-1959-N1-£30","465944-1975-B1-£30","475142-1949-E1-£30",
            "476224-1962-N1-£30","476367-1980-B1-£30","492181-1933-W1-£30","535522-1972-L1-£30",
            "535666-1956-M1-£35","537317-1986-E1-£30","537410-1940-N1-£30","542402-1968-E11-£30",
            "543480-1953-EH4-£40","545023-1979-675-£30","552213-1947-St4-£70","557361-1983-AL4-£65",
        ]
    },
    "dj1": {
        "name": "DVLA-Jul1st", "price": 30, "price_max": 70,
        "cards": [
            "537410-1964-Ls1-£30","537410-1982-DN5-£30","537410-1941-ST1-£30","537410-1975-BS2-£30",
            "537410-1958-Cm1-£30","537410-1936-BS7-£30","537410-1970-PR4-£30","537410-1953-Ss1-£30",
            "537410-1986-bd1-£30","476367-1945-G44-£30","493848-1978-BT4-£30","535199-1933-YO2-£60",
            "535199-1967-RH1-£60","535522-1950-LN6-£45","535522-1984-MK1-£45","535666-1942-ML2-£40",
            "535666-1971-TS2-£40","535666-1960-SK2-£40","537317-1988-G33-£30","537410-1937-WS6-£30",
            "537410-1976-LL1-£30","557351-1955-DD6-£60","557351-1980-NW3-£60","557483-1948-S80-£80",
            "402073-1973-E1-£30","416549-1961-N1-£30","446291-1985-B1-£30","465865-1939-W1-£30",
            "535456-1977-L1-£30","542402-1952-E11-£30",
        ]
    },
}

ALL_BINS = {}
for dk, dd in DATABASES.items():
    for i, card in enumerate(dd["cards"]):
        bn = card.split("-")[0]
        if bn not in ALL_BINS:
            ALL_BINS[bn] = []
        ALL_BINS[bn].append({"db": dd["name"], "card": card, "dk": dk, "idx": i})

TOPUP_AMOUNTS = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 750, 1000]

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
    counter = Counter(card.split("-")[0] for card in cards)
    lines = [f"{bin_num} x{count}" for bin_num, count in sorted(counter.items())]
    return "\n".join(lines)

async def sendLog(context, user, text):
    try:
        username = f"@{user.username}" if user.username else user.first_name
        await context.bot.send_message(
            CONSOLE_CHAT,
            f"{username} {text}"
        )
    except Exception:
        pass

def is_admin(update):
    user_id = str(update.effective_user.id)
    chat_id = str(update.effective_chat.id)
    return user_id == ADMIN_CHAT_ID or chat_id == str(CONSOLE_CHAT)

def get_balance(context, user_id):
    return context.bot_data.get("balances", {}).get(user_id, 0)

def credits_to_btc(credits):
    return round(credits / 60000, 8)

def main_menu_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Store",   callback_data="store"),
         InlineKeyboardButton("💷 Wallet",  callback_data="wallet")],
        [InlineKeyboardButton("🛡️ Rules",   callback_data="rules"),
         InlineKeyboardButton("☎️ Support", url="https://t.me/EXCELV33")],
        [InlineKeyboardButton("📄 Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("Search BIN 🔍", callback_data="search_bin")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if "join_dates" not in context.bot_data:
        context.bot_data["join_dates"] = {}
    if user.id not in context.bot_data["join_dates"]:
        context.bot_data["join_dates"][user.id] = datetime.now().strftime("%d-%m-%Y")
    await sendLog(context, user, "just started the bot")

    await update.message.reply_text(
        "Welcome to EXCEL Store 👋\n"
        "Use the menu below to interact with the bot 🤖\n"
        "======================\n"
        "Managed by @EXCELV33\n"
        "Coded by @Kr3ptoV1 on session 05a5c62989edb4dadf7cb1274e35e37d498b5af459b04e08fe08ab037a206ec841",
        reply_markup=main_menu_kb()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    await query.answer()
    data    = query.data
    user    = query.from_user
    user_id = user.id
    balance = get_balance(context, user_id)

    if data == "main_menu":
        await query.edit_message_text(
            "Welcome to EXCEL Store 👋\n"
            "Use the menu below to interact with the bot 🤖\n"
            "======================\n"
            "Managed by @EXCELV33\n"
            "Coded by @Kr3ptoV1 on session 05a5c62989edb4dadf7cb1274e35e37d498b5af459b04e08fe08ab037a206ec841",
            reply_markup=main_menu_kb()
        )

    elif data == "store":
        await sendLog(context, user, "is browsing through leads")
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
        buttons.append([InlineKeyboardButton("Search BIN 🔍", callback_data="search_bin")])
        buttons.append([InlineKeyboardButton("🌐 Main Menu", callback_data="main_menu")])
        await query.edit_message_text(
            f"🚨 {total} Products Total\n\n--- AVAILABLE FULLZ DATABASES ---",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif data.startswith("sb|"):
        dk          = data.split("|")[1]
        dd          = DATABASES.get(dk)
        if not dd:
            return
        await sendLog(context, user, f"is viewing category {dd['name']}")
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

        buttons = []
        for i, card in enumerate(page_cards):
            display = card.replace("-", " - ")
            buttons.append([InlineKeyboardButton(display, callback_data=f"bc|{dk}|{i}")])

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
            await sendLog(context, user, "tried to buy fullz, but no credits")
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
        order_id = f"ORD-{user_id}-{datetime.now().strftime('%H%M%S')}"
        await sendLog(context, user, f"purchased fullz successfully ({order_id})")
        await query.edit_message_text(
            f"✅ *Purchase Successful!*\n\nCard: {card}\nCost: £{price}\nRemaining Balance: £{new_bal}\n\nYour file will be delivered shortly.\nContact {SUPPORT_USER} if you have any issues.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌐 Main Menu", callback_data="main_menu")]] )
        )
        if ADMIN_CHAT_ID:
            try:
                await context.bot.send_message(chat_id=ADMIN_CHAT_ID,
                    text=f"NEW ORDER\nUser: @{user.username or user.first_name}\nID: {user_id}\nCard: {card}\nPrice: £{price}\nBalance: £{new_bal}")
            except Exception:
                pass
        context.user_data.pop("pending", None)

    elif data == "search_bin":
        context.user_data["waiting_bin"] = True
        await sendLog(context, user, "is searching for a BIN")
        await query.edit_message_text(
            "Enter first 6 digits of BIN",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]])
        )

    elif data == "wallet":
        await sendLog(context, user, f"({user_id}) opened the wallet")
        join_date = context.bot_data.get("join_dates", {}).get(user_id, datetime.now().strftime("%d-%m-%Y"))
        rows = [
            [InlineKeyboardButton("£50", callback_data="tp|50"), InlineKeyboardButton("£100", callback_data="tp|100")],
            [InlineKeyboardButton("£150", callback_data="tp|150"), InlineKeyboardButton("£200", callback_data="tp|200")],
            [InlineKeyboardButton("£250", callback_data="tp|250"), InlineKeyboardButton("£300", callback_data="tp|300")],
            [InlineKeyboardButton("£350", callback_data="tp|350"), InlineKeyboardButton("£400", callback_data="tp|400")],
            [InlineKeyboardButton("£450", callback_data="tp|450"), InlineKeyboardButton("£500", callback_data="tp|500")],
            [InlineKeyboardButton("£750", callback_data="tp|750"), InlineKeyboardButton("£1000", callback_data="tp|1000")],
            [InlineKeyboardButton("Custom Amount", callback_data="tp_custom")],
            [InlineKeyboardButton("Main Menu", callback_data="main_menu")]
        ]
        await query.edit_message_text(
            f"🔹 Payment BTC ONLY\n\n🔹 BY PURCHASING YOU AGREE TO THESE RULES.\n\n"
            f"============================\n🪪 ID: {user_id}\n💰 Balance: £{balance}\n📅 Join Date: {join_date}\n============================",
            reply_markup=InlineKeyboardMarkup(rows)
        )

    elif data.startswith("tp|"):
        amount  = int(data.split("|")[1])
        btc_amt = credits_to_btc(amount)
        await sendLog(context, user, f"({user_id}) opened the topup page for £{amount}")
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
        await sendLog(context, user, f"submitted a payment of £{amount}")
        await query.edit_message_text(
            f"✅ Payment submitted for £{amount}!\n\nYou will be funded once confirmed.\nContact {SUPPORT_USER} if you have any issues.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌐 Main Menu", callback_data="main_menu")]] )
        )
        if ADMIN_CHAT_ID:
            try:
                await context.bot.send_message(chat_id=ADMIN_CHAT_ID,
                    text=f"TOP-UP REQUEST\nUser: @{user.username or user.first_name}\nID: {user_id}\nAmount: £{amount}\n\nUse /userbal {user_id} {amount} pass to credit.")
            except Exception:
                pass

    elif data == "rules":
        await query.edit_message_text(RULES_TEXT, parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌐 Main Menu", callback_data="main_menu")]] ))

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text.strip()

    if context.user_data.get("waiting_bin"):
        context.user_data["waiting_bin"] = False
        import re
        if not re.match(r"^\d{6}$", text):
            await update.message.reply_text("Invalid BIN. Send 6 digits.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]]))
            return
        
        bin_num = text
        await sendLog(context, user, f"BIN_SEARCH: BIN: {bin_num}")
        await update.message.reply_text(
            f"BIN: {bin_num}\nBank: Test Bank\nType: Debit\nLevel: Classic\nCountry: UK",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌐 Main Menu", callback_data="main_menu")]]))
        return

    if context.user_data.get("waiting_custom"):
        context.user_data["waiting_custom"] = False
        try:
            amount  = int(text.replace("£","").strip())
            btc_amt = credits_to_btc(amount)
            await sendLog(context, user, f"({user.id}) opened the topup page for £{amount}")
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
    if not TOKEN or TOKEN == "YOUR_BOT_TOKEN":
        raise ValueError("BOT_TOKEN environment variable is missing or not set properly!")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start",         start))
    app.add_handler(CommandHandler("getid",         get_id))
    app.add_handler(CommandHandler("userbal",       userbal))
    app.add_handler(CommandHandler("removebalance", removebalance))
    app.add_handler(CommandHandler("checkbalance",  checkbalance))
    app.add_handler(CommandHandler("adminhelp",     adminhelp))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
