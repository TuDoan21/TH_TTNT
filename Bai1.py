import copy
import math
import numpy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Trả về trạng thái bắt đầu của bàn cờ.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Trả về người chơi có lượt đi tiếp theo.
    X đi trước, O đi sau.
    """
    x_count = 0
    o_count = 0
    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1
    
    # Nếu X đã đi nhiều hơn O, thì đến lượt O. Ngược lại là lượt X.
    if x_count > o_count:
        return O
    return X

def actions(board):
    """
    Trả về tập hợp tất cả các hành động (i, j) có thể thực hiện trên bàn cờ.
    """
    res = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                res.add((i, j))
    return res

def result(board, action):
    """
    Trả về bàn cờ kết quả sau khi thực hiện nước đi (i, j).
    """
    if action not in actions(board):
        raise Exception("Hành động không hợp lệ")
        
    curr_player = player(board)
    result_board = copy.deepcopy(board)
    (i, j) = action
    result_board[i][j] = curr_player
    return result_board

def winner(board):
    """
    Trả về người thắng cuộc nếu có.
    """
    # Kiểm tra các hàng
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]
            
    # Kiểm tra các cột
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]
            
    # Kiểm tra các đường chéo
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
        
    return None

def terminal(board):
    """
    Trả về True nếu trò chơi kết thúc, ngược lại là False.
    """
    if winner(board) is not None:
        return True
        
    # Kiểm tra xem còn ô trống nào không
    for row in board:
        if EMPTY in row:
            return False
    return True

def utility(board):
    """
    Trả về 1 nếu X thắng, -1 nếu O thắng, 0 nếu hòa.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    return 0

def maxValue(state):
    if terminal(state):
        return utility(state)
    v = -math.inf
    for action in actions(state):
        v = max(v, minValue(result(state, action)))
    return v

def minValue(state):
    if terminal(state):
        return utility(state)
    v = math.inf
    for action in actions(state):
        v = min(v, maxValue(result(state, action)))
    return v

def minimax(board):
    """
    Trả về hành động tối ưu cho người chơi hiện tại.
    """
    if terminal(board):
        return None
        
    current_player = player(board)
    best_move = None

    if current_player == X:
        v = -math.inf
        for action in actions(board):
            val = minValue(result(board, action))
            if val > v:
                v = val
                best_move = action
    else:
        v = math.inf
        for action in actions(board):
            val = maxValue(result(board, action))
            if val < v:
                v = val
                best_move = action
                
    return best_move

if __name__ == "__main__":
    board = initial_state()
    
    print("\nChọn người chơi (X đi trước, O đi sau):")
    user_input = input().upper()
    
    if user_input == "O":
        user = O
        ai = X
    else:
        user = X
        ai = O
        
    print(f"\nBạn là: {user}")
    print(f"AI là: {ai}\n")
    print(numpy.array(board))
    print("-----------------")

    while True:
        game_over = terminal(board)
        if game_over:
            win = winner(board)
            if win is None:
                print("Kết thúc: Hòa.")
            else:
                print(f"Kết thúc: {win} thắng.")
            break
        
        # Xác định lượt đi dựa trên trạng thái bàn cờ
        current_turn = player(board)

        if current_turn == ai:
            print(f"AI ({ai}) đang suy nghĩ...")
            move = minimax(board)
            board = result(board, move)
            print(numpy.array(board))
            print("-----------------")
            
        else:
            # Lượt người chơi
            print(f"Lượt của bạn ({user}). Các ô trống: {actions(board)}")
            while True:
                try:
                    print("Nhập tọa độ (hàng,cột):")
                    i = int(input("Hàng: "))
                    j = int(input("Cột: "))
                    
                    if (i, j) in actions(board):
                        board = result(board, (i, j))
                        print(numpy.array(board))
                        print("-----------------")
                        break
                    else:
                        print("Nước đi không hợp lệ. Ô đã có người hoặc ngoài phạm vi.")
                except ValueError:
                    print("Vui lòng nhập số nguyên hợp lệ.")