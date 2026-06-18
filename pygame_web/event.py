# -*- coding: utf-8 -*-
# event.py
from settings import get_text

class GameEvent:
    def __init__(self, data, is_random=False):
        self.x = data.get("x", 0)
        self.title = data["title"]
        self.desc = data["desc"]
        self.options = data["options"]
        self.best = data.get("best", "")
        self.triggered = False
        self.chosen_option_idx = None
        self.is_random = is_random

    def get_option_texts(self):
        return [opt[0] for opt in self.options]

    def apply_choice(self, player):
        if self.chosen_option_idx is None:
            return "未选择任何选项", False, 0, 0
        idx = self.chosen_option_idx
        _, hp_delta, sp_delta = self.options[idx]
        if hp_delta > 0:
            player.heal(hp_delta)
        elif hp_delta < 0:
            player.take_damage(-hp_delta)
        if sp_delta > 0:
            player.heal(0, sp_delta)
        elif sp_delta < 0:
            player.take_damage(0, -sp_delta)
        effect_parts = []
        if hp_delta != 0:
            effect_parts.append(f"HP {hp_delta:+d}")
        if sp_delta != 0:
            effect_parts.append(f"SP {sp_delta:+d}")
        effect_text = get_text("effect_prefix") + ("  ".join(effect_parts) if effect_parts else get_text("effect_no_change"))
        is_bad = (hp_delta < 0) or (sp_delta < 0)
        return effect_text, is_bad, hp_delta, sp_delta