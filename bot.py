from api import *
from user import *
from config import *
from pyrogram import Client, filters
from pyrogram.types import *

app = Client("bot", 
                bot_token=bot_token,
                api_id=api_id,
                api_hash=api_hash,
            )

mainmenu = ReplyKeyboardMarkup(
    [
        [KeyboardButton("Fast Search")],
        [KeyboardButton("Detailed Search")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

back = ReplyKeyboardMarkup(
    [
        [KeyboardButton("back")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

async def detailed_search_city(message:Message):
    cities = search_city(message.text)
    if len(cities) == 0:
        await message.reply_text("Nothing found. please try again.")
        return
    buttons = []
    for city in cities:
        name = city['name'] 
        lat = city['lat']
        lon = city['lon']
        data = str(lat) + "_" + str(lon)
        buttons.append([InlineKeyboardButton(name, data)])
    
    menu_cities = InlineKeyboardMarkup(
        buttons
    )
    
    await message.reply_text("Please choose a city from the list below:", reply_markup=menu_cities)
    return

@app.on_message(filters.command('start'))
async def start(client:Client, message:Message):
    user = UserBot(int(message.chat.id))
    user.setMenu(0)
    await app.set_bot_commands(
        [BotCommand("start", 'start bot')]
    )
    await message.reply_text("wellcome to the bot. please choose from the menu below.", reply_markup=mainmenu)

@app.on_message(filters.text & filters.private)
async def search(client:Client, message:Message):
    user = UserBot(int(message.chat.id))
    menu = user.getMenu()
    if menu == 0:
        if message.text == "Fast Search":
            await message.reply_text("Fast Search\nPlease Send me name of a city",
                                     reply_markup=back)
            user.setMenu(1)
            
        elif message.text == "Detailed Search":
            await message.reply_text("Detailed Search\nPlease send me name of a city", 
                                     reply_markup=back)
            user.setMenu(2)
            
        else:
            await message.reply_text("please choose from the menu.", reply_markup=mainmenu)
            
    elif message.text == "back":
        user.setMenu(0)
        await message.reply_text("back to main menu.", reply_markup=mainmenu)
        
    elif menu == 1:
        text = fast_search(message.text)
        await message.reply_text(text)
        
    elif menu == 2:
        await detailed_search_city(message)

@app.on_callback_query()
async def answer(client:Client, callback_query:CallbackQuery):
    data = callback_query.data
    key = data[0]
    data = data.split("_")
    

    if key == "A":
        lat = data[1]
        lon = data[2]
        message = get_air_pollution(lat, lon)
        await callback_query.message.reply_text(message)
        
    elif key == "F":
        lat = data[1]
        lon = data[2]
        message = full_data(lat, lon)
        await callback_query.message.reply_text(message)
        
    else:
        lat = data[0]
        lon = data[1]
        message = city_data(lat, lon)
        maplink = f"https://openweathermap.org/weathermap?basemap=map&cities=true&layer=temperature&lat={lat}&lon={lon}&zoom=12"
        moredata = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Show Map", 
                                      url=maplink)],
                [InlineKeyboardButton("Air Pollution", 
                                      callback_data="A_"+lat+"_"+lon)],
                [InlineKeyboardButton('More Data',
                                      callback_data="F_"+lat+"_"+lon)],
            ],
        )
        await callback_query.message.reply(message, reply_markup=moredata)
    await callback_query.answer(
            "sent.",
            show_alert=False
        )
    

app.run()