import os
import re
import time
import imaplib
import email
import json
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime
import threading
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

# تم وضع التوكن الجديد والمفعل هنا
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8415364406:AAGaQd9ege6upEj0XQH2X0Thl9ASPWIYTs4")
IMAP_SERVER = "imap.gmail.com"
EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT", "hrdwrermdy@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "yxiycsytfwnztwzy")

IMAP_YAHOO_SERVER = "imap.mail.yahoo.com"
IMAP_AOL_SERVER = "imap.aol.com"

YAHOO_ACCOUNTS = {
    "bibozd@yahoo.com": "jljigwcrjxkuyeao",
    "hamzausmh267@yahoo.com": "cozqfgxssbkrhcnq",
    "zikomycanal1@yahoo.com": "pagwxvirzkxvlqul",
    "icknause@yahoo.com": "oryqtcogihjabkim",
    "zikomycanal@yahoo.com": "jpwjkmwfqqxbuhmv",
    "zazabenmebarek@aol.com": "xjejcqhvzhkgasbk"
}

admin_env = os.getenv("ADMIN_IDS", "6786498950")
ADMIN_IDS = [int(admin_id.strip()) for admin_id in admin_env.split(",") if admin_id.strip().isdigit()]

NETFLIX_IMAGE_URL = "https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?q=80&w=1000&auto=format&fit=crop"
SUBSCRIPTIONS_FILE = "subscriptions.json"
LOG_FILE = "activity.log"
LAST_BROADCAST_FILE = "last_broadcast.json"
USERS_FILE = "users.json"
STATS_FILE = "stats.json"

