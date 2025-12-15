import tkinter as tk
from tkinter import messagebox
import math
import random

# --- KHU VỰC IMPORT THƯ VIỆN KHOA HỌC DỮ LIỆU ---
# Numpy: Dùng để tính toán ma trận, khoảng cách (cần cho K-Means)
import numpy as np
# Matplotlib: Dùng để vẽ biểu đồ minh họa thuật toán
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# Sklearn: Dùng để tạo dữ liệu giả lập (các cụm điểm)
from sklearn.datasets import make_blobs

# =============================================================================
# PHẦN 1: CẤU HÌNH GIAO DIỆN (CONSTANTS)
# Định nghĩa các màu sắc và font chữ dùng chung cho toàn bộ ứng dụng
# giúp dễ dàng thay đổi giao diện ở một nơi duy nhất.
# =============================================================================
COLORS = {
    "bg_main": "#F0F2F5",       # Màu nền chính (Xám nhạt)
    "bg_dark": "#2C3E50",       # Màu nền header (Xanh đậm)
    "text_header": "#ECF0F1",   # Màu chữ header
    "btn_primary": "#3498DB",   # Nút chính (Xanh dương)
    "btn_hover": "#2980B9",     # Nút khi di chuột
    "btn_success": "#27AE60",   # Nút hành động (Xanh lá - Bắt đầu)
    "btn_danger": "#E74C3C",    # Nút thoát/Hủy (Đỏ)
    "btn_ml": "#8E44AD",        # Màu riêng cho nút Machine Learning (Tím)
    "btn_ml_hover": "#9B59B6",  
    "board_bg": "#FFFFFF",      # Nền bàn cờ Caro
    "x_color": "#E74C3C",       # Màu quân X
    "o_color": "#3498DB"        # Màu quân O
}

FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_NORMAL = ("Segoe UI", 11)
FONT_BOLD = ("Segoe UI", 11, "bold")

# =============================================================================
# PHẦN 2: CLASS TIỆN ÍCH GIAO DIỆN (CUSTOM WIDGETS)
# Tạo ra một nút bấm (Button) đẹp hơn nút mặc định của Tkinter
# =============================================================================
class StyledButton(tk.Button):
    """
    Class này kế thừa tk.Button để tạo nút có hiệu ứng đổi màu 
    khi di chuột vào (Hover effect).
    """
    def __init__(self, master, **kwargs):
        self.bg_color = kwargs.get("bg", COLORS["btn_primary"])
        self.hover_color = kwargs.pop("hover_bg", COLORS["btn_hover"])
        
        # Thiết lập style mặc định (không viền, con trỏ tay, padding)
        kwargs.setdefault("fg", "white")
        kwargs.setdefault("font", FONT_BOLD)
        kwargs.setdefault("relief", "flat")
        kwargs.setdefault("cursor", "hand2")
        kwargs.setdefault("pady", 8)
        
        super().__init__(master, **kwargs)
        # Gắn sự kiện chuột
        self.bind("<Enter>", self.on_enter) # Khi chuột đi vào
        self.bind("<Leave>", self.on_leave) # Khi chuột đi ra

    def on_enter(self, e):
        self['bg'] = self.hover_color

    def on_leave(self, e):
        self['bg'] = self.bg_color

