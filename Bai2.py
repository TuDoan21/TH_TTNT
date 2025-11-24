import os
import math
import time

# Các tổ hợp chiến thắng (theo chỉ số 0-8)
WIN_COMBINATIONS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8), # Hàng ngang
    (0, 3, 6), (1, 4, 7), (2, 5, 8), # Hàng dọc
    (0, 4, 8), (2, 4, 6)             # Chéo
]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board(board):
    """In bàn cờ ra màn hình"""
    clear_screen()
    print(f"\n {board[0]} | {board[1]} | {board[2]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} \n")

def check_winner(board):
    """Kiểm tra người thắng, trả về 'X', 'O' hoặc None"""
    for a, b, c in WIN_COMBINATIONS:
        if board[a] == board[b] == board[c]:
            return board[a]
    return None

def get_available_cells(board):
    """Trả về danh sách các ô còn trống (là số nguyên)"""
    return [cell for cell in board if isinstance(cell, int)]

def is_board_full(board):
    """Kiểm tra xem bàn cờ đã đầy chưa"""
    return len(get_available_cells(board)) == 0

def minimax(board, depth, alpha, beta, is_maximizing):
    winner = check_winner(board)
    if winner == "X":
        return 10 - depth  # X thắng càng sớm càng tốt
    if winner == "O":
        return -10 + depth # O thắng (hoặc X thua) càng muộn càng tốt
    if is_board_full(board):
        return 0 # Hòa

    if is_maximizing:
        max_eval = -math.inf
        for cell in get_available_cells(board):
            original_val = cell
            board[cell - 1] = "X"
            eval_score = minimax(board, depth + 1, alpha, beta, False)
            board[cell - 1] = original_val # Backtrack
            
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for cell in get_available_cells(board):
            original_val = cell
            board[cell - 1] = "O"
            eval_score = minimax(board, depth + 1, alpha, beta, True)
            board[cell - 1] = original_val # Backtrack
            
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval

def find_best_move(board, ai_player):
    """Tìm nước đi tối ưu cho AI"""
    best_val = -math.inf if ai_player == "X" else math.inf
    best_move = -1
    
    # Nếu là lượt đầu tiên và bàn cờ trống, đi luôn vào giữa để tiết kiệm CPU
    if len(get_available_cells(board)) == 9:
        return 5

    for cell in get_available_cells(board):
        original_val = cell
        board[cell - 1] = ai_player
        
        # Nếu AI là X, lượt tiếp theo là O (minimizing -> False)
        # Nếu AI là O, lượt tiếp theo là X (maximizing -> True)
        is_max_next = False if ai_player == "X" else True
        
        move_val = minimax(board, 0, -math.inf, math.inf, is_max_next)
        
        board[cell - 1] = original_val # Backtrack

        if ai_player == "X": # AI muốn Maximize điểm
            if move_val > best_val:
                best_val = move_val
                best_move = cell
        else: # AI muốn Minimize điểm (vì O thắng là -10)
            if move_val < best_val:
                best_val = move_val
                best_move = cell
                
    return best_move

def main():
    clear_screen()
    while True:
        choice = input("Bạn muốn chơi X hay O? (X đi trước): ").strip().upper()
        if choice in ['X', 'O']:
            human = choice
            ai = "O" if human == "X" else "X"
            break
        print("Vui lòng chỉ nhập X hoặc O.")

    # Bàn cờ lưu trữ số 1-9
    board = list(range(1, 10))
    current_turn = "X"
    
    print_board(board)

    while True:
        # --- LƯỢT CỦA AI ---
        if current_turn == ai:
            print(f"AI ({ai}) đang suy nghĩ...")
            move = find_best_move(board, ai)
            board[move - 1] = ai
            current_turn = human
            print_board(board)

        # --- LƯỢT CỦA NGƯỜI CHƠI ---
        elif current_turn == human:
            try:
                move = int(input(f"Lượt của bạn ({human}). Nhập số (1-9): "))
                if move in get_available_cells(board):
                    board[move - 1] = human
                    current_turn = ai
                    print_board(board)
                else:
                    print("Nước đi không hợp lệ hoặc ô đã có người đánh. Thử lại.")
            except ValueError:
                print("Vui lòng nhập một con số nguyên.")
                continue

        # --- KIỂM TRA KẾT THÚC GAME ---
        winner = check_winner(board)
        if winner:
            if winner == ai:
                print(f"AI ({winner}) ĐÃ CHIẾN THẮNG!")
            else:
                print(f"BẠN ({winner}) ĐÃ THẮNG! (Điều này không thể xảy ra nếu code đúng ^^)")
            break
        
        if is_board_full(board):
            print("TRÒ CHƠI KẾT THÚC: HÒA!")
            break

if __name__ == "__main__":
    main()