RAW_ALLOWED_EMAILS = [
    "ALOK2000X@outlook.fr", "hamzausmh267@yahoo.com", "zaki10000007@gmail.com",
    "znetflix903@gmail.com", "X1000ZAK@outlook.fr", "fredomax29@hotmail.fr",
    "zazio1990@gmail.com", "sfr-22222@outlook.fr", "zaki065853@gmail.com",
    "alokza05@gmail.com", "x2netflix101@gmail.com", "zazazabrlo@gmail.com",
    "Zak1.1@outlook.fr", "papyclaude@live.fr", "zdz49132@gmail.com",
    "zaza055272@gmail.com", "nalbgz723@gmail.com", "saint_paul@hotmail.fr",
    "znetflix802@gmail.com", "zaki10000004@gmail.com", "rx104net@gmail.com",
    "znetflix900@gmail.com", "zaki100000003@gmail.com", "znetflix403@gmail.com",
    "znetflix804@gmail.com", "zk.2009@outlook.fr", "bibo--@outlook.com",
    "bibo.zaza@yandex.com", "netflix10zak@gmail.com", "gefloem1@hotmail.fr",
    "alfx895@gmail.com", "zatil101.10@gmail.com", "zess0301@gmail.com",
    "zo2121112@gmail.com", "zaki10000006@gmail.com", "zaza1992X@outlook.fr",
    "zaki100000002@gmail.com", "x3zaza@gmail.com", "remagelbisivni@gmail.com",
    "sfr-33333@outlook.fr", "Zaza1997X@outlook.fr", "lmza73940@gmail.com",
    "zqa10ut@gmail.com", "mechalalba140@gmail.com", "dido444444444@gmail.com",
    "x4netflix103@gmail.com", "Zaza1994X@outlook.fr", "benzaki331@gmail.com",
    "x17netflix17@gmail.com", "Zak.16.16@outlook.fr", "crdon631@gmail.com",
    "ragnarzad@gmail.com", "zazausma673@gmail.com", "Drago.60.zk@outlook.com",
    "bibo150000@gmail.com", "dido555555555@gmail.com", "Drago.10.zk@hotmail.com",
    "benmebarekzaki2@gmail.com", "sfr-55555@outlook.fr", "ben898352@gmail.com",
    "Cr7-900@outlook.com", "xza70392@gmail.com", "10trdut@gmail.com",
    "aemb72888@gmail.com", "ALOK2004X@outlook.fr", "acques.berthier30@gmail.com",
    "zaki10000005@gmail.com", "carson474444@gmail.com", "zk.2005@outlook.fr",
    "Zaza1996X@outlook.fr", "madridess17@gmail.com", "zakbza54@gmail.com",
    "moumounedu59@hotmail.fr", "zaki01115@outlook.com", "Zaki1Netflix2@gmail.com",
    "pilipaviciusmiss@gmail.com", "zizazakiki@gmail.com", "dz7283983@gmail.com",
    "znetflix801@gmail.com", "zaza065992@gmail.com", "x5netflix104@gmail.com",
    "znetflix402@gmail.com", "rosline.grellier85@gmail.com", "fqsere@gmail.com",
    "zk.2006@outlook.fr", "itajvi2@gmail.com", "zaz72171@gmail.com",
    "Drago.50.zk@outlook.com", "zaki01113@outlook.fr", "x4zaza10@gmail.com",
    "zaki01116@outlook.com", "sfr-44444@outlook.fr", "la.tribale@hotmail.fr",
    "zaki01114@outlook.com", "juoz4209@gmail.com", "Zaza1995X@outlook.fr",
    "zaza1993X@outlook.fr", "zaakak373@gmail.com", "zazabibo09@gmail.com",
    "znetflix904@gmail.com", "znetflix902@gmail.com", "zess280@gmail.com",
    "zntflix405@gmail.com", "znetflix803@gmail.com", "kza61487@gmail.com",
    "zaza-12-13-14@hotmail.com", "Zaza1991X@outlook.fr", "zaki100000001@gmail.com",
    "zaza1000000009@gmail.com", "zaza100000010@gmail.com", "zak244441@gmail.com",
    "x1netflix100@gmail.com", "Cr7-400@hotmail.com", "X20netflix20@gmail.com",
    "yhhjiaze28@gmail.com", "zazkak102@gmail.com", "dzkoki54@gmail.com",
    "zaki10000008@gmail.com", "znetflix901@gmail.com", "zaki1190000@gmail.com",
    "zaza.3636@outlook.fr", "X16netflix16@gmail.com", "zbe8274@gmail.com",
    "zddz848@gmail.com", "chclement1@hotmail.fr", "rx102net@gmail.com",
    "Cr7-800@outlook.com", "zk.2007@outlook.fr", "dhaimi.28@outlook.fr",
    "X19netflix19@gmail.com", "melanie91580@hotmail.fr", "zaki01112@outlook.fr",
    "zakimestr@gmail.com", "greg59245@hotmail.fr", "nkbbvn@gmail.com",
    "zakimadridbibo@gmail.com", "zk.2008@outlook.fr", "taliamathias@hotmail.fr",
    "zoro17816@gmail.com", "dido333333333@gmail.com", "zaqsdqa@gmail.com",
    "qsqszaz10@gmail.com", "zaki01111@outlook.fr", "ALOK2001X@outlook.fr",
    "benbz4533@gmail.com", "sasukefans@hotmail.fr", "zaki1999001@gmail.com",
    "zaki1999000@gmail.com", "cheifdido@gmail.com", "zazabibo306@gmail.com",
    "X12netflix12@gmail.com", "sfr-66666@outlook.fr", "ffbibo051@gmail.com",
    "zaki069843@gmail.com", "oku69134@gmail.com", "zaza10236@gmail.com",
    "zaza.netflix@yandex.com", "zak1.ben@yandex.com", "bibo.zaza@yandex.com",
    "bibozd@yahoo.com", "hamzausmh267@yahoo.com", "zikomycanal1@yahoo.com",
    "icknause@yahoo.com", "zikomycanal@yahoo.com", "zazabenmebarek@aol.com"
]

WHATSAPP_NUMBER = "+213552725828"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
user_selected_emails = {}
user_bot_messages = {}
admin_waiting_broadcast = set()
user_cooldowns = {}

