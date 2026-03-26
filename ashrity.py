from pywebio.input import input, NUMBER
from pywebio.output import put_text, put_table, put_buttons, clear, put_markdown
from pywebio import start_server
import random, time

# ---------------- GLOBALS ----------------
board = [" " for _ in range(9)]
player = "X"
bot = "O"
game_over = False

# ---------------- RESET ----------------
def restart_game():
    clear()
    put_markdown("# 💥 You Lost!")
    put_buttons(["🔁 Restart Game"], onclick=lambda _: main())

# ---------------- TIC TAC TOE ----------------
def reset_board():
    global board, game_over
    board = [" " for _ in range(9)]
    game_over = False
    draw_board()

def check_winner():
    win_positions = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    for a,b,c in win_positions:
        if board[a] == board[b] == board[c] and board[a] != " ":
            return board[a]
    return None

def bot_move():
    empty = [i for i in range(9) if board[i] == " "]
    if empty:
        board[random.choice(empty)] = bot

def button_cell(i):
    return put_buttons(
        [board[i] if board[i] != " " else str(i+1)],
        onclick=lambda _: player_move(i)
    )

def draw_board():
    clear()
    put_markdown("## 🎮 Tic Tac Toe (You vs Bot 🤖)")
    
    put_table([
        [button_cell(0), button_cell(1), button_cell(2)],
        [button_cell(3), button_cell(4), button_cell(5)],
        [button_cell(6), button_cell(7), button_cell(8)]
    ])

def player_move(i):
    global game_over

    if game_over or board[i] != " ":
        return

    board[i] = player

    if check_winner() == player:
        game_over = True
        put_markdown("## 🎉 You Win!")
        put_buttons(["➡️ Free Play"], onclick=lambda _: free_play_menu())
        return

    if " " not in board:
        game_over = True
        put_markdown("## 🤝 Draw!")
        put_buttons(["➡️ Free Play"], onclick=lambda _: free_play_menu())
        return

    bot_move()

    if check_winner() == bot:
        game_over = True
        restart_game()
        return

    draw_board()

# ---------------- CAR GAMES ----------------
def main_car_game():
    clear()
    put_markdown("## 🚗 Choose the Safe lane")

    def choose(_):
        clear()
        put_text("🎉 Safe path!")
        put_buttons(["➡️ Continue"], onclick=lambda _: reset_board())

    put_buttons(["1", "2", "3"], onclick=choose)

def mini_car_game():
    clear()
    put_markdown("## 🚗 Mini Car Game")

    safe = random.randint(1,3)

    def choose(choice):
        clear()
        if int(choice) == safe:
            put_text("🎉 You won!")
        else:
            put_text("💥 You lost!")

        put_buttons(["🔙 Back"], onclick=lambda _: free_play_menu())

    put_buttons(["1", "2", "3"], onclick=choose)

# ---------------- CALCULATORS ----------------
def math_calc():
    clear()
    put_markdown("## ➕ Math Calculator")

    try:
        a = input("First number:", type=NUMBER)
        op = input("Operation (+ - * /):")
        b = input("Second number:", type=NUMBER)

        if op == "+": result = a + b
        elif op == "-": result = a - b
        elif op == "*": result = a * b
        elif op == "/": result = a / b if b != 0 else "Error (÷0)"
        else: result = "Invalid"

        put_text(f"Result: {result}")
    except:
        put_text("❌ Error")

    put_buttons(["🔙 Back"], onclick=lambda _: free_play_menu())

def shape_calc():
    clear()
    put_markdown("## 📐 Shape Calculator")

    def triangle():
        b = input("Base:", type=NUMBER)
        h = input("Height:", type=NUMBER)
        put_text(f"Area: {0.5 * b * h}")
        back()

    def rectangle():
        l = input("Length:", type=NUMBER)
        w = input("Width:", type=NUMBER)
        put_text(f"Area: {l * w}")
        back()

    def square():
        s = input("Side:", type=NUMBER)
        put_text(f"Area: {s * s}")
        back()

    def circle():
        r = input("Radius:", type=NUMBER)
        put_text(f"Area: {3.14 * r * r}")
        back()

    def back():
        put_buttons(["🔙 Back"], onclick=lambda _: free_play_menu())

    put_buttons(
        ["Triangle","Rectangle","Square","Circle"],
        onclick=lambda c: {
            "Triangle": triangle,
            "Rectangle": rectangle,
            "Square": square,
            "Circle": circle
        }[c]()
    )

