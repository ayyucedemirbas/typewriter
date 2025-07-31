import numpy as np
import pygame
import threading
import time
from pynput import keyboard
import rumps
import sys
import os
import random

class TypewriterApp(rumps.App):
    def __init__(self):
        super(TypewriterApp, self).__init__("⌨️", quit_button="Quit")
        
        # Initialize menu
        self.menu = [
            "Toggle Sounds",
            None,  # Separator
            rumps.MenuItem("Typewriter Model", callback=None),
            rumps.MenuItem("  Classic Typewriter", callback=self.set_classic_model),
            rumps.MenuItem("  IBM Selectric", callback=self.set_ibm_model),
            rumps.MenuItem("  Mechanical Keyboard", callback=self.set_mechanical_model),
            None,  # Separator
            rumps.MenuItem("Volume", callback=None),
            rumps.MenuItem("  Low (25%)", callback=self.set_volume_low),
            rumps.MenuItem("  Medium (50%)", callback=self.set_volume_medium),
            rumps.MenuItem("  High (75%)", callback=self.set_volume_high),
            rumps.MenuItem("  Maximum (100%)", callback=self.set_volume_max),
        ]
        
        # Sound settings
        self.typewriter_model = "classic"  # classic, ibm, mechanical
        self.volume_level = 0.75  # 0.0 to 1.0
        self.sounds = {}  # Will store different sounds
        
        try:
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=1, buffer=1024)
            pygame.mixer.init()
            self.create_all_sounds()
        except Exception as e:
            print(f"Audio init failed: {e}")
            self.sounds = {}
        
        # Keyboard listener
        self.listener = None
        self.sounds_enabled = True
        self.update_menu_checkmarks()
        self.start_listening()
    
    def create_all_sounds(self):
        """Create all sound variations for different keys and models"""
        key_types = ['regular', 'space', 'enter', 'backspace', 'number', 
                    'punctuation', 'symbol', 'tab', 'modifier', 'arrow', 'special']
        
        self.sounds = {}
        for model in ['classic', 'ibm', 'mechanical']:
            self.sounds[model] = {}
            for key_type in key_types:
                self.sounds[model][key_type] = self.create_typewriter_sound(model, key_type)
    
    def create_typewriter_sound(self, model='classic', key_type='regular'):
        sample_rate = 22050
        
        # Adjust duration and characteristics based on key type
        if key_type == 'space':
            duration = 0.08
            base_freq_mult = 0.6  # Much deeper sound
            velocity = 0.9  # Spacebar is hit harder
        elif key_type == 'enter':
            duration = 0.12
            base_freq_mult = 0.75
            velocity = 1.1  # Enter is often hit with force
        elif key_type == 'backspace':
            duration = 0.03
            base_freq_mult = 1.3  # Higher pitch
            velocity = 0.8  # Usually lighter touch
        elif key_type == 'tab':
            duration = 0.06
            base_freq_mult = 0.8  # Slightly deeper
            velocity = 0.85
        elif key_type == 'number':
            duration = 0.04
            base_freq_mult = 1.1  # Slightly higher pitch
            velocity = 0.85 + random.random() * 0.2
        elif key_type == 'punctuation':
            duration = 0.035
            base_freq_mult = 1.15  # Higher pitch for precision
            velocity = 0.8 + random.random() * 0.2
        elif key_type == 'symbol':
            duration = 0.04
            base_freq_mult = 1.2  # Higher pitch
            velocity = 0.9 + random.random() * 0.2
        elif key_type == 'modifier':
            duration = 0.07
            base_freq_mult = 0.7  # Deeper, longer keys
            velocity = 0.75  # Usually lighter touch
        elif key_type == 'arrow':
            duration = 0.035
            base_freq_mult = 1.1
            velocity = 0.7  # Light touch
        elif key_type == 'special':
            duration = 0.04
            base_freq_mult = 0.95
            velocity = 0.8
        else:  # regular
            duration = 0.045
            base_freq_mult = 1.0
            velocity = 0.85 + random.random() * 0.3  # Vary typing force
        
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        # More sophisticated random variations
        pitch_variation = 1.0 + (random.random() - 0.5) * 0.15
        timing_variation = 1.0 + (random.random() - 0.5) * 0.05
        
        # Enhanced noise generation - multiple layers
        white_noise = np.random.normal(0, 0.2, len(t))
        # Pink noise simulation (filtered white noise)
        pink_noise = np.zeros_like(white_noise)
        for i in range(1, len(pink_noise)):
            pink_noise[i] = pink_noise[i-1] * 0.7 + white_noise[i] * 0.3
        
        # Add mechanical resonance noise
        resonance_freq = 40 + random.random() * 20
        mechanical_noise = np.sin(2 * np.pi * resonance_freq * t) * np.exp(-t * 80) * 0.1
        
        # Combine noise layers
        noise = (white_noise * 0.4 + pink_noise * 0.5 + mechanical_noise) * velocity
        
        # Model-specific sophisticated sound generation
        if model == 'classic':
            # Classic typewriter - complex mechanical sound
            # Hammer impact frequencies
            hammer1 = np.sin(2 * np.pi * 75 * base_freq_mult * t * pitch_variation) * 0.6
            hammer2 = np.sin(2 * np.pi * 150 * base_freq_mult * t * pitch_variation) * 0.4
            hammer3 = np.sin(2 * np.pi * 225 * base_freq_mult * t * pitch_variation) * 0.2
            
            # Type bar impact
            impact1 = np.sin(2 * np.pi * 580 * base_freq_mult * t * pitch_variation) * 0.5
            impact2 = np.sin(2 * np.pi * 870 * base_freq_mult * t * pitch_variation) * 0.3
            impact3 = np.sin(2 * np.pi * 1160 * base_freq_mult * t * pitch_variation) * 0.2
            
            # Metal spring resonance
            spring = np.sin(2 * np.pi * 320 * t) * np.exp(-t * 60) * 0.3
            
            thud = hammer1 + hammer2 + hammer3 + spring
            click = impact1 + impact2 + impact3
            noise_weight, thud_weight, click_weight = 0.7, 0.8, 0.6
            
        elif model == 'ibm':
            # IBM Selectric - ball mechanism sound
            # Selectric ball rotation
            ball_freq = 110 * base_freq_mult * pitch_variation
            ball_impact = (np.sin(2 * np.pi * ball_freq * t) * 0.5 + 
                          np.sin(2 * np.pi * ball_freq * 2 * t) * 0.3 +
                          np.sin(2 * np.pi * ball_freq * 3 * t) * 0.2)
            
            # Electric motor harmonics
            motor = np.sin(2 * np.pi * 60 * t) * np.exp(-t * 40) * 0.2
            
            # Sharp contact sound
            contact1 = np.sin(2 * np.pi * 900 * base_freq_mult * t * pitch_variation) * 0.6
            contact2 = np.sin(2 * np.pi * 1350 * base_freq_mult * t * pitch_variation) * 0.4
            contact3 = np.sin(2 * np.pi * 1800 * base_freq_mult * t * pitch_variation) * 0.2
            
            thud = ball_impact + motor
            click = contact1 + contact2 + contact3
            noise_weight, thud_weight, click_weight = 0.4, 0.7, 0.9
            
        else:  # mechanical keyboard
            # Mechanical switch sound - very detailed
            # Switch housing resonance
            housing = np.sin(2 * np.pi * 95 * base_freq_mult * t * pitch_variation) * 0.4
            
            # Spring compression/release
            spring_comp = np.sin(2 * np.pi * 180 * t) * np.exp(-t * 120) * 0.3
            spring_rel = np.sin(2 * np.pi * 220 * t) * np.exp(-t * 80) * 0.2
            
            # Sharp click frequencies (tactile feedback)
            click1 = np.sin(2 * np.pi * 1200 * base_freq_mult * t * pitch_variation) * 0.7
            click2 = np.sin(2 * np.pi * 1800 * base_freq_mult * t * pitch_variation) * 0.5
            click3 = np.sin(2 * np.pi * 2400 * base_freq_mult * t * pitch_variation) * 0.3
            click4 = np.sin(2 * np.pi * 3000 * base_freq_mult * t * pitch_variation) * 0.2
            
            thud = housing + spring_comp + spring_rel
            click = click1 + click2 + click3 + click4
            noise_weight, thud_weight, click_weight = 0.2, 0.4, 1.0
        
        # More realistic envelope shapes
        if key_type == 'enter':
            # Enter key: Sharp attack, bell-like sustain
            bell_freq = 1400 + random.random() * 200
            bell = np.sin(2 * np.pi * bell_freq * t) * np.exp(-t * 45) * 0.4
            
            # Multi-stage envelope for complex attack
            attack = np.exp(-t * 200) * (1 - np.exp(-t * 2000))
            sustain = np.exp(-t * 25) * 0.5
            decay = np.exp(-t * 60) * 0.3
            combined_env = attack + sustain + decay
            
            sound_wave = (noise * noise_weight + thud * thud_weight + 
                         click * click_weight + bell) * combined_env * 0.35
            
        elif key_type == 'space':
            # Spacebar: Longer, deeper envelope
            attack = np.exp(-t * 150) * (1 - np.exp(-t * 1500))
            sustain = np.exp(-t * 20) * 0.6
            combined_env = attack + sustain
            
            sound_wave = (noise * noise_weight + thud * thud_weight + 
                         click * click_weight) * combined_env * 0.4
            
        elif key_type == 'backspace':
            # Backspace: Quick, sharp envelope
            attack = np.exp(-t * 300) * (1 - np.exp(-t * 3000))
            decay = np.exp(-t * 100) * 0.2
            combined_env = attack + decay
            
            sound_wave = (noise * noise_weight + thud * thud_weight + 
                         click * click_weight) * combined_env * 0.25
        else:
            # Regular keys: Natural typing envelope with micro-variations
            attack_speed = 180 + random.random() * 40
            sustain_speed = 35 + random.random() * 10
            
            attack = np.exp(-t * attack_speed) * (1 - np.exp(-t * (1400 + random.random() * 400)))
            sustain = np.exp(-t * sustain_speed) * (0.25 + random.random() * 0.1)
            combined_env = attack + sustain
            
            sound_wave = (noise * noise_weight + thud * thud_weight + 
                         click * click_weight) * combined_env * (0.28 + random.random() * 0.04)
        
        # Add subtle reverb effect for realism
        reverb_delay = int(sample_rate * 0.008)  # 8ms delay
        if len(sound_wave) > reverb_delay:
            reverb = np.zeros_like(sound_wave)
            reverb[reverb_delay:] = sound_wave[:-reverb_delay] * 0.08
            sound_wave = sound_wave + reverb
        
        # Apply velocity and volume
        sound_wave *= velocity * self.volume_level
        
        # Soft limiting to prevent clipping while maintaining dynamics
        max_val = np.max(np.abs(sound_wave))
        if max_val > 0.95:
            sound_wave = np.tanh(sound_wave * 0.8) * 0.95
        
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
    
    def get_key_type(self, key):
        """Determine the type of key pressed with more detailed classification"""
        try:
            if hasattr(key, 'char') and key.char:
                # Character keys
                if key.char == ' ':
                    return 'space'
                elif key.char.isalpha():
                    return 'regular'
                elif key.char.isdigit():
                    return 'number'
                elif key.char in ',.?!;:':
                    return 'punctuation'
                else:
                    return 'symbol'
            else:
                # Special keys
                if key == keyboard.Key.enter:
                    return 'enter'
                elif key == keyboard.Key.backspace:
                    return 'backspace'
                elif key == keyboard.Key.space:
                    return 'space'
                elif key == keyboard.Key.tab:
                    return 'tab'
                elif key in [keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r]:
                    return 'modifier'
                elif key in [keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r,
                           keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r,
                           keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r]:
                    return 'modifier'
                elif key in [keyboard.Key.up, keyboard.Key.down, keyboard.Key.left, keyboard.Key.right]:
                    return 'arrow'
                else:
                    return 'special'
        except:
            return 'regular'
    
    def on_key_press(self, key):
        if self.sounds_enabled and self.sounds:
            try:
                key_type = self.get_key_type(key)
                if self.typewriter_model in self.sounds:
                    sound = self.sounds[self.typewriter_model].get(key_type)
                    if sound:
                        sound.play()
            except:
                pass  # Ignore audio errors
    
    def update_menu_checkmarks(self):
        """Update menu checkmarks to reflect current settings"""
        # Clear all checkmarks first
        for item_title in ["  Classic Typewriter", "  IBM Selectric", "  Mechanical Keyboard"]:
            if item_title in self.menu:
                self.menu[item_title].state = 0
        
        for item_title in ["  Low (25%)", "  Medium (50%)", "  High (75%)", "  Maximum (100%)"]:
            if item_title in self.menu:
                self.menu[item_title].state = 0
        
        # Set current model checkmark
        model_items = {
            "classic": "  Classic Typewriter",
            "ibm": "  IBM Selectric", 
            "mechanical": "  Mechanical Keyboard"
        }
        if self.typewriter_model in model_items:
            item_title = model_items[self.typewriter_model]
            if item_title in self.menu:
                self.menu[item_title].state = 1
        
        # Set current volume checkmark
        volume_items = {
            0.25: "  Low (25%)",
            0.5: "  Medium (50%)",
            0.75: "  High (75%)",
            1.0: "  Maximum (100%)"
        }
        if self.volume_level in volume_items:
            item_title = volume_items[self.volume_level]
            if item_title in self.menu:
                self.menu[item_title].state = 1

    # Model selection methods
    def set_classic_model(self, _):
        self.typewriter_model = "classic"
        self.update_menu_checkmarks()
    
    def set_ibm_model(self, _):
        self.typewriter_model = "ibm"
        self.update_menu_checkmarks()
    
    def set_mechanical_model(self, _):
        self.typewriter_model = "mechanical"
        self.update_menu_checkmarks()
    
    # Volume control methods
    def set_volume_low(self, _):
        self.volume_level = 0.25
        self.create_all_sounds()  # Recreate sounds with new volume
        self.update_menu_checkmarks()
    
    def set_volume_medium(self, _):
        self.volume_level = 0.5
        self.create_all_sounds()
        self.update_menu_checkmarks()
    
    def set_volume_high(self, _):
        self.volume_level = 0.75
        self.create_all_sounds()
        self.update_menu_checkmarks()
    
    def set_volume_max(self, _):
        self.volume_level = 1.0
        self.create_all_sounds()
        self.update_menu_checkmarks()

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
