import tkinter as tk
from tkinter import messagebox
import math
import random

# --- KHU VỰC IMPORT THƯ VIỆN KHOA HỌC DỮ LIỆU ---
# Numpy: Thư viện toán học, xử lý ma trận và tính toán khoảng cách nhanh (Dùng cho K-Means)
import numpy as np
# Matplotlib: Thư viện vẽ biểu đồ, dùng để hiển thị các cụm dữ liệu trực quan
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# Sklearn: Dùng hàm make_blobs để tạo ra dữ liệu giả lập (các đám mây điểm)
from sklearn.datasets import make_blobs

# =============================================================================
# PHẦN 1: CẤU HÌNH GIAO DIỆN "MODERN APP" (THEME)
# Tại đây định nghĩa các mã màu và font chữ dùng chung cho toàn bộ App.
# Thay đổi ở đây sẽ cập nhật giao diện toàn bộ chương trình.
# =============================================================================
APP_THEME = {
    "bg_main": "#121212",       # Nền đen chính (Dark mode background)
    "bg_card": "#1E1E1E",       # Nền các khối thẻ/nút (Sáng hơn nền chính)
    "accent": "#BB86FC",        # Màu nhấn chính (Tím nhạt - đặc trưng dark mode)
    "accent_2": "#03DAC6",      # Màu nhấn phụ (Xanh ngọc - dùng cho nút hành động)
    "text_main": "#FFFFFF",     # Màu chữ chính (Trắng)
    "text_sub": "#B0B0B0",      # Màu chữ phụ (Xám)
    "danger": "#CF6679",        # Màu đỏ (Dùng cho báo lỗi, nút Thoát)
    "success": "#03DAC6",       # Màu xanh (Thành công)
    "board_bg": "#1E1E1E",      # Nền bàn cờ Caro
    "grid_line": "#333333"      # Màu đường kẻ lưới
}

FONTS = {
    "h1": ("Segoe UI", 24, "bold"), # Font tiêu đề lớn
    "h2": ("Segoe UI", 16, "bold"), # Font tiêu đề vừa
    "body": ("Segoe UI", 11),       # Font nội dung thường
    "btn": ("Segoe UI", 11, "bold"),# Font nút bấm
    "icon": ("Segoe UI Emoji", 28)  # Font để hiển thị Emoji kích thước lớn
}

# =============================================================================
# PHẦN 2: WIDGET TÙY CHỈNH (CUSTOM UI)
# Tạo các class kế thừa từ Tkinter để làm đẹp giao diện mặc định
# =============================================================================
class AppButton(tk.Frame):
    """
    Nút bấm dạng Thẻ (Card) giống menu cài đặt trên điện thoại.
    Bao gồm: Icon bên trái, Tiêu đề, Mô tả nhỏ và Mũi tên bên phải.
    """
    def __init__(self, master, title, subtitle, icon, command, color=APP_THEME["bg_card"]):
        super().__init__(master, bg=color, cursor="hand2", pady=10, padx=10)
        self.command = command
        self.default_bg = color
        self.hover_bg = "#2C2C2C" # Màu khi di chuột vào (sáng hơn chút)

        # Gắn sự kiện click cho toàn bộ khung (Frame)
        self.bind("<Button-1>", lambda e: command())
        self.bind("<Enter>", self.on_enter) # Sự kiện chuột đi vào
        self.bind("<Leave>", self.on_leave) # Sự kiện chuột đi ra

        # Icon (Dùng Emoji)
        lbl_icon = tk.Label(self, text=icon, font=FONTS["icon"], bg=color, fg=APP_THEME["accent"])
        lbl_icon.pack(side="left", padx=(10, 15))
        lbl_icon.bind("<Button-1>", lambda e: command())

        # Container chứa chữ (Title + Subtitle)
        text_frame = tk.Frame(self, bg=color)
        text_frame.pack(side="left", fill="both", expand=True)
        text_frame.bind("<Button-1>", lambda e: command())

        # Tiêu đề ứng dụng
        lbl_title = tk.Label(text_frame, text=title, font=FONTS["h2"], bg=color, fg=APP_THEME["text_main"], anchor="w")
        lbl_title.pack(fill="x")
        lbl_title.bind("<Button-1>", lambda e: command())

        # Mô tả ngắn
        lbl_sub = tk.Label(text_frame, text=subtitle, font=("Segoe UI", 9), bg=color, fg=APP_THEME["text_sub"], anchor="w")
        lbl_sub.pack(fill="x")
        lbl_sub.bind("<Button-1>", lambda e: command())

        # Dấu mũi tên điều hướng (›)
        lbl_arrow = tk.Label(self, text="›", font=("Segoe UI", 20), bg=color, fg="#555555")
        lbl_arrow.pack(side="right", padx=10)
        lbl_arrow.bind("<Button-1>", lambda e: command())
        
        # Lưu danh sách các widget con để đổi màu đồng loạt khi hover
        self.children_widgets = [lbl_icon, text_frame, lbl_title, lbl_sub, lbl_arrow]

    def on_enter(self, e):
        """Hiệu ứng khi di chuột vào: Đổi màu nền sáng hơn"""
        self.config(bg=self.hover_bg)
        for w in self.children_widgets: w.config(bg=self.hover_bg)

    def on_leave(self, e):
        """Hiệu ứng khi chuột rời đi: Trả về màu cũ"""
        self.config(bg=self.default_bg)
        for w in self.children_widgets: w.config(bg=self.default_bg)

