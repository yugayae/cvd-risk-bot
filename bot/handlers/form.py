from datetime import datetime
import logging
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from bot.states import RiskForm
from bot.services.api_client import get_risk_prediction
from bot.utils.localization import bot_i18n
from app.services.google_sheets import gs_service
from bot.utils.user_stats import stats_manager

logger = logging.getLogger(__name__)
router = Router()


# --- Helper Keyboards ---
def get_gender_kb(lang):
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text=bot_i18n.t(lang, "option_male")),
                types.KeyboardButton(text=bot_i18n.t(lang, "option_female"))
            ]
        ], resize_keyboard=True, one_time_keyboard=True
    )

def get_yes_no_kb(lang):
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text=bot_i18n.t(lang, "option_yes")),
                types.KeyboardButton(text=bot_i18n.t(lang, "option_no"))
            ]
        ], resize_keyboard=True, one_time_keyboard=True
    )

def get_level_kb(lang):
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text=bot_i18n.t(lang, "option_normal")),
                types.KeyboardButton(text=bot_i18n.t(lang, "option_above_normal"))
            ],
            [types.KeyboardButton(text=bot_i18n.t(lang, "option_high"))]
        ], resize_keyboard=True, one_time_keyboard=True
    )

def get_consent_kb(lang):
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text=bot_i18n.get_bot_str(lang, "consent_yes"), callback_data="consent_yes"),
                types.InlineKeyboardButton(text=bot_i18n.get_bot_str(lang, "consent_no"), callback_data="consent_no")
            ]
        ]
    )

def get_post_result_menu(lang, user_id):
    remaining = stats_manager.get_remaining(user_id)
    limit = stats_manager.daily_limit
    assess_btn_text = bot_i18n.get_bot_str(lang, "btn_new_assessment").format(count=remaining, limit=limit)
    
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=assess_btn_text, callback_data="new_assess")],
            [
                types.InlineKeyboardButton(text=bot_i18n.get_bot_str(lang, "btn_tips"), callback_data="tips"),
                types.InlineKeyboardButton(text=bot_i18n.get_bot_str(lang, "btn_about"), callback_data="about")
            ]
        ]
    )

# --- Handlers ---

@router.message(RiskForm.birth_date)
async def process_birth_date(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "en")
    
    text = message.text.strip()
    
    # Strictly check for Age (integer)
    if not text.isdigit():
        return await message.answer(bot_i18n.get_bot_str(lang, "dob_error"))
        
    age_years = int(text)
    
    # 18-90 years check
    if not (18 <= age_years <= 90):
        return await message.answer(bot_i18n.get_bot_str(lang, "dob_error"))
    
    # Calculate approximate days for compatibility if needed, or just store years
    age_days = age_years * 365.25
    
    await state.update_data(age_days=age_days, age_years=age_years)
    await state.set_state(RiskForm.gender)
    
    gender_prompt = bot_i18n.t(lang, "shap_factors", "gender", "name")
    await message.answer(f"2. {gender_prompt}:", reply_markup=get_gender_kb(lang))

@router.message(RiskForm.gender)
async def process_gender(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "en")
    
    gender_map = {
        bot_i18n.t(lang, "option_male"): 2,
        bot_i18n.t(lang, "option_female"): 1
    }
    
    if message.text not in gender_map:
        return await message.answer("Please select an option from the keyboard.")
    
    await state.update_data(gender=gender_map[message.text])
    await state.set_state(RiskForm.height)
    
    height_prompt = bot_i18n.t(lang, "shap_factors", "height", "name")
    await message.answer(f"3. {height_prompt} (cm):", reply_markup=types.ReplyKeyboardRemove())

@router.message(RiskForm.height)
async def process_height(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "en")
    
    if not message.text.isdigit():
        return await message.answer("Please enter a valid number.")
    
    height = int(message.text)
    if not (100 <= height <= 250):
        return await message.answer("Height must be between 100 and 250 cm.")
    
    await state.update_data(height=height)
    await state.set_state(RiskForm.weight)
    
    weight_prompt = bot_i18n.t(lang, "shap_factors", "weight", "name")
    await message.answer(f"4. {weight_prompt} (kg):")

@router.message(RiskForm.weight)
async def process_weight(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "en")
    
    try:
        weight = float(message.text.replace(',', '.'))
    except ValueError:
        return await message.answer("Please enter a valid number.")
    
    if not (30 <= weight <= 250):
        return await message.answer("Weight must be between 30 and 250 kg.")
    
    # Calculate BMI automatically
    height_m = data.get("height") / 100
    bmi = round(weight / (height_m * height_m), 1)
    
    await state.update_data(weight=weight, bmi=bmi)
    await state.set_state(RiskForm.ap_hi)
    
    # Notify user of their calculated BMI
    bmi_text = bot_i18n.t(lang, "bmi_result").format(bmi=bmi)
    await message.answer(bmi_text)
    
    ap_hi_prompt = bot_i18n.t(lang, "shap_factors", "ap_hi", "name")
    await message.answer(f"5. {ap_hi_prompt} (mmHg):")

