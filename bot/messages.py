BOT_START_COMMAND = """سلام سیدِ عزیز!👋
به کمک دکمه های زیر میتونی از ربات استفاده کنی:
"""

MAIN_MENU_OPTIONS = [
    ("🔘 مدیریت گروه ها", "manage_groups::1"),
    ("🔘 مدیریت لینک دونی ها", "manage_link_storages::1"),
    ("🔘 مدیریت بنر ها", "manage_banners"),
    ("🔘 مدیریت منشی خودکار", "manage_message_sec")    
]
BOT_STATUS_OPTION = ["📌 مدیریت کاربر", "manage_bot"]
DEVELOPER_BUTTON = ['💻 نوشته شده توسط: @hawar', 'https://t.me/hawar']
AUTO_JOIN_SWITCH = ["خاموش / روشن جوین خودکار", "switch_auto_join_status"]
BOT_STATUS_SWITCH = ["خاموش / روشن ربات", "switch_bot_status"]
ON_EMOJI = "🟢"
OFF_EMOJI = "🔴"

RETURN_HOME_OPTION = ["🏠 بازگشت به منوی اصلی", "return_to_main_menu"]

MANAGE_BOT_OPTIONS = [
    ("⏰ تغییر روتین ارسال بنر در گروه ها", "update_bot_send_every_mins")
]

BOT_OPTIONS_REPORTS = """<b>اطلاعات ربات:</b>
🔻 آیدی ربات: {cliend_id}
🔻 یوزرنیم ربات: {client_username}
🔻 اسم اکانت ربات: {client_full_name}
🔻 وضعیت آنلاین بودن:{online_status}
🔻 جوین خودکار: {auto_join_status}
🔻 ارسال پیام(هر دقیقه یکبار): {every_mins}
—————————————————————————
💻 نوشته شده توسط: @hawar
"""

UPDATE_EVERY_MINS_TEXT = "🔹 روتین ارسال پیام جدید را وارد کنید: (پیشنهاد میشود که بالای 5 دقیقه یکبار باشد)"
RETURN_HOME_KEYBOARD = "🏠 بازگشت به منوی اصلی"
UPDATED = "✅ تغییرات جدید اعمال شد!"

AUTO_SEC_OPTIONS = [
    ("✍️ تغییر پیام خودکار", "change_auto_message"),
]
AUTO_SEC_STATUS_SWITCH = ["خاموش / روشن منشی خودکار", "switch_auto_sec_status"]
AUTO_SEC_REPORT = """<b>گزارش عمل کرد منشی خودکار</b>
🔻 تعداد پیام های موجود برای منشی: {count_message_secs}
🔻 پیام خودکار فعلی: 
{response_text}
🔻 تعداد کاربران جواب داده شده: {pv_count}
————————————————————————-
💻 نوشته شده توسط: @hawar
"""
UPDATE_MESSAGE_SEC_TEXT = "🔹 پیام جدید منشی را وارد کنید:"
NOT_IMPLEMENTED_MESSAGE = "🔄 این قابلیت هنوز به ربات اضافه نشده است! میتوانید به سازنده ربات پیام دهید."

MANAGE_ALL_BANNERS_REPORT = """<b>مدیریت بنرها:</b>
🔻 تعداد بنر های ثبت شده: {count_banners}
🔻 تعداد کل بنر های ارسال شده: {count_all_sent_banners}

➖ با کلیک روی هر بنر میتوانید اون رو مدیریت کنید:
————————————————————————-
💻 نوشته شده توسط: @hawar"""
ADD_NEW_BANNER_BUTTON = ['➕ اضافه کردن بنر جدید', 'create_new_banner']
CREATE_BANNER_TITLE_INPUT = "✏️ اسم بنر جدید را وارد کنید:"
CREAT_BANNER_CONTENT_INPUT = "✏️ حالا متن بنر را وارد کنید: (از لینک استفاده نکنید! بیشتر گروه ها ضد لینک دارن.)"

ERROR_MESSAGE = "شت:/ یه اروری رخ داد!"
MANAGE_BANNER_REPORT = """<b>مدیریت بنر:</b>
🔻 اسم بنر: {banner_title}
🔻 متن بنر: 
{banner_text}
🔻 تعداد ارسال: {sent_count}
————————————————————————-
💻 نوشته شده توسط: @hawar
"""
DELETE_BANNER_OPTION = ['❌ حذف بنر', "delete_banner::{banner_id}"]
MANAGE_ALL_LINK_CHANNELS_REPORT = """<b>مدیریت چنل ها:</b>
🔻 تعداد چنل ها: {channel_count}
➖ با کلیک روی هر چنل میتوانید اون رو مدیریت کنید:
————————————————————————-
💻 نوشته شده توسط: @hawar"""

CHANNELS_LINK_NEXT_PAGE_BUTTON = ['⏩ صفحه بعد', "manage_link_storages::{page}"]
CHANNELS_LINK_PER_PAGE_BUTTON = ['⏮️ صفحه قبل', "manage_link_storages::{page}"]
MANAGE_LINK_CHANNEL_REPORT = """<b>مدیریت چنل :</b>
🔻 آیدی چنل: {channel_id}
🔻 یوزرنیم چنل: @{channel_username}
🔻 اسم چنل: {channel_name}
————————————————————————-
💻 نوشته شده توسط: @hawar
"""
DELETE_LINK_CHANNEL_OPTION = ['❌ حذف چنل', "delete_link_channel::{id}"]

MANAGE_ALL_LINK_GROUPS_REPORT = """<b>مدیریت گروه ها:</b>
🔻 تعداد گروه ها: {groups_count}
➖ با کلیک روی هر گروه میتوانید اون رو مدیریت کنید:
————————————————————————-
💻 نوشته شده توسط: @hawar"""

GROUPS_NEXT_PAGE_BUTTON = ['⏩ صفحه بعد', "manage_groups::{page}"]
GROUPS__PER_PAGE_BUTTON = ['⏮️ صفحه قبل', "manage_groups::{page}"]
DELETE_GROUP_OPTION = ['❌ حذف گروه', "delete_group::{id}"]
MANAGE_GROUP_REPORT = """<b>مدیریت گروه :</b>
🔻 آیدی گروه: {group_id}
🔻 یوزرنیم گروه: @{group_username}
🔻 اسم گروه: {group_name}
🔻 تعداد بنر ارسالی: {group_count_sent_banners}
————————————————————————-
💻 نوشته شده توسط: @hawar
"""
