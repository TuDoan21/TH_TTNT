import tkinter as tk
from tkinter import messagebox
import math
import random
import json
import os 

# --- KHU VỰC IMPORT THƯ VIỆN KHOA HỌC DỮ LIỆU ---
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.datasets import make_blobs

# =============================================================================
# CẤU HÌNH ĐƯỜNG DẪN LƯU TRỮ
# =============================================================================
SAVE_FOLDER = r"E:\LuuDuLieuSV\DoanTuanTu-2001230840"

# =============================================================================
# PHẦN 1: CẤU HÌNH GIAO DIỆN (THEME)
# =============================================================================
APP_THEME = {
    "bg_main": "#121212",       
    "bg_card": "#1E1E1E",       
    "accent": "#BB86FC",        
    "accent_2": "#03DAC6",      
    "text_main": "#FFFFFF",     
    "text_sub": "#B0B0B0",      
    "danger": "#CF6679",        
    "success": "#03DAC6",       
    "board_bg": "#1E1E1E",      
    "grid_line": "#333333"      
}

FONTS = {
    "h1": ("Segoe UI", 24, "bold"),
    "h2": ("Segoe UI", 16, "bold"),
    "body": ("Segoe UI", 11),
    "btn": ("Segoe UI", 11, "bold"),
    "icon": ("Segoe UI Emoji", 28) 
}

# =============================================================================
# PHẦN 2: WIDGET TÙY CHỈNH
# =============================================================================
class AppButton(tk.Frame):
    def __init__(self, master, title, subtitle, icon, command, color=APP_THEME["bg_card"]):
        super().__init__(master, bg=color, cursor="hand2", pady=10, padx=10)
        self.command = command
        self.default_bg = color
        self.hover_bg = "#2C2C2C"

        self.bind("<Button-1>", lambda e: command())
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

        lbl_icon = tk.Label(self, text=icon, font=FONTS["icon"], bg=color, fg=APP_THEME["accent"])
        lbl_icon.pack(side="left", padx=(10, 15))
        lbl_icon.bind("<Button-1>", lambda e: command())

        text_frame = tk.Frame(self, bg=color)
        text_frame.pack(side="left", fill="both", expand=True)
        text_frame.bind("<Button-1>", lambda e: command())

        lbl_title = tk.Label(text_frame, text=title, font=FONTS["h2"], bg=color, fg=APP_THEME["text_main"], anchor="w")
        lbl_title.pack(fill="x")
        lbl_title.bind("<Button-1>", lambda e: command())

        lbl_sub = tk.Label(text_frame, text=subtitle, font=("Segoe UI", 9), bg=color, fg=APP_THEME["text_sub"], anchor="w")
        lbl_sub.pack(fill="x")
        lbl_sub.bind("<Button-1>", lambda e: command())

        lbl_arrow = tk.Label(self, text="›", font=("Segoe UI", 20), bg=color, fg="#555555")
        lbl_arrow.pack(side="right", padx=10)
        lbl_arrow.bind("<Button-1>", lambda e: command())
        
        self.children_widgets = [lbl_icon, text_frame, lbl_title, lbl_sub, lbl_arrow]

    def on_enter(self, e):
        self.config(bg=self.hover_bg)
        for w in self.children_widgets: w.config(bg=self.hover_bg)

    def on_leave(self, e):
        self.config(bg=self.default_bg)
        for w in self.children_widgets: w.config(bg=self.default_bg)

class FlatButton(tk.Button):
    def __init__(self, master, **kwargs):
        bg = kwargs.get("bg", APP_THEME["accent"])
        kwargs.setdefault("bg", bg)
        kwargs.setdefault("fg", "#000000" if bg in [APP_THEME["accent"], APP_THEME["accent_2"]] else "white")
        kwargs.setdefault("font", FONTS["btn"])
        kwargs.setdefault("relief", "flat")
        kwargs.setdefault("cursor", "hand2")
        kwargs.setdefault("pady", 8)
        super().__init__(master, **kwargs)

