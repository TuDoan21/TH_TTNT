import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.cm as cm
from sklearn.datasets import make_blobs
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from scipy.spatial.distance import cdist

# =============================================================================
# CLASS CƠ SỞ (BASE WINDOW) - Giúp tái sử dụng code giao diện
# =============================================================================
class MLWindow(tk.Toplevel):
    def __init__(self, parent, title, geometry):
        super().__init__(parent)
        self.title(title)
        self.geometry(geometry)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.parent = parent
        self.is_running = False
        
        # --- 1. Khu vực điều khiển (Input + Buttons) ---
        self.frame_controls = tk.Frame(self, bg="#ecf0f1", pady=10, padx=10)
        self.frame_controls.pack(side=tk.TOP, fill=tk.X)
        
        # --- 2. Khu vực chính (Split: Log bên trái, Graph bên phải) ---
        self.frame_main = tk.Frame(self)
        self.frame_main.pack(fill=tk.BOTH, expand=True)

        self.frame_left = tk.Frame(self.frame_main, width=350, bg="#f7f9fa")
        self.frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.frame_left.pack_propagate(False) # Giữ cố định chiều rộng

        self.frame_right = tk.Frame(self.frame_main)
        self.frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- Setup Log ---
        tk.Label(self.frame_left, text="Nhật ký hoạt động:", font=("Segoe UI", 10, "bold"), bg="#f7f9fa").pack(anchor="w", pady=5)
        self.txt_log = tk.Text(self.frame_left, font=("Consolas", 9), state=tk.DISABLED, bg="white", relief=tk.FLAT)
        scrollbar = tk.Scrollbar(self.frame_left, command=self.txt_log.yview)
        self.txt_log.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # --- Setup Matplotlib ---
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_right)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def add_input(self, label_text, default_val, var_type="int"):
        """Hàm helper để tạo ô nhập liệu nhanh"""
        frame = tk.Frame(self.frame_controls, bg="#ecf0f1")
        frame.pack(side=tk.LEFT, padx=10)
        tk.Label(frame, text=label_text, bg="#ecf0f1", font=("Segoe UI", 9)).pack(anchor="w")
        entry = tk.Entry(frame, width=8, font=("Segoe UI", 10))
        entry.insert(0, str(default_val))
        entry.pack()
        return entry

    def add_button(self, text, command, color, side=tk.LEFT):
        """Hàm helper tạo nút bấm"""
        btn = tk.Button(self.frame_controls, text=text, command=command, 
                        bg=color, fg="white", font=("Segoe UI", 9, "bold"), 
                        padx=15, pady=2, relief=tk.GROOVE, borderwidth=1)
        btn.pack(side=side, padx=10, pady=5)
        return btn

    def log(self, msg):
        """Ghi log an toàn"""
        if not self.winfo_exists(): return
        self.txt_log.config(state=tk.NORMAL)
        self.txt_log.insert(tk.END, f"> {msg}\n")
        self.txt_log.see(tk.END)
        self.txt_log.config(state=tk.DISABLED)

    def clear_plot(self, title=""):
        self.ax.clear()
        self.ax.set_title(title, fontsize=12)
        self.ax.set_xlabel('X feature')
        self.ax.set_ylabel('Y feature')
        self.ax.grid(True, linestyle='--', alpha=0.5)

    def on_close(self):
        """Xử lý khi đóng cửa sổ"""
        self.is_running = False
        plt.close(self.fig) # Giải phóng bộ nhớ Matplotlib
        self.destroy()

