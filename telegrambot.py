import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# 1. ඔයාගේ බොට් ටෝකන් එක
BOT_TOKEN = "8100648049:AAHBaQOx2z8NJVCLg_EtNXdXILL6puI8dv4"

# 2. ඔයාගේ Chat ID එක
ADMIN_ID = 7194717029 

# 3. ඔයාගේ VIP චැනල් එකේ Invite Link එක
VIP_LINK = "https://t.me/+G6Tt8c51EC5mNzJl"

bot = telebot.TeleBot(BOT_TOKEN)

# යටින් දිගටම පේන බොත්තම හදන කොටස
def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_details = KeyboardButton("🏦 බැංකු විස්තර බලන්න")
    markup.add(btn_details)
    return markup

# User /start යැව්වාම හරි, "බැංකු විස්තර බලන්න" බොත්තම එබුවාම හරි යන මැසේජ් එක
@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda message: message.text == "🏦 බැංකු විස්තර බලන්න")
def send_welcome(message):
    welcome_text = """
හායි! අපේ VIP Channel එකට එකතු වෙන්න කැමති නම්, පහත ගිණුමට මුදල් ගෙවන්න.

**බැංකු විස්තර:**
බැංකුව: Bank of Ceylon
ගිණුම් අංකය: 0088397225

මුදල් ගෙවලා, ඒකෙ රිසිට් එක (Slip එක) ෆොටෝ එකක් විදියට මෙතනට එවන්න.
    """
    bot.reply_to(message, welcome_text, reply_markup=get_main_menu())

# User Slip එක එව්වාම Admin ට බට්න් එක්ක යන විදිය
@bot.message_handler(content_types=['photo'])
def handle_payment_slip(message):
    user_id = message.chat.id
    user_name = message.from_user.first_name
    file_id = message.photo[-1].file_id # ෆොටෝ එක ගන්නවා

    # Admin ට පේන බොත්තම් දෙක හදනවා
    markup = InlineKeyboardMarkup()
    btn_approve = InlineKeyboardButton("✅ Approve කරන්න", callback_data=f"approve_{user_id}")
    btn_reject = InlineKeyboardButton("❌ Reject කරන්න", callback_data=f"reject_{user_id}")
    markup.add(btn_approve, btn_reject)

    # Admin ට ෆොටෝ එක යවනවා
    bot.send_photo(
        ADMIN_ID, 
        file_id, 
        caption=f"නව ගෙවීමක්!\nඑව්වේ: {user_name}\nID එක: {user_id}", 
        reply_markup=markup
    )
    
    # User ට යවන මැසේජ් එක
    bot.reply_to(message, "ඔයාගේ Payment Slip එක අපිට ලැබුණා. Admin check කරලා ලින්ක් එක එවාවි. ටිකක් රැඳී සිටින්න.")

# Admin බොත්තම් එබුවාම වෙන දේ
@bot.callback_query_handler(func=lambda call: True)
def handle_admin_action(call):
    # මේක ඔබන්නේ Admin ද කියලා බලනවා
    if call.message.chat.id == ADMIN_ID:
        action, user_id = call.data.split('_')
        user_id = int(user_id)

        if action == "approve":
            # Approve කරාම User ට ලින්ක් එක යනවා
            bot.send_message(user_id, f"සුබ පැතුම්! ඔයාගේ පේමන්ට් එක සාර්ථකයි. 🎉\nමේ තියෙන්නේ VIP චැනල් එකේ ලින්ක් එක: {VIP_LINK}")
            bot.answer_callback_query(call.id, "ඔයා මේක Approve කරා!")
            # Admin ගේ පැත්තේ මැසේජ් එක වෙනස් වෙනවා
            bot.edit_message_caption(caption="✅ මේ පේමන්ට් එක Approve කරා.", chat_id=ADMIN_ID, message_id=call.message.message_id)
            
        elif action == "reject":
            # Reject කරාම User ට යන මැසේජ් එක
            bot.send_message(user_id, "සමාවෙන්න, ඔයාගේ පේමන්ට් එක Reject කරලා තියෙන්නේ. ගැටලුවක් ඇත්නම් කරුණාකරලා Admin ව සම්බන්ධ කරගන්න.")
            bot.answer_callback_query(call.id, "ඔයා මේක Reject කරා!")
            # Admin ගේ පැත්තේ මැසේජ් එක වෙනස් වෙනවා
            bot.edit_message_caption(caption="❌ මේ පේමන්ට් එක Reject කරා.", chat_id=ADMIN_ID, message_id=call.message.message_id)

print("Bot වැඩ කරනවා...")
bot.infinity_polling()