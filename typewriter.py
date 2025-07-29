import numpy as np
import pygame
import threading
import time
from pynput import keyboard
import rumps
import sys
import os

class TypewriterApp(rumps.App):
    def __init__(self):
        super(TypewriterApp, self).__init__("⌨️", quit_button="Quit")
        self.menu = ["Toggle Sounds"]
        
        try:
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=1, buffer=1024)
            pygame.mixer.init()
            self.sound = self.create_typewriter_sound()
        except Exception as e:
            print(f"Audio init failed: {e}")
            self.sound = None
        
        # Keyboard listener
        self.listener = None
        self.sounds_enabled = True
        self.start_listening()
    
    def create_typewriter_sound(self):
        sample_rate = 22050
        duration = 0.04
        
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        noise = np.random.normal(0, 0.3, len(t))
        for i in range(1, len(noise)):
            noise[i] = noise[i] * 0.6 + noise[i-1] * 0.4
        thud = (np.sin(2 * np.pi * 80 * t) * 0.5 + 
                np.sin(2 * np.pi * 160 * t) * 0.3)
        
        click = (np.sin(2 * np.pi * 600 * t) * 0.4 +
                np.sin(2 * np.pi * 900 * t) * 0.2)
        
        envelope = np.exp(-t * 100) * (1 - np.exp(-t * 1200))
        sustain_env = np.exp(-t * 40) * 0.3
        combined_env = envelope + sustain_env
        
        sound_wave = (noise * 0.8 + thud * 0.6 + click * 0.5) * combined_env * 0.3
        
        sound_array = (sound_wave * 32767).astype(np.int16)
        sound_array = np.ascontiguousarray(sound_array)
        
        return pygame.sndarray.make_sound(sound_array)
    
    def start_listening(self):
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()
    
    def stop_listening(self):
        if self.listener:
            self.listener.stop()
            self.listener = None
    
    def on_key_press(self, key):
        if self.sounds_enabled and self.sound:
            try:
                self.sound.play()
            except:
                pass  # Ignore audio errors
    
    @rumps.clicked("Toggle Sounds")
    def toggle_sounds(self, _):
        self.sounds_enabled = not self.sounds_enabled
        if self.sounds_enabled:
            self.title = "⌨️"
            self.menu["Toggle Sounds"].title = "Disable Sounds"
        else:
            self.title = "⌨️💤"
            self.menu["Toggle Sounds"].title = "Enable Sounds"

def check_permissions():
    try:
        test_listener = keyboard.Listener(on_press=lambda key: None)
        test_listener.start()
        test_listener.stop()
        return True
    except:
        return False

def request_permissions():
    print("\n⚠️  Accessibility permissions required!")
    print("1. Open System Preferences > Security & Privacy > Privacy")
    print("2. Select 'Accessibility' from the left sidebar")
    print("3. Click the lock to make changes")
    print("4. Add Terminal (or your Python IDE) to the list")
    print("5. Restart this application\n")
    
    input("Press Enter after granting permissions...")

def main():
    try:
        import rumps
        import pynput
        import pygame
        import numpy as np
    except ImportError as e:
        print(f"Missing required package: {e}")
        print("Install with: pip install rumps pynput pygame numpy")
        sys.exit(1)
    
    if not check_permissions():
        request_permissions()
        sys.exit(1)
    
    app = TypewriterApp()
    app.run()

if __name__ == "__main__":
    main()
