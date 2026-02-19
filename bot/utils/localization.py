from app.localization import LOCALIZATION, t as app_t

class BotI18n:
    def __init__(self, default_lang="en"):
        self.default_lang = default_lang

    def t(self, lang, category, key=None, subkey=None):
        """
        Retrieves localized string for the bot.
        """
        # Ensure lang is supported
        if lang not in ["ru", "en", "kr"]:
            lang = self.default_lang
            
        return app_t(lang, category, key, subkey)

    def get_bot_str(self, lang, key):
        """
        Helper for bot-specific strings
        """
        return self.t(lang, "bot", key)

# Global instances
bot_i18n = BotI18n("en")