# =============================================================================
# PHẦN 3: MÀN HÌNH CHÍNH
# =============================================================================
class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Super App")
        self.root.geometry("400x750")
        self.root.configure(bg=APP_THEME["bg_main"])
        self.center_window(400, 750)
        
        header = tk.Frame(root, bg=APP_THEME["bg_main"], pady=30, padx=20)
        header.pack(fill="x")
        
        tk.Label(header, text="Xin chào,", font=("Segoe UI", 14), bg=APP_THEME["bg_main"], fg=APP_THEME["text_sub"]).pack(anchor="w")
        tk.Label(header, text="Tú Đoàn", font=("Segoe UI", 32, "bold"), bg=APP_THEME["bg_main"], fg=APP_THEME["text_main"]).pack(anchor="w")

        container = tk.Frame(root, bg=APP_THEME["bg_main"], padx=20)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="ỨNG DỤNG", font=("Segoe UI", 10, "bold"), bg=APP_THEME["bg_main"], fg="#555555").pack(anchor="w", pady=(10, 5))

        AppButton(container, "Cờ Caro Pro", "PvP hoặc đấu với AI", "❌", self.open_caro).pack(fill="x", pady=8)
        AppButton(container, "Tô Màu Đồ Thị", "Thuật toán tham lam", "🎨", self.open_graph).pack(fill="x", pady=8)
        AppButton(container, "K-Means AI", "Phân cụm dữ liệu", "🧠", self.open_kmeans).pack(fill="x", pady=8)
        AppButton(container, "Cờ Vua Master", "Kinh điển & Trí tuệ", "♟️", self.open_chess).pack(fill="x", pady=8)

        footer = tk.Frame(root, bg=APP_THEME["bg_main"], pady=20)
        footer.pack(side="bottom", fill="x")
        FlatButton(footer, text="Thoát Ứng Dụng", bg=APP_THEME["bg_card"], fg=APP_THEME["danger"], command=self.exit_app, width=20).pack()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def open_caro(self):
        CaroGame(tk.Toplevel(self.root))

    def open_graph(self):
        GraphColoring(tk.Toplevel(self.root))
    
    def open_kmeans(self):
        KMeansWindow(self.root)
        
    def open_chess(self):
        ChessGame(tk.Toplevel(self.root))
       
    def exit_app(self):
        self.root.destroy()