@router.message(RiskForm.ap_hi)
async def process_ap_hi(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "en")
    
    if not message.text.isdigit():
        return await message.answer("Please enter a valid number.")
    
    ap_hi = int(message.text)
    if not (60 <= ap_hi <= 240):
        return await message.answer("Value out of range.")
    
    await state.update_data(ap_hi=ap_hi)
    await state.set_state(RiskForm.ap_lo)
    
    ap_lo_prompt = bot_i18n.t(lang, "shap_factors", "ap_lo", "name")
    await message.answer(f"6. {ap_lo_prompt} (mmHg):")

@router.message(RiskForm.ap_lo)
async def process_ap_lo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "en")
    
    if not message.text.isdigit():
        return await message.answer("Please enter a valid number.")
    
    ap_lo = int(message.text)
    if not (40 <= ap_lo <= 160):
        return await message.answer("Value out of range.")
    
    await state.update_data(ap_lo=ap_lo)
    await state.set_state(RiskForm.cholesterol)
    
    chol_prompt = bot_i18n.t(lang, "shap_factors", "cholesterol", "name")
    chol_hint = bot_i18n.get_bot_str(lang, "chol_hint")
    guidance = bot_i18n.get_bot_str(lang, "clinical_guidance")
    
    await message.answer(
        f"7. {chol_prompt}:\n\n{chol_hint}\n\n{guidance}",
        reply_markup=get_level_kb(lang),
        parse_mode="Markdown"
    )

@router.message(RiskForm.cholesterol)
async def process_cholesterol(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "en")
    
    level_map = {
        bot_i18n.t(lang, "option_normal"): 1,
        bot_i18n.t(lang, "option_above_normal"): 2,
        bot_i18n.t(lang, "option_high"): 3
    }
    
    if message.text not in level_map:
        return await message.answer("Please use the keyboard.")
    
    await state.update_data(cholesterol=level_map[message.text])
    await state.set_state(RiskForm.gluc)
    
    gluc_prompt = bot_i18n.t(lang, "shap_factors", "gluc", "name")
    gluc_hint = bot_i18n.get_bot_str(lang, "gluc_hint")
    guidance = bot_i18n.get_bot_str(lang, "clinical_guidance")
    
    await message.answer(
        f"8. {gluc_prompt}:\n\n{gluc_hint}\n\n{guidance}",
        reply_markup=get_level_kb(lang),
        parse_mode="Markdown"
    )

@router.message(RiskForm.gluc)
async def process_gluc(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "en")
    
    level_map = {
        bot_i18n.t(lang, "option_normal"): 1,
        bot_i18n.t(lang, "option_above_normal"): 2,
        bot_i18n.t(lang, "option_high"): 3
    }
    
    if message.text not in level_map:
        return await message.answer("Please use the keyboard.")
    
    await state.update_data(gluc=level_map[message.text])
    await state.set_state(RiskForm.smoke)
    
    smoke_prompt = bot_i18n.t(lang, "shap_factors", "smoke", "name")
    smoke_clarification = bot_i18n.get_bot_str(lang, "smoke_clarification")
    
    await message.answer(
        f"9. {smoke_prompt}?\n\n{smoke_clarification}",
        reply_markup=get_yes_no_kb(lang)
    )

@router.message(RiskForm.smoke)
async def process_smoke(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "en")
    
    yes_no_map = {
        bot_i18n.t(lang, "option_yes"): 1,
        bot_i18n.t(lang, "option_no"): 0
    }
    
    if message.text not in yes_no_map:
        return await message.answer("Please use the keyboard.")
    
    await state.update_data(smoke=yes_no_map[message.text])
    await state.set_state(RiskForm.alco)
    
    alco_prompt = bot_i18n.t(lang, "shap_factors", "alco", "name")
    alco_clarification = bot_i18n.get_bot_str(lang, "alco_clarification")
    
    await message.answer(
        f"10. {alco_prompt}?\n\n{alco_clarification}",
        reply_markup=get_yes_no_kb(lang)
    )

@router.message(RiskForm.alco)
async def process_alco(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "en")
    
    yes_no_map = {
        bot_i18n.t(lang, "option_yes"): 1,
        bot_i18n.t(lang, "option_no"): 0
    }
    
    if message.text not in yes_no_map:
        return await message.answer("Please use the keyboard.")
    
    await state.update_data(alco=yes_no_map[message.text])
    await state.set_state(RiskForm.active)
    
    active_prompt = bot_i18n.t(lang, "shap_factors", "active", "name")
    await message.answer(f"11. {active_prompt}?", reply_markup=get_yes_no_kb(lang))

