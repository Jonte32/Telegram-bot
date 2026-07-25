"""
translations.py
All customer-facing UI text in 4 languages, plus the language picker metadata.
Admin commands stay in English (admins are the shop owner, not customers).

Add a new language by adding an entry to LANGUAGES and a matching dict to
TRANSLATIONS with the same keys as the "en" block.
"""

LANGUAGES = {
    "en": {"name": "English", "flag": "🇬🇧"},
    "zh": {"name": "中文", "flag": "🇨🇳"},
    "ar": {"name": "العربية", "flag": "🇸🇦"},
    "vi": {"name": "Tiếng Việt", "flag": "🇻🇳"},
}

TRANSLATIONS = {
    "en": {
        "welcome": "👋 Welcome to the shop!",
        "choose_language": "🌐 Please choose your language:",
        "language_set": "Language set to {flag} {name}.",
        "main_menu": "What would you like to do?",
        "btn_catalog": "📋 Catalog",
        "btn_cart": "🛒 Cart",
        "btn_help": "❓ Help",
        "btn_language": "🌐 Language",
        "choose_category": "Choose a category:",
        "no_products": "No products yet — check back soon!",
        "no_products_category": "No products in this category right now.",
        "added_to_cart": "Added {name} to your cart ✅",
        "item_unavailable": "Sorry, that item is no longer available.",
        "cart_empty": "Your cart is empty.",
        "cart_total": "Total",
        "btn_checkout": "✅ Checkout",
        "btn_clear_cart": "🗑 Clear cart",
        "cart_cleared": "Your cart is empty.",
        "checkout_empty": "Your cart is empty — add something from the catalog first.",
        "ask_name": "Great! What name should we put on the order?",
        "ask_phone": "What's the best phone number to reach you?",
        "ask_address": "And what's the delivery address?",
        "confirm_header": "Please confirm your order:",
        "label_name": "Name",
        "label_phone": "Phone",
        "label_address": "Address",
        "btn_confirm": "✅ Confirm",
        "btn_cancel": "❌ Cancel",
        "order_cancelled": "Order cancelled.",
        "order_placed": "🎉 Order #{order_id} placed! We'll be in touch shortly to confirm delivery.",
        "checkout_cancelled_cmd": "Checkout cancelled.",
        "help_customer": (
            "/start - main menu\n"
            "/catalog - browse products\n"
            "/cart - view your cart\n"
            "/language - change language\n"
            "/help - show this message"
        ),
    },
    "zh": {
        "welcome": "👋 欢迎光临本店！",
        "choose_language": "🌐 请选择您的语言：",
        "language_set": "语言已设置为 {flag} {name}。",
        "main_menu": "您想做什么？",
        "btn_catalog": "📋 商品目录",
        "btn_cart": "🛒 购物车",
        "btn_help": "❓ 帮助",
        "btn_language": "🌐 语言",
        "choose_category": "请选择分类：",
        "no_products": "暂无商品，请稍后再来看看！",
        "no_products_category": "该分类暂无商品。",
        "added_to_cart": "已将 {name} 加入购物车 ✅",
        "item_unavailable": "抱歉，该商品已下架。",
        "cart_empty": "您的购物车是空的。",
        "cart_total": "总计",
        "btn_checkout": "✅ 结账",
        "btn_clear_cart": "🗑 清空购物车",
        "cart_cleared": "购物车已清空。",
        "checkout_empty": "您的购物车是空的，请先从商品目录中添加商品。",
        "ask_name": "好的！订单应填写什么姓名？",
        "ask_phone": "请提供您的联系电话。",
        "ask_address": "请提供收货地址。",
        "confirm_header": "请确认您的订单：",
        "label_name": "姓名",
        "label_phone": "电话",
        "label_address": "地址",
        "btn_confirm": "✅ 确认",
        "btn_cancel": "❌ 取消",
        "order_cancelled": "订单已取消。",
        "order_placed": "🎉 订单 #{order_id} 已提交！我们会尽快与您联系确认送货事宜。",
        "checkout_cancelled_cmd": "结账已取消。",
        "help_customer": (
            "/start - 主菜单\n"
            "/catalog - 浏览商品\n"
            "/cart - 查看购物车\n"
            "/language - 更改语言\n"
            "/help - 显示此消息"
        ),
    },
    "ar": {
        "welcome": "👋 أهلاً بك في المتجر!",
        "choose_language": "🌐 الرجاء اختيار لغتك:",
        "language_set": "تم تعيين اللغة إلى {flag} {name}.",
        "main_menu": "ماذا تريد أن تفعل؟",
        "btn_catalog": "📋 الكتالوج",
        "btn_cart": "🛒 سلة التسوق",
        "btn_help": "❓ المساعدة",
        "btn_language": "🌐 اللغة",
        "choose_category": "اختر فئة:",
        "no_products": "لا توجد منتجات بعد — تحقق مرة أخرى قريباً!",
        "no_products_category": "لا توجد منتجات في هذه الفئة حالياً.",
        "added_to_cart": "تمت إضافة {name} إلى سلتك ✅",
        "item_unavailable": "عذراً، هذا المنتج لم يعد متوفراً.",
        "cart_empty": "سلتك فارغة.",
        "cart_total": "الإجمالي",
        "btn_checkout": "✅ إتمام الشراء",
        "btn_clear_cart": "🗑 إفراغ السلة",
        "cart_cleared": "سلتك فارغة.",
        "checkout_empty": "سلتك فارغة — أضف منتجاً من الكتالوج أولاً.",
        "ask_name": "رائع! ما الاسم الذي نضعه في الطلب؟",
        "ask_phone": "ما هو أفضل رقم هاتف للتواصل معك؟",
        "ask_address": "وما هو عنوان التوصيل؟",
        "confirm_header": "يرجى تأكيد طلبك:",
        "label_name": "الاسم",
        "label_phone": "الهاتف",
        "label_address": "العنوان",
        "btn_confirm": "✅ تأكيد",
        "btn_cancel": "❌ إلغاء",
        "order_cancelled": "تم إلغاء الطلب.",
        "order_placed": "🎉 تم تقديم الطلب رقم #{order_id}! سنتواصل معك قريباً لتأكيد التوصيل.",
        "checkout_cancelled_cmd": "تم إلغاء عملية الشراء.",
        "help_customer": (
            "/start - القائمة الرئيسية\n"
            "/catalog - تصفح المنتجات\n"
            "/cart - عرض السلة\n"
            "/language - تغيير اللغة\n"
            "/help - عرض هذه الرسالة"
        ),
    },
    "vi": {
        "welcome": "👋 Chào mừng bạn đến với cửa hàng!",
        "choose_language": "🌐 Vui lòng chọn ngôn ngữ của bạn:",
        "language_set": "Đã đặt ngôn ngữ thành {flag} {name}.",
        "main_menu": "Bạn muốn làm gì?",
        "btn_catalog": "📋 Danh mục sản phẩm",
        "btn_cart": "🛒 Giỏ hàng",
        "btn_help": "❓ Trợ giúp",
        "btn_language": "🌐 Ngôn ngữ",
        "choose_category": "Chọn danh mục:",
        "no_products": "Chưa có sản phẩm nào — vui lòng quay lại sau!",
        "no_products_category": "Hiện chưa có sản phẩm trong danh mục này.",
        "added_to_cart": "Đã thêm {name} vào giỏ hàng ✅",
        "item_unavailable": "Xin lỗi, sản phẩm này không còn nữa.",
        "cart_empty": "Giỏ hàng của bạn đang trống.",
        "cart_total": "Tổng cộng",
        "btn_checkout": "✅ Thanh toán",
        "btn_clear_cart": "🗑 Xóa giỏ hàng",
        "cart_cleared": "Giỏ hàng của bạn đang trống.",
        "checkout_empty": "Giỏ hàng của bạn đang trống — hãy thêm sản phẩm từ danh mục trước.",
        "ask_name": "Tuyệt! Chúng tôi nên ghi tên gì cho đơn hàng?",
        "ask_phone": "Số điện thoại liên hệ tốt nhất là gì?",
        "ask_address": "Địa chỉ giao hàng là gì?",
        "confirm_header": "Vui lòng xác nhận đơn hàng của bạn:",
        "label_name": "Tên",
        "label_phone": "Điện thoại",
        "label_address": "Địa chỉ",
        "btn_confirm": "✅ Xác nhận",
        "btn_cancel": "❌ Hủy",
        "order_cancelled": "Đơn hàng đã bị hủy.",
        "order_placed": "🎉 Đơn hàng #{order_id} đã được đặt! Chúng tôi sẽ liên hệ sớm để xác nhận giao hàng.",
        "checkout_cancelled_cmd": "Đã hủy thanh toán.",
        "help_customer": (
            "/start - menu chính\n"
            "/catalog - xem sản phẩm\n"
            "/cart - xem giỏ hàng\n"
            "/language - đổi ngôn ngữ\n"
            "/help - hiện trợ giúp này"
        ),
    },
}


def t(key: str, lang: str = "en", **kwargs) -> str:
    """Look up a translated string, falling back to English, then to the key itself."""
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    text = lang_dict.get(key, TRANSLATIONS["en"].get(key, key))
    if kwargs:
        text = text.format(**kwargs)
    return text
