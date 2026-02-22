import customtkinter as ctk
import sys
import io
import requests
from tkinter import font as tkfont

# --- 1. ENHANCED JUNGLE THEME CONFIGURATION ---
class JungleTheme:
    # Core jungle palette - Enhanced with more depth
    DARK_JUNGLE = "#0a1a0a"           # Deeper forest background
    JUNGLE_GREEN = "#1a3d1a"          # Panel backgrounds
    LEAF_GREEN = "#2d5a2d"            # Secondary elements
    VINE_GREEN = "#4a7c4a"            # Borders/accents
    MOSS_GREEN = "#3d6b3d"            # New: intermediate shade
    
    # Banana/Monkey accents - More vibrant
    BANANA_YELLOW = "#ffd700"         # Brighter primary accent
    RIPE_BANANA = "#ffe135"           # Hover states
    BROWN_MONKEY = "#5c4033"          # Dark accents
    MONKEY_FUR = "#8b6f47"            # Secondary brown
    LIGHT_BROWN = "#a67c52"           # New: lighter brown for highlights
    
    # Functional colors - Enhanced contrast
    CODE_BG = "#0d1f0d"               # Editor background (dark green)
    CONSOLE_BG = "#050f05"            # Darker console background
    TEXT_LIGHT = "#e8f5e9"            # Light text
    TEXT_DIM = "#a5d6a7"              # Dimmed text for line numbers
    SYNTAX_GREEN = "#69f0ae"          # Code text
    SYNTAX_YELLOW = "#ffeb3b"         # Keywords highlight
    ERROR_RED = "#ff5252"             # Errors (more vibrant)
    SUCCESS_GREEN = "#00e676"         # Success states
    WARNING_ORANGE = "#ff9800"        # Warnings
    
    # New: Gradient-like accents
    SHADOW_DARK = "#051005"           # For depth/shadows
    HIGHLIGHT_LIGHT = "#5a9a5a"       # For highlights/borders