class FlatButton(tk.Button):
    """
    Nút bấm phẳng (Flat Design), hiện đại hơn nút mặc định của Windows.
    Kế thừa từ tk.Button chuẩn.
    """
    def __init__(self, master, **kwargs):
        bg = kwargs.get("bg", APP_THEME["accent"])
        # Thiết lập mặc định nếu không truyền tham số
        kwargs.setdefault("bg", bg)
        # Tự động chọn màu chữ đen hoặc trắng tùy theo màu nền
        kwargs.setdefault("fg", "#000000" if bg in [APP_THEME["accent"], APP_THEME["accent_2"]] else "white")
        kwargs.setdefault("font", FONTS["btn"])
        kwargs.setdefault("relief", "flat") # Loại bỏ viền nổi 3D cũ kỹ
        kwargs.setdefault("cursor", "hand2")
        kwargs.setdefault("pady", 8)
        super().__init__(master, **kwargs)

# =============================================================================
# PHẦN 3: MÀN HÌNH CHÍNH (DASHBOARD)
# Nơi chứa danh sách các ứng dụng con.
# =============================================================================
class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Super App")
        self.root.geometry("400x750") # Kích thước chuẩn tỉ lệ điện thoại
        self.root.configure(bg=APP_THEME["bg_main"])
        self.center_window(400, 750)
        

        # --- Header (Phần chào hỏi) ---
        header = tk.Frame(root, bg=APP_THEME["bg_main"], pady=30, padx=20)
        header.pack(fill="x")
        
        tk.Label(header, text="Xin chào,", font=("Segoe UI", 14), bg=APP_THEME["bg_main"], fg=APP_THEME["text_sub"]).pack(anchor="w")
        tk.Label(header, text="Tú Đoàn", font=("Segoe UI", 32, "bold"), bg=APP_THEME["bg_main"], fg=APP_THEME["text_main"]).pack(anchor="w")

        # --- Container chứa danh sách App ---
        container = tk.Frame(root, bg=APP_THEME["bg_main"], padx=20)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="ỨNG DỤNG", font=("Segoe UI", 10, "bold"), bg=APP_THEME["bg_main"], fg="#555555").pack(anchor="w", pady=(10, 5))

        # Tạo 3 thẻ ứng dụng trỏ tới 3 hàm mở cửa sổ con
        AppButton(container, "Cờ Caro Pro", "PvP hoặc đấu với AI", "❌", self.open_caro).pack(fill="x", pady=8)
        AppButton(container, "Tô Màu Đồ Thị", "Thuật toán tham lam", "🎨", self.open_graph).pack(fill="x", pady=8)
        AppButton(container, "K-Means AI", "Phân cụm dữ liệu", "🧠", self.open_kmeans).pack(fill="x", pady=8)
        AppButton(container, "Cờ Vua Master", "Kinh điển & Trí tuệ", "♟️", self.open_chess).pack(fill="x", pady=8)

        # --- Footer (Nút thoát) ---
        footer = tk.Frame(root, bg=APP_THEME["bg_main"], pady=20)
        footer.pack(side="bottom", fill="x")
        FlatButton(footer, text="Thoát Ứng Dụng", bg=APP_THEME["bg_card"], fg=APP_THEME["danger"], command=self.exit_app, width=20).pack()

    def center_window(self, width, height):
        """Hàm toán học để căn giữa cửa sổ ứng dụng trên màn hình máy tính"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    # Các hàm mở cửa sổ con (dùng Toplevel để tạo cửa sổ mới đè lên cửa sổ chính)
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
# PHẦN 4: MODULE GAME CỜ CARO
# Logic: Ma trận 2 chiều, Check 5 ô liên tiếp, AI ngẫu nhiên/chặn.
# =============================================================================
class CaroGame:
    def __init__(self, window):
        self.window = window
        self.window.title("Caro Game")
        self.window.geometry("450x600")
        self.window.configure(bg=APP_THEME["bg_main"])
        
        # --- Màn hình Cài đặt (Setup Screen) ---
        self.frame_setup = tk.Frame(window, bg=APP_THEME["bg_main"], padx=30, pady=30)
        self.frame_setup.pack(expand=True, fill="both")
        
        tk.Label(self.frame_setup, text="CẤU HÌNH", font=FONTS["h1"], bg=APP_THEME["bg_main"], fg=APP_THEME["text_main"]).pack(pady=(0, 30))
        
        # Input kích thước bàn cờ
        lbl_n = tk.Label(self.frame_setup, text="Kích thước bàn cờ (3-30):", font=FONTS["body"], bg=APP_THEME["bg_main"], fg=APP_THEME["text_sub"])
        lbl_n.pack(anchor="w")
        self.entry_n = tk.Entry(self.frame_setup, font=("Segoe UI", 12), bg=APP_THEME["bg_card"], fg="white", insertbackground="white", relief="flat")
        self.entry_n.insert(0, "10") # Mặc định là 10x10
        self.entry_n.pack(fill="x", pady=(5, 20), ipady=5)

        # Radio button chọn chế độ chơi
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

        # Nút bắt đầu
        btn_start = FlatButton(self.frame_setup, text="VÀO TRẬN", command=self.start_game, bg=APP_THEME["accent"])
        btn_start.pack(fill="x", pady=30)

        # Khởi tạo biến
        self.canvas = None
        self.board = []   
        self.turn = 'X'   
        self.game_over = False
        self.move_count = 0

    def start_game(self):
        """Xử lý khi nhấn 'Vào Trận': Kiểm tra input và chuyển màn hình"""
        try:
            val = int(self.entry_n.get())
            if val < 3 or val > 30: raise ValueError
            self.n = val
        except ValueError:
            messagebox.showerror("Lỗi", "Nhập số từ 3 đến 30!")
            return

        self.is_pve = (self.mode_var.get() == "PvE")
        self.frame_setup.destroy() # Xóa màn hình cài đặt
        self.create_board_ui()     # Vẽ bàn cờ

    def create_board_ui(self):
        """Vẽ giao diện bàn cờ lên Canvas"""
        # Header hiển thị lượt đi
        top_bar = tk.Frame(self.window, bg=APP_THEME["bg_main"], pady=10)
        top_bar.pack(fill="x")
        self.lbl_turn = tk.Label(top_bar, text="Lượt: X", font=FONTS["h2"], bg=APP_THEME["bg_main"], fg=APP_THEME["danger"])
        self.lbl_turn.pack()

        # Tính toán kích thước ô dựa trên số lượng ô (n càng lớn ô càng nhỏ)
        if self.n <= 8: self.cell_size = 50
        elif self.n <= 15: self.cell_size = 32
        else: self.cell_size = 24

        w = self.n * self.cell_size
        h = self.n * self.cell_size

        frame_canvas = tk.Frame(self.window, bg=APP_THEME["bg_main"])
        frame_canvas.pack(expand=True)
        
        self.canvas = tk.Canvas(frame_canvas, width=w, height=h, bg=APP_THEME["board_bg"], highlightthickness=0)
        self.canvas.pack()
        
        # Vẽ lưới caro
        for i in range(self.n + 1):
             self.canvas.create_line(i*self.cell_size, 0, i*self.cell_size, h, fill=APP_THEME["grid_line"])
             self.canvas.create_line(0, i*self.cell_size, w, i*self.cell_size, fill=APP_THEME["grid_line"])

        # Gắn sự kiện click chuột
        self.canvas.bind("<Button-1>", self.on_user_click)
        
        # Thanh điều khiển phía dưới
        ctrl = tk.Frame(self.window, bg=APP_THEME["bg_main"], pady=20)
        ctrl.pack(fill="x")
        FlatButton(ctrl, text="Chơi Lại", command=self.reset_game, bg=APP_THEME["bg_card"], fg="white", width=12).pack(side="left", padx=20)
        FlatButton(ctrl, text="Thoát", command=self.window.destroy, bg=APP_THEME["danger"], width=12).pack(side="right", padx=20)

        # Reset dữ liệu ma trận
        self.board = [['' for _ in range(self.n)] for _ in range(self.n)]
        self.move_count = 0
        self.game_over = False
        self.turn = 'X'

    def reset_game(self):
        self.window.destroy()
        CaroGame(tk.Toplevel())

    def on_user_click(self, event):
        """Xử lý khi người chơi click vào bàn cờ"""
        if self.game_over: return
        if self.is_pve and self.turn == 'O': return # Nếu đang lượt máy thì chặn click

        # Tính tọa độ ô (hàng, cột) từ tọa độ pixel chuột
        c = event.x // self.cell_size
        r = event.y // self.cell_size

        if 0 <= r < self.n and 0 <= c < self.n and self.board[r][c] == '':
            self.make_move(r, c) 
            # Nếu chơi với máy, gọi máy đi sau 400ms
            if not self.game_over and self.is_pve:
                self.window.after(400, self.computer_move)

    def make_move(self, r, c):
        """Thực hiện nước đi tại ô (r, c) cho phe hiện tại"""
        cx = c * self.cell_size + self.cell_size // 2
        cy = r * self.cell_size + self.cell_size // 2
        
        if self.turn == 'X':
            # Vẽ chữ X màu Đỏ neon
            color = APP_THEME["danger"]
            offset = self.cell_size // 4
            self.canvas.create_line(cx-offset, cy-offset, cx+offset, cy+offset, width=3, fill=color, capstyle="round")
            self.canvas.create_line(cx+offset, cy-offset, cx-offset, cy+offset, width=3, fill=color, capstyle="round")
        else:
            # Vẽ chữ O màu Xanh neon
            color = APP_THEME["accent_2"]
            radius = self.cell_size // 3
            self.canvas.create_oval(cx-radius, cy-radius, cx+radius, cy+radius, width=3, outline=color)

        self.board[r][c] = self.turn
        self.move_count += 1 

        # Kiểm tra thắng
        if self.check_winner(r, c):
            messagebox.showinfo("Kết quả", f"{self.turn} Thắng!")
            self.game_over = True
            return

        # Kiểm tra hòa (full bàn)
        if self.move_count >= self.n * self.n:
            messagebox.showinfo("Kết quả", "Hòa!")
            self.game_over = True
            return

        # Đổi lượt
        self.turn = 'O' if self.turn == 'X' else 'X'
        self.lbl_turn.config(text=f"Lượt: {self.turn}", fg=APP_THEME["danger"] if self.turn=='X' else APP_THEME["accent_2"])

    def computer_move(self):
        """AI đơn giản: Ưu tiên Thắng -> Chặn -> Random"""
        if self.game_over: return
        empty = [(r, c) for r in range(self.n) for c in range(self.n) if self.board[r][c] == '']
        if not empty: return
        
        # 1. Thử đánh vào ô trống, nếu thắng thì đánh luôn
        for r, c in empty:
            self.board[r][c] = 'O'
            if self.check_winner(r, c):
                self.board[r][c] = ''
                self.make_move(r, c)
                return
            self.board[r][c] = ''
            
        # 2. Nếu người sắp thắng, đánh chặn ngay
        for r, c in empty:
            self.board[r][c] = 'X'
            if self.check_winner(r, c):
                self.board[r][c] = ''
                self.make_move(r, c)
                return
            self.board[r][c] = ''

        # 3. Đánh ngẫu nhiên
        move = random.choice(empty)
        self.make_move(move[0], move[1])

    def check_winner(self, r, c):
        """Thuật toán check 5 ô liên tiếp theo 4 hướng"""
        # Luật: Nếu bàn nhỏ thì số con cần thắng = kích thước bàn, lớn thì cần 5
        win_num = 5 if self.n >= 5 else self.n
        player = self.board[r][c]
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)] # Ngang, Dọc, Chéo chính, Chéo phụ
        
        for dr, dc in directions:
            count = 1
            # Duyệt về phía trước
            for k in range(1, win_num):
                nr, nc = r + dr*k, c + dc*k
                if 0 <= nr < self.n and 0 <= nc < self.n and self.board[nr][nc] == player: count += 1
                else: break
            # Duyệt về phía sau
            for k in range(1, win_num):
                nr, nc = r - dr*k, c - dc*k
                if 0 <= nr < self.n and 0 <= nc < self.n and self.board[nr][nc] == player: count += 1
                else: break
            
            if count >= win_num: return True
        return False

# =============================================================================
# PHẦN 5: MODULE ĐỒ THỊ (REAL-TIME COLORING)
# Logic: Tương tác trực tiếp trên canvas, nối dây là đổi màu ngay lập tức.
# =============================================================================
class GraphColoring:
    def __init__(self, window):
        self.window = window
        self.window.title("Graph Coloring")
        self.window.geometry("900x600")
        self.window.configure(bg=APP_THEME["bg_main"])

        # Biến đồ thị
        self.adj = {}        # Danh sách kề
        self.node_pos = {}   # Tọa độ các nút
        self.selected_node = None # Nút đang được chọn để nối
        self.radius = 25     # Bán kính nút vẽ
        self.n = 0           

        # Layout chính
        main_frame = tk.Frame(window, bg=APP_THEME["bg_main"])
        main_frame.pack(fill="both", expand=True)

        # Sidebar (Cột trái)
        sidebar = tk.Frame(main_frame, bg=APP_THEME["bg_card"], width=250, padx=20, pady=20)
        sidebar.pack(side="left", fill="y")
        
        tk.Label(sidebar, text="BẢNG ĐIỀU KHIỂN", font=FONTS["h2"], bg=APP_THEME["bg_card"], fg=APP_THEME["text_main"]).pack(pady=(0, 20))

        tk.Label(sidebar, text="Số đỉnh:", font=FONTS["body"], bg=APP_THEME["bg_card"], fg=APP_THEME["text_sub"]).pack(anchor="w")
        self.entry_nodes = tk.Entry(sidebar, font=("Segoe UI", 12), bg="#333", fg="white", relief="flat", justify="center")
        self.entry_nodes.insert(0, "6")
        self.entry_nodes.pack(fill="x", pady=5, ipady=5)
        
        FlatButton(sidebar, text="Tạo Mới", command=self.init_nodes, bg=APP_THEME["accent_2"]).pack(fill="x", pady=15)

        tk.Label(sidebar, text="Hướng dẫn:\nClick đỉnh để chọn.\nClick đỉnh khác để nối.", 
                 font=("Segoe UI", 10), bg=APP_THEME["bg_card"], fg="#888", justify="left").pack(pady=20)

        # Canvas vẽ (Bên phải)
        content = tk.Frame(main_frame, bg=APP_THEME["bg_main"], padx=20, pady=20)
        content.pack(side="right", fill="both", expand=True)
        self.canvas = tk.Canvas(content, bg="#252526", highlightthickness=0) # Canvas màu xám đậm
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def init_nodes(self):
        """Khởi tạo các nút xếp vòng tròn"""
        self.canvas.delete("all")
        try:
            self.n = int(self.entry_nodes.get())
            if self.n < 1: raise ValueError
        except:
            return

        self.adj = {i: [] for i in range(self.n)}
        self.node_pos = {}
        self.selected_node = None

        self.window.update() # Cập nhật layout để lấy kích thước thật
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        cx, cy = w/2, h/2
        r_layout = min(w, h)/2 - 60

        # Tính tọa độ sin/cos để xếp tròn
        for i in range(self.n):
            angle = 2 * math.pi * i / self.n - math.pi/2
            x = cx + r_layout * math.cos(angle)
            y = cy + r_layout * math.sin(angle)
            self.node_pos[i] = (x, y)

        self.solve_and_draw()

    def on_canvas_click(self, event):
        """Xử lý click: Chọn nút, nối dây, cập nhật màu"""
        if self.n == 0: return
        click_x, click_y = event.x, event.y
        clicked_node = None

        # Kiểm tra xem click trúng nút nào (Pythagoras)
        for i, (nx, ny) in self.node_pos.items():
            if (click_x - nx)**2 + (click_y - ny)**2 <= self.radius**2:
                clicked_node = i
                break
        
        if clicked_node is not None:
            if self.selected_node is None:
                self.selected_node = clicked_node # Chọn nút đầu
            else:
                if self.selected_node == clicked_node:
                    self.selected_node = None # Bỏ chọn
                else:
                    # Logic thêm/xóa cạnh
                    u, v = self.selected_node, clicked_node
                    if v in self.adj[u]:
                        self.adj[u].remove(v)
                        self.adj[v].remove(u)
                    else:
                        self.adj[u].append(v)
                        self.adj[v].append(u)
                    self.selected_node = None 
            self.solve_and_draw() # Vẽ lại ngay lập tức
        else:
            self.selected_node = None
            self.solve_and_draw()

    def solve_and_draw(self):
        """Thuật toán Greedy Coloring + Vẽ hình"""
        # Bảng màu rực rỡ cho nền tối
        colors_palette = ["#FF5252", "#448AFF", "#69F0AE", "#E040FB", "#FFD740", "#00BCD4", "#FF6E40"]
        node_colors = {}
        # Sắp xếp nút theo bậc (số cạnh nối) giảm dần để tô tối ưu
        sorted_nodes = sorted(range(self.n), key=lambda x: len(self.adj[x]), reverse=True)
        
        # Tô màu
        for u in sorted_nodes:
            forbidden = {node_colors[v] for v in self.adj[u] if v in node_colors}
            for color in colors_palette:
                if color not in forbidden:
                    node_colors[u] = color
                    break
            if u not in node_colors: node_colors[u] = "#757575" # Hết màu thì tô xám

        self.canvas.delete("all")
        
        # Vẽ dây (cạnh)
        drawn_edges = set()
        for u in range(self.n):
            for v in self.adj[u]:
                if (u, v) not in drawn_edges and (v, u) not in drawn_edges:
                    x1, y1 = self.node_pos[u]
                    x2, y2 = self.node_pos[v]
                    self.canvas.create_line(x1, y1, x2, y2, fill="#555", width=2)
                    drawn_edges.add((u, v))

        # Vẽ nút (đỉnh)
        for i in range(self.n):
            x, y = self.node_pos[i]
            c = node_colors.get(i, "white")
            
            # Hiệu ứng khi đang chọn nút
            if i == self.selected_node:
                outline_c = "white"
                width_line = 3
                r = self.radius + 3
            else:
                outline_c = ""
                width_line = 0
                r = self.radius

            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=c, outline=outline_c, width=width_line)
            # Chữ đen trên nền màu sáng
            self.canvas.create_text(x, y, text=str(i), font=("Segoe UI", 11, "bold"), fill="#121212")

# =============================================================================
# PHẦN 6: MODULE K-MEANS (MÔ PHỎNG PHÂN CỤM)
# Logic: Sinh dữ liệu ngẫu nhiên -> Chạy từng bước E-step, M-step -> Animation.
# =============================================================================
class KMeansWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("K-Means Clustering")
        self.geometry("900x600")
        self.configure(bg=APP_THEME["bg_main"])
        self.is_running = False
        
        # Thanh điều khiển (Trên cùng)
        controls = tk.Frame(self, bg=APP_THEME["bg_card"], pady=15, padx=15)
        controls.pack(side="top", fill="x")
        
        # Hàm phụ tạo ô input nhanh
        def create_input(lbl, val):
            tk.Label(controls, text=lbl, bg=APP_THEME["bg_card"], fg="white").pack(side="left", padx=(10, 5))
            e = tk.Entry(controls, width=5, bg="#333", fg="white", relief="flat", justify="center")
            e.insert(0, str(val))
            e.pack(side="left")
            return e

        self.entry_n = create_input("Số điểm:", 300)
        self.entry_c_true = create_input("Số cụm gốc:", 4) # Cụm thực tế (đề bài)
        self.entry_k = create_input("K tìm kiếm:", 4)     # Cụm máy đoán

        FlatButton(controls, text="CHẠY MÔ PHỎNG", command=self.start_process, bg=APP_THEME["accent"], width=15).pack(side="right", padx=10)

        # Khu vực vẽ biểu đồ
        plot_frame = tk.Frame(self, bg=APP_THEME["bg_main"])
        plot_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Cấu hình Matplotlib Dark Theme
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.fig.patch.set_facecolor(APP_THEME["bg_main"]) # Nền ngoài
        self.ax.set_facecolor(APP_THEME["bg_card"])        # Nền trong biểu đồ
        
        # Nhúng biểu đồ vào Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Thanh Log trạng thái
        self.lbl_log = tk.Label(self, text="Sẵn sàng...", bg=APP_THEME["bg_main"], fg=APP_THEME["text_sub"], font=("Consolas", 10))
        self.lbl_log.pack(side="bottom", pady=5)

    def visualize(self, X, centers, labels, k, msg):
        """Vẽ lại toàn bộ biểu đồ"""
        self.ax.clear()
        self.lbl_log.config(text=f"> {msg}")
        
        cmap = plt.get_cmap('tab10') # Bảng màu chuẩn
        # Vẽ các điểm dữ liệu
        for i in range(k):
            cluster_data = X[labels == i]
            if len(cluster_data) > 0:
                color = cmap(i % 10)
                self.ax.scatter(cluster_data[:, 0], cluster_data[:, 1], color=color, alpha=0.7, s=20, edgecolors='none')
        
        # Vẽ tâm cụm (Hình chữ X to)
        if centers is not None:
            self.ax.scatter(centers[:, 0], centers[:, 1], c='white', s=150, marker='X', edgecolors='black', linewidth=1.5, zorder=10)
        
        self.ax.grid(color='#333', linestyle='--', linewidth=0.5)
        self.canvas.draw()

    def start_process(self):
        """Bắt đầu thuật toán"""
        self.is_running = False 
        try:
            n = int(self.entry_n.get())
            c_true = int(self.entry_c_true.get())
            self.k = int(self.entry_k.get())

            # 1. Tạo dữ liệu giả lập
            self.X, _ = make_blobs(n_samples=n, centers=c_true, cluster_std=1.0, random_state=42)
            
            # 2. Chọn tâm ngẫu nhiên ban đầu
            idx = np.random.choice(n, self.k, replace=False)
            self.centers = self.X[idx]
            self.labels = np.zeros(n, dtype=int)
            
            self.visualize(self.X, self.centers, self.labels, self.k, "Khởi tạo tâm ngẫu nhiên...")
            
            # Bắt đầu vòng lặp
            self.is_running = True
            self.after(800, lambda: self.loop_step(0))

        except ValueError:
            messagebox.showerror("Lỗi", "Kiểm tra lại dữ liệu nhập!")

    def loop_step(self, step):
        """Bước E (Expectation): Gán mỗi điểm vào tâm gần nhất"""
        if not self.is_running: return
        distances = np.linalg.norm(self.X[:, np.newaxis] - self.centers, axis=2)
        self.labels = np.argmin(distances, axis=1)
        self.visualize(self.X, self.centers, self.labels, self.k, f"Bước {step+1}: Gán nhãn (Tìm cụm gần nhất)")
        self.after(600, lambda: self.update_step(step))

    def update_step(self, step):
        """Bước M (Maximization): Cập nhật vị trí tâm mới"""
        if not self.is_running: return
        old_centers = self.centers.copy()
        new_centers = np.zeros_like(self.centers)

        # Tính trung bình cộng vị trí các điểm trong cụm để tìm tâm mới
        for i in range(self.k):
            points = self.X[self.labels == i]
            if len(points) > 0:
                new_centers[i] = points.mean(axis=0)
            else:
                new_centers[i] = old_centers[i]

        self.centers = new_centers
        shift = np.linalg.norm(self.centers - old_centers)
        
        # Kiểm tra hội tụ (Tâm không di chuyển nữa)
        if shift < 1e-4:
            self.visualize(self.X, self.centers, self.labels, self.k, "Đã hội tụ! Hoàn tất.")
            self.is_running = False
            return

        self.visualize(self.X, self.centers, self.labels, self.k, f"Bước {step+1}: Cập nhật vị trí tâm")
        self.after(600, lambda: self.loop_step(step + 1))
        
# =============================================================================
# PHẦN 7: MODULE CỜ VUA (CHESS - FINAL FIX)
# =============================================================================
class ChessGame:
    def __init__(self, window):
        self.window = window
        self.window.title("Chess Master")
        self.window.geometry("500x680")
        self.window.configure(bg=APP_THEME["bg_main"])
        
        # Cấu hình bàn cờ
        self.cell_size = 55
        self.board_colors = ["#F0D9B5", "#B58863"] # Màu gỗ sáng/tối
        self.selected_piece = None
        self.turn = 'white'
        self.valid_moves = []

        # Unicode Quân cờ
        self.pieces_chars = {
            'w': {'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙'},
            'b': {'K': '♚', 'Q': '♛', 'R': '♜', 'B': '♝', 'N': '♞', 'P': '♟'}
        }
        
        # Header
        header = tk.Frame(window, bg=APP_THEME["bg_main"], pady=10)
        header.pack(fill="x")
        self.lbl_status = tk.Label(header, text="Lượt: Trắng (White)", font=FONTS["h2"], 
                                   bg=APP_THEME["bg_main"], fg="white")
        self.lbl_status.pack()

        # Canvas
        self.canvas = tk.Canvas(window, width=440, height=440, bg=APP_THEME["bg_main"], highlightthickness=0)
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.on_click)

        # Footer
        footer = tk.Frame(window, bg=APP_THEME["bg_main"], pady=10)
        footer.pack(fill="x")
        FlatButton(footer, text="Ván Mới", command=self.reset_game, bg=APP_THEME["accent_2"], width=15).pack()

        self.reset_game()

    def reset_game(self):
        # Khởi tạo bàn cờ
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
                
                # 1. Vẽ ô cờ
                bg_color = self.board_colors[(r + c) % 2]
                
                # Highlight ô đang chọn
                if self.selected_piece == (r, c):
                    bg_color = "#F6F669" # Vàng highlight

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg_color, outline="")

                # Highlight nước đi gợi ý
                if (r, c) in self.valid_moves:
                    if self.board[r][c] == '--':
                        # [ĐÃ SỬA LỖI] Dùng màu xám đặc thay vì rgba trong suốt
                        cx, cy = x1 + self.cell_size/2, y1 + self.cell_size/2
                        self.canvas.create_oval(cx-8, cy-8, cx+8, cy+8, fill="#888888", outline="")
                    else:
                        # Ô ăn quân: Viền đỏ
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#FF5252", outline="")

                # 2. Vẽ quân cờ
                piece = self.board[r][c]
                if piece != '--':
                    color_p = piece[0]
                    type_p = piece[1]
                    char = self.pieces_chars[color_p][type_p]
                    
                    # Vẽ quân cờ (Màu đen hết để tương phản tốt nhất trên nền gỗ)
                    # Quân trắng trong Unicode là nét rỗng (♔), Quân đen là nét đặc (♚)
                    # Nên ta tô fill="black" cho cả 2 là đẹp nhất
                    self.canvas.create_text(x1+27, y1+27, text=char, font=("Segoe UI Symbol", 36), fill="black")

    def on_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        if 0 <= row < 8 and 0 <= col < 8:
            # Nếu click vào ô gợi ý -> Di chuyển
            if (row, col) in self.valid_moves:
                self.move_piece(self.selected_piece, (row, col))
                return

            # Nếu click vào quân mình -> Chọn
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
        
        # Phong Hậu
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

        if type_p == 'P': # Tốt
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

        elif type_p == 'N': # Mã
            knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
            for dr, dc in knight_moves:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    if self.board[nr][nc] == '--' or self.board[nr][nc][0] == enemy:
                        moves.append((nr, nc))

        elif type_p == 'K': # Vua
            king_moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dr, dc in king_moves:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    if self.board[nr][nc] == '--' or self.board[nr][nc][0] == enemy:
                        moves.append((nr, nc))

        elif type_p in ['R', 'B', 'Q']: # Xe, Tượng, Hậu
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
    
# ==========================================
# KHỞI CHẠY CHƯƠNG TRÌNH
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
