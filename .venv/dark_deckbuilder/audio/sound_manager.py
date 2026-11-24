import os
import arcade
from config import resource_path
from core.events import bus
from audio.synth import generate_sfx_bank


class SoundManager:
    """Управляет звуковыми эффектами игры через подписку на EventBus."""

    def __init__(self):
        self.enabled: bool = True
        self.sfx_volume: float = 0.65
        self.sounds: dict[str, arcade.Sound] = {}
        self._load_sounds()
        self._bind_events()

    def _load_sounds(self):
        # 1. Генерируем базовый набор процедурных звуков в памяти
        self.sounds = generate_sfx_bank()

        # 2. Если в data/sounds/ появятся пользовательские .wav файлы — заменяем ими синтез
        custom_dir = resource_path(os.path.join("data", "sounds"))
        if os.path.isdir(custom_dir):
            for key in list(self.sounds.keys()):
                wav_path = os.path.join(custom_dir, f"{key}.wav")
                if os.path.isfile(wav_path):
                    self.sounds[key] = arcade.load_sound(wav_path)

    def _bind_events(self):
        bus.subscribe("ui_click", lambda **_: self.play("ui_click", vol_mult=0.55))
        bus.subscribe("card_played", lambda **_: self.play("card_play"))
        bus.subscribe("damage_dealt", self._on_damage)
        bus.subscribe("block_gained", lambda **_: self.play("block"))
        bus.subscribe("heal_gained", lambda **_: self.play("heal"))
        bus.subscribe("stamina_gained", lambda **_: self.play("heal", vol_mult=0.7))

    def _on_damage(self, value: int = 0, blocked: int = 0, **_):
        if value <= 0 and blocked > 0:
            self.play("block")
        elif value >= 14:
            self.play("hit_heavy")
        elif value > 0:
            self.play("hit_normal")

    def play(self, name: str, vol_mult: float = 1.0):
        if not self.enabled or self.sfx_volume <= 0.0:
            return
        snd = self.sounds.get(name)
        if snd:
            arcade.play_sound(snd, volume=min(1.0, self.sfx_volume * vol_mult))


# Глобальный звуковой менеджер
sound_manager = SoundManager()