# =============================================================================
# PHẦN 3: GIAO DIỆN CHÍNH (MAIN MENU)
# Cửa sổ đầu tiên hiện ra, chứa các nút để mở các game/tool khác.
# =============================================================================
class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python App Collection")
        self.root.geometry("500x550")
        self.root.configure(bg=COLORS["bg_main"])
        self.center_window(500, 550) # Căn giữa màn hình

        # --- Header (Tiêu đề trên cùng) ---
        header_frame = tk.Frame(root, bg=COLORS["bg_dark"], pady=20)
        header_frame.pack(fill="x")
        
        lbl_title = tk.Label(header_frame, text="TỔNG HỢP ỨNG DỤNG", font=("Segoe UI", 20, "bold"), 
                             bg=COLORS["bg_dark"], fg=COLORS["text_header"])
        lbl_title.pack()

        # --- Content (Khu vực chứa nút bấm) ---
        content_frame = tk.Frame(root, bg=COLORS["bg_main"], pady=30)
        content_frame.pack(fill="both", expand=True)

        # Nhóm Game
        tk.Label(content_frame, text="🎮 MINI GAMES", font=("Segoe UI", 12, "bold"), bg=COLORS["bg_main"], fg="#7F8C8D").pack(pady=(0, 10))

        # Nút mở Cờ Caro
        StyledButton(content_frame, text="Cờ Caro (PvP / PvE)", width=35, 
                     bg=COLORS["btn_primary"], hover_bg="#2980B9",
                     command=self.open_caro).pack(pady=5)

        # Nút mở Tô màu đồ thị
        StyledButton(content_frame, text="Thuật Toán Tô Màu Đồ Thị", width=35,
                     bg="#16A085", hover_bg="#1ABC9C",
                     command=self.open_graph).pack(pady=5)

        # Nhóm Machine Learning
        tk.Label(content_frame, text="🧠 MACHINE LEARNING", font=("Segoe UI", 12, "bold"), bg=COLORS["bg_main"], fg="#7F8C8D").pack(pady=(20, 10))

        # Nút mở K-Means
        StyledButton(content_frame, text="Mô Phỏng Gom Cụm K-Means", width=35,
                     bg=COLORS["btn_ml"], hover_bg=COLORS["btn_ml_hover"],
                     command=self.open_kmeans).pack(pady=5)

        # Nút Thoát
        tk.Frame(content_frame, height=20, bg=COLORS["bg_main"]).pack() # Khoảng trống
        StyledButton(content_frame, text="❌ Thoát Chương Trình", width=35,
                     bg=COLORS["btn_danger"], hover_bg="#C0392B",
                     command=self.exit_app).pack(pady=20)

        # Footer (Chữ ký cuối trang)
        tk.Label(root, text="Developed with Python Tkinter & Scikit-learn", font=("Segoe UI", 9), 
                 bg=COLORS["bg_main"], fg="#95A5A6").pack(side="bottom", pady=10)

    def center_window(self, width, height):
        """Hàm tính toán để cửa sổ luôn hiện giữa màn hình máy tính"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    # --- Các hàm mở cửa sổ con ---
    def open_caro(self):
        CaroGame(tk.Toplevel(self.root)) # Mở cửa sổ Caro

    def open_graph(self):
        GraphColoring(tk.Toplevel(self.root)) # Mở cửa sổ Đồ thị
    
    def open_kmeans(self):
        KMeansWindow(self.root) # Mở cửa sổ K-Means

    def exit_app(self):
        if messagebox.askokcancel("Xác nhận", "Bạn có chắc muốn thoát không?"):
            self.root.destroy()


# =============================================================================
# PHẦN 4: MODULE GAME CỜ CARO
# Xử lý logic game, vẽ bàn cờ, kiểm tra thắng thua, AI đơn giản.
# =============================================================================
class CaroGame:
    def __init__(self, window):
        self.window = window
        self.window.title("Cờ Caro Pro")
        self.window.configure(bg=COLORS["bg_main"])
        
        # --- Màn hình cài đặt (Setup) ---
        # Cho phép người dùng chọn kích thước bàn cờ và chế độ chơi
        self.frame_setup = tk.Frame(window, bg=COLORS["bg_main"], padx=30, pady=30)
        self.frame_setup.pack()

        # ... (Code tạo các ô nhập liệu Entry, Radiobutton cho setup) ...
        # [Đã lược bớt phần tạo widget UI chi tiết để tập trung vào logic]
        
        tk.Label(self.frame_setup, text="CẤU HÌNH TRẬN ĐẤU", font=FONT_TITLE, bg=COLORS["bg_main"], fg=COLORS["bg_dark"]).pack(pady=(0, 20))
        group = tk.LabelFrame(self.frame_setup, text="Tùy chọn", font=FONT_BOLD, bg=COLORS["bg_main"], fg=COLORS["bg_dark"], padx=20, pady=20)
        group.pack(fill="x", pady=10)
        
        # Nhập kích thước N
        tk.Label(group, text="Kích thước (5-20):", font=FONT_NORMAL, bg=COLORS["bg_main"]).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_n = tk.Entry(group, font=FONT_NORMAL, width=10, justify='center', relief="solid")
        self.entry_n.insert(0, "15")
        self.entry_n.grid(row=0, column=1, pady=5)

        # Chọn chế độ PvP hoặc PvE
        tk.Label(group, text="Chế độ:", font=FONT_NORMAL, bg=COLORS["bg_main"]).grid(row=1, column=0, sticky="w", pady=10)
        self.mode_var = tk.StringVar(value="PvP")
        frame_radio = tk.Frame(group, bg=COLORS["bg_main"])
        frame_radio.grid(row=1, column=1)
        tk.Radiobutton(frame_radio, text="Người vs Người", variable=self.mode_var, value="PvP", font=FONT_NORMAL, bg=COLORS["bg_main"]).pack(anchor="w")
        tk.Radiobutton(frame_radio, text="Người vs Máy", variable=self.mode_var, value="PvE", font=FONT_NORMAL, bg=COLORS["bg_main"]).pack(anchor="w")

        # Nút Bắt đầu
        btn_frame = tk.Frame(self.frame_setup, bg=COLORS["bg_main"])
        btn_frame.pack(pady=20)
        StyledButton(btn_frame, text="Bắt Đầu", bg=COLORS["btn_success"], width=12, command=self.start_game).pack(side="left", padx=5)
        StyledButton(btn_frame, text="Đóng", bg=COLORS["btn_danger"], width=10, command=self.window.destroy).pack(side="left", padx=5)

        # Biến lưu trạng thái game
        self.canvas = None
        self.board = []   # Ma trận lưu dữ liệu bàn cờ
        self.turn = 'X'   # Lượt đi hiện tại
        self.game_over = False

    def start_game(self):
        """Hàm được gọi khi nhấn nút Bắt đầu"""
        # Kiểm tra dữ liệu nhập vào có hợp lệ không
        try:
            val = int(self.entry_n.get())
            if val < 5 or val > 30: raise ValueError
            self.n = val
        except ValueError:
            messagebox.showerror("Lỗi", "Kích thước phải là số nguyên từ 5 đến 30!")
            return

        self.is_pve = (self.mode_var.get() == "PvE")
        self.frame_setup.destroy() # Ẩn màn hình cài đặt
        self.create_board_ui()     # Hiện bàn cờ

    def create_board_ui(self):
        """Vẽ giao diện bàn cờ bằng Canvas"""
        # Tính toán kích thước ô cờ dựa trên số lượng ô
        self.cell_size = 32 if self.n <= 15 else 24
        w = self.n * self.cell_size
        h = self.n * self.cell_size

        # Tạo Canvas vẽ lưới
        frame_canvas = tk.Frame(self.window, bg=COLORS["bg_main"], padx=10, pady=10)
        frame_canvas.pack()
        self.canvas = tk.Canvas(frame_canvas, width=w, height=h, bg=COLORS["board_bg"], highlightthickness=1, highlightbackground="#BDC3C7")
        self.canvas.pack(pady=5)
        
        # Vẽ các đường kẻ ngang dọc
        for i in range(self.n + 1):
             self.canvas.create_line(i*self.cell_size, 0, i*self.cell_size, h, fill="#BDC3C7")
             self.canvas.create_line(0, i*self.cell_size, w, i*self.cell_size, fill="#BDC3C7")

        # Gán sự kiện click chuột trái vào canvas
        self.canvas.bind("<Button-1>", self.on_user_click)
        
        # Nút điều khiển dưới bàn cờ
        ctrl_frame = tk.Frame(self.window, bg=COLORS["bg_main"], pady=15)
        ctrl_frame.pack(fill="x")
        StyledButton(ctrl_frame, text="Chơi Lại", bg=COLORS["btn_primary"], width=12, command=self.reset_game).pack(side="left", padx=20)
        StyledButton(ctrl_frame, text="Thoát", bg=COLORS["btn_danger"], width=12, command=self.window.destroy).pack(side="right", padx=20)

        # Khởi tạo ma trận rỗng
        self.board = [['' for _ in range(self.n)] for _ in range(self.n)]

    def reset_game(self):
        self.window.destroy()
        CaroGame(tk.Toplevel())

    def on_user_click(self, event):
        """Xử lý khi người dùng click chuột vào bàn cờ"""
        if self.game_over: return
        if self.is_pve and self.turn == 'O': return # Nếu là lượt máy thì chặn người dùng click

        # Tính tọa độ dòng (r) cột (c) từ tọa độ chuột pixel (x, y)
        c = event.x // self.cell_size
        r = event.y // self.cell_size

        if 0 <= r < self.n and 0 <= c < self.n and self.board[r][c] == '':
            self.make_move(r, c) # Thực hiện nước đi
            # Nếu chơi với máy và chưa hết game, gọi máy đi sau 400ms
            if not self.game_over and self.is_pve:
                self.window.after(400, self.computer_move)

    def make_move(self, r, c):
        """Vẽ X hoặc O lên bàn cờ và cập nhật logic"""
        cx = c * self.cell_size + self.cell_size // 2
        cy = r * self.cell_size + self.cell_size // 2
        
        if self.turn == 'X':
            # Vẽ chữ X
            color = COLORS["x_color"]
            offset = self.cell_size // 4
            self.canvas.create_line(cx-offset, cy-offset, cx+offset, cy+offset, width=3, fill=color, capstyle="round")
            self.canvas.create_line(cx+offset, cy-offset, cx-offset, cy+offset, width=3, fill=color, capstyle="round")
        else:
            # Vẽ chữ O
            color = COLORS["o_color"]
            radius = self.cell_size // 3
            self.canvas.create_oval(cx-radius, cy-radius, cx+radius, cy+radius, width=3, outline=color)

        self.board[r][c] = self.turn
        self.move_count += 1

        # Kiểm tra thắng
        if self.check_winner(r, c):
            messagebox.showinfo("Kết quả", f"Chúc mừng! {self.turn} đã chiến thắng!")
            self.game_over = True
            return

        # Kiểm tra hòa
        if self.move_count >= self.n * self.n:
            messagebox.showinfo("Kết quả", "Ván cờ Hòa!")
            self.game_over = True
            return

        # Đổi lượt
        self.turn = 'O' if self.turn == 'X' else 'X'

    def computer_move(self):
        """Logic đơn giản cho máy (AI)"""
        if self.game_over: return
        empty = [(r, c) for r in range(self.n) for c in range(self.n) if self.board[r][c] == '']
        if not empty: return
        
        # 1. Kiểm tra xem máy có thể thắng ngay không? -> Đánh
        for r, c in empty:
            self.board[r][c] = 'O'
            if self.check_winner(r, c):
                self.board[r][c] = ''
                self.make_move(r, c)
                return
            self.board[r][c] = ''
            
        # 2. Kiểm tra xem người có sắp thắng không? -> Chặn
        for r, c in empty:
            self.board[r][c] = 'X'
            if self.check_winner(r, c):
                self.board[r][c] = ''
                self.make_move(r, c)
                return
            self.board[r][c] = ''

        # 3. Nếu không thì đánh ngẫu nhiên
        move = random.choice(empty)
        self.make_move(move[0], move[1])

    def check_winner(self, r, c):
        """Thuật toán kiểm tra thắng thua (duyệt 4 hướng: ngang, dọc, chéo chính, chéo phụ)"""
        win_num = 5
        player = self.board[r][c]
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            # Duyệt về 1 phía
            for k in range(1, win_num):
                nr, nc = r + dr*k, c + dc*k
                if 0 <= nr < self.n and 0 <= nc < self.n and self.board[nr][nc] == player: count += 1
                else: break
            # Duyệt về phía ngược lại
            for k in range(1, win_num):
                nr, nc = r - dr*k, c - dc*k
                if 0 <= nr < self.n and 0 <= nc < self.n and self.board[nr][nc] == player: count += 1
                else: break
            if count >= win_num: return True
        return False


# =============================================================================
# PHẦN 5: MODULE TÔ MÀU ĐỒ THỊ
# Thực hiện thuật toán tô màu tham lam (Greedy Coloring).
# =============================================================================
class GraphColoring:
    def __init__(self, window):
        self.window = window
        self.window.title("Mô Phỏng Tô Màu Đồ Thị")
        self.window.geometry("900x600")
        self.window.configure(bg=COLORS["bg_main"])

        # Chia giao diện làm 2 phần: Sidebar (Nhập liệu) và Content (Vẽ hình)
        container = tk.Frame(window, bg=COLORS["bg_main"])
        container.pack(fill="both", expand=True)

        # --- Sidebar bên trái ---
        sidebar = tk.Frame(container, bg="white", width=280, padx=20, pady=20, relief="groove", borderwidth=1)
        sidebar.pack(side="left", fill="y")
        
        tk.Label(sidebar, text="Dữ Liệu Đồ Thị", font=("Segoe UI", 14, "bold"), bg="white", fg=COLORS["bg_dark"]).pack(pady=(0, 20))

        # Ô nhập số đỉnh
        tk.Label(sidebar, text="Số lượng đỉnh (N):", font=FONT_BOLD, bg="white").pack(anchor="w")
        self.entry_nodes = tk.Entry(sidebar, font=FONT_NORMAL, bg="#FAFAFA", relief="solid", bd=1)
        self.entry_nodes.insert(0, "6")
        self.entry_nodes.pack(fill="x", pady=5)

        # Ô nhập danh sách cạnh
        tk.Label(sidebar, text="Danh sách cạnh (u-v):", font=FONT_BOLD, bg="white").pack(anchor="w", pady=(15,0))
        self.txt_edges = tk.Text(sidebar, height=12, font=("Consolas", 10), bg="#FAFAFA", relief="solid", bd=1)
        self.txt_edges.insert("1.0", "0-1\n1-2\n2-3\n3-4\n4-5\n5-0\n0-3\n1-4") # Dữ liệu mẫu
        self.txt_edges.pack(fill="x", pady=5)

        # Nút thực hiện
        StyledButton(sidebar, text="VẼ VÀ TÔ MÀU", bg=COLORS["btn_primary"], command=self.execute_coloring).pack(fill="x", pady=20)
        StyledButton(sidebar, text="Đóng", bg=COLORS["btn_danger"], command=self.window.destroy).pack(fill="x", side="bottom")

        # --- Khu vực vẽ bên phải ---
        content = tk.Frame(container, bg=COLORS["bg_main"], padx=10, pady=10)
        content.pack(side="right", fill="both", expand=True)
        self.canvas = tk.Canvas(content, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

    def execute_coloring(self):
        """Hàm chính: Xử lý input -> Chạy thuật toán -> Vẽ"""
        self.canvas.delete("all") # Xóa hình cũ
        
        # 1. Parse số đỉnh
        try:
            n = int(self.entry_nodes.get())
            if n < 1: raise ValueError
        except:
            messagebox.showerror("Lỗi", "Số đỉnh phải là số nguyên dương!")
            return

        # 2. Xây dựng danh sách kề (Adjacency List) từ dữ liệu nhập
        nodes = list(range(n))
        adj = {i: [] for i in nodes}
        raw = self.txt_edges.get("1.0", tk.END).strip().split('\n')
        for line in raw:
            parts = line.replace(" ", "-").split("-")
            if len(parts) >= 2:
                try:
                    u, v = int(parts[0]), int(parts[1])
                    if u in adj and v in adj:
                        if v not in adj[u]: adj[u].append(v)
                        if u not in adj[v]: adj[v].append(u)
                except: pass

        # 3. Tính toán vị trí các đỉnh (Xếp thành vòng tròn để dễ nhìn)
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        cx, cy = w/2, h/2
        r_layout = min(w, h)/2 - 60
        node_pos = {}
        for i, u in enumerate(nodes):
            angle = 2 * math.pi * i / n - math.pi/2
            x = cx + r_layout * math.cos(angle)
            y = cy + r_layout * math.sin(angle)
            node_pos[u] = (x, y)

        # 4. THUẬT TOÁN TÔ MÀU THAM LAM (Greedy Coloring)
        colors = ["#E74C3C", "#2ECC71", "#3498DB", "#F1C40F", "#9B59B6", "#E67E22", "#1ABC9C", "#34495E"]
        node_color = {}
        
        # Sắp xếp đỉnh theo bậc (số cạnh nối) giảm dần để tối ưu
        sorted_nodes = sorted(nodes, key=lambda x: len(adj[x]), reverse=True)
        
        for u in sorted_nodes:
            # Tìm các màu đã bị dùng bởi hàng xóm
            forbidden = {node_color[v] for v in adj[u] if v in node_color}
            # Chọn màu đầu tiên trong danh sách không bị cấm
            c_idx = 0
            while c_idx < len(colors):
                if colors[c_idx] not in forbidden:
                    node_color[u] = colors[c_idx]
                    break
                c_idx += 1
            if u not in node_color: node_color[u] = "#95A5A6" # Màu mặc định nếu hết màu

        # 5. Vẽ đồ thị lên Canvas
        drawn = set()
        # Vẽ các đường nối (cạnh) trước
        for u in nodes:
            for v in adj[u]:
                if (u, v) not in drawn and (v, u) not in drawn:
                    x1, y1 = node_pos[u]
                    x2, y2 = node_pos[v]
                    self.canvas.create_line(x1, y1, x2, y2, fill="#7F8C8D", width=1.5)
                    drawn.add((u, v))
        
        # Vẽ các hình tròn (đỉnh) sau
        r = 20
        for u in nodes:
            x, y = node_pos[u]
            c = node_color.get(u, "white")
            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=c, outline="white", width=2)
            self.canvas.create_text(x, y, text=str(u), font=("Segoe UI", 10, "bold"), fill="white")


# =============================================================================
# PHẦN 6: CLASS CƠ SỞ CHO MACHINE LEARNING
# Tạo khung sườn chung cho các cửa sổ ML (Gồm Panel điều khiển, Log, Matplotlib)
# =============================================================================
class MLWindow(tk.Toplevel):
    def __init__(self, parent, title, geometry):
        super().__init__(parent)
        self.title(title)
        self.geometry(geometry)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.is_running = False
        
        # Khu vực phía trên: Chứa các ô nhập liệu và nút bấm
        self.frame_controls = tk.Frame(self, bg=COLORS["bg_main"], pady=10, padx=10)
        self.frame_controls.pack(side=tk.TOP, fill=tk.X)
        
        # Khu vực chính: Chia đôi (Log bên trái, Biểu đồ bên phải)
        self.frame_main = tk.Frame(self)
        self.frame_main.pack(fill=tk.BOTH, expand=True)

        # Panel Log (Trái)
        self.frame_left = tk.Frame(self.frame_main, width=350, bg="#f7f9fa")
        self.frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.frame_left.pack_propagate(False)

        # Panel Biểu đồ (Phải)
        self.frame_right = tk.Frame(self.frame_main)
        self.frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Tạo Text box để ghi log
        tk.Label(self.frame_left, text="Nhật ký hoạt động:", font=("Segoe UI", 10, "bold"), bg="#f7f9fa").pack(anchor="w", pady=5)
        self.txt_log = tk.Text(self.frame_left, font=("Consolas", 9), state=tk.DISABLED, bg="white", relief=tk.FLAT)
        self.txt_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Nhúng Matplotlib Figure vào Tkinter Canvas
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_right)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Các hàm tiện ích để thêm ô input và nút bấm nhanh
    def add_input(self, label_text, default_val):
        frame = tk.Frame(self.frame_controls, bg=COLORS["bg_main"])
        frame.pack(side=tk.LEFT, padx=10)
        tk.Label(frame, text=label_text, bg=COLORS["bg_main"], font=("Segoe UI", 9)).pack(anchor="w")
        entry = tk.Entry(frame, width=8, font=("Segoe UI", 10), justify='center')
        entry.insert(0, str(default_val))
        entry.pack()
        return entry

    def add_button(self, text, command, color, side=tk.LEFT):
        btn = tk.Button(self.frame_controls, text=text, command=command, 
                        bg=color, fg="white", font=("Segoe UI", 9, "bold"), 
                        padx=15, pady=2, relief=tk.FLAT)
        btn.pack(side=side, padx=10, pady=5)
        return btn

    def log(self, msg):
        """Hàm ghi thông báo vào ô log"""
        if not self.winfo_exists(): return
        self.txt_log.config(state=tk.NORMAL)
        self.txt_log.insert(tk.END, f"> {msg}\n")
        self.txt_log.see(tk.END)
        self.txt_log.config(state=tk.DISABLED)

    def clear_plot(self, title=""):
        """Xóa biểu đồ cũ để vẽ mới"""
        self.ax.clear()
        self.ax.set_title(title, fontsize=12)
        self.ax.grid(True, linestyle='--', alpha=0.5)

    def on_close(self):
        self.is_running = False
        plt.close(self.fig) # Giải phóng bộ nhớ biểu đồ
        self.destroy()

# =============================================================================
# PHẦN 7: MODULE K-MEANS CLUSTERING (THAY THẾ CHO KNN)
# Kế thừa từ MLWindow, thực hiện thuật toán phân cụm không giám sát.
# =============================================================================
class KMeansWindow(MLWindow):
    def __init__(self, parent):
        super().__init__(parent, "Mô Phỏng K-Means Clustering", "1100x700")

        # Tạo các ô nhập tham số K-Means
        self.entry_n = self.add_input("Số điểm (N):", 300)      # Tổng số điểm dữ liệu
        self.entry_c_true = self.add_input("Số cụm gốc:", 4)    # Số cụm để sinh dữ liệu mẫu
        self.entry_k = self.add_input("K cần tìm:", 4)          # Số K mà thuật toán dùng để tìm

        # Nút điều khiển
        self.add_button("CHẠY K-MEANS", self.start_process, COLORS["btn_ml"])
        self.add_button("Đóng", self.on_close, COLORS["btn_danger"], side=tk.RIGHT)

    def visualize(self, X, centers, labels, k, title):
        """Vẽ dữ liệu và tâm cụm lên biểu đồ"""
        if not self.winfo_exists(): return
        self.clear_plot(title)
        
        # Bảng màu
        cmap = plt.get_cmap('tab10')
        
        # Vẽ các điểm dữ liệu (tô màu theo nhãn cụm hiện tại)
        for i in range(k):
            cluster_data = X[labels == i]
            if len(cluster_data) > 0:
                color = cmap(i % 10)
                self.ax.scatter(cluster_data[:, 0], cluster_data[:, 1], color=color, alpha=0.6, s=30)
        
        # Vẽ các tâm cụm (Centers) hình chữ X to
        for i in range(len(centers)):
            color = cmap(i % 10)
            self.ax.scatter(centers[i, 0], centers[i, 1], color=color, s=200, marker='X', edgecolor='black', linewidth=2, label='Tâm')
        
        self.canvas.draw() # Cập nhật Canvas

    def start_process(self):
        """Bắt đầu quy trình chạy thuật toán"""
        self.is_running = False 
        
        try:
            n = int(self.entry_n.get())
            c_true = int(self.entry_c_true.get())
            self.k = int(self.entry_k.get())

            self.log("\n--- BẮT ĐẦU K-MEANS ---")
            
            # Bước 1: Tạo dữ liệu giả lập (Blobs)
            self.X, _ = make_blobs(n_samples=n, centers=c_true, cluster_std=1.0, random_state=42)
            
            # Bước 2: Khởi tạo tâm ngẫu nhiên (chọn K điểm bất kỳ từ dữ liệu)
            idx = np.random.choice(n, self.k, replace=False)
            self.centers = self.X[idx]
            self.labels = np.zeros(n, dtype=int) # Nhãn tạm thời
            
            self.visualize(self.X, self.centers, self.labels, self.k, "Bước 0: Khởi tạo tâm ngẫu nhiên")
            self.log(f"Đã tạo {n} điểm. Khởi tạo {self.k} tâm.")

            # Kích hoạt vòng lặp thuật toán (bắt đầu từ bước 0)
            self.is_running = True
            self.after(1000, lambda: self.loop_step(0)) # Đợi 1s rồi chạy tiếp

        except ValueError:
            messagebox.showerror("Lỗi", "Dữ liệu nhập không hợp lệ!")

    def loop_step(self, step):
        """Bước E (Expectation): Gán điểm vào tâm gần nhất"""
        if not self.is_running: return

        # Tính khoảng cách từ mọi điểm đến mọi tâm
        distances = np.linalg.norm(self.X[:, np.newaxis] - self.centers, axis=2)
        # Gán nhãn cho điểm dựa trên tâm gần nhất (index của khoảng cách nhỏ nhất)
        self.labels = np.argmin(distances, axis=1)

        self.visualize(self.X, self.centers, self.labels, self.k, f"Bước {step+1}: Gán nhãn (Assignment)")
        self.log(f"Iter {step+1}: Gán điểm vào cụm gần nhất.")
        
        # Chuyển sang bước cập nhật sau 800ms
        self.after(800, lambda: self.update_step(step))

    def update_step(self, step):
        """Bước M (Maximization): Cập nhật vị trí tâm mới"""
        if not self.is_running: return

        old_centers = self.centers.copy()
        new_centers = np.zeros_like(self.centers)

        # Tính trung bình cộng tọa độ các điểm trong từng cụm
        for i in range(self.k):
            points_in_cluster = self.X[self.labels == i]
            if len(points_in_cluster) > 0:
                new_centers[i] = points_in_cluster.mean(axis=0)
            else:
                new_centers[i] = old_centers[i] # Giữ nguyên nếu cụm rỗng

        self.centers = new_centers

        # Kiểm tra hội tụ (Tâm có di chuyển không?)
        shift = np.linalg.norm(self.centers - old_centers)
        
        if shift < 1e-4: # Nếu di chuyển cực nhỏ coi như xong
            self.visualize(self.X, self.centers, self.labels, self.k, f"ĐÃ HỘI TỤ sau {step+1} bước!")
            self.log("--- THUẬT TOÁN ĐÃ HỘI TỤ ---")
            self.is_running = False
            return

        self.visualize(self.X, self.centers, self.labels, self.k, f"Bước {step+1}: Cập nhật tâm (Update)")
        self.log(f"Iter {step+1}: Di chuyển tâm (Shift: {shift:.4f})")

        # Lặp lại bước gán nhãn sau 800ms (Đệ quy)
        self.after(800, lambda: self.loop_step(step + 1))

# ==========================================
# KHỞI CHẠY CHƯƠNG TRÌNH
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()