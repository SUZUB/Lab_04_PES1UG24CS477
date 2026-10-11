import os
import math
import wave
import struct
import random
import pygame

class SoundManager:
    def __init__(self):
        self.enabled = False
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.enabled = True
        except Exception:
            self.enabled = False

        self.sounds = {}
        if self.enabled:
            self._ensure_sound_files()
            self._load_sounds()

    def _ensure_sound_files(self):
        sound_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "sounds")
        os.makedirs(sound_dir, exist_ok=True)
        files = {
            "laser.wav": self._gen_laser,
            "explosion.wav": self._gen_explosion,
            "hit.wav": self._gen_hit,
            "ufo.wav": self._gen_ufo,
            "game_over.wav": self._gen_game_over
        }
        for name, generator in files.items():
            path = os.path.join(sound_dir, name)
            if not os.path.exists(path):
                samples = generator()
                self._write_wav(path, samples)

    def _write_wav(self, path, samples, rate=44100):
        with wave.open(path, "w") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(rate)
            raw = bytearray()
            for s in samples:
                val = max(-32767, min(32767, int(s * 32767)))
                raw.extend(struct.pack("<h", val))
            wav_file.writeframes(raw)

    def _gen_laser(self, rate=44100):
        dur = 0.14
        n = int(dur * rate)
        data = []
        for i in range(n):
            t = i / rate
            freq = 950 - (700 * (t / dur))
            env = (1 - t / dur) ** 1.5
            data.append(math.sin(2 * math.pi * freq * t) * env)
        return data

    def _gen_explosion(self, rate=44100):
        dur = 0.35
        n = int(dur * rate)
        data = []
        for i in range(n):
            t = i / rate
            env = (1 - t / dur) ** 1.8
            noise = random.random() * 2 - 1
            tone = math.sin(2 * math.pi * 90 * t)
            data.append((noise * 0.75 + tone * 0.25) * env)
        return data

    def _gen_hit(self, rate=44100):
        dur = 0.22
        n = int(dur * rate)
        data = []
        for i in range(n):
            t = i / rate
            env = (1 - t / dur) ** 1.2
            freq = 320 - (180 * (t / dur))
            noise = random.random() * 2 - 1
            data.append((noise * 0.5 + math.sin(2 * math.pi * freq * t) * 0.5) * env)
        return data

    def _gen_ufo(self, rate=44100):
        dur = 0.3
        n = int(dur * rate)
        data = []
        for i in range(n):
            t = i / rate
            freq = 600 + 150 * math.sin(2 * math.pi * 12 * t)
            data.append(math.sin(2 * math.pi * freq * t) * 0.6)
        return data

    def _gen_game_over(self, rate=44100):
        dur = 0.8
        n = int(dur * rate)
        tones = [350, 300, 250, 180]
        data = []
        for i in range(n):
            t = i / rate
            step = min(int((t / dur) * len(tones)), len(tones) - 1)
            freq = tones[step]
            step_t = (t % (dur / len(tones))) / (dur / len(tones))
            env = max(0.0, 1.0 - step_t)
            data.append(math.sin(2 * math.pi * freq * t) * env * 0.7)
        return data

    def _load_sounds(self):
        sound_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "sounds")
        names = ["laser", "explosion", "hit", "ufo", "game_over"]
        for name in names:
            path = os.path.join(sound_dir, f"{name}.wav")
            if os.path.exists(path):
                try:
                    sound = pygame.mixer.Sound(path)
                    sound.set_volume(0.4)
                    self.sounds[name] = sound
                except Exception:
                    pass

    def play(self, name):
        if not self.enabled:
            return
        sound = self.sounds.get(name)
        if sound:
            try:
                sound.play()
            except Exception:
                pass

    def play_laser(self):
        self.play("laser")

    def play_explosion(self):
        self.play("explosion")

    def play_hit(self):
        self.play("hit")

    def play_ufo(self):
        self.play("ufo")

    def play_game_over(self):
        self.play("game_over")