# =============================================================================
# CLASS KNN WINDOW
# =============================================================================
class KNNWindow(MLWindow):
    def __init__(self, parent):
        super().__init__(parent, "KNN Classification Simulation", "1100x700")
        
        # Inputs
        self.entry_n = self.add_input("Số điểm (N):", 200)
        self.entry_c = self.add_input("Số lớp:", 3)
        self.entry_std = self.add_input("Độ nhiễu:", 1.5)
        self.entry_k = self.add_input("K Neighbors:", 5)
        
        # Buttons
        self.add_button("CHẠY MÔ HÌNH", self.run_process, "#2980b9")
        self.add_button("Đóng", self.on_close, "#c0392b", side=tk.RIGHT)

    def run_process(self):
        try:
            # Lấy dữ liệu
            n_samples = int(self.entry_n.get())
            n_classes = int(self.entry_c.get())
            std = float(self.entry_std.get())
            k = int(self.entry_k.get())

            if n_samples < 10 or k < 1:
                messagebox.showerror("Lỗi", "Tham số không hợp lệ!")
                return

            self.log("--- BẮT ĐẦU KNN ---")
            
            # 1. Tạo dữ liệu
            self.X, self.y = make_blobs(n_samples=n_samples, n_features=2, centers=n_classes, cluster_std=std)
            
            self.clear_plot("Bước 1: Dữ liệu gốc")
            scatter = self.ax.scatter(self.X[:, 0], self.X[:, 1], c=self.y, s=50, cmap='viridis', edgecolor='k', alpha=0.8)
            self.canvas.draw()
            self.log(f"Đã tạo {n_samples} điểm dữ liệu, {n_classes} lớp.")

            # Sử dụng self.after để không block UI, chuyển sang bước tiếp theo sau 1 giây
            self.after(1000, lambda: self.step_train_test(k))

        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số!")

    def step_train_test(self, k):
        # 2. Train/Test Split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        self.log(f"Chia tập dữ liệu: Train ({len(self.X_train)}) - Test ({len(self.X_test)})")
        
        # 3. Model
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(self.X_train, self.y_train)
        y_pred = knn.predict(self.X_test)
        score = knn.score(self.X_test, self.y_test)

        self.clear_plot(f"Kết quả KNN (K={k}) - Độ chính xác: {score:.2f}")
        # Vẽ tập train mờ
        self.ax.scatter(self.X_train[:, 0], self.X_train[:, 1], c=self.y_train, alpha=0.2, cmap='viridis', label='Train')
        # Vẽ tập test đậm và viền đỏ
        self.ax.scatter(self.X_test[:, 0], self.X_test[:, 1], c=y_pred, marker='s', s=60, cmap='viridis', edgecolor='r', linewidth=1.5, label='Test Predicted')
        self.ax.legend()
        self.canvas.draw()
        
        self.log(f"Hoàn tất! Accuracy: {score:.2f}")

