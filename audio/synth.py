import os
import math
import random
import tempfile
import struct
import wave
import arcade


def _build_wav_sound(name: str, samples: list[float], sample_rate: int = 22050) -> arcade.Sound:
    """Записывает сгенерированный .wav во временную папку ОС и загружает через arcade.Sound."""
    cache_dir = os.path.join(tempfile.gettempdir(), "dark_deckbuilder_sfx")
    os.makedirs(cache_dir, exist_ok=True)
    wav_path = os.path.join(cache_dir, f"{name}.wav")

    with wave.open(wav_path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        raw = bytearray()
        for s in samples:
            clamped = max(-1.0, min(1.0, s))
            raw.extend(struct.pack("<h", int(clamped * 32767)))
        wf.writeframes(raw)

    return arcade.Sound(wav_path)


def generate_sfx_bank() -> dict[str, arcade.Sound]:
    """Генерирует набор процедурных звуковых эффектов для тёмного колодостроя."""
    sr = 22050
    bank: dict[str, arcade.Sound] = {}

    # 1. Мягкий приглушённый клик кнопки (плавная атака + низкий тёплый тон)
    click_samples = []
    dur_click = 0.065
    for i in range(int(sr * dur_click)):
        t = i / sr
        attack = min(1.0, t / 0.008)  # Плавное нарастание за 8 мс убирает резкий щелчок
        decay = math.exp(-t * 52.0)
        freq = 330.0 - 70.0 * (t / dur_click)  # Мягкий спад частоты вниз (330 -> 260 Гц)
        val = math.sin(2 * math.pi * freq * t) * attack * decay * 0.18
        click_samples.append(val)
    bank["ui_click"] = _build_wav_sound("ui_click", click_samples, sr)

    # 2. Мягкий шелест карты (свист пергамента)
    card_samples = []
    dur_card = 0.14
    for i in range(int(sr * dur_card)):
        t = i / sr
        env = math.sin(math.pi * (t / dur_card)) ** 1.5
        noise = random.uniform(-1.0, 1.0)
        tone = math.sin(2 * math.pi * (240 + 420 * (t / dur_card)) * t)
        card_samples.append((noise * 0.35 + tone * 0.25) * env * 0.3)
    bank["card_play"] = _build_wav_sound("card_play", card_samples, sr)

    # 3. Обычный удар (резкий лязг + низкий толчок)
    hit_samples = []
    dur_hit = 0.18
    for i in range(int(sr * dur_hit)):
        t = i / sr
        env = math.exp(-t * 24.0)
        freq = 165 * math.exp(-t * 9.0) + 45
        noise = random.uniform(-1.0, 1.0) * math.exp(-t * 40.0)
        val = (math.sin(2 * math.pi * freq * t) * 0.7 + noise * 0.5) * env * 0.55
        hit_samples.append(val)
    bank["hit_normal"] = _build_wav_sound("hit_normal", hit_samples, sr)

    # 4. Тяжёлый / критический удар (глубокий бас + звон стали)
    heavy_samples = []
    dur_heavy = 0.30
    for i in range(int(sr * dur_heavy)):
        t = i / sr
        env = math.exp(-t * 14.0)
        bass = math.sin(2 * math.pi * (95 * math.exp(-t * 6.0) + 32) * t)
        clang = math.sin(2 * math.pi * 540 * t) * math.exp(-t * 28.0)
        noise = random.uniform(-1.0, 1.0) * math.exp(-t * 30.0)
        heavy_samples.append((bass * 0.75 + clang * 0.35 + noise * 0.4) * env * 0.65)
    bank["hit_heavy"] = _build_wav_sound("hit_heavy", heavy_samples, sr)

    # 5. Блок щитом (глухой металлический звон)
    block_samples = []
    dur_block = 0.20
    for i in range(int(sr * dur_block)):
        t = i / sr
        env = math.exp(-t * 20.0)
        val = (
            math.sin(2 * math.pi * 310 * t) * 0.5
            + math.sin(2 * math.pi * 465 * t) * 0.35
            + math.sin(2 * math.pi * 120 * t) * 0.4
        ) * env * 0.45
        block_samples.append(val)
    bank["block"] = _build_wav_sound("block", block_samples, sr)

    # 6. Магическое исцеление / усиление (мягкий восходящий аккорд)
    heal_samples = []
    dur_heal = 0.32
    for i in range(int(sr * dur_heal)):
        t = i / sr
        env = math.sin(math.pi * (t / dur_heal)) * math.exp(-t * 4.5)
        f1 = 440 + 180 * (t / dur_heal)
        f2 = 554 + 220 * (t / dur_heal)
        val = (math.sin(2 * math.pi * f1 * t) + 0.7 * math.sin(2 * math.pi * f2 * t)) * env * 0.3
        heal_samples.append(val)
    bank["heal"] = _build_wav_sound("heal", heal_samples, sr)


    return bank