# Apply theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class MonkeyIDE(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup with jungle vibes
        self.title("🌴 Riri's Jungle IDE 🐵")
        self.geometry("1200x850")
        self.minsize(900, 600)
        self.configure(fg_color=JungleTheme.DARK_JUNGLE)
        
        # Animation state
        self.banana_count = 3
        self.animation_running = False

        # Configure Grid Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=3)  # Code editor
        self.grid_rowconfigure(2, weight=0)  # Toolbar
        self.grid_rowconfigure(3, weight=1)  # Console

        # --- ROW 0: ENHANCED JUNGLE HEADER ---
        self._create_header()

        # --- ROW 1: CODE EDITOR (The "Banana Patch") ---
        self._create_editor()

        # --- ROW 2: JUNGLE TOOLBAR ---
        self._create_toolbar()

        # --- ROW 3: OUTPUT CONSOLE (The "Jungle Floor") ---
        self._create_console()

        # Welcome message
        self._print_welcome()

    def _create_header(self):
        """Create an enhanced themed header with gradient-like effect"""
        # Main header with layered design
        header_container = ctk.CTkFrame(
            self, 
            fg_color="transparent",
            corner_radius=0,
            height=70
        )
        header_container.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header_container.grid_propagate(False)
        
        # Background layer with gradient simulation
        header_bg = ctk.CTkFrame(
            header_container,
            fg_color=JungleTheme.JUNGLE_GREEN,
            corner_radius=0,
            height=70
        )
        header_bg.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Top highlight strip (simulates light hitting leaves)
        top_highlight = ctk.CTkFrame(
            header_container,
            fg_color=JungleTheme.MOSS_GREEN,
            corner_radius=0,
            height=2
        )
        top_highlight.place(relx=0, rely=0, relwidth=1)

        # Left side: Enhanced logo area
        logo_frame = ctk.CTkFrame(
            header_container,
            fg_color=JungleTheme.LEAF_GREEN,
            corner_radius=15,
            width=200,
            height=50
        )
        logo_frame.place(x=20, rely=0.5, anchor="w")
        
        # Monkey icon with shadow effect
        shadow_label = ctk.CTkLabel(
            logo_frame,
            text="🐵",
            font=("Segoe UI Emoji", 26),
            text_color=JungleTheme.SHADOW_DARK
        )
        shadow_label.place(x=12, y=12)
        
        monkey_label = ctk.CTkLabel(
            logo_frame,
            text="🐵",
            font=("Segoe UI Emoji", 26)
        )
        monkey_label.place(x=10, y=10)
        
        # Title with enhanced styling
        title_label = ctk.CTkLabel(
            logo_frame,
            text="Riri's IDE",
            font=("Consolas", 18, "bold"),
            text_color=JungleTheme.BANANA_YELLOW
        )
        title_label.place(x=50, rely=0.5, anchor="w")

        # Center: Animated tagline
        self.tagline_label = ctk.CTkLabel(
            header_container,
            text="🌿 Code Like a Monkey, Think Like a Jungle 🌿",
            font=("Comic Sans MS", 14, "italic"),
            text_color=JungleTheme.TEXT_DIM
        )
        self.tagline_label.place(relx=0.5, rely=0.5, anchor="center")

        # Right: Banana counter with decorative frame
        banana_frame = ctk.CTkFrame(
            header_container,
            fg_color=JungleTheme.BROWN_MONKEY,
            corner_radius=15,
            width=120,
            height=50
        )
        banana_frame.place(x=1160, rely=0.5, anchor="e")
        
        self.banana_label = ctk.CTkLabel(
            banana_frame,
            text="🍌 🍌 🍌",
            font=("Segoe UI Emoji", 16)
        )
        self.banana_label.place(relx=0.5, rely=0.5, anchor="center")

        # Bottom border (vine decoration)
        vine = ctk.CTkFrame(
            header_container,
            fg_color=JungleTheme.VINE_GREEN,
            height=4,
            corner_radius=0
        )
        vine.place(relx=0, rely=1, relwidth=1, anchor="sw")
        
        # Add subtle leaves decoration on the vine
        for i in range(6):
            leaf = ctk.CTkLabel(
                vine,
                text="🍃",
                font=("Segoe UI Emoji", 10)
            )
            leaf.place(relx=i/5, rely=0.5, anchor="center")

    def _create_editor(self):
        """Create the code editor with enhanced visual design"""
        # Outer glow container
        glow_container = ctk.CTkFrame(
            self,
            fg_color=JungleTheme.VINE_GREEN,
            corner_radius=15
        )
        glow_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=15)
        
        # Editor container with layered borders
        editor_container = ctk.CTkFrame(
            glow_container,
            fg_color=JungleTheme.LEAF_GREEN,
            corner_radius=12
        )
        editor_container.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Header bar for editor
        editor_header = ctk.CTkFrame(
            editor_container,
            fg_color=JungleTheme.MOSS_GREEN,
            corner_radius=10,
            height=35
        )
        editor_header.pack(fill="x", padx=3, pady=(3, 0))
        editor_header.pack_propagate(False)
        
        editor_title = ctk.CTkLabel(
            editor_header,
            text="🍌 Banana Patch (Code Editor) 🍌",
            font=("Consolas", 13, "bold"),
            text_color=JungleTheme.BANANA_YELLOW
        )
        editor_title.pack(side="left", padx=15, pady=5)
        
        # Tab-like decoration
        fake_tab = ctk.CTkFrame(
            editor_header,
            fg_color=JungleTheme.CODE_BG,
            corner_radius=8,
            width=120,
            height=25
        )
        fake_tab.pack(side="left", padx=5)
        fake_tab.pack_propagate(False)
        
        tab_label = ctk.CTkLabel(
            fake_tab,
            text="🐒 main.riri",
            font=("Consolas", 11),
            text_color=JungleTheme.TEXT_DIM
        )
        tab_label.pack(expand=True)
        
        # Inner editor frame
        inner_frame = ctk.CTkFrame(
            editor_container,
            fg_color=JungleTheme.CODE_BG,
            corner_radius=10
        )
        inner_frame.pack(fill="both", expand=True, padx=3, pady=3)

        # Enhanced line numbers bar
        line_number_container = ctk.CTkFrame(
            inner_frame,
            fg_color=JungleTheme.JUNGLE_GREEN,
            corner_radius=0,
            width=60
        )
        line_number_container.pack(side="left", fill="y")
        line_number_container.pack_propagate(False)
        
        self.line_numbers = ctk.CTkTextbox(
            line_number_container,
            font=("Consolas", 14),
            fg_color=JungleTheme.JUNGLE_GREEN,
            text_color=JungleTheme.TEXT_DIM,
            activate_scrollbars=False
        )
        self.line_numbers.pack(fill="both", expand=True, padx=5)
        self.line_numbers.insert("0.0", "1\n2\n3\n4\n5\n6\n7\n8\n9\n10")
        self.line_numbers.configure(state="disabled")

        # Vertical separator
        separator = ctk.CTkFrame(
            inner_frame,
            fg_color=JungleTheme.VINE_GREEN,
            width=2
        )
        separator.pack(side="left", fill="y", padx=2)

        # Main code editor with enhanced styling
        self.code_input = ctk.CTkTextbox(
            inner_frame,
            font=("Consolas", 15),
            fg_color=JungleTheme.CODE_BG,
            text_color=JungleTheme.SYNTAX_GREEN,
            activate_scrollbars=True,
            wrap="none",
            border_width=0
        )
        self.code_input.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Enhanced default code with more personality
        default_code = '''# 🌴 Welcome to the Jungle! 🐵🍌
# This is where monkeys write code!

print("🐒 Hello from Riri's Jungle!")
print("=" * 40)

# Count those bananas! 🍌
banana_count = 5
print(f"Bananas collected: {banana_count} 🍌")

if banana_count >= 5:
    print("🎉 Happy monkey! Belly full!")
else:
    print("😢 Hungry monkey... need more bananas!")

# Swing through the trees
for i in range(3):
    print(f"🌿 Swing {i+1}... wheee!")

print("\\n🌴 Ready to code? Go BANANAS! 🍌")'''
        
        self.code_input.insert("0.0", default_code)

        # Bind to update line numbers
        self.code_input.bind("<KeyRelease>", self._update_line_numbers)
        self.code_input.bind("<MouseWheel>", self._sync_scroll)
        self.code_input.bind("<Button-4>", self._sync_scroll)  # Linux scroll
        self.code_input.bind("<Button-5>", self._sync_scroll)

    def _update_line_numbers(self, event=None):
        """Update line numbers based on content"""
        lines = self.code_input.get("0.0", "end").count('\n')
        line_text = '\n'.join(str(i) for i in range(1, lines + 2))
        self.line_numbers.configure(state="normal")
        self.line_numbers.delete("0.0", "end")
        self.line_numbers.insert("0.0", line_text)
        self.line_numbers.configure(state="disabled")
        
    def _sync_scroll(self, event=None):
        """Synchronize line numbers scrolling with code editor"""
        # Get the current view position
        first_visible = self.code_input.yview()[0]
        self.line_numbers.yview_moveto(first_visible)

    def _create_toolbar(self):
        """Create enhanced jungle-themed toolbar"""
        toolbar_container = ctk.CTkFrame(
            self,
            fg_color="transparent",
            height=60
        )
        toolbar_container.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        toolbar_container.grid_propagate(False)

        # Left side: Enhanced status panel
        status_container = ctk.CTkFrame(
            toolbar_container,
            fg_color=JungleTheme.JUNGLE_GREEN,
            corner_radius=25,
            height=50
        )
        status_container.pack(side="left", fill="y", padx=(0, 10))
        
        # Add inner glow
        status_inner = ctk.CTkFrame(
            status_container,
            fg_color=JungleTheme.LEAF_GREEN,
            corner_radius=23
        )
        status_inner.pack(fill="both", expand=True, padx=2, pady=2)

        self.status_icon = ctk.CTkLabel(
            status_inner,
            text="🐵",
            font=("Segoe UI Emoji", 22)
        )
        self.status_icon.pack(side="left", padx=(15, 5))

        self.status_label = ctk.CTkLabel(
            status_inner,
            text="Έτοιμος να σκαρφαλώσω!",
            text_color=JungleTheme.TEXT_LIGHT,
            font=("Consolas", 13, "bold")
        )
        self.status_label.pack(side="left", padx=(5, 15))

        # Right side: Enhanced button group
        button_frame = ctk.CTkFrame(toolbar_container, fg_color="transparent")
        button_frame.pack(side="right")

        # New button (banana peel themed)
        self.new_btn = ctk.CTkButton(
            button_frame,
            text="🍌 New",
            command=self.new_file,
            fg_color=JungleTheme.MOSS_GREEN,
            hover_color=JungleTheme.VINE_GREEN,
            text_color=JungleTheme.TEXT_LIGHT,
            font=("Consolas", 13, "bold"),
            height=45,
            corner_radius=22,
            width=100,
            border_width=2,
            border_color=JungleTheme.VINE_GREEN
        )
        self.new_btn.pack(side="left", padx=5)

        # Clear Button (Enhanced brown like tree bark)
        self.clear_btn = ctk.CTkButton(
            button_frame,
            text="🧹 Clear",
            command=self.clear_console,
            fg_color=JungleTheme.BROWN_MONKEY,
            hover_color=JungleTheme.MONKEY_FUR,
            text_color=JungleTheme.TEXT_LIGHT,
            font=("Consolas", 13, "bold"),
            height=45,
            corner_radius=22,
            width=120,
            border_width=2,
            border_color=JungleTheme.LIGHT_BROWN
        )
        self.clear_btn.pack(side="left", padx=5)

        # Run Button (Enhanced banana yellow with glow effect!)
        run_glow = ctk.CTkFrame(
            button_frame,
            fg_color=JungleTheme.RIPE_BANANA,
            corner_radius=24
        )
        run_glow.pack(side="left", padx=5)
        
        self.run_btn = ctk.CTkButton(
            run_glow,
            text="▶ GO BANANAS!",
            command=self.run_code,
            fg_color=JungleTheme.BANANA_YELLOW,
            hover_color=JungleTheme.RIPE_BANANA,
            text_color=JungleTheme.BROWN_MONKEY,
            font=("Consolas", 15, "bold"),
            height=45,
            corner_radius=22,
            width=180
        )
        self.run_btn.pack(padx=2, pady=2)

    def _create_console(self):
        """Create enhanced jungle floor console"""
        # Console outer glow
        console_glow = ctk.CTkFrame(
            self,
            fg_color=JungleTheme.SHADOW_DARK,
            corner_radius=15
        )
        console_glow.grid(row=3, column=0, sticky="nsew", padx=20, pady=(5, 20))
        
        # Console container
        console_container = ctk.CTkFrame(
            console_glow,
            fg_color=JungleTheme.LEAF_GREEN,
            corner_radius=12
        )
        console_container.pack(fill="both", expand=True, padx=2, pady=2)

        # Console header with enhanced design
        console_header = ctk.CTkFrame(
            console_container,
            fg_color=JungleTheme.JUNGLE_GREEN,
            corner_radius=10,
            height=40
        )
        console_header.pack(fill="x", padx=3, pady=(3, 0))
        console_header.pack_propagate(False)
        
        # Header content with icons
        header_left = ctk.CTkFrame(console_header, fg_color="transparent")
        header_left.pack(side="left", fill="y")

        console_icon = ctk.CTkLabel(
            header_left,
            text="🌴",
            font=("Segoe UI Emoji", 18)
        )
        console_icon.pack(side="left", padx=(15, 5))

        console_title = ctk.CTkLabel(
            header_left,
            text="Jungle Floor Output",
            font=("Consolas", 13, "bold"),
            text_color=JungleTheme.BANANA_YELLOW
        )
        console_title.pack(side="left", padx=5)

        # Decorative monkey on right side of header
        console_monkey = ctk.CTkLabel(
            console_header,
            text="🐒",
            font=("Segoe UI Emoji", 16)
        )
        console_monkey.pack(side="right", padx=15)

        # Console text area with enhanced styling
        console_inner = ctk.CTkFrame(
            console_container,
            fg_color=JungleTheme.CONSOLE_BG,
            corner_radius=10
        )
        console_inner.pack(fill="both", expand=True, padx=3, pady=3)
        
        self.console_output = ctk.CTkTextbox(
            console_inner,
            font=("Consolas", 13),
            fg_color=JungleTheme.CONSOLE_BG,
            text_color=JungleTheme.SUCCESS_GREEN,
            activate_scrollbars=True,
            border_width=0
        )
        self.console_output.pack(fill="both", expand=True, padx=5, pady=5)
        self.console_output.configure(state="disabled")

    def _print_welcome(self):
        """Print enhanced welcome message to console"""
        welcome_msg = """╔════════════════════════════════════════════════════════╗
║     🐵 Welcome to Riri's Jungle IDE! 🐵               ║
╚════════════════════════════════════════════════════════╝

🌴 JUNGLE SURVIVAL GUIDE 🌴
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🍌 Type your monkey code in the Banana Patch above
🌿 Click 'GO BANANAS!' to swing into action
🌴 Watch your code grow on the jungle floor below
🐒 Clear the jungle with the broom when needed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ready to swing through the trees! 🌳
Let's go bananas! 🍌🍌🍌

"""
        self._append_to_console(welcome_msg, JungleTheme.SUCCESS_GREEN)

    def _append_to_console(self, text, color=None):
        """Helper to append text with optional color"""
        self.console_output.configure(state="normal")
        if color:
            # Create a tag for this color if it doesn't exist
            tag_name = f"color_{color}"
            self.console_output.tag_config(tag_name, foreground=color)
            
            # Insert with tag
            start_pos = self.console_output.index("end-1c")
            self.console_output.insert("end", text)
            end_pos = self.console_output.index("end-1c")
            self.console_output.tag_add(tag_name, start_pos, end_pos)
        else:
            self.console_output.insert("end", text)
        self.console_output.see("end")
        self.console_output.configure(state="disabled")

    def new_file(self):
        """Create a new file"""
        self.code_input.delete("0.0", "end")
        self.code_input.insert("0.0", "# 🍌 New banana patch ready!\n\n")
        self._append_to_console("\n🌱 Fresh banana patch created!\n", JungleTheme.BANANA_YELLOW)

    def clear_console(self):
        """Clear the jungle floor with animation"""
        self.console_output.configure(state="normal")
        self.console_output.delete("0.0", "end")
        self.console_output.configure(state="disabled")
        
        clear_msg = "\n🧹✨ Jungle floor swept clean! ✨🧹\n🌿 Ready for new adventures...\n\n"
        self._append_to_console(clear_msg, JungleTheme.BANANA_YELLOW)
        
        self.status_label.configure(text="Jungle Cleared!", text_color=JungleTheme.SUCCESS_GREEN)
        self.status_icon.configure(text="✨")
        
        # Animate back to normal
        self.after(1500, lambda: self.status_icon.configure(text="🐵"))
        self.after(1500, lambda: self.status_label.configure(
            text="Έτοιμος να σκαρφαλώσω!",
            text_color=JungleTheme.TEXT_LIGHT
        ))

    def run_code(self):
        """Execute code via Cloud API with enhanced jungle flair and animations"""
        code = self.code_input.get("0.0", "end-1c")
        
        if not code.strip():
            self._append_to_console("\n⚠️ No code to run! Add some monkey business first!\n", 
                                  JungleTheme.WARNING_ORANGE)
            return
        
        # Animate button
        self.run_btn.configure(state="disabled", text="🐒 SWINGING...")
        
        # Update status with swinging animation
        self.status_label.configure(text="Swinging through trees...", 
                                   text_color=JungleTheme.BANANA_YELLOW)
        self.status_icon.configure(text="🌿")
        self.update()

        try:
            # Add visual separator
            separator = "\n" + "="*60 + "\n"
            self._append_to_console(separator, JungleTheme.VINE_GREEN)
            self._append_to_console("🌿 Sending code to the Cloud Jungle...\n", JungleTheme.VINE_GREEN)
            self._append_to_console("─"*60 + "\n", JungleTheme.MOSS_GREEN)
            
            # Request to API
            response = requests.post(
                "http://localhost:8000/execute",
                json={"code": code, "timeout": 2.0},
                timeout=3.0 # requests timeout
            )
            response.raise_for_status()
            
            data = response.json()
            output = data.get("output", "")
            status = data.get("status", "")
            error = data.get("error", None)

            if status == "success":
                # Success animation
                self.status_icon.configure(text="🎉")
                self.banana_count += 1
                self._update_banana_display()
                
                self._append_to_console(output, JungleTheme.SUCCESS_GREEN)
                self._append_to_console("\n─"*60 + "\n", JungleTheme.SUCCESS_GREEN)
                self._append_to_console("✅ Code executed successfully! Bananas collected! 🍌\n", 
                                      JungleTheme.BANANA_YELLOW)
                self.status_label.configure(text="Bananas collected! 🍌", 
                                          text_color=JungleTheme.BANANA_YELLOW)
            else:
                error_msg = f"\n🙈 Oops! Monkey slipped on a API banana peel!\n"
                error_msg += f"🐒 Error: {error}\n"
                self.status_icon.configure(text="🙈")

                self._append_to_console(error_msg, JungleTheme.ERROR_RED)
                if output:
                     self._append_to_console(output, JungleTheme.ERROR_RED)

                self._append_to_console("\n─"*60 + "\n", JungleTheme.ERROR_RED)
                self.status_label.configure(text="Monkey business went wrong!", 
                                          text_color=JungleTheme.ERROR_RED)
            
        except requests.exceptions.RequestException as e:
            error_msg = f"\n🔥 NETWORK FIRE! Cannot reach the Cloud Jungle!\n"
            error_msg += f"🔥 Is the FastAPI server running on port 8000?\n"
            error_msg += f"🐒 Details: {str(e)}\n"
            
            self.status_icon.configure(text="🔥")
            self._append_to_console(error_msg, JungleTheme.ERROR_RED)
            self._append_to_console("\n─"*60 + "\n", JungleTheme.ERROR_RED)
            self.status_label.configure(text="Cloud Jungle Offline!", 
                                      text_color=JungleTheme.ERROR_RED)
        
        # Re-enable button
        self.run_btn.configure(state="normal", text="▶ GO BANANAS!")
        
        # Return to normal status after delay
        self.after(3000, lambda: self.status_icon.configure(text="🐵"))
        self.after(3000, lambda: self.status_label.configure(
            text="Έτοιμος να σκαρφαλώσω!",
            text_color=JungleTheme.TEXT_LIGHT
        ))

    def _update_banana_display(self):
        """Update banana counter animation"""
        bananas = "🍌 " * min(self.banana_count, 5)
        if self.banana_count > 5:
            bananas += f"x{self.banana_count - 5}"
        self.banana_label.configure(text=bananas)

if __name__ == "__main__":
    app = MonkeyIDE()
    app.mainloop()