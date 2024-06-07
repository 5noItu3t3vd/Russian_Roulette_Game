import os
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from engine import Engine
from Characters.Player import Player
from Characters.Computer import Computer
import re
from PIL import Image,ImageTk

SINGLE_PLAYER_IMAGE = r"resources\\single.png"
SHOT_RESULT_IMAGE = r"resources\\shot_result.png"
BULLET_IMAGE = r"resources\\bullet.png"
FALSE_BULLET_IMAGE = r"resources\\false_bullet.png"
LIFE_IMAGE = r"resources\\life.png"

class SinglePlayerMode(tk.Toplevel):
    def __init__(self, master, mainmenu,player):
        super().__init__(master)
        self.player1 = player
        self.player2 = Computer()
        if self.player1.name == self.player2.name:
            self.player2.name = 'cpu'

        self.engine = Engine(self.master, gamemode="single", player1=self.player1, player2=self.player2)
        self.next_bullet = self.engine.start_round()

        self.current_player = self.player1
        self.other_player = self.player2
        self.mainmenu = mainmenu
        
        self.title("Single Player Mode")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        
        
        self.image = Image.open(SINGLE_PLAYER_IMAGE)
        self.image_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image_copy)
        self.width,self.height = self.background_image.width(),self.background_image.height()
        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack(fill="both", expand=True)
        
        self.bg_image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background_image)
        
        self.turnlabel = tk.Label(self.canvas, text="Single Player Mode activated.")
        self.turnlabel.place(relx=0.5, rely=0.1, anchor="center")
        
        self.button_frame = tk.Frame(self)
        self.button_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self.bullet_frame = tk.Frame(self)
        self.bullet_frame.place(relx=0.05, rely=0.5, anchor="w")

        self.life_frame = tk.Frame(self)
        self.life_frame.place(relx=0.95, rely=0.5, anchor="e")

        self.canvas.bind('<Configure>', self.resize_background)

        self.initiate("Player1")

    def on_close(self):
        self.destroy()
        self.mainmenu.deiconify()
    
    def action_buttons(self):
        self.add_action_buttons()
    
    def add_action_buttons(self, itemson=False):
        if hasattr(self, 'self_button'):
            self.self_button.destroy()
        if hasattr(self, 'other_button'):
            self.other_button.destroy()

        self.self_button = tk.Button(self.button_frame, text="Pull Trigger to Yourself", command=self.pull_trigger_self)
        self.self_button.pack(side="left", padx=10)

        self.other_button = tk.Button(self.button_frame, text=f"Pull Trigger to Opponent", command=self.pull_trigger_other)
        self.other_button.pack(side="left", padx=10)
    
    def pull_trigger_self(self):
        self.perform_action("self")
    
    def pull_trigger_other(self):
        self.perform_action("opp")

    def perform_action(self, action):
        self.self_button.config(state="disabled")
        self.other_button.config(state="disabled")

        self.label.config(text="Taking the shot...")
        
        self.after(2000, lambda: self.execute_action(action))

    def execute_action(self, action):
        nextShot = self.engine.get_random_index(self.engine.shotgun.rounds)
        isDead, nextplayer, isExhausted, luck_shot = self.engine.make_action(self.current_player, self.other_player, action, nextShot=nextShot)
        
        self.show_result(action, isDead, nextplayer, isExhausted, luck_shot)
        
    def show_result(self, action, isDead, nextplayer, isExhausted, luck_shot):
        result_image = Image.open(SHOT_RESULT_IMAGE)
        result_photo = ImageTk.PhotoImage(result_image)
        result_label = tk.Label(self.canvas, image=result_photo)
        result_label.image = result_photo
        result_label.place(relx=0.5, rely=0.8, anchor="center")
        
        self.after(2000, lambda: self.clear_result(result_label, isDead, nextplayer, isExhausted, luck_shot))

    def clear_result(self, result_label, isDead, nextplayer, isExhausted, luck_shot):
        result_label.destroy()

        if isDead:
            messagebox.showinfo("Game Over", f"{nextplayer.name} is dead! Game over.")
            self.on_close()
        elif isExhausted:
            messagebox.showinfo("Game Over", "No more shots left. The game is exhausted.")
            self.on_close()
        else:
            self.current_player = nextplayer
            if luck_shot:
                self.perform_action("self")
            else:
                self.update_gui()
                self.update_bullet_frame()
                self.update_life_frame()
                if self.current_player == self.engine.player2:
                    self.after(2000, self.engine.computer_phase)
                else:
                    self.reset_buttons()

    def reset_buttons(self):
        self.self_button.config(state="normal")
        self.other_button.config(state="normal")

    def initiate(self):
        
        while not self.engine.round_over:
            if type(self.current_player) == Computer:
                self.update_gui                
                self.update_bullet_frame()
                self.update_life_frame()
                
            else:
                self.update_gui()
                self.add_action_buttons()
                self.update_bullet_frame()
                self.update_life_frame()
            
        self.on_close()
        
        
    def update_gui(self):
        self.turnlabel.config(text=f"It's {self.current_player.name}'s turn")
        if self.current_player == self.player1:
            pass
            
        
    def update_bullet_frame(self):
        for widget in self.bullet_frame.winfo_children():
            widget.destroy()

        bullet_image = Image.open(BULLET_IMAGE)
        bullet_photo = ImageTk.PhotoImage(bullet_image)
        false_bullet_image = Image.open(FALSE_BULLET_IMAGE)
        false_bullet_photo = ImageTk.PhotoImage(false_bullet_image)

        bullet_count = self.engine.shotgun.rounds.count(True)
        false_bullet_count = self.engine.shotgun.rounds.count(False)

        for _ in range(bullet_count):
            bullet_label = tk.Label(self.bullet_frame, image=bullet_photo)
            bullet_label.image = bullet_photo
            bullet_label.pack()

        for _ in range(false_bullet_count):
            false_bullet_label = tk.Label(self.bullet_frame, image=false_bullet_photo)
            false_bullet_label.image = false_bullet_photo
            false_bullet_label.pack()

        bullet_count_label = tk.Label(self.bullet_frame, text=f"Bullets: {bullet_count}")
        bullet_count_label.pack()

        false_bullet_count_label = tk.Label(self.bullet_frame, text=f"False Bullets: {false_bullet_count}")
        false_bullet_count_label.pack()

    def update_life_frame(self):
        for widget in self.life_frame.winfo_children():
            widget.destroy()

        life_image = Image.open(LIFE_IMAGE)
        life_photo = ImageTk.PhotoImage(life_image)

        player1_life_label = tk.Label(self.life_frame, text=f"{self.engine.player1.name}'s Lives:")
        player1_life_label.grid(row=0, column=0, columnspan=3)

        for i in range(self.engine.player1.life):
            player1_life_icon = tk.Label(self.life_frame, image=life_photo)
            player1_life_icon.image = life_photo
            player1_life_icon.grid(row=1, column=i)

        player2_life_label = tk.Label(self.life_frame, text=f"{self.engine.player2.name}'s Lives:")
        player2_life_label.grid(row=2, column=0, columnspan=3)

        for i in range(self.engine.player2.life):
            player2_life_icon = tk.Label(self.life_frame, image=life_photo)
            player2_life_icon.image = life_photo
            player2_life_icon.grid(row=3, column=i)
        
    def resize_background(self, event):
        width = event.width
        height = event.height
        self.image_copy = self.image.resize((width, height), Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(self.image_copy)
        self.canvas.itemconfig(self.bg_image_id, image=self.background_image)
        self.canvas.image = self.background_image