# =============================================================================
# PHẦN 4: MODULE GAME CỜ CARO (CÓ SAVE/LOAD)
# =============================================================================
class CaroGame:
    def __init__(self, window):
        self.window = window
        self.window.title("Caro Game")
        self.window.geometry("450x650")
        self.window.configure(bg=APP_THEME["bg_main"])
        
        self.frame_setup = tk.Frame(window, bg=APP_THEME["bg_main"], padx=30, pady=30)
        self.frame_setup.pack(expand=True, fill="both")
        
        tk.Label(self.frame_setup, text="CẤU HÌNH", font=FONTS["h1"], bg=APP_THEME["bg_main"], fg=APP_THEME["text_main"]).pack(pady=(0, 30))
        
        lbl_n = tk.Label(self.frame_setup, text="Kích thước bàn cờ (3-30):", font=FONTS["body"], bg=APP_THEME["bg_main"], fg=APP_THEME["text_sub"])
        lbl_n.pack(anchor="w")
        self.entry_n = tk.Entry(self.frame_setup, font=("Segoe UI", 12), bg=APP_THEME["bg_card"], fg="white", insertbackground="white", relief="flat")
        self.entry_n.insert(0, "10") 
        self.entry_n.pack(fill="x", pady=(5, 20), ipady=5)

        lbl_mode = tk.Label(self.frame_setup, text="Chế độ:", font=FONTS["body"], bg=APP_THEME["bg_main"], fg=APP_THEME["text_sub"])
        lbl_mode.pack(anchor="w")
        
        self.mode_var = tk.StringVar(value="PvP")
        mode_frame = tk.Frame(self.frame_setup, bg=APP_THEME["bg_main"])
        mode_frame.pack(fill="x", pady=5)
        
        for mode, val in [("Người vs Người", "PvP"), ("Đấu với Máy (AI)", "PvE")]:
            tk.Radiobutton(mode_frame, text=mode, variable=self.mode_var, value=val, 
                           bg=APP_THEME["bg_main"], fg="white", selectcolor=APP_THEME["bg_card"],
                           activebackground=APP_THEME["bg_main"], activeforeground=APP_THEME["accent"],
                           font=FONTS["body"]).pack(anchor="w", pady=2)

        btn_start = FlatButton(self.frame_setup, text="VÀO TRẬN", command=self.start_game, bg=APP_THEME["accent"])
        btn_start.pack(fill="x", pady=30)
        
        # Nút tải game ở màn hình chào
        FlatButton(self.frame_setup, text="Tải Game Cũ", command=self.load_game, bg="#FF9800", width=15).pack(pady=5)

        self.canvas = None
        self.board = []   
        self.turn = 'X'   
        self.game_over = False
        self.move_count = 0

    def start_game(self):
        try:
            val = int(self.entry_n.get())
            if val < 3 or val > 30: raise ValueError
            self.n = val
        except ValueError:
            messagebox.showerror("Lỗi", "Nhập số từ 3 đến 30!")
            return

        self.is_pve = (self.mode_var.get() == "PvE")
        self.frame_setup.destroy() 
        self.create_board_ui()     

    def create_board_ui(self):
        top_bar = tk.Frame(self.window, bg=APP_THEME["bg_main"], pady=10)
        top_bar.pack(fill="x")
        self.lbl_turn = tk.Label(top_bar, text=f"Lượt: {self.turn}", font=FONTS["h2"], bg=APP_THEME["bg_main"], fg=APP_THEME["danger"])
        self.lbl_turn.pack()

        if self.n <= 8: self.cell_size = 50
        elif self.n <= 15: self.cell_size = 32
        else: self.cell_size = 24

        w = self.n * self.cell_size
        h = self.n * self.cell_size

        frame_canvas = tk.Frame(self.window, bg=APP_THEME["bg_main"])
        frame_canvas.pack(expand=True)
        
        self.canvas = tk.Canvas(frame_canvas, width=w, height=h, bg=APP_THEME["board_bg"], highlightthickness=0)
        self.canvas.pack()
        
        for i in range(self.n + 1):
             self.canvas.create_line(i*self.cell_size, 0, i*self.cell_size, h, fill=APP_THEME["grid_line"])
             self.canvas.create_line(0, i*self.cell_size, w, i*self.cell_size, fill=APP_THEME["grid_line"])

        self.canvas.bind("<Button-1>", self.on_user_click)
        
        ctrl = tk.Frame(self.window, bg=APP_THEME["bg_main"], pady=20)
        ctrl.pack(fill="x")
        FlatButton(ctrl, text="Chơi Lại", command=self.reset_game, bg=APP_THEME["bg_card"], fg="white", width=8).pack(side="left", padx=5)
        FlatButton(ctrl, text="Lưu Game", command=self.save_game, bg="#4CAF50", width=8).pack(side="left", padx=5)
        FlatButton(ctrl, text="Thoát", command=self.window.destroy, bg=APP_THEME["danger"], width=8).pack(side="right", padx=5)

        # Nếu board rỗng (chơi mới), khởi tạo lại
        if not self.board:
            self.board = [['' for _ in range(self.n)] for _ in range(self.n)]
            self.move_count = 0
            self.game_over = False
            self.turn = 'X'
        else:
            # Nếu board có dữ liệu (Load game), vẽ lại các quân cờ
            self.redraw_pieces()

    def reset_game(self):
        self.window.destroy()
        CaroGame(tk.Toplevel())

    def on_user_click(self, event):
        if self.game_over: return
        if self.is_pve and self.turn == 'O': return 

        c = event.x // self.cell_size
        r = event.y // self.cell_size

        if 0 <= r < self.n and 0 <= c < self.n and self.board[r][c] == '':
            self.make_move(r, c) 
            if not self.game_over and self.is_pve:
                self.window.after(400, self.computer_move)

    def make_move(self, r, c):
        cx = c * self.cell_size + self.cell_size // 2
        cy = r * self.cell_size + self.cell_size // 2
        
        if self.turn == 'X':
            color = APP_THEME["danger"] 
            offset = self.cell_size // 4
            self.canvas.create_line(cx-offset, cy-offset, cx+offset, cy+offset, width=3, fill=color, capstyle="round")
            self.canvas.create_line(cx+offset, cy-offset, cx-offset, cy+offset, width=3, fill=color, capstyle="round")
        else:
            color = APP_THEME["accent_2"] 
            radius = self.cell_size // 3
            self.canvas.create_oval(cx-radius, cy-radius, cx+radius, cy+radius, width=3, outline=color)

        self.board[r][c] = self.turn
        self.move_count += 1 

        if self.check_winner(r, c):
            messagebox.showinfo("Kết quả", f"{self.turn} Thắng!")
            self.game_over = True
            return

        if self.move_count >= self.n * self.n:
            messagebox.showinfo("Kết quả", "Hòa!")
            self.game_over = True
            return

        self.turn = 'O' if self.turn == 'X' else 'X'
        self.lbl_turn.config(text=f"Lượt: {self.turn}", fg=APP_THEME["danger"] if self.turn=='X' else APP_THEME["accent_2"])

    def redraw_pieces(self):
        """Vẽ lại toàn bộ quân cờ khi Load Game"""
        for r in range(self.n):
            for c in range(self.n):
                val = self.board[r][c]
                if val != '':
                    cx = c * self.cell_size + self.cell_size // 2
                    cy = r * self.cell_size + self.cell_size // 2
                    if val == 'X':
                        color = APP_THEME["danger"]
                        offset = self.cell_size // 4
                        self.canvas.create_line(cx-offset, cy-offset, cx+offset, cy+offset, width=3, fill=color, capstyle="round")
                        self.canvas.create_line(cx+offset, cy-offset, cx-offset, cy+offset, width=3, fill=color, capstyle="round")
                    else:
                        color = APP_THEME["accent_2"]
                        radius = self.cell_size // 3
                        self.canvas.create_oval(cx-radius, cy-radius, cx+radius, cy+radius, width=3, outline=color)

    def computer_move(self):
        if self.game_over: return
        empty = [(r, c) for r in range(self.n) for c in range(self.n) if self.board[r][c] == '']
        if not empty: return
        
        for r, c in empty:
            self.board[r][c] = 'O'
            if self.check_winner(r, c):
                self.board[r][c] = ''
                self.make_move(r, c)
                return
            self.board[r][c] = ''
            
        for r, c in empty:
            self.board[r][c] = 'X'
            if self.check_winner(r, c):
                self.board[r][c] = ''
                self.make_move(r, c)
                return
            self.board[r][c] = ''

        move = random.choice(empty)
        self.make_move(move[0], move[1])

    def check_winner(self, r, c):
        win_num = 5 if self.n >= 5 else self.n
        player = self.board[r][c]
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            for k in range(1, win_num):
                nr, nc = r + dr*k, c + dc*k
                if 0 <= nr < self.n and 0 <= nc < self.n and self.board[nr][nc] == player: count += 1
                else: break
            for k in range(1, win_num):
                nr, nc = r - dr*k, c - dc*k
                if 0 <= nr < self.n and 0 <= nc < self.n and self.board[nr][nc] == player: count += 1
                else: break
            if count >= win_num: return True
        return False

    def save_game(self):
        if not os.path.exists(SAVE_FOLDER): os.makedirs(SAVE_FOLDER)
        data = {
            "n": self.n,
            "board": self.board,
            "turn": self.turn,
            "mode": self.mode_var.get(),
            "move_count": self.move_count
        }
        try:
            path = os.path.join(SAVE_FOLDER, "caro_save.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f)
            messagebox.showinfo("Đã lưu", f"File: {path}")
        except Exception as e: messagebox.showerror("Lỗi", str(e))

    def load_game(self):
        path = os.path.join(SAVE_FOLDER, "caro_save.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.n = data["n"]
            self.board = data["board"]
            self.turn = data["turn"]
            self.mode_var.set(data.get("mode", "PvP"))
            self.move_count = data.get("move_count", 0)
            
            # Nếu đang ở màn hình setup thì phá hủy nó để vào game
            if hasattr(self, 'frame_setup') and self.frame_setup.winfo_exists():
                self.frame_setup.destroy()
            # Nếu đang chơi dở mà load thì vẽ lại
            self.create_board_ui()
            messagebox.showinfo("Thành công", "Đã tải game Caro!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không tải được file: {e}")

# =============================================================================
# PHẦN 5: MODULE ĐỒ THỊ (CÓ SAVE/LOAD)
# =============================================================================
class GraphColoring:
    def __init__(self, window):
        self.window = window
        self.window.title("Graph Coloring")
        self.window.geometry("900x600")
        self.window.configure(bg=APP_THEME["bg_main"])

        self.adj = {}        
        self.node_pos = {}   
        self.selected_node = None 
        self.radius = 25     
        self.n = 0           

        main_frame = tk.Frame(window, bg=APP_THEME["bg_main"])
        main_frame.pack(fill="both", expand=True)

        sidebar = tk.Frame(main_frame, bg=APP_THEME["bg_card"], width=250, padx=20, pady=20)
        sidebar.pack(side="left", fill="y")
        
        tk.Label(sidebar, text="BẢNG ĐIỀU KHIỂN", font=FONTS["h2"], bg=APP_THEME["bg_card"], fg=APP_THEME["text_main"]).pack(pady=(0, 20))

        tk.Label(sidebar, text="Số đỉnh:", font=FONTS["body"], bg=APP_THEME["bg_card"], fg=APP_THEME["text_sub"]).pack(anchor="w")
        self.entry_nodes = tk.Entry(sidebar, font=("Segoe UI", 12), bg="#333", fg="white", relief="flat", justify="center")
        self.entry_nodes.insert(0, "6")
        self.entry_nodes.pack(fill="x", pady=5, ipady=5)
        
        FlatButton(sidebar, text="Tạo Mới", command=self.init_nodes, bg=APP_THEME["accent_2"]).pack(fill="x", pady=10)
        FlatButton(sidebar, text="Lưu Đồ Thị", command=self.save_graph, bg="#4CAF50").pack(fill="x", pady=5)
        FlatButton(sidebar, text="Tải Đồ Thị", command=self.load_graph, bg="#FF9800").pack(fill="x", pady=5)

        tk.Label(sidebar, text="Hướng dẫn:\nClick đỉnh để chọn.\nClick đỉnh khác để nối.", 
                 font=("Segoe UI", 10), bg=APP_THEME["bg_card"], fg="#888", justify="left").pack(pady=20)

        content = tk.Frame(main_frame, bg=APP_THEME["bg_main"], padx=20, pady=20)
        content.pack(side="right", fill="both", expand=True)
        self.canvas = tk.Canvas(content, bg="#252526", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def init_nodes(self):
        self.canvas.delete("all")
        try:
            self.n = int(self.entry_nodes.get())
            if self.n < 1: raise ValueError
        except:
            return

        self.adj = {i: [] for i in range(self.n)}
        self.node_pos = {}
        self.selected_node = None

        self.window.update() 
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        cx, cy = w/2, h/2
        r_layout = min(w, h)/2 - 60

        for i in range(self.n):
            angle = 2 * math.pi * i / self.n - math.pi/2
            x = cx + r_layout * math.cos(angle)
            y = cy + r_layout * math.sin(angle)
            self.node_pos[i] = (x, y)

        self.solve_and_draw()

    def on_canvas_click(self, event):
        if self.n == 0: return
        click_x, click_y = event.x, event.y
        clicked_node = None

        for i, (nx, ny) in self.node_pos.items():
            if (click_x - nx)**2 + (click_y - ny)**2 <= self.radius**2:
                clicked_node = i
                break
        
        if clicked_node is not None:
            if self.selected_node is None:
                self.selected_node = clicked_node 
            else:
                if self.selected_node == clicked_node:
                    self.selected_node = None 
                else:
                    u, v = self.selected_node, clicked_node
                    if v in self.adj[u]:
                        self.adj[u].remove(v)
                        self.adj[v].remove(u)
                    else:
                        self.adj[u].append(v)
                        self.adj[v].append(u)
                    self.selected_node = None 
            self.solve_and_draw() 
        else:
            self.selected_node = None
            self.solve_and_draw()

    def solve_and_draw(self):
        colors_palette = ["#FF5252", "#448AFF", "#69F0AE", "#E040FB", "#FFD740", "#00BCD4", "#FF6E40"]
        node_colors = {}
        sorted_nodes = sorted(range(self.n), key=lambda x: len(self.adj[x]), reverse=True)
        
        for u in sorted_nodes:
            forbidden = {node_colors[v] for v in self.adj[u] if v in node_colors}
            for color in colors_palette:
                if color not in forbidden:
                    node_colors[u] = color
                    break
            if u not in node_colors: node_colors[u] = "#757575"

        self.canvas.delete("all")
        
        drawn_edges = set()
        for u in range(self.n):
            for v in self.adj[u]:
                if (u, v) not in drawn_edges and (v, u) not in drawn_edges:
                    x1, y1 = self.node_pos[u]
                    x2, y2 = self.node_pos[v]
                    self.canvas.create_line(x1, y1, x2, y2, fill="#555", width=2)
                    drawn_edges.add((u, v))

        for i in range(self.n):
            x, y = self.node_pos[i]
            c = node_colors.get(i, "white")
            
            if i == self.selected_node:
                outline_c = "white"
                width_line = 3
                r = self.radius + 3
            else:
                outline_c = ""
                width_line = 0
                r = self.radius

            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=c, outline=outline_c, width=width_line)
            self.canvas.create_text(x, y, text=str(i), font=("Segoe UI", 11, "bold"), fill="#121212")

    def save_graph(self):
        if not os.path.exists(SAVE_FOLDER): os.makedirs(SAVE_FOLDER)
        data = { "n": self.n, "adj": self.adj }
        path = os.path.join(SAVE_FOLDER, "graph_save.json")
        try:
            with open(path, "w") as f: json.dump(data, f)
            messagebox.showinfo("Đã lưu", f"File: {path}")
        except Exception as e: messagebox.showerror("Lỗi", str(e))

    def load_graph(self):
        path = os.path.join(SAVE_FOLDER, "graph_save.json")
        try:
            with open(path, "r") as f: data = json.load(f)
            self.n = data["n"]
            # JSON lưu key dictionary là string ("0", "1"), cần convert lại int (0, 1)
            raw_adj = data["adj"]
            self.adj = {int(k): v for k, v in raw_adj.items()}
            
            # Tính lại tọa độ
            self.node_pos = {}
            self.selected_node = None
            self.window.update() 
            w = self.canvas.winfo_width()
            h = self.canvas.winfo_height()
            cx, cy = w/2, h/2
            r_layout = min(w, h)/2 - 60
            for i in range(self.n):
                angle = 2 * math.pi * i / self.n - math.pi/2
                x = cx + r_layout * math.cos(angle)
                y = cy + r_layout * math.sin(angle)
                self.node_pos[i] = (x, y)
                
            self.solve_and_draw()
            messagebox.showinfo("Thành công", "Đã tải đồ thị!")
        except Exception as e: messagebox.showerror("Lỗi", str(e))

# =============================================================================
# PHẦN 6: MODULE K-MEANS (CÓ SAVE/LOAD)
# =============================================================================
class KMeansWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("K-Means Clustering")
        self.geometry("900x600")
        self.configure(bg=APP_THEME["bg_main"])
        self.is_running = False
        
        controls = tk.Frame(self, bg=APP_THEME["bg_card"], pady=15, padx=15)
        controls.pack(side="top", fill="x")
        
        def create_input(lbl, val):
            tk.Label(controls, text=lbl, bg=APP_THEME["bg_card"], fg="white").pack(side="left", padx=(10, 5))
            e = tk.Entry(controls, width=5, bg="#333", fg="white", relief="flat", justify="center")
            e.insert(0, str(val))
            e.pack(side="left")
            return e

        self.entry_n = create_input("Số điểm:", 300)
        self.entry_c_true = create_input("Số cụm gốc:", 4) 
        self.entry_k = create_input("K tìm kiếm:", 4)     

        FlatButton(controls, text="CHẠY", command=self.start_process, bg=APP_THEME["accent"], width=10).pack(side="right", padx=5)
        FlatButton(controls, text="LƯU", command=self.save_sim, bg="#4CAF50", width=8).pack(side="right", padx=5)
        FlatButton(controls, text="TẢI", command=self.load_sim, bg="#FF9800", width=8).pack(side="right", padx=5)

        plot_frame = tk.Frame(self, bg=APP_THEME["bg_main"])
        plot_frame.pack(fill="both", expand=True, padx=20, pady=20)

        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.fig.patch.set_facecolor(APP_THEME["bg_main"]) 
        self.ax.set_facecolor(APP_THEME["bg_card"])        
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        self.lbl_log = tk.Label(self, text="Sẵn sàng...", bg=APP_THEME["bg_main"], fg=APP_THEME["text_sub"], font=("Consolas", 10))
        self.lbl_log.pack(side="bottom", pady=5)
        
        # Biến lưu dữ liệu
        self.X = None
        self.centers = None
        self.labels = None
        self.k = 4

    def visualize(self, X, centers, labels, k, msg):
        self.ax.clear()
        self.lbl_log.config(text=f"> {msg}")
        
        cmap = plt.get_cmap('tab10') 
        for i in range(k):
            cluster_data = X[labels == i]
            if len(cluster_data) > 0:
                color = cmap(i % 10)
                self.ax.scatter(cluster_data[:, 0], cluster_data[:, 1], color=color, alpha=0.7, s=20, edgecolors='none')
        
        if centers is not None:
            self.ax.scatter(centers[:, 0], centers[:, 1], c='white', s=150, marker='X', edgecolors='black', linewidth=1.5, zorder=10)
        
        self.ax.grid(color='#333', linestyle='--', linewidth=0.5)
        self.canvas.draw()

    def start_process(self):
        self.is_running = False 
        try:
            n = int(self.entry_n.get())
            c_true = int(self.entry_c_true.get())
            self.k = int(self.entry_k.get())

            self.X, _ = make_blobs(n_samples=n, centers=c_true, cluster_std=1.0, random_state=42)
            
            idx = np.random.choice(n, self.k, replace=False)
            self.centers = self.X[idx]
            self.labels = np.zeros(n, dtype=int)
            
            self.visualize(self.X, self.centers, self.labels, self.k, "Khởi tạo tâm ngẫu nhiên...")
            
            self.is_running = True
            self.after(800, lambda: self.loop_step(0))

        except ValueError:
            messagebox.showerror("Lỗi", "Kiểm tra lại dữ liệu nhập!")

    def loop_step(self, step):
        if not self.is_running: return
        distances = np.linalg.norm(self.X[:, np.newaxis] - self.centers, axis=2)
        self.labels = np.argmin(distances, axis=1)
        self.visualize(self.X, self.centers, self.labels, self.k, f"Bước {step+1}: Gán nhãn (Tìm cụm gần nhất)")
        self.after(600, lambda: self.update_step(step))

    def update_step(self, step):
        if not self.is_running: return
        old_centers = self.centers.copy()
        new_centers = np.zeros_like(self.centers)

        for i in range(self.k):
            points = self.X[self.labels == i]
            if len(points) > 0:
                new_centers[i] = points.mean(axis=0)
            else:
                new_centers[i] = old_centers[i]

        self.centers = new_centers
        shift = np.linalg.norm(self.centers - old_centers)
        
        if shift < 1e-4:
            self.visualize(self.X, self.centers, self.labels, self.k, "Đã hội tụ! Hoàn tất.")
            self.is_running = False
            return

        self.visualize(self.X, self.centers, self.labels, self.k, f"Bước {step+1}: Cập nhật vị trí tâm")
        self.after(600, lambda: self.loop_step(step + 1))

    def save_sim(self):
        if self.X is None: return
        if not os.path.exists(SAVE_FOLDER): os.makedirs(SAVE_FOLDER)
        # Numpy array không serialize trực tiếp ra JSON được, phải convert tolist()
        data = {
            "X": self.X.tolist(),
            "centers": self.centers.tolist(),
            "labels": self.labels.tolist(),
            "k": self.k
        }
        path = os.path.join(SAVE_FOLDER, "kmeans_save.json")
        try:
            with open(path, "w") as f: json.dump(data, f)
            messagebox.showinfo("Đã lưu", f"File: {path}")
        except Exception as e: messagebox.showerror("Lỗi", str(e))

    def load_sim(self):
        path = os.path.join(SAVE_FOLDER, "kmeans_save.json")
        try:
            with open(path, "r") as f: data = json.load(f)
            self.X = np.array(data["X"])
            self.centers = np.array(data["centers"])
            self.labels = np.array(data["labels"])
            self.k = data["k"]
            self.is_running = False # Dừng animation nếu đang chạy
            self.visualize(self.X, self.centers, self.labels, self.k, "Đã tải kết quả cũ")
            messagebox.showinfo("Thành công", "Đã tải dữ liệu K-Means!")
        except Exception as e: messagebox.showerror("Lỗi", str(e))

# =============================================================================
# PHẦN 7: MODULE CỜ VUA (CÓ SAVE/LOAD)
# =============================================================================
class ChessGame:
    def __init__(self, window):
        self.window = window
        self.window.title("Chess Master")
        self.window.geometry("500x680")
        self.window.configure(bg=APP_THEME["bg_main"])
        
        self.cell_size = 55
        self.board_colors = ["#F0D9B5", "#B58863"] 
        self.selected_piece = None
        self.turn = 'white'
        self.valid_moves = []

        self.pieces_chars = {
            'w': {'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙'},
            'b': {'K': '♚', 'Q': '♛', 'R': '♜', 'B': '♝', 'N': '♞', 'P': '♟'}
        }
        
        header = tk.Frame(window, bg=APP_THEME["bg_main"], pady=10)
        header.pack(fill="x")
        self.lbl_status = tk.Label(header, text="Lượt: Trắng (White)", font=FONTS["h2"], 
                                   bg=APP_THEME["bg_main"], fg="white")
        self.lbl_status.pack()

        self.canvas = tk.Canvas(window, width=440, height=440, bg=APP_THEME["bg_main"], highlightthickness=0)
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.on_click)

        footer = tk.Frame(window, bg=APP_THEME["bg_main"], pady=10)
        footer.pack(fill="x")
        
        FlatButton(footer, text="Ván Mới", command=self.reset_game, bg=APP_THEME["accent_2"], width=10).pack(side="left", padx=10)
        FlatButton(footer, text="Lưu Game", command=self.save_game, bg="#4CAF50", width=10).pack(side="left", padx=10)
        FlatButton(footer, text="Tải Game", command=self.load_game, bg="#FF9800", width=10).pack(side="left", padx=10)

        self.reset_game()

    def reset_game(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
        self.turn = 'white'
        self.selected_piece = None
        self.valid_moves = []
        self.draw_board()
        self.lbl_status.config(text="Lượt: Trắng (White)", fg="white")

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(8):
            for c in range(8):
                x1, y1 = c * self.cell_size, r * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                
                bg_color = self.board_colors[(r + c) % 2]
                
                if self.selected_piece == (r, c):
                    bg_color = "#F6F669" 

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg_color, outline="")

                if (r, c) in self.valid_moves:
                    if self.board[r][c] == '--':
                        cx, cy = x1 + self.cell_size/2, y1 + self.cell_size/2
                        self.canvas.create_oval(cx-8, cy-8, cx+8, cy+8, fill="#888888", outline="")
                    else:
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#FF5252", outline="")

                piece = self.board[r][c]
                if piece != '--':
                    color_p = piece[0]
                    type_p = piece[1]
                    char = self.pieces_chars[color_p][type_p]
                    self.canvas.create_text(x1+27, y1+27, text=char, font=("Segoe UI Symbol", 36), fill="black")

    def on_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        if 0 <= row < 8 and 0 <= col < 8:
            if (row, col) in self.valid_moves:
                self.move_piece(self.selected_piece, (row, col))
                return

            piece = self.board[row][col]
            if piece != '--' and piece[0] == self.turn[0]:
                self.selected_piece = (row, col)
                self.valid_moves = self.get_valid_moves(row, col, piece)
                self.draw_board()
            else:
                self.selected_piece = None
                self.valid_moves = []
                self.draw_board()

    def move_piece(self, start, end):
        r1, c1 = start
        r2, c2 = end
        
        self.board[r2][c2] = self.board[r1][c1]
        self.board[r1][c1] = '--'
        
        if self.board[r2][c2][1] == 'P':
            if (self.turn == 'white' and r2 == 0) or (self.turn == 'black' and r2 == 7):
                self.board[r2][c2] = self.turn[0] + 'Q'

        self.turn = 'black' if self.turn == 'white' else 'white'
        self.lbl_status.config(text=f"Lượt: {'Đen (Black)' if self.turn == 'black' else 'Trắng (White)'}",
                               fg="#FF5252" if self.turn == 'black' else "white")
        self.selected_piece = None
        self.valid_moves = []
        self.draw_board()

    def get_valid_moves(self, r, c, piece):
        moves = []
        color = piece[0]
        type_p = piece[1]
        enemy = 'b' if color == 'w' else 'w'
        direction = -1 if color == 'w' else 1

        if type_p == 'P': 
            if 0 <= r + direction < 8:
                if self.board[r + direction][c] == '--':
                    moves.append((r + direction, c))
                    if (color == 'w' and r == 6) or (color == 'b' and r == 1):
                        if self.board[r + direction*2][c] == '--':
                            moves.append((r + direction*2, c))
            for dc in [-1, 1]:
                if 0 <= r + direction < 8 and 0 <= c + dc < 8:
                    target = self.board[r + direction][c + dc]
                    if target != '--' and target[0] == enemy:
                        moves.append((r + direction, c + dc))

        elif type_p == 'N': 
            knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
            for dr, dc in knight_moves:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    if self.board[nr][nc] == '--' or self.board[nr][nc][0] == enemy:
                        moves.append((nr, nc))

        elif type_p == 'K': 
            king_moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dr, dc in king_moves:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    if self.board[nr][nc] == '--' or self.board[nr][nc][0] == enemy:
                        moves.append((nr, nc))

        elif type_p in ['R', 'B', 'Q']: 
            directions = []
            if type_p == 'R' or type_p == 'Q': directions.extend([(0, 1), (0, -1), (1, 0), (-1, 0)])
            if type_p == 'B' or type_p == 'Q': directions.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])
            
            for dr, dc in directions:
                for i in range(1, 8):
                    nr, nc = r + dr*i, c + dc*i
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        if self.board[nr][nc] == '--':
                            moves.append((nr, nc))
                        elif self.board[nr][nc][0] == enemy:
                            moves.append((nr, nc))
                            break
                        else: break
                    else: break
        return moves

    def save_game(self):
        if not os.path.exists(SAVE_FOLDER):
            try:
                os.makedirs(SAVE_FOLDER)
            except OSError as e:
                messagebox.showerror("Lỗi", f"Không tạo được thư mục lưu trữ:\n{e}")
                return

        file_path = os.path.join(SAVE_FOLDER, "chess_save.json")
        data = {
            "board": self.board,
            "turn": self.turn
        }
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f)
            messagebox.showinfo("Thành công", f"Đã lưu ván cờ tại:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không lưu được file: {e}")

    def load_game(self):
        file_path = os.path.join(SAVE_FOLDER, "chess_save.json")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            self.board = data["board"]
            self.turn = data["turn"]
            self.draw_board() 
            
            text_turn = 'Trắng (White)' if self.turn == 'white' else 'Đen (Black)'
            color_turn = 'white' if self.turn == 'white' else '#FF5252'
            self.lbl_status.config(text=f"Lượt: {text_turn}", fg=color_turn)
            
            messagebox.showinfo("Thành công", "Đã tải ván cờ cũ!")
        except FileNotFoundError:
            messagebox.showerror("Lỗi", f"Chưa có file lưu game tại:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"File bị lỗi: {e}")

# ==========================================
# KHỞI CHẠY CHƯƠNG TRÌNH
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