@router.message(RiskForm.active)
async def process_active(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "en")
    
    yes_no_map = {
        bot_i18n.t(lang, "option_yes"): 1,
        bot_i18n.t(lang, "option_no"): 0
    }
    
    if message.text not in yes_no_map:
        return await message.answer("Please use the keyboard.")
    
    await state.update_data(active=yes_no_map[message.text])
    
    # --- PREDICTION ---
    form_data = await state.get_data()
    form_data['ui_language'] = lang
    
    wait_msg = "⏳ ..." if lang != "ru" else "⏳ Анализ данных..."
    await message.answer(wait_msg, reply_markup=types.ReplyKeyboardRemove())
    
    try:
        result = await get_risk_prediction(form_data)
        
        if "error" in result:
             await message.answer(f"❌ Error: {result['error']}")
             return

        # Record assessment stats
        stats_manager.record_assessment(message.from_user.id)

        # Format Result (Localized)
        risk_prob = result.get('risk_probability', 0)
        risk_cat = result.get('risk_category', 'low')
        risk_percent = round(risk_prob * 100, 1)
        
        risk_cat_loc = bot_i18n.t(lang, "risk_category", risk_cat)
        
        emoji = "🟢"
        if risk_cat == "moderate": emoji = "🟡"
        if risk_cat == "high": emoji = "🔴"
        
        title_loc = bot_i18n.t(lang, "results_title")
        prob_loc = bot_i18n.t(lang, "risk_cvd")
        factors_loc = bot_i18n.t(lang, "results_key_factors")
        
        response_text = (
            f"{emoji} **{title_loc}**\n\n"
            f"**{risk_cat_loc}**\n"
            f"**{prob_loc}:** {risk_percent}%\n\n"
            f"**{factors_loc}:**\n"
        )
        
        recommendations = []
        for explanation in result.get('clinical_explanation', []):
             if explanation['raw_direction'] == "increases":
                 direction = "⬆️"
                 response_text += f"- {direction} **{explanation['factor']}**: {explanation['clinical_note']}\n"
                 
                 # Look for a specific recommendation for this factor
                 rec = bot_i18n.t(lang, "factor_recommendations", explanation['key'])
                 if rec and rec not in recommendations:
                     recommendations.append(rec)

        rec_loc = bot_i18n.t(lang, "results_recommendations")
        
        if recommendations:
            recommendation_text = "\n".join([f"• {r}" for r in recommendations])
        else:
            recommendation_text = result.get('risk_card', {}).get('recommendation') or bot_i18n.get_bot_str(lang, "default_recommendation")
            
        response_text += f"\n💡 **{rec_loc}:**\n{recommendation_text}"
        
        # Add Disclaimer
        disclaimer = bot_i18n.t(lang, "disclaimer")
        if disclaimer:
             response_text += f"\n\n⚠️ **Disclaimer**: {disclaimer}"
             
        await message.answer(response_text, parse_mode="Markdown")
        
        # Save result to state
        await state.update_data(
            risk_probability=risk_percent,
            risk_category=risk_cat,
            confidence_level=result.get('audit', {}).get('confidence_level', 'unknown'),
            model_version=result.get('audit', {}).get('model_version', 'unknown'),
            bmi=result.get('patient_bmi', 0)
        )
        
        # LOGGING (If Consent Given)
        has_consent = form_data.get("consent", False)
        if has_consent:
             # Re-fetch full data including result
             final_data = await state.get_data()
             await gs_service.append_patient_data(final_data)
        
        # Show Post-Result Menu
        menu_text = bot_i18n.get_bot_str(lang, "main_menu")
        await message.answer(menu_text, reply_markup=get_post_result_menu(lang, message.from_user.id))
        
    except Exception as e:
        logger.error(f"Error in bot prediction flow: {e}")
        await message.answer(f"❌ Error: {str(e)}")
        await state.clear()

# --- Menu Handlers ---

@router.callback_query(F.data == "new_assess")
async def handle_new_assess(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    
    data = await state.get_data()
    lang = data.get("language", "en")
    region = data.get("region", "EUR")
    consent = data.get("consent", False) # Preserve consent
    
    # Check limits again
    can_assess, reason = stats_manager.can_assess(callback.from_user.id)
    if not can_assess:
        if reason == "limit":
            msg = bot_i18n.get_bot_str(lang, "limit_reached").format(limit=stats_manager.daily_limit)
        else:
            msg = bot_i18n.get_bot_str(lang, "cooldown")
        return await callback.message.answer(msg)

    await state.clear()
    await state.update_data(language=lang, region=region, consent=consent)
    
    # Start assessment directly
    dob_prompt = bot_i18n.get_bot_str(lang, "dob_prompt")
    await callback.message.answer(f"1. {dob_prompt}", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(RiskForm.birth_date)

@router.callback_query(F.data == "tips")
async def handle_tips(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "en")
    await callback.answer()
    await callback.message.answer(bot_i18n.get_bot_str(lang, "tips_text"))

@router.callback_query(F.data == "about")
async def handle_about(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "en")
    await callback.answer()
    await callback.message.answer(bot_i18n.get_bot_str(lang, "about_text"))