DEFAULT_USERS = {
    "5789291272": "Farouk",
    "5022811857": "Muslim",
    "5393880306": "AZ STORE",
    "5638977180": "moh"
}

def notify_admin_error(error_msg):
    if ADMIN_IDS and error_msg:
        for admin_id in ADMIN_IDS:
            try:
                bot.send_message(admin_id, f"🚨 <b>تنبيه خطأ في النظام:</b>\n<code>{error_msg}</code>", parse_mode="HTML")
            except:
                pass

def log_user_action_detail(user_obj, email_addr, service_type, result_status):
    try:
        user_id = user_obj.id if user_obj and hasattr(user_obj, 'id') else "Unknown_ID"
        first_name = user_obj.first_name if user_obj and hasattr(user_obj, 'first_name') and user_obj.first_name else ""
        last_name = user_obj.last_name if user_obj and hasattr(user_obj, 'last_name') and user_obj.last_name else ""
        full_name = f"{first_name} {last_name}".strip()
        if not full_name:
            full_name = f"User_{user_id}"
            
        username = user_obj.username if user_obj and hasattr(user_obj, 'username') and user_obj.username else ""
        username_str = f"@{username}" if username else "بدون اسم مستخدم"
        
        date_formatted = datetime.now().strftime("%d/%m/%Y")
        
        log_entry = (
            f"========================================\n"
            f"📅 التاريخ : {date_formatted}\n"
            f"👤 اسم المستخدم : {full_name}\n"
            f"🆔 معرف التليجرام : {user_id}\n"
            f"🔗 اليوزرنيم      : {username_str}\n"
            f"📧 البريد المطلوب : {email_addr}\n"
            f"🛠 الخدمة المطلوبة : {service_type}\n"
            f"📝 حالة النتيجة    : {result_status}\n"
            f"========================================\n\n"
        )
        
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except:
        pass

def save_sale_to_client_file(client_name, client_id, email_addr, days, start_time, expiry_time):
    try:
        folder_name = "clients_folder"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            
        safe_filename = "".join(c for c in client_name if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_')
        if not safe_filename:
            safe_filename = "Unknown_Client"
            
        file_path = os.path.join(folder_name, f"{safe_filename}_{client_id}.txt")
        
        start_dt_obj = datetime.fromisoformat(str(start_time)) if isinstance(start_time, str) else start_time
        expiry_dt_obj = datetime.fromisoformat(str(expiry_time)) if isinstance(expiry_time, str) else expiry_time
        
        start_formatted = start_dt_obj.strftime("%d/%m/%Y")
        expiry_formatted = expiry_dt_obj.strftime("%d/%m/%Y")
        
        sale_entry = (
            f"========================================\n"
            f"🛒 عملية بيع / تفعيل حساب جديدة\n"
            f"👤 اسم الزبون : {client_name}\n"
            f"🆔 معرف التليجرام : {client_id}\n"
            f"📧 البريد المباع : {email_addr}\n"
            f"⏳ المدة : {days} يوماً\n"
            f"🟢 من تاريخ : {start_formatted}\n"
            f"🔴 إلى تاريخ : {expiry_formatted}\n"
            f"========================================\n\n"
        )
        
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(sale_entry)
    except:
        pass

def load_users():
    users = DEFAULT_USERS.copy()
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    users.update(data)
        except:
            pass
    return users

all_bot_users = load_users()

def save_users(users_dict):
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users_dict, f, ensure_ascii=False, indent=4)
    except:
        pass

def register_user_from_user_obj(user_obj):
    if user_obj and hasattr(user_obj, 'id'):
        chat_id_str = str(user_obj.id)
        first = user_obj.first_name if user_obj.first_name else ""
        last = user_obj.last_name if user_obj.last_name else ""
        full_name = f"{first} {last}".strip()
        if not full_name:
            full_name = "Unknown"
        all_bot_users[chat_id_str] = full_name
        save_users(all_bot_users)

def register_user(message):
    if message and hasattr(message, 'from_user') and message.from_user:
        register_user_from_user_obj(message.from_user)