# ---------------- EXTRA MINI GAMES ----------------
def guess_number():
    clear()
    put_markdown("## 🎲 Guess the Number (1–10)")
    num = random.randint(1,10)
    guess = input("Your guess:", type=NUMBER)

    if guess == num:
        put_text("🎉 Correct!")
    else:
        put_text(f"❌ Wrong! It was {num}")

    put_buttons(["🔙 Back"], onclick=lambda _: free_play_menu())

def memory_game():
    clear()
    put_markdown("## 🧠 Memory Game")

    nums = [random.randint(1,9) for _ in range(3)]
    put_text(f"Remember: {nums}")

    input("Press enter when ready...")

    clear()
    guess = input("Enter numbers (space separated):")

    if guess == " ".join(map(str, nums)):
        put_text("🎉 Correct!")
    else:
        put_text(f"❌ It was {nums}")

    put_buttons(["🔙 Back"], onclick=lambda _: free_play_menu())

def reaction_game():
    clear()
    put_markdown("## ⚡ Reaction Test")

    input("Wait... then click fast!")

    delay = random.randint(2,5)
    time.sleep(delay)

    start = time.time()
    input("CLICK NOW!")
    end = time.time()

    reaction = round(end - start, 2)
    put_text(f"⏱️ {reaction} seconds")

    put_buttons(["🔙 Back"], onclick=lambda _: free_play_menu())

def word_scramble():
    clear()
    put_markdown("## 🔤 Word Scramble")

    words = ["python","game","car","math","code"]
    word = random.choice(words)

    scrambled = "".join(random.sample(word, len(word)))

    put_text(f"Unscramble: {scrambled}")
    guess = input("Your answer:")

    if guess.lower() == word:
        put_text("🎉 Correct!")
    else:
        put_text(f"❌ It was {word}")

    put_buttons(["🔙 Back"], onclick=lambda _: free_play_menu())

def lucky_button():
    clear()
    put_markdown("## 🎯 Lucky Button")

    win = random.randint(1,4)

    def choose(c):
        clear()
        if int(c) == win:
            put_text("🎉 You got it!")
        else:
            put_text("💥 Nope!")

        put_buttons(["🔙 Back"], onclick=lambda _: free_play_menu())

    put_buttons(["1","2","3","4"], onclick=choose)

# ---------------- FREE PLAY ----------------
def free_play_menu():
    clear()
    put_markdown("# 🎉 Free Play Menu")

    put_buttons(
        [
            "➕ Math", "📐 Shapes", "🎮 Tic Tac Toe",
            "🚗 Car Game",
            "🎲 Guess", "🧠 Memory", "⚡ Reaction",
            "🔤 Word", "🎯 Lucky",
            "🔁 Reset Game"
        ],
        onclick=handle_menu
    )

def handle_menu(choice):
    if choice == "➕ Math":
        math_calc()
    elif choice == "📐 Shapes":
        shape_calc()
    elif choice == "🎮 Tic Tac Toe":
        reset_board()
    elif choice == "🚗 Car Game":
        mini_car_game()
    elif choice == "🎲 Guess":
        guess_number()
    elif choice == "🧠 Memory":
        memory_game()
    elif choice == "⚡ Reaction":
        reaction_game()
    elif choice == "🔤 Word":
        word_scramble()
    elif choice == "🎯 Lucky":
        lucky_button()
    else:
        main()

# ---------------- MAIN GAME ----------------
def main():
    clear()
    put_markdown("# 🎯 Game Hub Challenge Mode")

    for _ in range(2):
        a, b = random.randint(1,10), random.randint(1,10)
        ans = input(f"{a} + {b} = ?", type=NUMBER)

        if ans != a + b:
            restart_game()
            return

        put_text("✅ Correct!")

    main_car_game()

# ---------------- RUN ----------------
import os
start_server(main, port=int(os.environ.get("PORT", 8080)))
