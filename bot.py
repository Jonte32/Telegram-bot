"""
bot.py
A Telegram sales bot: customers browse a product catalog by category,
add items to a cart, and check out by leaving their name/phone/address.
Admins get notified of every new order and can manage products via chat commands.

Run locally:
    python bot.py

Requires a .env file (see .env.example) with:
    BOT_TOKEN=123456:ABC-your-telegram-bot-token
    ADMIN_CHAT_ID=123456789
"""
import os
import logging
import json
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

import database as db

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")  # your personal Telegram chat id, as a string

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states for checkout
ASK_NAME, ASK_PHONE, ASK_ADDRESS, CONFIRM = range(4)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_cart(context: ContextTypes.DEFAULT_TYPE):
    """Cart is stored per-user in bot memory (user_data). Structure: {product_id: qty}"""
    return context.user_data.setdefault("cart", {})


def cart_total(cart):
    total = 0.0
    for product_id, qty in cart.items():
        product = db.get_product(product_id)
        if product:
            total += product["price"] * qty
    return total


def format_cart(cart):
    if not cart:
        return "Your cart is empty."
    lines = []
    for product_id, qty in cart.items():
        product = db.get_product(product_id)
        if product:
            lines.append(f"• {product['name']} x{qty} — {product['price'] * qty:.2f}")
    lines.append(f"\nTotal: {cart_total(cart):.2f}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Customer-facing handlers
# ---------------------------------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 Welcome to the shop!\n\n"
        "Browse products with /catalog, view your cart with /cart, "
        "and check out whenever you're ready."
    )
    await update.message.reply_text(text)


async def catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    categories = db.get_categories()
    if not categories:
        await update.message.reply_text("No products yet — check back soon!")
        return

    buttons = [
        [InlineKeyboardButton(cat["name"], callback_data=f"cat:{cat['id']}")]
        for cat in categories
    ]
    await update.message.reply_text(
        "Choose a category:", reply_markup=InlineKeyboardMarkup(buttons)
    )


async def show_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category_id = int(query.data.split(":")[1])
    products = db.get_products_by_category(category_id)

    if not products:
        await query.edit_message_text("No products in this category right now.")
        return

    for product in products:
        caption = f"*{product['name']}*\n{product['description'] or ''}\n\n💰 {product['price']:.2f}"
        buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton("➕ Add to cart", callback_data=f"add:{product['id']}")]]
        )
        if product["image_url"]:
            await context.bot.send_photo(
                chat_id=query.message.chat_id,
                photo=product["image_url"],
                caption=caption,
                parse_mode="Markdown",
                reply_markup=buttons,
            )
        else:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=caption,
                parse_mode="Markdown",
                reply_markup=buttons,
            )


async def add_to_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    product_id = int(query.data.split(":")[1])
    product = db.get_product(product_id)
    if not product:
        await query.answer("Sorry, that item is no longer available.", show_alert=True)
        return

    cart = get_cart(context)
    cart[product_id] = cart.get(product_id, 0) + 1
    await query.answer(f"Added {product['name']} to your cart ✅")


async def view_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cart = get_cart(context)
    text = format_cart(cart)
    if cart:
        buttons = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("✅ Checkout", callback_data="checkout")],
                [InlineKeyboardButton("🗑 Clear cart", callback_data="clear_cart")],
            ]
        )
        await update.message.reply_text(text, reply_markup=buttons)
    else:
        await update.message.reply_text(text)


async def clear_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    context.user_data["cart"] = {}
    await query.answer("Cart cleared.")
    await query.edit_message_text("Your cart is empty.")


# ---------------------------------------------------------------------------
# Checkout conversation
# ---------------------------------------------------------------------------

async def checkout_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cart = get_cart(context)
    if not cart:
        await query.edit_message_text("Your cart is empty — add something from /catalog first.")
        return ConversationHandler.END

    await query.edit_message_text("Great! What name should we put on the order?")
    return ASK_NAME


async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["checkout_name"] = update.message.text
    await update.message.reply_text("What's the best phone number to reach you?")
    return ASK_PHONE


async def ask_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["checkout_phone"] = update.message.text
    await update.message.reply_text("And what's the delivery address?")
    return ASK_ADDRESS


async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["checkout_address"] = update.message.text
    cart = get_cart(context)
    summary = format_cart(cart)
    text = (
        f"Please confirm your order:\n\n"
        f"Name: {context.user_data['checkout_name']}\n"
        f"Phone: {context.user_data['checkout_phone']}\n"
        f"Address: {context.user_data['checkout_address']}\n\n"
        f"{summary}"
    )
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("✅ Confirm", callback_data="confirm_order")],
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel_order")],
        ]
    )
    await update.message.reply_text(text, reply_markup=buttons)
    return CONFIRM


