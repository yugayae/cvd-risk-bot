from aiogram import Router, types, F
import logging
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.states import RiskForm
from bot.utils.localization import bot_i18n
from bot.utils.user_stats import stats_manager

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    logging.info(f"HANDLER: cmd_start triggered for user {message.from_user.id}")
    try:
        await state.clear()
        logging.info("HANDLER: state cleared")
        
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
        
        logging.info("HANDLER: attempting to send message")
        await message.answer(
            "Please select your language / Пожалуйста, выберите язык / 언어를 선택하세요:",
            reply_markup=keyboard
        )
        logging.info("HANDLER: message sent successfully")
        await state.set_state(RiskForm.language)
        logging.info("HANDLER: state set to language")
    except Exception as e:
        logging.error(f"HANDLER ERROR: {e}", exc_info=True)

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
    
    # Region Selection Keyboard (WHO regions with full names)
    regions_code = ["AFR", "AMR", "SEAR", "EUR", "EMR", "WPR"]
    region_names_map = bot_i18n.t(lang, "bot", "region_names")
    
    keyboard_btns = []
    # Create buttons using full localized names
    for i in range(0, len(regions_code), 2):
        row = []
        code1 = regions_code[i]
        name1 = region_names_map.get(code1, code1)
        row.append(types.KeyboardButton(text=name1))
        
        if i+1 < len(regions_code):
            code2 = regions_code[i+1]
            name2 = region_names_map.get(code2, code2)
            row.append(types.KeyboardButton(text=name2))
        keyboard_btns.append(row)
        
    unknown_text = bot_i18n.get_bot_str(lang, "region_unknown")
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
    # Reverse lookup region code from name
    data = await state.get_data()
    lang = data.get("language", "en")
    region_names_map = bot_i18n.t(lang, "bot", "region_names")
    
    # Create reverse map: Name -> Code
    name_to_code = {v: k for k, v in region_names_map.items()}
    unknown_text = bot_i18n.get_bot_str(lang, "region_unknown")
    
    selected_text = message.text
    if selected_text == unknown_text:
        region_code = "Unknown"
    else:
        region_code = name_to_code.get(selected_text, "EUR") # Default to EUR if mismatch
        
    await state.update_data(region=region_code)
    
    # ASK CONSENT HERE (Early)
    from bot.handlers.form import get_consent_kb # Import here to avoid circular
    consent_request = bot_i18n.get_bot_str(lang, "consent_request")
    
    await message.answer(consent_request, reply_markup=get_consent_kb(lang))
    await state.set_state(RiskForm.consent)

@router.callback_query(RiskForm.consent, F.data.startswith("consent_"))
async def process_consent_early(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "en")
    consent_given = callback.data == "consent_yes"
    
    await state.update_data(consent=consent_given)
    await callback.answer()
    
    confirm_text = bot_i18n.get_bot_str(lang, "consent_thanks")
    await callback.message.edit_text(f"{'✅' if consent_given else '👌'} {confirm_text}")
    
    # Show WELCOME MENU
    remaining = stats_manager.get_remaining(callback.from_user.id)
    limit = stats_manager.daily_limit
    
    welcome_text = bot_i18n.get_bot_str(lang, "welcome").format(count=remaining, limit=limit)
    assess_btn_text = bot_i18n.get_bot_str(lang, "btn_new_assessment").format(count=remaining, limit=limit)
    
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=assess_btn_text)],
            [types.KeyboardButton(text=bot_i18n.get_bot_str(lang, "btn_help")), types.KeyboardButton(text=bot_i18n.get_bot_str(lang, "btn_about"))]
        ],
        resize_keyboard=True
    )
    
    await callback.message.answer(welcome_text, parse_mode="Markdown", reply_markup=keyboard)
    
    # Clear state for menu interaction, BUT keep data
    # We set state to None so global handlers catch the buttons
    await state.set_state(None)

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