# =============================================================================
# CLASS K-MEANS WINDOW
# =============================================================================
class KMeansWindow(MLWindow):
    def __init__(self, parent):
        super().__init__(parent, "K-Means Clustering Simulation", "1100x700")

        # Inputs
        self.entry_n = self.add_input("Số điểm (N):", 300)
        self.entry_c_true = self.add_input("Số cụm gốc:", 4)
        self.entry_k = self.add_input("K tìm kiếm:", 4)

        # Buttons
        self.add_button("CHẠY K-MEANS", self.start_process, "#27ae60")
        self.add_button("Đóng", self.on_close, "#c0392b", side=tk.RIGHT)

    def init_centers(self, X, k):
        return X[np.random.choice(X.shape[0], k, replace=False)]

    def assign_labels(self, X, centers):
        D = cdist(X, centers)
        return np.argmin(D, axis=1)

    def update_centers(self, X, labels, k):
        centers = np.zeros((k, X.shape[1]))
        for i in range(k):
            Xk = X[labels == i, :]
            if len(Xk) > 0:
                centers[i, :] = np.mean(Xk, axis=0)
        return centers

    def has_converged(self, old_centers, new_centers):
        return np.allclose(old_centers, new_centers, atol=1e-4)

    def visualize(self, X, centers, labels, k, title):
        if not self.winfo_exists(): return
        self.clear_plot(title)
        
        # Lấy bảng màu an toàn
        cmap = plt.get_cmap('tab10')
        
        for i in range(k):
            cluster_data = X[labels == i]
            color = cmap(i % 10)
            # Vẽ dữ liệu
            self.ax.scatter(cluster_data[:, 0], cluster_data[:, 1], color=color, alpha=0.6, s=30)
            # Vẽ tâm
            self.ax.scatter(centers[i, 0], centers[i, 1], color=color, s=200, marker='X', edgecolor='black', linewidth=2)
        
        self.canvas.draw()

    def start_process(self):
        # Reset trạng thái
        self.is_running = False 
        
        try:
            n = int(self.entry_n.get())
            c_true = int(self.entry_c_true.get())
            self.k = int(self.entry_k.get())

            self.log("\n--- BẮT ĐẦU K-MEANS ---")
            
            # Tạo dữ liệu
            self.X, _ = make_blobs(n_samples=n, centers=c_true, cluster_std=1.0)
            
            # Khởi tạo tâm
            self.centers = self.init_centers(self.X, self.k)
            self.labels = np.zeros(self.X.shape[0]) # Dummy labels để vẽ lần đầu
            
            self.visualize(self.X, self.centers, np.zeros(n), self.k, "Bước 0: Khởi tạo tâm ngẫu nhiên")
            self.log("Đã khởi tạo dữ liệu và tâm cụm.")

            # Bắt đầu vòng lặp
            self.is_running = True
            self.after(1000, lambda: self.loop_step(0)) # Gọi bước 1 sau 1 giây

        except ValueError:
            messagebox.showerror("Lỗi", "Dữ liệu nhập không hợp lệ!")

    def loop_step(self, step):
        if not self.is_running: return

        # 1. Gán nhãn (E-step)
        self.labels = self.assign_labels(self.X, self.centers)
        self.visualize(self.X, self.centers, self.labels, self.k, f"Bước {step+1}: Gán nhãn dữ liệu")
        self.log(f"Bước {step+1}: Gán điểm vào tâm gần nhất.")
        
        # Chuyển sang bước update sau 800ms
        self.after(800, lambda: self.update_step(step))

    def update_step(self, step):
        if not self.is_running: return

        # 2. Cập nhật tâm (M-step)
        new_centers = self.update_centers(self.X, self.labels, self.k)
        
        # Kiểm tra hội tụ
        if self.has_converged(self.centers, new_centers):
            self.centers = new_centers
            self.visualize(self.X, self.centers, self.labels, self.k, f"HỘI TỤ sau {step+1} bước!")
            self.log("--- THUẬT TOÁN ĐÃ HỘI TỤ ---")
            self.is_running = False
            return

        self.centers = new_centers
        self.visualize(self.X, self.centers, self.labels, self.k, f"Bước {step+1}: Cập nhật vị trí tâm")
        self.log(f"Bước {step+1}: Di chuyển tâm cụm.")

        # Lặp lại bước gán nhãn sau 800ms
        self.after(800, lambda: self.loop_step(step + 1))


# =============================================================================
# MAIN APPLICATION
# =============================================================================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Machine Learning Educational Tool")
        self.geometry("450x400")
        self.configure(bg="#2c3e50")

        # Title
        tk.Label(self, text="MÔ PHỎNG THUẬT TOÁN", font=("Segoe UI", 20, "bold"), bg="#2c3e50", fg="#ecf0f1").pack(pady=40)

        # Buttons Frame
        frame_btn = tk.Frame(self, bg="#2c3e50")
        frame_btn.pack(expand=True)

        self.create_main_btn(frame_btn, "KNN Classification", "#3498db", lambda: KNNWindow(self))
        self.create_main_btn(frame_btn, "K-Means Clustering", "#27ae60", lambda: KMeansWindow(self))
        
        # Footer / Exit
        tk.Button(self, text="THOÁT CHƯƠNG TRÌNH", command=self.quit, 
                  bg="#c0392b", fg="white", font=("Segoe UI", 10, "bold"),
                  relief=tk.FLAT, pady=5, width=20).pack(side=tk.BOTTOM, pady=30)

    def create_main_btn(self, parent, text, color, command):
        btn = tk.Button(parent, text=text, font=("Segoe UI", 14), 
                        bg=color, fg="white", width=25, height=2, 
                        relief=tk.RAISED, borderwidth=0, cursor="hand2",
                        command=command)
        btn.pack(pady=10)

if __name__ == "__main__":
    try:
        app = App()
        app.mainloop()
    except KeyboardInterrupt:
        print("Đã đóng chương trình.")