async def finalize_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "cancel_order":
        await query.edit_message_text("Order cancelled.")
        return ConversationHandler.END

    cart = get_cart(context)
    items = []
    for product_id, qty in cart.items():
        product = db.get_product(product_id)
        if product:
            items.append({"name": product["name"], "qty": qty, "price": product["price"]})

    total = cart_total(cart)
    user = update.effective_user
    order_id = db.create_order(
        user_id=user.id,
        username=user.username or "",
        full_name=context.user_data["checkout_name"],
        phone=context.user_data["checkout_phone"],
        address=context.user_data["checkout_address"],
        items=items,
        total=total,
    )

    await query.edit_message_text(
        f"🎉 Order #{order_id} placed! We'll be in touch shortly to confirm delivery."
    )

    context.user_data["cart"] = {}

    if ADMIN_CHAT_ID:
        items_text = "\n".join(f"• {i['name']} x{i['qty']}" for i in items)
        admin_text = (
            f"🛒 New order #{order_id}\n"
            f"From: {context.user_data['checkout_name']} (@{user.username or 'no username'})\n"
            f"Phone: {context.user_data['checkout_phone']}\n"
            f"Address: {context.user_data['checkout_address']}\n\n"
            f"{items_text}\n\nTotal: {total:.2f}"
        )
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_text)

    return ConversationHandler.END


async def cancel_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Checkout cancelled.")
    return ConversationHandler.END


# ---------------------------------------------------------------------------
# Admin commands
# ---------------------------------------------------------------------------

def is_admin(update: Update):
    return ADMIN_CHAT_ID and str(update.effective_user.id) == str(ADMIN_CHAT_ID)


async def add_product_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Usage: /addproduct Name | Description | Price | ImageURL | Category"""
    if not is_admin(update):
        await update.message.reply_text("You're not authorized to do that.")
        return

    text = update.message.text.partition(" ")[2]
    parts = [p.strip() for p in text.split("|")]
    if len(parts) != 5:
        await update.message.reply_text(
            "Usage:\n/addproduct Name | Description | Price | ImageURL | Category\n\n"
            "Example:\n/addproduct Blue Mug | Ceramic 350ml | 12.50 | https://example.com/mug.jpg | Kitchen"
        )
        return

    name, description, price, image_url, category = parts
    try:
        price = float(price)
    except ValueError:
        await update.message.reply_text("Price must be a number.")
        return

    db.add_product(name, description, price, image_url or None, category)
    await update.message.reply_text(f"Added '{name}' to category '{category}'.")


async def list_products_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        await update.message.reply_text("You're not authorized to do that.")
        return
    products = db.get_all_products()
    if not products:
        await update.message.reply_text("No products yet.")
        return
    lines = [f"#{p['id']} {p['name']} — {p['price']:.2f}" for p in products]
    await update.message.reply_text("\n".join(lines))


async def remove_product_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Usage: /removeproduct <id>"""
    if not is_admin(update):
        await update.message.reply_text("You're not authorized to do that.")
        return
    args = context.args
    if not args or not args[0].isdigit():
        await update.message.reply_text("Usage: /removeproduct <id>")
        return
    db.remove_product(int(args[0]))
    await update.message.reply_text("Removed.")


async def orders_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        await update.message.reply_text("You're not authorized to do that.")
        return
    orders = db.get_recent_orders()
    if not orders:
        await update.message.reply_text("No orders yet.")
        return
    lines = []
    for o in orders:
        lines.append(f"#{o['id']} {o['full_name']} — {o['total']:.2f} — {o['status']}")
    await update.message.reply_text("\n".join(lines))


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "/start - welcome message\n"
        "/catalog - browse products\n"
        "/cart - view your cart\n"
    )
    if is_admin(update):
        text += (
            "\nAdmin:\n"
            "/addproduct Name | Description | Price | ImageURL | Category\n"
            "/listproducts - list all products with IDs\n"
            "/removeproduct <id>\n"
            "/orders - view recent orders\n"
        )
    await update.message.reply_text(text)


# ---------------------------------------------------------------------------
# App wiring
# ---------------------------------------------------------------------------

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set. Add it to your .env file.")

    db.init_db()

    app = Application.builder().token(BOT_TOKEN).build()

    checkout_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(checkout_start, pattern="^checkout$")],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_phone)],
            ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_address)],
            ASK_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_order)],
            CONFIRM: [CallbackQueryHandler(finalize_order, pattern="^(confirm_order|cancel_order)$")],
        },
        fallbacks=[CommandHandler("cancel", cancel_checkout)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("catalog", catalog))
    app.add_handler(CommandHandler("cart", view_cart))
    app.add_handler(CommandHandler("addproduct", add_product_cmd))
    app.add_handler(CommandHandler("listproducts", list_products_cmd))
    app.add_handler(CommandHandler("removeproduct", remove_product_cmd))
    app.add_handler(CommandHandler("orders", orders_cmd))

    app.add_handler(checkout_conv)
    app.add_handler(CallbackQueryHandler(show_category, pattern="^cat:"))
    app.add_handler(CallbackQueryHandler(add_to_cart, pattern="^add:"))
    app.add_handler(CallbackQueryHandler(clear_cart, pattern="^clear_cart$"))

    logger.info("Bot starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