def save_subscriptions(subs_dict):
    try:
        with open(SUBSCRIPTIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(subs_dict, f, ensure_ascii=False, indent=4)
    except:
        pass

def load_subscriptions():
    subs = {}
    default_expiry = (datetime.now() + timedelta(days=31)).replace(hour=0, minute=0, second=0, microsecond=0)
    for email_addr in RAW_ALLOWED_EMAILS:
        subs[email_addr.strip().lower()] = {
            "active": True,
            "expiry": default_expiry.isoformat(),
            "owner_id": None,
            "client_name": "مشترك",
            "notified_expiry": False
        }
    if os.path.exists(SUBSCRIPTIONS_FILE):
        try:
            with open(SUBSCRIPTIONS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    for k, v in data.items():
                        clean_k = k.strip().lower()
                        if clean_k in subs and isinstance(v, dict):
                            subs[clean_k] = v
        except:
            pass
    return subs

subscriptions = load_subscriptions()

def check_expirations_loop():
    while True:
        try:
            now = datetime.now()
            for email_addr, data in subscriptions.items():
                if data and data.get("active") and data.get("expiry"):
                    exp_date = datetime.fromisoformat(data["expiry"])
                    if 0 < (exp_date - now).days <= 3 and not data.get("notified_expiry"):
                        owner_id = data.get("owner_id")
                        if owner_id:
                            try:
                                bot.send_message(owner_id, f"⚠️ <b>تنبيه:</b> اشتراكك للبريد <code>{email_addr}</code> سينتهي خلال 3 أيام.", parse_mode="HTML")
                                data["notified_expiry"] = True
                                save_subscriptions(subscriptions)
                            except:
                                pass
        except:
            pass
        time.sleep(86400)

threading.Thread(target=check_expirations_loop, daemon=True).start()

def load_stats():
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
        except:
            pass
    return {"requests_count": 0, "top_emails": {}}

stats_data = load_stats()

def increment_request_stat(email_addr):
    if email_addr:
        stats_data["requests_count"] = stats_data.get("requests_count", 0) + 1
        top = stats_data.get("top_emails", {})
        top[email_addr] = top.get(email_addr, 0) + 1
        stats_data["top_emails"] = top
        try:
            with open(STATS_FILE, 'w', encoding='utf-8') as f:
                json.dump(stats_data, f, ensure_ascii=False, indent=4)
        except:
            pass

def is_subscription_active(email_addr, user_id):
    if not email_addr:
        return "not_found"
    email_lower = email_addr.strip().lower()
    if email_lower not in subscriptions:
        return "not_found"
    sub_data = subscriptions[email_lower]
    if not sub_data.get("active", True):
        return "inactive"
    expiry_str = sub_data.get("expiry")
    try:
        if expiry_str and datetime.now() > datetime.fromisoformat(expiry_str):
            sub_data["active"] = False
            sub_data["owner_id"] = None
            save_subscriptions(subscriptions)
            return "expired"
    except:
        pass
    owner_id = sub_data.get("owner_id")
    if ADMIN_IDS and user_id in ADMIN_IDS:
        return "active"
    if owner_id is None:
        sub_data["owner_id"] = user_id
        save_subscriptions(subscriptions)
        return "active"
    elif str(owner_id) != str(user_id):
        return "wrong_owner"
    return "active"

def create_banner_with_text(text, image_url, output_path="banner.jpg"):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content)).convert("RGB")
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("arial.ttf", 45)
            except:
                font = ImageFont.load_default()
            width, height = img.size
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_x = (width - text_width) // 2
            text_y = int(height * 0.52)
            draw.text((text_x, text_y), text, fill=(229, 9, 20), font=font)
            img.save(output_path)
            return output_path
    except:
        pass
    return None

def track_message(chat_id, message_id):
    if chat_id and message_id:
        if chat_id not in user_bot_messages:
            user_bot_messages[chat_id] = []
        user_bot_messages[chat_id].append(message_id)

