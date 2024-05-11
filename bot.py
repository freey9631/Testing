from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN, ADMINS 
from database import db

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

verification_data = {}
admins = ADMINS

# Command to start the verification process
@app.on_message(filters.command("verify"))
async def start_verification(client, message):
    user_id = message.from_user.id
    verification_data[user_id] = {}
    verification_data[user_id]['step'] = 1
    await message.reply_text("Welcome to the verification process!\n\nPlease send your full name.")

# Handler for receiving user input
@app.on_message(filters.text & filters.private | filters.photo & filters.private | filters.video & filters.private)
async def receive_input(client, message):
    user_id = message.from_user.id
    if user_id in verification_data:
        step = verification_data[user_id]['step']
        if step == 1:
            verification_data[user_id]['name'] = message.text
            verification_data[user_id]['step'] = 2
            await message.reply_text("Thank you! Now please send your username (if any).")
        elif step == 2:
            verification_data[user_id]['username'] = message.text
            verification_data[user_id]['step'] = 3
            await message.reply_text("Got it! Now please send your address.")
        elif step == 3:
            verification_data[user_id]['address'] = message.text
            verification_data[user_id]['step'] = 4
            # Send normal keyboard to select document type
            reply_keyboard = ReplyKeyboardMarkup(
                [
                    [KeyboardButton("NID"), KeyboardButton("PASSPORT")],
                    [KeyboardButton("JONMONIBONDON")]
                ],
                resize_keyboard=True
            )
            await message.reply_text("Please select the type of document you want to add for verification:", reply_markup=reply_keyboard)
        elif step == 4:
            if message.text:
                document_type = message.text.lower()
                if document_type in ["nid", "passport", "jonmonibondon"]:
                    verification_data[user_id]['document_type'] = document_type
                    verification_data[user_id]['step'] = 5
                    await message.reply_text(f"Please send the {document_type} photo for verification.")
                else:
                    await message.reply_text("Invalid document type! Please select from the provided options.")
        elif step == 5:
            if message.photo:
                document_type = verification_data[user_id]['document_type']
                verification_data[user_id][f'{document_type}_photo'] = message.photo.file_id
                verification_data[user_id]['step'] = 6
                await message.reply_text("Got it! Now please send your selfie/photo for verification.")
        elif step == 6:
            if message.photo:
                verification_data[user_id]['selfie_photo'] = message.photo.file_id
                verification_data[user_id]['step'] = 7
                await message.reply_text("Great! Now please send the verification video.")
        elif step == 7 and message.video:
            verification_data[user_id]['verification_video'] = message.video.file_id
            # Send user data to admins for verification
            await send_to_admins(verification_data.pop(user_id))
            await message.reply_text("Thank you for completing the verification process! Your information will be verified soon.")

# Function to send user data to admins for verification
async def send_to_admins(user_data):
    for admin_id in admins:
        await app.send_message(admin_id, f"New verification request:\n{user_data}")

# Command to approve and add user data to the database
@app.on_message(filters.command("approve") & filters.user(admins))
async def approve_data(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])
        user_data = verification_data.pop(user_id)
        await db.add_user(user_data['name'], user_data['username'], user_data['address'], user_data.get('nid_photo', ''), user_data.get('passport_photo', ''), user_data.get('jonmo_nibondon_photo', ''), user_data.get('selfie_photo', ''), user_data.get('verification_video', ''))
        await message.reply_text("User data approved and added to the database successfully!")
    else:
        await message.reply_text("Invalid command usage! Please use /approve <user_id>.")

# Command to disapprove user data
@app.on_message(filters.command("disapprove") & filters.user(admins))
async def disapprove_data(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])
        if user_id in verification_data:
            user_data = verification_data.pop(user_id)
            await send_to_admins(user_data, disapproved=True)
            await message.reply_text("User data disapproved.")
        else:
            await message.reply_text("User data not found in the verification queue.")
    else:
        await message.reply_text("Invalid command usage! Please use /disapprove <user_id>.")

# Function to send user data to admins for verification or disapproval
async def send_to_admins(user_data, disapproved=False):
    for admin_id in admins:
        if disapproved:
            await app.send_message(admin_id, f"User data disapproved:\n{user_data}")
        else:
            await app.send_message(admin_id, f"New verification request:\n{user_data}")

# Start the Bot
app.run()
