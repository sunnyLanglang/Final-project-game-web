# -*- coding: utf-8 -*-
# scenes.py
import sys, random, pygame
from pygame.locals import *
from constants import *
from settings import settings, get_text
from utils import load_font, wrap_text, Button, MultiLineButton
from player import Player
from event import GameEvent
from story import get_events

class Scene:
    def __init__(self, game):
        self.game = game
        self.font_small = load_font(18)
        self.font_medium = load_font(22)
        self.font_large = load_font(28)

    def handle_events(self, events):
        pass
    def update(self):
        pass
    def draw(self, screen):
        pass

class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.buttons = []
        self._create_buttons()

    def _create_buttons(self):
        self.buttons = []
        btn_w = 250
        btn_h = 50
        start_x = (SCREEN_WIDTH - btn_w) // 2
        y0 = 200
        texts = [
            ("menu_start", self._start_game),
            ("menu_settings", self._open_settings),
            ("menu_about", self._open_about),
            ("menu_quit", self._quit_game)
        ]
        for i, (key, func) in enumerate(texts):
            btn = Button(start_x, y0 + i*(btn_h+20), btn_w, btn_h, get_text(key), self.font_medium)
            btn.func = func
            self.buttons.append(btn)

    def _start_game(self):
        self.game.scene = GameScene(self.game)

    def _open_settings(self):
        self.game.scene = SettingsScene(self.game)

    def _open_about(self):
        self.game.scene = AboutScene(self.game)

    def _quit_game(self):
        pygame.quit()
        sys.exit()

    def handle_events(self, events):
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            for btn in self.buttons:
                if btn.handle_event(event):
                    btn.func()
                    break

    def draw(self, screen):
        screen.fill(SKY_BLUE)
        title = self.font_large.render(get_text("menu_title"), True, BLUE)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        for btn in self.buttons:
            btn.draw(screen)

class SettingsScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.sliders = [
            {"key": "bgm_volume", "label": "settings_bgm", "min": 0, "max": 100, "value": settings.bgm_volume*100},
            {"key": "sfx_volume", "label": "settings_sfx", "min": 0, "max": 100, "value": settings.sfx_volume*100},
            {"key": "move_speed", "label": "settings_speed", "min": 1, "max": 5, "value": settings.move_speed},
        ]
        self.back_btn = Button(SCREEN_WIDTH//2-100, 500, 200, 50, get_text("settings_back"), self.font_medium)
        self.lang_btn = Button(SCREEN_WIDTH//2-100, 420, 200, 50, get_text("settings_lang_zh" if settings.language=="zh" else "settings_lang_ru"), self.font_medium)
        self.dragging = None
        self.update_labels()

    def update_labels(self):
        self.lang_btn.text = get_text("settings_lang_zh" if settings.language=="zh" else "settings_lang_ru")

    def handle_events(self, events):
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if self.back_btn.handle_event(event):
                    self.game.scene = MenuScene(self.game)
                    return
                if self.lang_btn.handle_event(event):
                    settings.language = "ru" if settings.language=="zh" else "zh"
                    self.update_labels()
                    self.game.scene = SettingsScene(self.game)
                    return
                for i, s in enumerate(self.sliders):
                    rect = pygame.Rect(350, 150+i*70, 300, 20)
                    if rect.collidepoint(event.pos):
                        self.dragging = i
            if event.type == MOUSEBUTTONUP:
                self.dragging = None
            if event.type == MOUSEMOTION and self.dragging is not None:
                idx = self.dragging
                x = max(350, min(650, event.pos[0]))
                val = (x - 350) / 300 * (self.sliders[idx]["max"] - self.sliders[idx]["min"]) + self.sliders[idx]["min"]
                self.sliders[idx]["value"] = int(round(val))
                if idx == 0:
                    settings.bgm_volume = self.sliders[idx]["value"] / 100
                    pygame.mixer.music.set_volume(settings.bgm_volume)
                elif idx == 1:
                    settings.sfx_volume = self.sliders[idx]["value"] / 100
                elif idx == 2:
                    settings.move_speed = self.sliders[idx]["value"]

    def draw(self, screen):
        screen.fill(BLACK)
        title = self.font_large.render(get_text("settings_title"), True, WHITE)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 30))
        for i, s in enumerate(self.sliders):
            label = self.font_medium.render(get_text(s["label"]), True, WHITE)
            screen.blit(label, (50, 150+i*70))
            rect = pygame.Rect(350, 150+i*70, 300, 20)
            pygame.draw.rect(screen, DARK_GRAY, rect)
            width = int((s["value"] - s["min"]) / (s["max"] - s["min"]) * 300)
            pygame.draw.rect(screen, GREEN, (350, 150+i*70, width, 20))
            val_text = self.font_small.render(str(s["value"]), True, WHITE)
            screen.blit(val_text, (660, 150+i*70))
        self.lang_btn.draw(screen)
        self.back_btn.draw(screen)

class AboutScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.back_btn = Button(SCREEN_WIDTH//2-100, 500, 200, 50, get_text("about_back"), self.font_medium)

    def handle_events(self, events):
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if self.back_btn.handle_event(event):
                self.game.scene = MenuScene(self.game)

    def draw(self, screen):
        screen.fill(BLACK)
        title = self.font_large.render(get_text("about_title"), True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 30))
        lines = get_text("about_text").split('\n')
        y = 100
        for line in lines:
            if line.strip() == "":
                y += 20
                continue
            surf = self.font_medium.render(line, True, WHITE)
            screen.blit(surf, (50, y))
            y += 35
        self.back_btn.draw(screen)

class GameScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        pygame.mixer.init()
        self.screen = game.screen

        self.correct_sound = self._load_sound("assets/sounds/correct.ogg")
        self.wrong_sound = self._load_sound("assets/sounds/wrong.ogg")
        try:
            pygame.mixer.music.load("assets/sounds/bgm.ogg")
            pygame.mixer.music.set_volume(settings.bgm_volume)
            pygame.mixer.music.play(-1)
            print("背景音乐已启动")
        except:
            print("未找到背景音乐")

        self.correct_img = self._load_image("assets/images/correct.png")
        self.wrong_img = self._load_image("assets/images/wrong.png")
        self.neutral_img = self._load_image("assets/images/neutral.png")
        self.popup_img = None
        self.popup_timer = 0

        
        self.clouds = []
        for _ in range(20):
            x = random.randint(0, END_X)
            y = random.randint(20, SCREEN_HEIGHT // 2 - 30)
            w = random.randint(60, 150)
            h = random.randint(20, 50)
            alpha = random.randint(120, 220)
            self.clouds.append((x, y, w, h, alpha))

        events_data, random_data = get_events()
        self.events = [GameEvent(e) for e in events_data]
        self.random_events_data = random_data
        self.used_random_indices = []
        self.player = Player(START_X, PLAYER_Y)
        self.camera_x = 0
        self.state = "playing"
        self.current_event = None
        self.dialog_buttons = []
        self.selected_option_idx = 0
        self.message = None
        self.face_message = None
        self.message_timer = 0
        self.random_event_counter = 0
        self.narrative = get_text("game_narrative_start")
        self.just_opened_dialog = False
        self.triggered_ids = set()
        self.flags = {}
        self.total_score = 0
        self.summary_scroll = 0
        self.summary_max_lines = 14
        self.restart_btn = Button(SCREEN_WIDTH//2 - 220, SCREEN_HEIGHT - 60, 200, 40, get_text("restart_btn"), self.font_medium)
        self.menu_btn = Button(SCREEN_WIDTH//2 + 20, SCREEN_HEIGHT - 60, 200, 40, get_text("menu_btn"), self.font_medium)

        self.move_right = False

    def _load_sound(self, path):
        try:
            s = pygame.mixer.Sound(path)
            s.set_volume(settings.sfx_volume)
            return s
        except:
            return None

    def _load_image(self, path):
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, (200, 200))
        except:
            return None

    def _stop_all_sfx(self):
        if self.correct_sound:
            self.correct_sound.stop()
        if self.wrong_sound:
            self.wrong_sound.stop()

    def _reset_dialog_buttons(self):
        self.dialog_buttons = []
        self.selected_option_idx = 0

    def _create_dialog_buttons(self, event):
        try:
            self.dialog_buttons = []
            opts = event.options
            if not opts:
                self.state = "playing"
                self.current_event = None
                return
            btn_max_width = 820
            option_lines = []
            for opt in opts:
                lines = wrap_text(opt[0], self.font_small, btn_max_width - 20)
                option_lines.append(lines)
            total_h = sum(len(lines) * (self.font_small.get_linesize() + 4) for lines in option_lines) + 20
            start_y = (SCREEN_HEIGHT - total_h) // 2 + 50
            y = start_y
            for i, lines in enumerate(option_lines):
                btn = MultiLineButton((SCREEN_WIDTH - btn_max_width) // 2, y, btn_max_width, lines, self.font_small)
                btn.opt_index = i
                btn.opt_data = opts[i]
                self.dialog_buttons.append(btn)
                y += len(lines) * (self.font_small.get_linesize() + 4) + 8
            self.selected_option_idx = 0
        except Exception as e:
            print(f"创建按钮出错: {e}")
            self.state = "playing"
            self.current_event = None

    def _check_event_triggers(self):
        try:
            for idx, ev in enumerate(self.events):
                if idx in self.triggered_ids:
                    continue
                if self.player.x >= (ev.x - TRIGGER_AHEAD):
                    self.triggered_ids.add(idx)
                    self.current_event = ev
                    if not ev.options:
                        self.state = "playing"
                        self.current_event = None
                        return False
                    self._create_dialog_buttons(ev)
                    self._stop_all_sfx()
                    self.move_right = False
                    self.state = "dialog"
                    self.just_opened_dialog = True
                    pygame.event.clear()
                    remaining = len(self.events) - len(self.triggered_ids)
                    print(f"[事件触发] {ev.title} | 剩余: {remaining}")
                    self.narrative = f"【{ev.title}】 {ev.desc[:50]}..."
                    return True
            return False
        except:
            self.state = "playing"
            self.current_event = None
            return False

    def _trigger_random_event(self):
        if self.state != "playing":
            return
        available = [i for i in range(len(self.random_events_data)) if i not in self.used_random_indices]
        if not available:
            self.used_random_indices = []
            available = list(range(len(self.random_events_data)))
        idx = random.choice(available)
        self.used_random_indices.append(idx)
        rd = self.random_events_data[idx]
        ev = GameEvent(rd, is_random=True)
        self.current_event = ev
        self._create_dialog_buttons(ev)
        self._stop_all_sfx()
        self.move_right = False
        self.state = "dialog"
        self.just_opened_dialog = True
        pygame.event.clear()
        self.narrative = f"【随机事件】{ev.desc[:60]}..."
        print(f"随机事件: {ev.title}")

    def _update_camera(self):
        target = self.player.x - SCREEN_WIDTH // 2
        target = max(0, min(target, END_X - SCREEN_WIDTH))
        self.camera_x = target

    def _apply_dialog_choice(self, idx):
        try:
            if self.current_event is None or idx < 0 or idx >= len(self.current_event.options):
                self.state = "playing"
                self._reset_dialog_buttons()
                return
            _, hp_delta, sp_delta = self.current_event.options[idx]
            self.current_event.chosen_option_idx = idx
            effect, is_bad, hp_delta_val, sp_delta_val = self.current_event.apply_choice(self.player)
            self.total_score += hp_delta_val + sp_delta_val

            self._stop_all_sfx()
            if (hp_delta_val > 0 and sp_delta_val >= 0) or (hp_delta_val >= 0 and sp_delta_val > 0):
                if self.correct_sound:
                    self.correct_sound.play()
                self.popup_img = self.correct_img
                self.face_message = None
            elif (hp_delta_val < 0 and sp_delta_val <= 0) or (hp_delta_val <= 0 and sp_delta_val < 0):
                if self.wrong_sound:
                    self.wrong_sound.play()
                self.popup_img = self.wrong_img
                self.face_message = random.choice(RAGE_FACES)
            else:
                self.popup_img = self.neutral_img
                self.face_message = None
            self.popup_timer = 60
            self.message = effect
            self.message_timer = 90
            if not self.current_event.is_random:
                chosen = self.current_event.options[idx][0]
                self.narrative = f"{get_text('chosen_prefix')}{chosen}。{get_text('best_suffix')}{self.current_event.best[:50]}..."
            else:
                self.narrative = get_text("random_event_end")
            self.state = "playing"
            self.move_right = False
            self.current_event = None
            self._reset_dialog_buttons()
            self.just_opened_dialog = False
            if not self.player.is_alive():
                self.state = "game_over"
                self.narrative = get_text("game_over")
                return
            if len(self.triggered_ids) >= len(self.events):
                self.state = "summary"
                self._generate_summary()
                print("通关！")
        except Exception as e:
            print(f"应用选项异常: {e}")
            self.state = "playing"
            self.current_event = None
            self._reset_dialog_buttons()

    def _generate_summary(self):
        if self.total_score >= 250:
            self.narrative = get_text("ending_good")
        elif self.total_score >= 50:
            self.narrative = get_text("ending_neutral")
        else:
            self.narrative = get_text("ending_bad")
        self.summary_lines = []
        for ev in self.events:
            if ev.best and ev.best != "随机事件不影响总结":
                self.summary_lines.append((ev.title, ev.best))
        self.summary_scroll = 0
        self.restart_btn.text = get_text("restart_btn")
        self.menu_btn.text = get_text("menu_btn")

    def _reset_game(self):
        self._stop_all_sfx()
        events_data, random_data = get_events()
        self.events = [GameEvent(e) for e in events_data]
        self.random_events_data = random_data
        self.used_random_indices = []
        self.player = Player(START_X, PLAYER_Y)
        self.camera_x = 0
        self.state = "playing"
        self.current_event = None
        self.message = None
        self.face_message = None
        self.message_timer = 0
        self.popup_img = None
        self.popup_timer = 0
        self.random_event_counter = 0
        self._reset_dialog_buttons()
        self.just_opened_dialog = False
        self.triggered_ids = set()
        self.flags = {}
        self.total_score = 0
        self.summary_scroll = 0
        self.move_right = False
        self.narrative = get_text("game_narrative_reset")
        print("游戏重置")

    def handle_events(self, events):
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if self.state == "playing":
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        self._reset_game()
                    elif event.key == K_ESCAPE:
                        self.game.scene = MenuScene(self.game)
                        return
                    elif event.key == K_RIGHT:
                        self.move_right = True
                elif event.type == KEYUP:
                    if event.key == K_RIGHT:
                        self.move_right = False
            elif self.state == "dialog":
                if self.just_opened_dialog:
                    self.just_opened_dialog = False
                    continue
                for i, btn in enumerate(self.dialog_buttons):
                    if btn.handle_event(event):
                        self._apply_dialog_choice(i)
                        break
                if event.type == KEYDOWN:
                    if event.key == K_UP and self.dialog_buttons:
                        self.selected_option_idx = (self.selected_option_idx - 1) % len(self.dialog_buttons)
                    elif event.key == K_DOWN and self.dialog_buttons:
                        self.selected_option_idx = (self.selected_option_idx + 1) % len(self.dialog_buttons)
                    elif event.key == K_SPACE:
                        if self.dialog_buttons and 0 <= self.selected_option_idx < len(self.dialog_buttons):
                            self._apply_dialog_choice(self.selected_option_idx)
            elif self.state == "game_over":
                if event.type == KEYDOWN and event.key == K_r:
                    self._reset_game()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    self._reset_game()
            elif self.state == "summary":
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        self._reset_game()
                        return
                    elif event.key == K_UP:
                        self.summary_scroll = max(0, self.summary_scroll - 1)
                    elif event.key == K_DOWN:
                        max_scroll = max(0, len(self.summary_lines) - self.summary_max_lines)
                        self.summary_scroll = min(max_scroll, self.summary_scroll + 1)
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if self.restart_btn.handle_event(event):
                        self._reset_game()
                        return
                    elif self.menu_btn.handle_event(event):
                        self.game.scene = MenuScene(self.game)
                        return
                    self._reset_game()

    def update(self):
        if self.state == "playing":
            if self.move_right and self.player.x < END_X:
                self.player.move_right(settings.move_speed)
                self._update_camera()
                self._check_event_triggers()
            self.random_event_counter += 1
            if self.random_event_counter >= RANDOM_EVENT_INTERVAL:
                self.random_event_counter = 0
                self._trigger_random_event()
            if self.player.x >= END_X and len(self.triggered_ids) >= len(self.events) and self.state != "summary":
                self.state = "summary"
                self._generate_summary()
                print("到达终点，通关")
        if self.message_timer > 0:
            self.message_timer -= 1
            if self.message_timer <= 0:
                self.message = None
                self.face_message = None
        if self.popup_timer > 0:
            self.popup_timer -= 1
            if self.popup_timer <= 0:
                self.popup_img = None

    def draw_background(self):
        self.screen.fill(SKY_BLUE)
        
        for (cx, cy, cw, ch, alpha) in self.clouds:
            cloud_surf = pygame.Surface((cw, ch), pygame.SRCALPHA)
            positions = [(0, ch//2), (cw//3, 0), (cw//2, ch//3), (2*cw//3, 0), (cw, ch//2)]
            for px, py in positions:
                pygame.draw.ellipse(cloud_surf, (255, 255, 255, alpha), (px, py, cw//3, ch))
            screen_x = cx - self.camera_x * 0.2
            screen_x %= (SCREEN_WIDTH + 200)
            if -200 < screen_x < SCREEN_WIDTH + 200:
                self.screen.blit(cloud_surf, (screen_x, cy))

        
        pygame.draw.rect(self.screen, BROWN, (0, SCREEN_HEIGHT-60, SCREEN_WIDTH, 60))
        pygame.draw.rect(self.screen, GREEN, (0, SCREEN_HEIGHT-65, SCREEN_WIDTH, 5))

        
        for i in range(0, END_X, 150):
            x = i - self.camera_x
            if -50 < x < SCREEN_WIDTH:
                h = 80
                pygame.draw.rect(self.screen, (100,100,100), (x, SCREEN_HEIGHT-60-h, 50, h))

        
        for ev in self.events:
            if not ev.triggered:
                x = ev.x - self.camera_x
                if 0 <= x < SCREEN_WIDTH:
                    pygame.draw.circle(self.screen, YELLOW, (x, SCREEN_HEIGHT-70), 8)
                    pygame.draw.line(self.screen, RED, (x, SCREEN_HEIGHT-70), (x, SCREEN_HEIGHT-90), 3)

        
        fx = END_X - self.camera_x
        if -100 < fx < SCREEN_WIDTH+100:
            pygame.draw.rect(self.screen, (139,69,19), (fx-20, SCREEN_HEIGHT-130, 15, 70))
            pygame.draw.rect(self.screen, (139,69,19), (fx+5, SCREEN_HEIGHT-130, 15, 70))
            pygame.draw.arc(self.screen, GREEN, (fx-25, SCREEN_HEIGHT-150, 50, 40), 0, 3.14, 5)
            ft = self.font_medium.render("ФИНИШ", True, WHITE)
            self.screen.blit(ft, (fx-30, SCREEN_HEIGHT-140))

    def draw_dialog(self, event):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0,0,0,180))
        self.screen.blit(overlay, (0,0))
        dw, dh = 900, 480
        dx = (SCREEN_WIDTH - dw) // 2
        dy = (SCREEN_HEIGHT - dh) // 2 - 30
        pygame.draw.rect(self.screen, WHITE, (dx, dy, dw, dh), border_radius=15)
        pygame.draw.rect(self.screen, BLACK, (dx, dy, dw, dh), 3, border_radius=15)
        title = self.font_large.render(event.title, True, BLUE)
        self.screen.blit(title, (dx+20, dy+15))
        desc_lines = wrap_text(event.desc, self.font_medium, dw-80)
        y = dy + 70
        for line in desc_lines:
            self.screen.blit(self.font_medium.render(line, True, BLACK), (dx+20, y))
            y += 30

        if self.dialog_buttons:
            btn_max_width = 820
            total_h = 0
            for btn in self.dialog_buttons:
                total_h += btn.height + 8
            total_h -= 8
            start_y = dy + dh - total_h - 40
            for i, btn in enumerate(self.dialog_buttons):
                btn.x = (SCREEN_WIDTH - btn_max_width) // 2
                btn.y = start_y
                btn.max_width = btn_max_width
                btn.rect.x = btn.x
                btn.rect.y = btn.y
                btn.rect.width = btn_max_width
                btn.rect.height = btn.height
                if i == self.selected_option_idx:
                    btn.color = (200,200,50)
                    btn.text_color = BLACK
                else:
                    btn.color = BLUE
                    btn.text_color = WHITE
                btn.draw(self.screen)
                start_y += btn.height + 8

        tip = self.font_small.render(get_text("dialog_tip"), True, WHITE)
        tip_rect = tip.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT-25))
        tip_bg = pygame.Surface((tip_rect.width+20, tip_rect.height+8), pygame.SRCALPHA)
        tip_bg.fill((0,0,0,200))
        self.screen.blit(tip_bg, (tip_rect.x-10, tip_rect.y-4))
        self.screen.blit(tip, tip_rect)

    def draw_summary(self):
        self.screen.fill(BLACK)
        title = self.font_large.render(get_text("game_summary_title"), True, YELLOW)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 30))

        score_text = f"{get_text('total_score_label')}{self.total_score}"
        score_surf = self.font_medium.render(score_text, True, WHITE)
        self.screen.blit(score_surf, (SCREEN_WIDTH//2 - score_surf.get_width()//2, 90))

        y = 140
        lines = wrap_text(self.narrative, self.font_medium, SCREEN_WIDTH-80)
        for line in lines:
            surf = self.font_medium.render(line, True, WHITE)
            self.screen.blit(surf, (SCREEN_WIDTH//2 - surf.get_width()//2, y))
            y += 30

        y += 20
        label = self.font_medium.render("—— " + get_text("best_suffix")[:-1] + " ——", True, YELLOW)
        self.screen.blit(label, (SCREEN_WIDTH//2 - label.get_width()//2, y))
        y += 30

        start = self.summary_scroll
        end = min(start + self.summary_max_lines, len(self.summary_lines))
        for i in range(start, end):
            title, best = self.summary_lines[i]
            text = f"{i+1}. {title}：{best}"
            lines = wrap_text(text, self.font_small, SCREEN_WIDTH-60)
            for line in lines:
                surf = self.font_small.render(line, True, WHITE)
                self.screen.blit(surf, (30, y))
                y += 22
            y += 5
            if y > SCREEN_HEIGHT - 120:
                break

        if len(self.summary_lines) > self.summary_max_lines:
            hint_text = get_text("scroll_hint").format(start+1, end, len(self.summary_lines))
            hint = self.font_small.render(hint_text, True, GRAY)
            self.screen.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, SCREEN_HEIGHT - 80))

        self.restart_btn.draw(self.screen)
        self.menu_btn.draw(self.screen)

    def draw_game_over(self):
        self.screen.fill(BLACK)
        over = self.font_large.render(get_text("game_over_title"), True, RED)
        restart = self.font_medium.render(get_text("game_over_hint"), True, WHITE)
        self.screen.blit(over, (SCREEN_WIDTH//2 - over.get_width()//2, SCREEN_HEIGHT//2-50))
        self.screen.blit(restart, (SCREEN_WIDTH//2 - restart.get_width()//2, SCREEN_HEIGHT//2+20))

    def draw(self, screen):
        if self.state == "playing":
            self.draw_background()
            self.player.draw(screen, self.camera_x)
            if self.popup_img:
                r = self.popup_img.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-100))
                screen.blit(self.popup_img, r)
            if self.message:
                msg = self.font_medium.render(self.message, True, YELLOW)
                msg_r = msg.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT-150))
                screen.blit(msg, msg_r)
            if self.face_message:
                face = self.font_large.render(self.face_message, True, RED)
                face_r = face.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT-200))
                screen.blit(face, face_r)
            self.player.draw_status_bars(screen, self.font_small)
            if self.player.x >= END_X and len(self.triggered_ids) < len(self.events):
                remaining = len(self.events) - len(self.triggered_ids)
                w1 = self.font_medium.render(get_text("game_warn_incomplete"), True, RED)
                w2 = self.font_small.render(get_text("game_warn_remaining").format(remaining), True, YELLOW)
                r1 = w1.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-40))
                r2 = w2.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2+10))
                bg = pygame.Rect(r1.x-20, r1.y-10, r1.width+40, r2.height+r1.height+20)
                s = pygame.Surface((bg.width, bg.height), pygame.SRCALPHA)
                s.fill((0,0,0,200))
                screen.blit(s, (bg.x, bg.y))
                screen.blit(w1, r1)
                screen.blit(w2, r2)
            nb_height = 50
            nb = pygame.Surface((SCREEN_WIDTH, nb_height), pygame.SRCALPHA)
            nb.fill((0,0,0,180))
            screen.blit(nb, (0, SCREEN_HEIGHT - nb_height))
            narr_lines = wrap_text(self.narrative, self.font_small, SCREEN_WIDTH-40)
            for i, line in enumerate(narr_lines):
                screen.blit(self.font_small.render(line, True, WHITE), (20, SCREEN_HEIGHT- nb_height + i*22))
        elif self.state == "dialog":
            self.draw_background()
            self.player.draw(screen, self.camera_x)
            self.player.draw_status_bars(screen, self.font_small)
            self.draw_dialog(self.current_event)
        elif self.state == "game_over":
            self.draw_game_over()
        elif self.state == "summary":
            self.draw_summary()