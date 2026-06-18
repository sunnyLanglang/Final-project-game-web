# -*- coding: utf-8 -*-
# settings.py
import pygame

class Settings:
    def __init__(self):
        self.bgm_volume = 0.4
        self.sfx_volume = 0.6
        self.move_speed = 1.5
        self.language = "zh"

settings = Settings()

TEXTS = {
    "zh": {
        "menu_title": "自我之路",
        "menu_start": "开始游戏",
        "menu_settings": "设置",
        "menu_about": "简介",
        "menu_quit": "退出",
        "settings_title": "设置",
        "settings_bgm": "背景音乐音量",
        "settings_sfx": "音效音量",
        "settings_speed": "移动速度",
        "settings_lang": "语言",
        "settings_lang_zh": "中文",
        "settings_lang_ru": "Русский",
        "settings_back": "返回",
        "about_title": "关于游戏",
        "about_text": "《自我之路》—— 一部关于成长与选择的留学叙事游戏。\n你将在圣彼得堡经历学习、生活、文化碰撞，\n每个选择都会影响你的命运。\n\n操作：长按 → 移动，遇到事件自动弹出选项。\n↑/↓ 选择选项，空格确认。按 ESC 打开菜单。",
        "about_back": "返回",
        "game_narrative_start": "你即将踏上圣彼得堡的留学之旅。长按 → 向前走，路上会遇到各种挑战。",
        "game_narrative_reset": "游戏已重置。再次踏上留学之旅吧！",
        "game_over": "你倒在了异国的土地上... 点击屏幕重新开始。",
        "game_restart_hint": "点击屏幕重新开始游戏",
        "game_over_hint": "点击屏幕重新开始",
        "game_warn_incomplete": " 已到达终点，但还有事件未完成！",
        "game_warn_remaining": "剩余 {} 个问题未触发。按 R 重新开始。",
        "dialog_tip": "↑/↓ 选择 | 空格 确认",
        "effect_prefix": "效果: ",
        "effect_no_change": "效果: 无变化",
        "random_event_end": "随机事件结束。",
        "chosen_prefix": "你选择了：",
        "best_suffix": "最佳做法：",
        "game_over_title": " 游戏结束 ",
        "game_summary_title": " 故事结局 ",
        "total_score_label": "你的累计得分：",
        "restart_btn": "重新开始",
        "menu_btn": "返回主菜单",
        "scroll_hint": "↑/↓ ({}-{}/{})",
        "ending_good": "你以优异的适应能力完成了留学，不仅在学业上优秀，更融入了当地文化。你带着满满的收获和回忆，踏上了新的征程。",
        "ending_neutral": "你顺利度过了留学时光，虽然有些坎坷，但整体上收获颇丰。你带着成长和友谊，准备迎接未来。",
        "ending_bad": "留学之路充满挑战，你经历了不少困难，但也从中获得了宝贵的经验。这段经历让你更加坚强。",
    },
    "ru": {
        "menu_title": "Путь к себе",
        "menu_start": "Начать игру",
        "menu_settings": "Настройки",
        "menu_about": "Об игре",
        "menu_quit": "Выход",
        "settings_title": "Настройки",
        "settings_bgm": "Громкость фона",
        "settings_sfx": "Громкость эффектов",
        "settings_speed": "Скорость",
        "settings_lang": "Язык",
        "settings_lang_zh": "Китайский",
        "settings_lang_ru": "Русский",
        "settings_back": "Назад",
        "about_title": "Об игре",
        "about_text": "?Путь к себе? — интерактивная игра-нарратив о студенте в Петербурге.\nВы столкнётесь с учёбой, бытом, культурой, каждый выбор влияет на судьбу.\nУправление: удерживайте → для движения, при событии появляются варианты.\n↑/↓ — выбор, пробел — подтвердить. ESC — меню.",
        "about_back": "Назад",
        "game_narrative_start": "Вы отправляетесь в путешествие по Петербургу. Удерживайте →, чтобы двигаться.",
        "game_narrative_reset": "Игра перезапущена. В путь!",
        "game_over": "Вы пали на чужой земле... Нажмите кликните, чтобы начать заново.",
        "game_restart_hint": "Нажмите кликните для перезапуска",
        "game_over_hint": "Нажмите кликните для перезапуска",
        "game_warn_incomplete": " Вы дошли до финиша, но не все события пройдены!",
        "game_warn_remaining": "Осталось {} событий. Нажмите R для перезапуска.",
        "dialog_tip": "↑/↓ выбор | пробел подтвердить",
        "effect_prefix": "Эффект: ",
        "effect_no_change": "Нет изменений",
        "random_event_end": "Случайное событие завершено.",
        "chosen_prefix": "Вы выбрали: ",
        "best_suffix": "Лучшее решение: ",
        "game_over_title": " Конец игры ",
        "game_summary_title": " Финал ",
        "total_score_label": "Ваш общий счёт: ",
        "restart_btn": "Перезапустить",
        "menu_btn": "В главное меню",
        "scroll_hint": "↑/↓ ({}-{}/{})",
        "ending_good": "Вы блестяще справились с адаптацией, преуспели в учёбе и влились в культуру. Вы увозите с собой полный багаж знаний и тёплых воспоминаний.",
        "ending_neutral": "Вы успешно пережили студенческую жизнь, хоть и были трудности. Вы обрели друзей и повзрослели. Впереди новое будущее.",
        "ending_bad": "Путь был полон испытаний, вы многое преодолели и получили бесценный опыт. Этот опыт сделал вас сильнее.",
    }
}

def get_text(key):
    return TEXTS[settings.language].get(key, key)