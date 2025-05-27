from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters, ConversationHandler
)

# Global adminlar ro'yxati
ADMINS = [6290847497]
ADD_ADMIN, ADD_PRODUCT_NAME, ADD_PRODUCT_PRICE = range(3)

MAHSULOTLAR = []  # Bu ro‘yxatga mahsulotlar saqlanadi

def admin_check(user_id):
    return user_id in ADMINS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    tugmalar = [["📦 Mahsulotlar", "📝 Buyurtma berish"],
                ["📍 Manzil", "📞 Bog‘lanish", "🔩 Santexnika", "💡Dusel"]]

    if admin_check(user_id):
        tugmalar.append(["⚙️ Admin panel"]) 

    markup = ReplyKeyboardMarkup(tugmalar, resize_keyboard=True)
    await update.message.reply_text(
        "Assalomu alaykum! Qurilish Market botiga xush kelibsiz.",
        reply_markup=markup
    )

# Tugmalar
async def tugma_javobi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    if text == "📦 Mahsulotlar":
        javob = "📦 Mavjud mahsulotlar:\n\n"
        if MAHSULOTLAR:
            for m in MAHSULOTLAR:
                javob += f"🛒 {m['nomi']} – {m['narx']} so‘m\n"
        else:
            javob += "Mahsulotlar yo‘q."

        await update.message.reply_text(javob)

    elif text == "⚙️ Admin panel" and admin_check(user_id):
        markup = ReplyKeyboardMarkup(
            [["➕ Admin qo‘shish"], ["➕ Mahsulot qo‘shish"], ["⬅️ Orqaga"]],
            resize_keyboard=True
        )
        await update.message.reply_text("Admin paneliga xush kelibsiz:", reply_markup=markup)

    elif text == "⬅️ Orqaga":
        await start(update, context)

    elif text == "📝 Buyurtma berish":
        await update.message.reply_text("Telefon raqamingiz va mahsulot nomini yozing, siz bilan bog‘lanamiz.")

    elif text == "📍 Manzil":
        await update.message.reply_text("📍 Manzil: Marg‘ilon, Toshloq tumani, VARZAK FAYZ 777")

    elif text == "📞 Bog‘lanish":
        await update.message.reply_text("☎️ +998 91 283 81 43")

    elif text == "🔩 Santexnika":
        await update.message.reply_text(
            "🔩 Santexnika:\n\n"
            "Atvot 20 – 1000 so‘m\n"
            "Atvot 25 – 2000 so‘m\n"
            "Pol Atvot 20 – 1000 so‘m"
        )

    elif text == "💡Dusel":
        await update.message.reply_text(
            "Dusel mahsulotlari:\n\n"
            "Dusel lampa 7W - 7000 so‘m\n"
            "Dusel lampa 10W - 10 000 so‘m\n"
            "Dusel lampa 12W - 12 000 so‘m\n"
            "Dusel lampa 15W - 15 000 so‘m\n"
            "Dusel lampa 18W - 18 000 so‘m\n"
            "Dusel lampa 20W - 20 000 so‘m\n"
            "Dusel lampa 30W - 35 000 so‘m\n"
            "Dusel lampa 40W - 55 000 so‘m\n"
            "Dusel lampa 50W - 60 000 so‘m"
        )

# --- Admin funksiyalar ---

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not admin_check(update.message.from_user.id):
        await update.message.reply_text("⛔ Sizda ruxsat yo‘q.")
        return ConversationHandler.END

    await update.message.reply_text("🆔 Yangi adminning ID raqamini yuboring:")
    return ADD_ADMIN

async def add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        new_admin_id = int(update.message.text)
        if new_admin_id not in ADMINS:
            ADMINS.append(new_admin_id)
            await update.message.reply_text(f"✅ Admin qo‘shildi: {new_admin_id}")
        else:
            await update.message.reply_text("⚠️ Bu foydalanuvchi allaqachon admin.")
    except ValueError:
        await update.message.reply_text("❌ Iltimos, faqat ID raqamini yuboring.")
    return ConversationHandler.END

# --- Mahsulot qo‘shish funksiyasi ---

async def start_add_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛒 Mahsulot nomini kiriting:")
    return ADD_PRODUCT_NAME

async def product_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['mahsulot_nomi'] = update.message.text
    await update.message.reply_text("💰 Narxini kiriting (faqat son):")
    return ADD_PRODUCT_PRICE

async def product_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        narx = int(update.message.text)
        nomi = context.user_data['mahsulot_nomi']
        MAHSULOTLAR.append({"nomi": nomi, "narx": narx})
        await update.message.reply_text(f"✅ Mahsulot qo‘shildi: {nomi} – {narx} so‘m")
    except ValueError:
        await update.message.reply_text("❌ Narx noto‘g‘ri. Faqat raqam yuboring.")
    return ConversationHandler.END

# --- Botni ishga tushurish ---

app = ApplicationBuilder().token("8068283579:AAE8mEogFjOPIdxUnQcQwizznZRjvrPsW2c").build()

# Handlerlar
app.add_handler(CommandHandler("start", start))

admin_conv = ConversationHandler(
    entry_points=[
        MessageHandler(filters.TEXT & filters.Regex("^➕ Admin qo‘shish$"), admin_panel)
    ],
    states={ADD_ADMIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_admin)]},
    fallbacks=[MessageHandler(filters.TEXT & filters.Regex("^⬅️ Orqaga$"), tugma_javobi)]
)

product_conv = ConversationHandler(
    entry_points=[
        MessageHandler(filters.TEXT & filters.Regex("^➕ Mahsulot qo‘shish$"), start_add_product)
    ],
    states={
        ADD_PRODUCT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, product_name)],
        ADD_PRODUCT_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, product_price)],
    },
    fallbacks=[MessageHandler(filters.TEXT & filters.Regex("^⬅️ Orqaga$"), tugma_javobi)]
)

tugma_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, tugma_javobi)

# Qo‘shish
app.add_handler(admin_conv)
app.add_handler(product_conv)
app.add_handler(tugma_handler)

app.run_polling()