def clean_previous_messages(chat_id):
    if chat_id and chat_id in user_bot_messages:
        for msg_id in user_bot_messages[chat_id]:
            try:
                bot.delete_message(chat_id, msg_id)
            except:
                pass
        user_bot_messages[chat_id] = []

def delete_message_later(chat_id, message_id, delay=45):
    time.sleep(delay)
    try:
        if chat_id and message_id:
            bot.delete_message(chat_id, message_id)
    except:
        pass

def connect_email(target_email):
    try:
        if not target_email:
            return None
        target_lower = target_email.strip().lower()
        if target_lower in YAHOO_ACCOUNTS:
            if target_lower.endswith("@aol.com"):
                mail = imaplib.IMAP4_SSL(IMAP_AOL_SERVER, 993)
            else:
                mail = imaplib.IMAP4_SSL(IMAP_YAHOO_SERVER, 993)
            mail.login(target_lower, YAHOO_ACCOUNTS[target_lower])
            return mail
        else:
            mail = imaplib.IMAP4_SSL(IMAP_SERVER)
            mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
            return mail
    except Exception as e:
        notify_admin_error(f"Failed IMAP login for {target_email}: {e}")
        return None

def extract_netflix_link(body, request_type):
    if not body:
        return None
    urls = re.findall(r'href=[\'"]?([^\'" >]+)', body)
    ignored_keywords = ["URL_LOGO", "privacy", "help", "terms", "unsub", "contact"]
    valid_urls = []
    for url in urls:
        url = url.replace('&amp;', '&')
        if "netflix.com" in url:
            if not any(ign in url for ign in ignored_keywords):
                valid_urls.append(url)
    for url in valid_urls:
        if request_type == "household" and ("update-primary-location" in url or "travel" in url or "verify" in url or "account" in url):
            return url
        elif request_type == "update_foyer" and ("update-primary-location" in url or "foyer" in url or "household" in url or "account" in url):
            return url
        elif request_type == "password" and ("password" in url or "reset" in url or "login" in url or "account" in url):
            return url
        elif request_type == "tv" and ("tv" in url or "device" in url or "signin" in url or "update-primary-location" in url or "account" in url):
            return url
    if valid_urls:
        return valid_urls[0]
    return None

def extract_netflix_code(body):
    if not body:
        return None
    code_match = re.search(r'(?:code|pin|identifier|رمز|كود)[\s:]*([0-9]{4})\b', body, re.IGNORECASE)
    if code_match:
        return code_match.group(1)
    matches = re.findall(r'\b\d{4}\b', body)
    for m in matches:
        if not (len(m) == 4 and m.startswith("202")):
            return m
    return None

