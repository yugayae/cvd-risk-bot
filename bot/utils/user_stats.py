import os
import json
import time
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class StatsManager:
    def __init__(self, stats_file="bot/data/stats.json", daily_limit=10, cooldown_sec=30):
        self.stats_file = stats_file
        self.daily_limit = daily_limit
        self.cooldown_sec = cooldown_sec
        self.stats = self._load_stats()

    def _load_stats(self):
        os.makedirs(os.path.dirname(self.stats_file), exist_ok=True)
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load stats: {e}")
        return {}

    def _save_stats(self):
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save stats: {e}")

    def _reset_if_needed(self, user_id):
        user_id = str(user_id)
        today = datetime.now().strftime("%Y-%m-%d")
        
        if user_id not in self.stats:
            self.stats[user_id] = {
                "date": today,
                "count": 0,
                "last_assessment": 0
            }
        
        if self.stats[user_id]["date"] != today:
            self.stats[user_id]["date"] = today
            self.stats[user_id]["count"] = 0
            self._save_stats()

    def get_remaining(self, user_id):
        self._reset_if_needed(user_id)
        current = self.stats[str(user_id)]["count"]
        return max(0, self.daily_limit - current)

    def can_assess(self, user_id):
        self._reset_if_needed(user_id)
        stats = self.stats[str(user_id)]
        
        # Check daily limit
        if stats["count"] >= self.daily_limit:
            return False, "limit"
        
        # Check cooldown
        now = time.time()
        if now - stats["last_assessment"] < self.cooldown_sec:
            return False, "cooldown"
            
        return True, None

    def record_assessment(self, user_id):
        self._reset_if_needed(user_id)
        user_id = str(user_id)
        self.stats[user_id]["count"] += 1
        self.stats[user_id]["last_assessment"] = time.time()
        self._save_stats()

# Global instance
stats_manager = StatsManager()
