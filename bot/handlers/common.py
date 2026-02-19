from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.states import RiskForm
from bot.utils.localization import bot_i18n
from bot.utils.user_stats import stats_manager

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    
    # Language Selection Keyboard
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Русский 🇷🇺")],
            [types.KeyboardButton(text="English 🇺🇸")],
            [types.KeyboardButton(text="한국어 🇰🇷")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    await message.answer(
        "Please select your language / Пожалуйста, выберите язык / 언어를 선택하세요:",
        reply_markup=keyboard
    )
    await state.set_state(RiskForm.language)

@router.message(RiskForm.language)
async def process_language(message: types.Message, state: FSMContext):
    lang_map = {
        "Русский 🇷🇺": "ru",
        "English 🇺🇸": "en",
        "한국어 🇰🇷": "kr"
    }
    
    if message.text not in lang_map:
        return await message.answer("Please use the keyboard.")
    
    lang = lang_map[message.text]
    await state.update_data(language=lang)
    
    # Region Selection Keyboard (WHO regions)
    regions = ["AFR", "AMR", "SEAR", "EUR", "EMR", "WPR"]
    lang_data = await state.get_data()
    unknown_text = bot_i18n.get_bot_str(lang, "region_unknown")
    
    keyboard_btns = []
    # Two buttons per row
    for i in range(0, len(regions), 2):
        keyboard_btns.append([types.KeyboardButton(text=regions[i]), types.KeyboardButton(text=regions[i+1])])
    keyboard_btns.append([types.KeyboardButton(text=unknown_text)])
        
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=keyboard_btns,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    await message.answer(
        bot_i18n.get_bot_str(lang, "select_region"),
        reply_markup=keyboard
    )
    await state.set_state(RiskForm.region)

@router.message(RiskForm.region)
async def process_region(message: types.Message, state: FSMContext):
    await state.update_data(region=message.text)
    data = await state.get_data()
    lang = data.get("language", "en")
    
    remaining = stats_manager.get_remaining(message.from_user.id)
    limit = stats_manager.daily_limit
    
    # Welcome message in selected language
    welcome_text = bot_i18n.get_bot_str(lang, "welcome").format(count=remaining, limit=limit)
    
    assess_btn_text = bot_i18n.get_bot_str(lang, "btn_new_assessment").format(count=remaining, limit=limit)
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=assess_btn_text)],
            [types.KeyboardButton(text=bot_i18n.get_bot_str(lang, "btn_help")), types.KeyboardButton(text=bot_i18n.get_bot_str(lang, "btn_about"))]
        ],
        resize_keyboard=True
    )
    
    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=keyboard)

@router.message(Command("assess"))
async def cmd_assess(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language")
    
    if not lang:
        return await cmd_start(message, state)
    
    # Check limits
    can_assess, reason = stats_manager.can_assess(message.from_user.id)
    if not can_assess:
        if reason == "limit":
            msg = bot_i18n.get_bot_str(lang, "limit_reached").format(limit=stats_manager.daily_limit)
        else:
            msg = bot_i18n.get_bot_str(lang, "cooldown")
        return await message.answer(msg)

    # Use localized birth_date prompt
    dob_prompt = bot_i18n.get_bot_str(lang, "dob_prompt")
    await message.answer(
        f"1. {dob_prompt}",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(RiskForm.birth_date)

@router.message(F.text.regexp(r"📈.*|Assess Risk"))
async def text_assess(message: types.Message, state: FSMContext):
    await cmd_assess(message, state)

@router.message(Command("help"))
@router.message(F.text.regexp(r"❓.*"))
async def cmd_help(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "ru")
    await message.answer(bot_i18n.get_bot_str(lang, "help_text"))

@router.message(Command("about"))
@router.message(F.text.regexp(r"ℹ️.*"))
async def cmd_about(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "ru")
    await message.answer(bot_i18n.get_bot_str(lang, "about_text"))