def fetch_specific_code(target_email, request_type):
    mail = connect_email(target_email)
    if not mail:
        return "❌ Error connecting to the email server."
    try:
        mail.select("inbox")
        status, messages = mail.search(None, 'ALL')
        if status != "OK" or not messages or not messages[0].split():
            try:
                mail.logout()
            except:
                pass
            return "❌ No messages found in the inbox."
        message_numbers = messages[0].split()
        recent_messages = message_numbers[-25:]
        recent_messages.reverse()

        keywords = []
        if request_type == "household":
            keywords = ["foyer", "household", "regarder maintenant", "temporaire", "travel", "مؤقت"]
        elif request_type == "signin":
            keywords = ["identifier", "code", "sign-in", "login", "تسجيل الدخول", "connexion"]
        elif request_type == "tv":
            keywords = ["tv", "appareil", "device", "تلفزيون", "confirmer", "confirmation"]
        elif request_type == "update_foyer":
            keywords = ["mettre à jour", "update", "foyer", "household", "demande", "الفوكس", "ip"]
        elif request_type == "password":
            keywords = ["mot de passe", "password", "réinitialiser", "reset", "كلمة المرور"]
        else:
            keywords = ["netflix"]

        target_lower = target_email.strip().lower()
        now = datetime.now()

        for num in recent_messages:
            status, data = mail.fetch(num, "(RFC822)")
            if status != "OK" or not data:
                continue
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            date_header = msg.get("Date")
            if date_header:
                try:
                    msg_date = parsedate_to_datetime(date_header)
                    if msg_date and msg_date.tzinfo:
                        msg_date = msg_date.astimezone().replace(tzinfo=None)
                    if msg_date and (now - msg_date).total_seconds() > 900:
                        continue
                except:
                    pass

            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part:
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        if content_type in ["text/plain", "text/html"] and "attachment" not in content_disposition:
                            payload = part.get_payload(decode=True)
                            if payload:
                                body += payload.decode(errors='ignore') + "\n"
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    body = payload.decode(errors='ignore')

            body_lower = body.lower()
            msg_str_lower = str(msg).lower()
            is_target_email_match = (target_lower in body_lower) or (target_lower in msg_str_lower) or (target_lower in YAHOO_ACCOUNTS)

            if is_target_email_match:
                if any(k in body_lower or k in msg_str_lower for k in keywords):
                    if request_type == "signin":
                        code = extract_netflix_code(body)
                        if code:
                            try:
                                mail.logout()
                            except:
                                pass
                            increment_request_stat(target_email)
                            return f"🔑 <b>Votre code de connexion :</b> <code>{code}</code>\n\n📫 <b>Source : Boîte de réception</b>\n\n⏳ <i>Ce message sera supprimé automatiquement dans 45 secondes.</i>"
                    else:
                        link = extract_netflix_link(body, request_type)
                        if link:
                            try:
                                mail.logout()
                            except:
                                pass
                            increment_request_stat(target_email)
                            return f"🔗 <b>Lien de confirmation :</b>\n\n👉 <a href='{link}'>Cliquer ici pour ouvrir directement</a>\n\n⏳ <i>Ce message sera supprimé automatiquement dans 45 secondes.</i>"

        try:
            mail.logout()
        except:
            pass
        return f"⚠️ Aucun message récent (dans les 15 dernières minutes) n'a été trouvé pour l'e-mail <code>{target_email}</code>."
    except Exception as e:
        if mail:
            try:
                mail.logout()
            except:
                pass
        notify_admin_error(f"Error fetching email for {target_email}: {e}")
        return f"❌ Une erreur est survenue lors de la vérification des e-mails : {e}"

def get_main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("📧 إدخال بريد جديد"),
        KeyboardButton("📞 الدعم الفني")
    )
    return markup

def get_result_inline_markup():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📱 Contact WhatsApp", url=f"https://wa.me/{WHATSAPP_NUMBER.replace('+', '')}"),
        InlineKeyboardButton("🔄 Demander un autre service", callback_data="reset_session")
    )
    return markup

