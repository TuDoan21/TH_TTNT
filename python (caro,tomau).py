import tkinter as tk
from tkinter import messagebox
import math
import random

# ==========================================
# CẤU HÌNH MÀU SẮC & STYLE
# ==========================================
COLORS = {
    "bg_main": "#F0F2F5",       # Màu nền chính (Xám nhạt)
    "bg_dark": "#2C3E50",       # Màu nền header (Xanh đậm)
    "text_header": "#ECF0F1",   # Màu chữ header
    "btn_primary": "#3498DB",   # Nút chính (Xanh dương)
    "btn_hover": "#2980B9",     # Nút khi di chuột
    "btn_success": "#27AE60",   # Nút hành động (Xanh lá)
    "btn_danger": "#E74C3C",    # Nút thoát (Đỏ)
    "board_bg": "#FFFFFF",      # Nền bàn cờ
    "line_color": "#BDC3C7",    # Màu đường kẻ
    "x_color": "#E74C3C",       # Màu quân X
    "o_color": "#3498DB"        # Màu quân O
}

FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_NORMAL = ("Segoe UI", 11)
FONT_BOLD = ("Segoe UI", 11, "bold")

class StyledButton(tk.Button):
    """Tạo nút bấm có hiệu ứng hover"""
    def __init__(self, master, **kwargs):
        self.bg_color = kwargs.get("bg", COLORS["btn_primary"])
        self.hover_color = kwargs.pop("hover_bg", COLORS["btn_hover"])
        
        # Thiết lập mặc định
        kwargs.setdefault("fg", "white")
        kwargs.setdefault("font", FONT_BOLD)
        kwargs.setdefault("relief", "flat")
        kwargs.setdefault("cursor", "hand2")
        kwargs.setdefault("pady", 8)
        
        super().__init__(master, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['bg'] = self.hover_color

    def on_leave(self, e):
        self['bg'] = self.bg_color

# ==========================================
# GIAO DIỆN CHÍNH (MENU)
# ==========================================
class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Mini Games Collection")
        self.root.geometry("450x400")
        self.root.configure(bg=COLORS["bg_main"])
        self.center_window(450, 400)

        # Header
        header_frame = tk.Frame(root, bg=COLORS["bg_dark"], pady=20)
        header_frame.pack(fill="x")
        
        lbl_title = tk.Label(header_frame, text="MENU CHƯƠNG TRÌNH", font=("Segoe UI", 20, "bold"), 
                             bg=COLORS["bg_dark"], fg=COLORS["text_header"])
        lbl_title.pack()

        # Content
        content_frame = tk.Frame(root, bg=COLORS["bg_main"], pady=30)
        content_frame.pack(fill="both", expand=True)

        # Nút Cờ Caro
        StyledButton(content_frame, text="🎮 Game Cờ Caro (PvP / PvE)", width=30, 
                     bg=COLORS["btn_primary"], hover_bg="#2980B9",
                     command=self.open_caro).pack(pady=10)

        # Nút Tô màu
        StyledButton(content_frame, text="🎨 Thuật Toán Tô Màu Đồ Thị", width=30,
                     bg="#9B59B6", hover_bg="#8E44AD",
                     command=self.open_graph).pack(pady=10)

        # Nút Thoát
        StyledButton(content_frame, text="❌ Thoát Chương Trình", width=30,
                     bg=COLORS["btn_danger"], hover_bg="#C0392B",
                     command=self.exit_app).pack(pady=20)

        # Footer
        tk.Label(root, text="Designed with Python Tkinter", font=("Segoe UI", 9), 
                 bg=COLORS["bg_main"], fg="#7F8C8D").pack(side="bottom", pady=10)

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
    
    def exit_app(self):
        if messagebox.askokcancel("Xác nhận", "Bạn có chắc muốn thoát không?"):
            self.root.destroy()


# ==========================================
# MODULE 1: CỜ CARO (Giao diện đẹp)
# ==========================================
class CaroGame:
    def __init__(self, window):
        self.window = window
        self.window.title("Cờ Caro Pro")
        self.window.configure(bg=COLORS["bg_main"])
        
        # --- Màn hình Setup ---
        self.frame_setup = tk.Frame(window, bg=COLORS["bg_main"], padx=30, pady=30)
        self.frame_setup.pack()

        # Tiêu đề
        tk.Label(self.frame_setup, text="CẤU HÌNH TRẬN ĐẤU", font=FONT_TITLE, 
                 bg=COLORS["bg_main"], fg=COLORS["bg_dark"]).pack(pady=(0, 20))

        # Nhóm nhập liệu
        group = tk.LabelFrame(self.frame_setup, text="Tùy chọn", font=FONT_BOLD, 
                              bg=COLORS["bg_main"], fg=COLORS["bg_dark"], padx=20, pady=20)
        group.pack(fill="x", pady=10)

        # Input Size
        tk.Label(group, text="Kích thước (3-30):", font=FONT_NORMAL, bg=COLORS["bg_main"]).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_n = tk.Entry(group, font=FONT_NORMAL, width=10, justify='center', relief="solid")
        self.entry_n.insert(0, "15")
        self.entry_n.grid(row=0, column=1, pady=5)

        # Input Mode
        tk.Label(group, text="Chế độ:", font=FONT_NORMAL, bg=COLORS["bg_main"]).grid(row=1, column=0, sticky="w", pady=10)
        self.mode_var = tk.StringVar(value="PvP")
        
        frame_radio = tk.Frame(group, bg=COLORS["bg_main"])
        frame_radio.grid(row=1, column=1)
        tk.Radiobutton(frame_radio, text="Người vs Người", variable=self.mode_var, value="PvP", 
                       font=FONT_NORMAL, bg=COLORS["bg_main"]).pack(anchor="w")
        tk.Radiobutton(frame_radio, text="Người vs Máy", variable=self.mode_var, value="PvE", 
                       font=FONT_NORMAL, bg=COLORS["bg_main"]).pack(anchor="w")

        # Buttons
        btn_frame = tk.Frame(self.frame_setup, bg=COLORS["bg_main"])
        btn_frame.pack(pady=20)

        StyledButton(btn_frame, text="Bắt Đầu", bg=COLORS["btn_success"], width=12, command=self.start_game).pack(side="left", padx=5)
        StyledButton(btn_frame, text="Hủy Bỏ", bg=COLORS["btn_danger"], width=10, command=self.window.destroy).pack(side="left", padx=5)

        # Biến game
        self.canvas = None
        self.board = []
        self.turn = 'X'
        self.n = 10
        self.cell_size = 30
        self.game_over = False
        self.move_count = 0
        self.is_pve = False

    def start_game(self):
        try:
            val = int(self.entry_n.get())
            if val < 3 or val > 30: raise ValueError
            self.n = val
        except ValueError:
            messagebox.showerror("Lỗi", "Kích thước phải là số nguyên từ 3 đến 30!")
            return

        self.is_pve = (self.mode_var.get() == "PvE")
        self.frame_setup.destroy()
        self.create_board_ui()

    def create_board_ui(self):
        # Thanh trạng thái phía trên
        status_frame = tk.Frame(self.window, bg=COLORS["bg_dark"], pady=10)
        status_frame.pack(fill="x")
        
        mode_text = "NGƯỜI ĐẤU VỚI MÁY" if self.is_pve else "NGƯỜI ĐẤU VỚI NGƯỜI"
        self.lbl_status = tk.Label(status_frame, text=f"Lượt: X - {mode_text}", 
                                   font=("Segoe UI", 12, "bold"), bg=COLORS["bg_dark"], fg="white")
        self.lbl_status.pack()

        # Canvas
        self.cell_size = 32 if self.n <= 15 else 24
        w = self.n * self.cell_size
        h = self.n * self.cell_size

        frame_canvas = tk.Frame(self.window, bg=COLORS["bg_main"], padx=10, pady=10)
        frame_canvas.pack()

        self.canvas = tk.Canvas(frame_canvas, width=w, height=h, bg=COLORS["board_bg"], 
                                highlightthickness=1, highlightbackground="#BDC3C7")
        self.canvas.pack(pady=5)
        
        # Vẽ lưới mờ
        for i in range(self.n):
            self.canvas.create_line(i*self.cell_size, 0, i*self.cell_size, h, fill="#ECF0F1")
            self.canvas.create_line(0, i*self.cell_size, w, i*self.cell_size, fill="#ECF0F1")
            
        # Vẽ lưới đậm (trục chính) - tùy chọn, ở đây vẽ lưới thường màu xám
        for i in range(self.n + 1):
             self.canvas.create_line(i*self.cell_size, 0, i*self.cell_size, h, fill="#BDC3C7")
             self.canvas.create_line(0, i*self.cell_size, w, i*self.cell_size, fill="#BDC3C7")

        self.canvas.bind("<Button-1>", self.on_user_click)
        
        # Thanh điều khiển phía dưới
        ctrl_frame = tk.Frame(self.window, bg=COLORS["bg_main"], pady=15)
        ctrl_frame.pack(fill="x")
        
        StyledButton(ctrl_frame, text="Chơi Lại", bg=COLORS["btn_primary"], width=12, command=self.reset_game).pack(side="left", padx=20, expand=True)
        StyledButton(ctrl_frame, text="Thoát", bg=COLORS["btn_danger"], width=12, command=self.window.destroy).pack(side="right", padx=20, expand=True)

        self.board = [['' for _ in range(self.n)] for _ in range(self.n)]
        self.turn = 'X'
        self.game_over = False
        self.move_count = 0

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
            color = COLORS["x_color"]
            # Vẽ chữ X đậm
            offset = self.cell_size // 4
            self.canvas.create_line(cx-offset, cy-offset, cx+offset, cy+offset, width=3, fill=color, capstyle="round")
            self.canvas.create_line(cx+offset, cy-offset, cx-offset, cy+offset, width=3, fill=color, capstyle="round")
        else:
            color = COLORS["o_color"]
            # Vẽ hình tròn O đậm
            radius = self.cell_size // 3
            self.canvas.create_oval(cx-radius, cy-radius, cx+radius, cy+radius, width=3, outline=color)

        self.board[r][c] = self.turn
        self.move_count += 1

        if self.check_winner(r, c):
            self.lbl_status.config(text=f"KẾT QUẢ: {self.turn} THẮNG!", fg="#E67E22")
            messagebox.showinfo("Kết quả", f"Chúc mừng! {self.turn} đã chiến thắng!")
            self.game_over = True
            return

        if self.move_count >= self.n * self.n:
            self.lbl_status.config(text="KẾT QUẢ: HÒA!", fg="#7F8C8D")
            messagebox.showinfo("Kết quả", "Ván cờ Hòa!")
            self.game_over = True
            return

        self.turn = 'O' if self.turn == 'X' else 'X'
        self.lbl_status.config(text=f"Lượt đi: {self.turn}")

    def computer_move(self):
        if self.game_over: return
        best_move = self.find_best_move()
        if best_move:
            self.make_move(best_move[0], best_move[1])

    def find_best_move(self):
        # Chiến thuật đơn giản: Thắng ngay -> Chặn ngay -> Random gần
        empty = [(r, c) for r in range(self.n) for c in range(self.n) if self.board[r][c] == '']
        if not empty: return None

        # 1. Thắng ngay
        for r, c in empty:
            self.board[r][c] = 'O'
            if self.check_winner(r, c):
                self.board[r][c] = ''
                return (r, c)
            self.board[r][c] = ''
        
        # 2. Chặn X
        for r, c in empty:
            self.board[r][c] = 'X'
            if self.check_winner(r, c):
                self.board[r][c] = ''
                return (r, c)
            self.board[r][c] = ''

        # 3. Đánh gần các ô đã có
        candidates = []
        for r, c in empty:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < self.n and 0 <= nc < self.n and self.board[nr][nc] != '':
                        candidates.append((r, c))
                        break
                if candidates and candidates[-1] == (r, c): break
        
        return random.choice(candidates) if candidates else random.choice(empty)

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


# ==========================================
# MODULE 2: TÔ MÀU ĐỒ THỊ (Giao diện đẹp)
# ==========================================
class GraphColoring:
    def __init__(self, window):
        self.window = window
        self.window.title("Mô Phỏng Tô Màu Đồ Thị")
        self.window.geometry("950x650")
        self.window.configure(bg=COLORS["bg_main"])

        # Layout chính: Sidebar bên trái, Canvas bên phải
        container = tk.Frame(window, bg=COLORS["bg_main"])
        container.pack(fill="both", expand=True)

        # --- Sidebar ---
        sidebar = tk.Frame(container, bg="white", width=300, padx=20, pady=20, relief="groove", borderwidth=1)
        sidebar.pack(side="left", fill="y")
        
        tk.Label(sidebar, text="Dữ Liệu Đồ Thị", font=("Segoe UI", 14, "bold"), bg="white", fg=COLORS["bg_dark"]).pack(pady=(0, 20))

        # Input Số đỉnh
        tk.Label(sidebar, text="1. Số lượng đỉnh (N):", font=FONT_BOLD, bg="white").pack(anchor="w")
        self.entry_nodes = tk.Entry(sidebar, font=FONT_NORMAL, bg="#FAFAFA", relief="solid", bd=1)
        self.entry_nodes.insert(0, "6")
        self.entry_nodes.pack(fill="x", pady=5, ipady=3)

        # Input Cạnh
        tk.Label(sidebar, text="2. Danh sách cạnh (u-v):", font=FONT_BOLD, bg="white").pack(anchor="w", pady=(15,0))
        tk.Label(sidebar, text="(Mỗi dòng một cạnh, vd: 0-1)", font=("Segoe UI", 9, "italic"), fg="gray", bg="white").pack(anchor="w")
        
        self.txt_edges = tk.Text(sidebar, height=12, font=("Consolas", 10), bg="#FAFAFA", relief="solid", bd=1)
        self.txt_edges.insert("1.0", "0-1\n1-2\n2-3\n3-4\n4-5\n5-0\n0-3\n1-4")
        self.txt_edges.pack(fill="x", pady=5)

        # Buttons Sidebar
        StyledButton(sidebar, text="🚀 VẼ VÀ TÔ MÀU", bg=COLORS["btn_primary"], command=self.execute_coloring).pack(fill="x", pady=20)
        StyledButton(sidebar, text="Thoát", bg=COLORS["btn_danger"], command=self.window.destroy).pack(fill="x", side="bottom")

        # --- Canvas Area ---
        content = tk.Frame(container, bg=COLORS["bg_main"], padx=10, pady=10)
        content.pack(side="right", fill="both", expand=True)

        self.canvas = tk.Canvas(content, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Watermark
        self.canvas.create_text(300, 300, text="Khu vực vẽ đồ thị", fill="#EEEEEE", font=("Arial", 30, "bold"))

    def execute_coloring(self):
        self.canvas.delete("all")
        # 1. Parse Số đỉnh
        try:
            n = int(self.entry_nodes.get())
            if n < 1: raise ValueError
        except:
            messagebox.showerror("Lỗi", "Số đỉnh phải là số nguyên dương!")
            return

        nodes = list(range(n))
        adj = {i: [] for i in nodes}

        # 2. Parse Cạnh
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

        # 3. Tính toán vị trí (Vòng tròn)
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

        # 4. Tô màu Greedy
        # Bảng màu Flat Design
        colors = ["#E74C3C", "#2ECC71", "#3498DB", "#F1C40F", "#9B59B6", "#E67E22", "#1ABC9C", "#34495E"]
        node_color = {}
        sorted_nodes = sorted(nodes, key=lambda x: len(adj[x]), reverse=True)
        
        for u in sorted_nodes:
            forbidden = {node_color[v] for v in adj[u] if v in node_color}
            c_idx = 0
            while c_idx < len(colors):
                if colors[c_idx] not in forbidden:
                    node_color[u] = colors[c_idx]
                    break
                c_idx += 1
            if u not in node_color: node_color[u] = "#95A5A6" # Xám nếu hết màu

        # 5. Vẽ
        # Vẽ cạnh
        drawn = set()
        for u in nodes:
            for v in adj[u]:
                if (u, v) not in drawn and (v, u) not in drawn:
                    x1, y1 = node_pos[u]
                    x2, y2 = node_pos[v]
                    self.canvas.create_line(x1, y1, x2, y2, fill="#7F8C8D", width=1.5)
                    drawn.add((u, v))
        
        # Vẽ đỉnh
        r = 22
        for u in nodes:
            x, y = node_pos[u]
            c = node_color.get(u, "white")
            # Bóng đổ nhẹ
            self.canvas.create_oval(x-r+2, y-r+2, x+r+2, y+r+2, fill="#DDDDDD", outline="")
            # Hình chính
            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=c, outline="white", width=2)
            self.canvas.create_text(x, y, text=str(u), font=("Segoe UI", 11, "bold"), fill="white")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()