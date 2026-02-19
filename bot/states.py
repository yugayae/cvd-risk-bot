from aiogram.fsm.state import State, StatesGroup

class RiskForm(StatesGroup):
    language = State()
    region = State()
    birth_date = State()
    age = State()
    gender = State()
    height = State()
    weight = State()
    ap_hi = State()
    ap_lo = State()
    cholesterol = State()
    gluc = State()
    smoke = State()
    alco = State()
    active = State()
    consent = State()
    confirmation = State()