def show_service_options(chat_id, email_addr):
    if chat_id and email_addr:
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🏠 Foyer", callback_data="type_household"),
            InlineKeyboardButton("🔄 Mettre à jour Foyer", callback_data="type_update_foyer")
        )
        markup.add(
            InlineKeyboardButton("🔑 Code de connexion", callback_data="type_signin"),
            InlineKeyboardButton("📺 Lien TV", callback_data="type_tv")
        )
        markup.add(
            InlineKeyboardButton("🔒 Mot de passe", callback_data="type_password")
        )
        msg = bot.send_message(
            chat_id,
            f"📧 <b>E-mail sélectionné :</b> <code>{email_addr}</code>\n\nVeuillez choisir le type de service demandé :",
            reply_markup=markup,
            parse_mode="HTML"
        )
        track_message(chat_id, msg.message_id)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message and message.chat:
        chat_id = message.chat.id
        register_user(message)
        clean_previous_messages(chat_id)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("❓ Aide", callback_data="help"))
        markup.add(InlineKeyboardButton("📱 Contact WhatsApp", url=f"https://wa.me/{WHATSAPP_NUMBER.replace('+', '')}"))
        banner_path = create_banner_with_text("Zaki", NETFLIX_IMAGE_URL)
        welcome_text = (
            "<b>🔴 Zaki : Sponsoring officiel Netflix en Algérie et Afrique du Nord 🍿</b>\n\n"
            "📊 <b>Bienvenue sur le bot de récupération des codes et liens Netflix</b>\n\n"
            f"📱 <b>Numéro WhatsApp :</b> <code>{WHATSAPP_NUMBER}</code>\n\n"
            "Envoyez l'adresse e-mail enregistrée pour obtenir le lien d'accès temporaire ou le code de connexion."
        )
        bot.send_message(chat_id, "مرحباً بك! اختر من القائمة السفلى أو أدخل البريد الإلكتروني مباشرة:", reply_markup=get_main_keyboard())
        try:
            if banner_path and os.path.exists(banner_path):
                with open(banner_path, 'rb') as photo:
                    sent_msg = bot.send_photo(chat_id, photo, caption=welcome_text, reply_markup=markup, parse_mode="HTML")
            else:
                sent_msg = bot.send_photo(chat_id, NETFLIX_IMAGE_URL, caption=welcome_text, reply_markup=markup, parse_mode="HTML")
            track_message(chat_id, sent_msg.message_id)
        except:
            sent_msg = bot.send_message(chat_id, welcome_text, reply_markup=markup, parse_mode="HTML")
            track_message(chat_id, sent_msg.message_id)

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message and message.chat and message.from_user:
        chat_id = message.chat.id
        register_user(message)
        user_id = message.from_user.id
        if ADMIN_IDS and user_id not in ADMIN_IDS:
            return
        total_emails = len(subscriptions)
        active_emails = sum(1 for sub in subscriptions.values() if sub and sub.get("active", True))
        inactive_emails = total_emails - active_emails
        total_users = len(all_bot_users)
        admin_text = (
            "🛠 <b>لوحة تحكم المشرف المتقدمة (Admin Dashboard)</b>\n\n"
            f"📊 <b>إجمالي الإيميلات:</b> <code>{total_emails}</code>\n"
            f"🟢 <b>الإيميلات المشتغلة:</b> <code>{active_emails}</code>\n"
            f"🔴 <b>الإيميلات المتوقفة/المنتهية:</b> <code>{inactive_emails}</code>\n"
            f"👥 <b>المستخدمين المسجلين:</b> <code>{total_users}</code> | 🔄 <b>الطلبات الناجحة:</b> <code>{stats_data.get('requests_count', 0)}</code>"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📊 حالة النظام والإحصائيات", callback_data="admin_stats"))
        markup.add(InlineKeyboardButton("📧 عرض قائمة الإيميلات والمشتركين", callback_data="admin_list_emails"))
        markup.add(InlineKeyboardButton("📢 إذاعة رسالة مع صورة وتفاعلات", callback_data="admin_broadcast"))
        markup.add(InlineKeyboardButton("🗑 حذف آخر إذاعة", callback_data="admin_delete_broadcast"))
        sent_msg = bot.send_message(chat_id, admin_text, reply_markup=markup, parse_mode="HTML")
        track_message(chat_id, sent_msg.message_id)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if not message or not message.chat or not message.from_user or not message.text:
        return
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text.strip()

    if ADMIN_IDS and user_id in ADMIN_IDS:
        if text.startswith("+") and "@" in text:
            content = text[1:].strip()
            days = 31
            target_email = ""
            client_name_input = []

            words = content.split()
            for word in words:
                if "@" in word:
                    target_email = word.strip().lower()
                elif word.isdigit():
                    days = int(word)
                else:
                    client_name_input.append(word)

            client_name = " ".join(client_name_input) if client_name_input else "غير محدد"

            if target_email:
                start_dt = datetime.now()
                expiry_date = (start_dt + timedelta(days=days)).replace(hour=0, minute=0, second=0, microsecond=0)
                
                matched_user_id = "Unknown_ID"
                for uid, name in all_bot_users.items():
                    if name and client_name.lower() in name.lower():
                        matched_user_id = uid
                        break

                subscriptions[target_email] = {
                    "active": True,
                    "expiry": expiry_date.isoformat(),
                    "owner_id": matched_user_id if matched_user_id != "Unknown_ID" else None,
                    "client_name": client_name,
                    "notified_expiry": False
                }
                save_subscriptions(subscriptions)
                
                save_sale_to_client_file(
                    client_name, 
                    matched_user_id, 
                    target_email, 
                    days, 
                    start_dt, 
                    expiry_date
                )
                
                bot.send_message(
                    chat_id, 
                    f"✅ <b>تمت إضافة وتفعيل الحساب بنجاح وتوثيقه في ملف الزبون:</b>\n\n"
                    f"📧 <b>البريد:</b> <code>{target_email}</code>\n"
                    f"👤 <b>اسم الزبون:</b> <code>{client_name}</code>\n"
                    f"🆔 <b>مُعرف التليجرام:</b> <code>{matched_user_id}</code>\n"
                    f"⏳ <b>المدة:</b> <code>{days} يوماً</code>\n"
                    f"🔴 <b>ينتهي في:</b> <code>{expiry_date.strftime('%d/%m/%Y')}</code>", 
                    parse_mode="HTML"
                )
            else:
                bot.send_message(chat_id, "⚠️ صيغة غير صحيحة. مثال للاستخدام: <code>+31 example@gmail.com اسم_الزبون</code>", parse_mode="HTML")
            return

        elif text.startswith("!"):
            words = text[1:].strip().split()
            blocked_count = 0
            not_found_list = []

            for word in words:
                email_to_block = word.strip().lower()
                if "@" in email_to_block:
                    if email_to_block in subscriptions:
                        subscriptions[email_to_block]["active"] = False
                        blocked_count += 1
                    else:
                        not_found_list.append(email_to_block)
            
            if blocked_count > 0:
                save_subscriptions(subscriptions)
                msg_reply = f"⏸ <b>تم إيقاف {blocked_count} بريداً مؤقتاً بنجاح.</b>"
                if not_found_list:
                    msg_reply += f"\n\n⚠️ <b>لم يتم العثور عليها:</b> {', '.join(not_found_list)}"
                bot.send_message(chat_id, msg_reply, parse_mode="HTML")
            else:
                bot.send_message(chat_id, "⚠️ لم يتم العثور على أي بريد صحيح للإيقاف. تأكد من الصيغة (مثال: <code>!email1@gmail.com email2@gmail.com</code>)", parse_mode="HTML")
            return

    if text == "📧 إدخال بريد جديد":
        bot.send_message(chat_id, "الرجاء كتابة البريد الإلكتروني الخاص بك الآن:")
        return
    elif text == "📞 الدعم الفني":
        bot.send_message(chat_id, f"للتواصل مع الدعم الفني، يرجى مراسلتنا عبر الرابط التالي:\nhttps://wa.me/{WHATSAPP_NUMBER.replace('+', '')}")
        return

    email_text = text.lower()
    if "@" in email_text:
        register_user(message)
        status_check = is_subscription_active(email_text, user_id)
        if status_check == "not_found":
            bot.send_message(chat_id, "❌ عذراً، هذا البريد الإلكتروني غير مسجل في قائمة الحسابات المفعلة.")
        elif status_check == "inactive" or status_check == "expired":
            bot.send_message(chat_id, "❌ عذراً، انتهت صلاحية اشتراك هذا البريد أو تم إيقافه.")
        elif status_check == "wrong_owner":
            bot.send_message(chat_id, "❌ هذا البريد مرتبط بحساب مستخدم آخر ولا يمكنك استخدامه.")
        elif status_check == "active":
            user_selected_emails[chat_id] = email_text
            show_service_options(chat_id, email_text)
    else:
        bot.send_message(chat_id, "⚠️ يرجى إرسال بريد إلكتروني صالح أو استخدام الأزرار في القائمة.")

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()