import tkinter as tk
from PIL import Image, ImageTk  # Import Pillow for image handling

middle_wall = None
wall_active = False

# Function to switch frames
def show_frame(frame):
    """Displays the specified frame and resets relevant elements if needed."""
    global left_score, right_score, timer_running, timer_id

    if frame == main_frame:  # Check if we're going to the main menu
        # Pause the timer
        timer_running = False
        if timer_id is not None:
            root.after_cancel(timer_id)
            timer_id = None

        if not game_paused:  # Only reset if not coming from a paused game
            left_score = 0
            right_score = 0
            update_score_display()  # Reset the score display

    frame.tkraise()


# Create the main window
root = tk.Tk()
root.title("Quarterback Clash")

# Create a container frame for each section
main_frame = tk.Frame(root)
game_frame = tk.Frame(root)
settings_frame = tk.Frame(root)
leaderboard_frame = tk.Frame(root)

# Add the frames to the window
for frame in (main_frame, game_frame, settings_frame, leaderboard_frame):
    frame.grid(row=0, column=0, sticky="news")

# --- Main Menu Frame with Background ---
# Create a canvas for the main menu to hold the background
main_menu_canvas = tk.Canvas(main_frame, width=800, height=600)
main_menu_canvas.pack(fill="both", expand=True)

# Loading and setting the main menu background image
main_menu_bg = Image.open("bg.jpg")
main_menu_bg = main_menu_bg.resize((1050, 800), Image.LANCZOS)
main_menu_bg_photo = ImageTk.PhotoImage(main_menu_bg)
main_menu_canvas.create_image(0, 0, image=main_menu_bg_photo, anchor="nw")


tk.Label(
    main_menu_canvas,
    text="Quarterback Clash",
    font=("Bebas Neue", 24),
    bg="crimson",
    fg="gold",
).pack(pady=20)

start_button = tk.Button(
    main_menu_canvas,
    text="Start Game",
    font=("Bebas Neue", 16),
    bg="navy",
    fg="white",
    command=lambda: start_game(),
)
start_button.pack(pady=10)

# Add Resume Game button
resume_button = tk.Button(
    main_menu_canvas,
    text="Resume Game",
    font=("Bebas Neue", 16),
    bg="navy",
    fg="white",
    command=lambda: load_game(),
)
resume_button.pack(pady=10)

settings_button = tk.Button(
    main_menu_canvas,
    text="Settings",
    font=("Bebas Neue", 16),
    bg="navy",
    fg="white",
    command=lambda: show_frame(settings_frame),
)
settings_button.pack(pady=10)


leaderboard_button = tk.Button(
    main_menu_canvas,
    text="Leaderboard",
    font=("Bebas Neue", 16),
    bg="navy",
    fg="white",
    command=lambda: show_frame(leaderboard_frame),
)
leaderboard_button.pack(pady=10)

# --- Settings Frame with Background ---
settings_canvas = tk.Canvas(settings_frame, width=800, height=600)
settings_canvas.pack(fill="both", expand=True)

# Loading and setting the settings background image
settings_bg = Image.open("bg.jpg")  
settings_bg = settings_bg.resize((1050, 800), Image.LANCZOS)
settings_bg_photo = ImageTk.PhotoImage(settings_bg)
settings_canvas.create_image(0, 0, image=settings_bg_photo, anchor="nw")


# Add settings content to the frame
tk.Label(
    settings_canvas, text="Settings", font=("Bebas Neue", 24), bg="crimson", fg="gold"
).pack(pady=20)

# Initial control keys
left_up_key = "w"
left_down_key = "s"
right_up_key = "Up"
right_down_key = "Down"

# Functions to update keybindings based on player input
def change_key(control):
    """Change the key binding for the specified control."""

    def on_key_press(event):
        global left_up_key, left_down_key, right_up_key, right_down_key
        if control == "left_up":
            left_up_key = event.keysym
        elif control == "left_down":
            left_down_key = event.keysym
        elif control == "right_up":
            right_up_key = event.keysym
        elif control == "right_down":
            right_down_key = event.keysym
        update_key_bindings()
        root.unbind("<Key>")
        show_frame(settings_frame)

    tk.Label(
        settings_canvas,
        text=f"Press a key for {control.replace('_', ' ')}...",
        bg="crimson",
        fg="white",
    ).pack()
    root.bind("<Key>", on_key_press)


# Keybinding buttons
tk.Button(
    settings_canvas,
    text="Change Left Paddle Up Key",
    bg="navy",
    fg="white",
    command=lambda: change_key("left_up"),
).pack(pady=5)
tk.Button(
    settings_canvas,
    text="Change Left Paddle Down Key",
    bg="navy",
    fg="white",
    command=lambda: change_key("left_down"),
).pack(pady=5)
tk.Button(
    settings_canvas,
    text="Change Right Paddle Up Key",
    bg="navy",
    fg="white",
    command=lambda: change_key("right_up"),
).pack(pady=5)
tk.Button(
    settings_canvas,
    text="Change Right Paddle Down Key",
    bg="navy",
    fg="white",
    command=lambda: change_key("right_down"),
).pack(pady=5)

# ---Cheat code section---

# Create a wall in the middle of the screen
def toggle_middle_wall(event=None):
    """Toggle the middle wall on/off in the game."""
    global middle_wall, wall_active
    if not wall_active:
        middle_wall = canvas.create_rectangle(
            395, 100, 405, 500, fill="gold", outline="white"
        )
        wall_active = True
    else:
        # Remove the wall
        if middle_wall:
            canvas.delete(middle_wall)
        wall_active = False

#Adding 1 score to the left player's score
def auto_score_left(event=None):
    """Increase the left player's score by 1."""
    global left_score
    left_score += 1
    update_score_display()

#Adding 1 score to the right player's score
def auto_score_right(event=None):
    """Increase the right player's score by 1."""
    global right_score
    right_score += 1
    update_score_display()


#Reduce ball speed by half
def slow_ball_speed(event=None):
    """Halve the ball's speed."""
    global ball_speed_x, ball_speed_y
    ball_speed_x *= 0.5
    ball_speed_y *= 0.5


# Bind cheat keys
root.bind("1", auto_score_left)  # '1' key to add to left player's score
root.bind("2", auto_score_right)  # '2' key to add to right player's score
root.bind("3", slow_ball_speed)  # '3' key to slow down the ball speed
root.bind("4", toggle_middle_wall)  # '4' key to toggle the middle wall
tk.Label(
    settings_canvas,
    text="Cheat Codes",
    font=("Bebas Neue", 20),
    bg="crimson",
    fg="white",
).pack(pady=20)
tk.Label(
    settings_canvas,
    text="Cheat Key Bindings:\n1 - Left Player +1 Point\n2 - Right Player +1 Point\n3 - Slow Down Ball\n4 - Toggle Middle Wall",
    font=("Bebas Neue", 12),
    bg="crimson",
    fg="white",
).pack(pady=10)


# ---Boss key feature---
fake_workspace_image = Image.open("fake_workspace.jpg")
fake_workspace_image = fake_workspace_image.resize((800, 600), Image.LANCZOS)
fake_workspace_photo = ImageTk.PhotoImage(fake_workspace_image)
fake_workspace_overlay = None


def toggle_boss_key(event=None):
    """Show/hide the fake workspace and pause the game."""
    global fake_workspace_overlay, game_paused

    # Pause the game if not already paused
    if not game_paused:
        game_paused = True
        pause_button.config(text="Resume")
        canvas.create_text(
            400,
            300,
            text="PAUSED",
            fill="white",
            font=("Bebas Neue", 36),
            tags="pause_text",
        )

    # Toggle the fake workspace overlay
    if fake_workspace_overlay:
        canvas.delete(fake_workspace_overlay)
        fake_workspace_overlay = None
    else:
        fake_workspace_overlay = canvas.create_image(
            0, 0, image=fake_workspace_photo, anchor="nw"
        )


# Bind boss key
root.bind("b", toggle_boss_key)

tk.Label(
    settings_canvas,
    text="Boss Key Binding",
    font=("Bebas Neue", 20),
    bg="crimson",
    fg="white",
).pack(pady=20)
tk.Label(
    settings_canvas,
    text="B - Display Forex Chart",
    font=("Bebas Neue", 12),
    bg="crimson",
    fg="white",
).pack(pady=10)

# Bind Pause/Resume key
root.bind("p", lambda event: toggle_pause())

tk.Label(
    settings_canvas,
    text="Pause Game Key Binding",
    font=("Bebas Neue", 20),
    bg="crimson",
    fg="white",
).pack(pady=20)

tk.Label(
    settings_canvas,
    text="P - Pause/Resume Game",
    font=("Bebas Neue", 12),
    bg="crimson",
    fg="white",
).pack(pady=10)

tk.Button(
    settings_canvas,
    text="Back to Menu",
    font=("Bebas Neueial", 16),
    bg="navy",
    fg="white",
    command=lambda: show_frame(main_frame),
).pack(pady=20)


# ---Save/Load game functionality---
def save_game():
    """Save the current game state in a text file."""
    try:
        with open(
            "saved_game.txt", "w"
        ) as f:  # use a text file to save the value of the variables at current state.
            f.write(f"{left_score}\n")
            f.write(f"{right_score}\n")
            f.write(f"{ball_x}\n")
            f.write(f"{ball_y}\n")
            f.write(f"{ball_speed_x}\n")
            f.write(f"{ball_speed_y}\n")
            f.write(f"{left_paddle_y}\n")
            f.write(f"{right_paddle_y}\n")
            f.write(f"{wall_active}\n")
            f.write(f"{time_remaining}\n")

        canvas.create_text(
            400,
            200,
            text="Game Saved!",
            fill="white",
            font=("Bebas Neue", 24),
            tags="save_text",
        )
        root.after(2000, lambda: canvas.delete("save_text"))
    except:
        canvas.create_text(
            400,
            200,
            text="Error Saving Game!",
            fill="red",
            font=("Bebas Neue", 24),
            tags="save_text",
        )
        root.after(2000, lambda: canvas.delete("save_text"))


# Add load game function
def load_game():
    """Loads the saved game states from a file and updates the game elements accordingly."""
    global left_score, right_score, ball_x, ball_y, ball_speed_x, ball_speed_y
    global left_paddle_y, right_paddle_y, wall_active, time_remaining
    global timer_running, game_paused

    try:
        with open("saved_game.txt", "r") as f:
            lines = f.readlines()
            left_score = int(lines[0])
            right_score = int(lines[1])
            ball_x = float(lines[2])
            ball_y = float(lines[3])
            ball_speed_x = 4.5
            left_paddle_y = float(lines[6])
            right_paddle_y = float(lines[7])
            wall_active = lines[8].strip().lower() == "true"
            time_remaining = int(lines[9])

        # Update visual elements
        canvas.coords(ball, ball_x, ball_y)
        canvas.coords(left_paddle, 60, left_paddle_y)
        canvas.coords(right_paddle, 755, right_paddle_y)
        update_score_display()

        # Recreate wall if it was active
        if wall_active and not middle_wall:
            toggle_middle_wall()

        # Start game
        show_frame(game_frame)
        game_paused = False
        timer_running = True
        update_timer()
        move_ball()

    except:  # If the game was not saved, give error message to user.
        error_label = tk.Label(
            main_menu_canvas,
            text="No saved game found!",
            fg="white",
            bg="crimson",
            font=("Bebas Neue", 16),
        )
        error_label.pack(pady=5)
        root.after(2000, error_label.destroy)


# Function to check if saved game exists
def has_saved_game():
    """Checks if there is a saved game file available."""
    try:
        with open("saved_game.txt", "r") as f:
            return True
    except:
        return False


# Modify show_frame function to handle game resumption
def show_frame(frame):
    """Displays the specified frame and resets relevant elements if needed."""
    global left_score, right_score
    if frame == main_frame:  # Check if we're going to the main menu
        if not game_paused:  # Only reset if not coming from a paused game
            left_score = 0
            right_score = 0
            update_score_display()  # Reset the score display
    frame.tkraise()


def update_resume_button():
    """Enables or disables the resume button based on the existence of a saved game."""
    if has_saved_game():
        resume_button.config(state="normal")
    else:
        resume_button.config(state="disabled")


# --- Leaderboard Frame with Image Background ---
leaderboard_canvas = tk.Canvas(leaderboard_frame, width=800, height=600)
leaderboard_canvas.pack(fill="both", expand=True)

# Loading and setting the leaderboard background image
leaderboard_bg = Image.open("bg.jpg")  # You can use a different image if desired
leaderboard_bg = leaderboard_bg.resize((1050, 800), Image.LANCZOS)
leaderboard_bg_photo = ImageTk.PhotoImage(leaderboard_bg)
leaderboard_canvas.create_image(0, 0, image=leaderboard_bg_photo, anchor="nw")

# Function to read leaderboard data from file
def read_leaderboard():
    """Reads the leaderboard data from the file and returns a sorted list of scores."""
    try:
        with open("leaderboard.txt", "r") as f:
            scores = [line.strip().split(",") for line in f]
            return sorted(
                scores, key=lambda x: int(x[1]), reverse=True
            )  # Sort by score
    except FileNotFoundError:
        return []


# Function to update leaderboard display
def display_leaderboard():
    """Displays the leaderboard with player names and scores on the canvas."""
    for widget in leaderboard_canvas.winfo_children():
        widget.destroy()

    tk.Label(
        leaderboard_canvas,
        text="Leaderboard",
        font=("Bebas Neue", 24),
        bg="crimson",
        fg="gold",
    ).pack(pady=20)

    scores = read_leaderboard()
    for i, (player, score) in enumerate(scores, 1):
        tk.Label(
            leaderboard_canvas,
            text=f"{i}. {player} - {score} points",
            font=("Bebas Neueal", 16),
            bg="crimson",
            fg="white",
        ).pack(pady=5)

    tk.Button(
        leaderboard_canvas,
        text="Back to Menu",
        font=("Bebas Neue", 16),
        bg="navy",
        fg="white",
        command=lambda: show_frame(main_frame),
    ).pack(pady=20)


# Function to update or append a player's score
def update_leaderboard(player, score):
    """Updates the leaderboard with the player's score, adding or modifying the entry as needed."""
    scores = read_leaderboard()
    updated = False

    # Check if player already exists in the leaderboard
    for entry in scores:
        if entry[0] == player:
            entry[1] = str(max(int(entry[1]), score))  # Update the score if higher
            updated = True
            break

    if not updated:
        scores.append([player, str(score)])  # Add new player

    # Write updated leaderboard back to the file
    with open("leaderboard.txt", "w") as f:
        for entry in scores:
            f.write(",".join(entry) + "\n")


# Prompt winner for their name and update leaderboard
def prompt_winner(score):
    """Prompts the winner to enter their name and updates the leaderboard with their score."""

    def save_name():
        player_name = name_entry.get().strip()
        if player_name:
            update_leaderboard(player_name, score)
            winner_prompt.destroy()
            show_frame(leaderboard_frame)
            display_leaderboard()

    winner_prompt = tk.Toplevel(root)
    winner_prompt.title("Winner!")
    tk.Label(
        winner_prompt, text="Congratulations! Enter your name:", font=("Bebas Neue", 16)
    ).pack(pady=10)
    name_entry = tk.Entry(winner_prompt, font=("Bebas Neue", 14))
    name_entry.pack(pady=10)
    tk.Button(winner_prompt, text="Submit", command=save_name).pack(pady=10)


# Initially display leaderboard content
display_leaderboard()

# --- Pong Game Frame ---
canvas = tk.Canvas(game_frame, width=800, height=600, bg="black")
canvas.pack()

# Function to toggle pause state
def toggle_pause():
    """Toggles the game's pause state and updates the UI elements accordingly."""
    global game_paused
    game_paused = not game_paused
    if game_paused:
        pause_button.config(text="Resume")
        canvas.create_text(
            400,
            300,
            text="PAUSED",
            fill="white",
            font=("Bebas Neue", 36),
            tags="pause_text",
        )
    else:
        pause_button.config(text="Pause")
        canvas.delete("pause_text")
        move_ball()
        # Resume timer if it was running
        if timer_running:
            update_timer()


# Create a frame for the game controls
game_controls_frame = tk.Frame(game_frame)
game_controls_frame.pack(fill="x", padx=10)
# Add buttons and score display in the same row
back_button = tk.Button(
    game_controls_frame,
    text="Back to Main Menu",
    font=("Bebas Neue", 16),
    bg="navy",
    fg="white",
    command=lambda: show_frame(main_frame),
)
back_button.pack(side="left", pady=10)

# Add pause button
pause_button = tk.Button(
    game_controls_frame,
    text="Pause",
    font=("Bebas Neue", 16),
    bg="navy",
    fg="white",
    command=toggle_pause,
)
pause_button.pack(side="left", padx=10, pady=10)

# Create a label for the score display
score_label = tk.Label(
    game_controls_frame,
    text="Player 1: 0 - Player 2: 0",
    font=("Bebas Neue", 16),
    fg="black",
    bg="white",
)
score_label.pack(side="left", padx=20, pady=10)

# Add Save Game button
save_button = tk.Button(
    game_controls_frame,
    text="Save Game",
    font=("Bebas Neue", 16),
    bg="navy",
    fg="white",
    command=save_game,
)
save_button.pack(side="left", padx=10, pady=10)

# Add game state variable
game_paused = False

# Loading and setting the background image
background_image = Image.open("background.jpg")  # Loading background image
background_image = background_image.resize((800, 600), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)
background_label = canvas.create_image(0, 0, image=background_photo, anchor="nw")

# Loading glove images for paddles
left_glove_image = Image.open("left_glove.png")  # Opening left glove image
right_glove_image = Image.open("right_glove.png")  # Opening right glove image

# Resize the gloves to fit the paddle area (e.g., 500x500 for paddles)
left_glove_image = left_glove_image.resize((500, 500), Image.LANCZOS)
right_glove_image = right_glove_image.resize((500, 500), Image.LANCZOS)

# Convert to PhotoImage for use on canvas
left_glove_photo = ImageTk.PhotoImage(left_glove_image)
right_glove_photo = ImageTk.PhotoImage(right_glove_image)

# Create the glove paddles on the canvas
left_paddle = canvas.create_image(60, 250, image=left_glove_photo)
right_paddle = canvas.create_image(755, 250, image=right_glove_photo)

# Loading the American football image and set it as the ball
football_image = Image.open(
    "american_football.png"
)  # Replace with your image file path
football_image = football_image.resize(
    (50, 50), Image.LANCZOS
)  # Resize it to fit as the ball
football_photo = ImageTk.PhotoImage(football_image)
ball = canvas.create_image(390, 290, image=football_photo)


# ---Game variables---
# Score variables
left_score = 0
right_score = 0
# Initial speeds
initial_ball_speed_x = 3.0
initial_ball_speed_y = 3.0
ball_speed_x = initial_ball_speed_x
ball_speed_y = initial_ball_speed_y
paddle_speed = 50
left_paddle_y = 250
right_paddle_y = 250
ball_x = 390
ball_y = 290
max_speed = 7.0  # Set maximum speed for the ball
speed_increment = 1.03  # The amount to increase speed each frame
ball_move_id = None  # To store the `after` ID for ball movement


# Functions to move paddles
def move_left_paddle_up(event=None):
    """Moves the left paddle upwards within the allowed bounds."""
    global left_paddle_y
    if left_paddle_y > 0 and not game_paused:
        left_paddle_y -= paddle_speed
        canvas.coords(left_paddle, 60, left_paddle_y)


def move_left_paddle_down(event=None):
    """Moves the left paddle downwards within the allowed bounds."""
    global left_paddle_y
    if left_paddle_y < 500 and not game_paused:
        left_paddle_y += paddle_speed
        canvas.coords(left_paddle, 60, left_paddle_y)


def move_right_paddle_up(event=None):
    """Moves the right paddle upwards within the allowed bounds."""
    global right_paddle_y
    if right_paddle_y > 0 and not game_paused:
        right_paddle_y -= paddle_speed
        canvas.coords(right_paddle, 755, right_paddle_y)


def move_right_paddle_down(event=None):
    """Moves the right paddle downwards within the allowed bounds."""
    global right_paddle_y
    if right_paddle_y < 500 and not game_paused:
        right_paddle_y += paddle_speed
        canvas.coords(right_paddle, 755, right_paddle_y)


# Define maximum speed limits
def check_win_condition():
    """Checks if any player has reached the win condition and pauses the game if true."""
    global game_paused
    if left_score >= 15 or right_score >= 15:
        game_paused = True
        winner = "Player 1" if left_score >= 15 else "Player 2"
        # Create win message on canvas
        canvas.create_text(
            400,
            250,
            text=f"{winner} Wins!",
            fill="white",
            font=("Bebas Neue", 36),
            tags="win_text",
        )
        canvas.create_text(
            400,
            300,
            text="Game Over",
            fill="white",
            font=("Bebas Neue", 24),
            tags="win_text",
        )
        # Update leaderboard and show winner prompt
        prompt_winner(15)
        return True
    return False


def move_ball():
    """Moves the ball, handling collisions and updating its position on the canvas."""
    global ball_x, ball_y, ball_speed_x, ball_speed_y, left_score, right_score, ball_move_id

    if not game_paused:
        # Move ball
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Ball collision with top and bottom walls
        if ball_y <= 0 or ball_y >= 550:
            ball_speed_y = -ball_speed_y

        # Ball collision with middle wall when active
        if wall_active and 390 <= ball_x <= 410 and 100 <= ball_y <= 500:
            ball_speed_x = -ball_speed_x
            ball_x += ball_speed_x * 2  # Prevent ball from getting stuck in wall

        # Ball collision with paddles
        if ball_x <= 110 and left_paddle_y <= ball_y <= left_paddle_y + 100:
            ball_speed_x = -ball_speed_x
            if abs(ball_speed_x) < max_speed:
                ball_speed_x = ball_speed_x * speed_increment

        if ball_x >= 690 and right_paddle_y <= ball_y <= right_paddle_y + 100:
            ball_speed_x = -ball_speed_x
            if abs(ball_speed_x) < max_speed:
                ball_speed_x = ball_speed_x * speed_increment

        # Enforce speed limits
        ball_speed_x = max(min(ball_speed_x, max_speed), -max_speed)
        ball_speed_y = max(min(ball_speed_y, max_speed), -max_speed)

        # Ball out of bounds
        if ball_x <= 0:
            right_score += 1
            update_score_display()
            reset_ball()

        if ball_x >= 800:
            left_score += 1
            update_score_display()
            reset_ball()

        # Update ball position
        canvas.coords(ball, ball_x, ball_y)

        # Continue game loop
        ball_move_id = root.after(16, move_ball)


# Function to reset ball position
def reset_ball():
    """Resets the ball to the center position and restores its initial speed."""
    global ball_x, ball_y, ball_speed_x, ball_speed_y, initial_ball_speed_x, initial_ball_speed_y
    # Set ball to center position
    ball_x = 390
    ball_y = 290
    # Reset to initial speeds
    ball_speed_x = initial_ball_speed_x
    ball_speed_y = initial_ball_speed_y
    canvas.coords(ball, ball_x, ball_y)


# Function to update the score display
def update_score_display():
    """Updates the score display with the current scores of both players."""
    score_label.config(
        text=f"Player 1: {left_score} - Player 2: {right_score}",
        bg="crimson",
        fg="white",
    )


# Add timer variables
game_duration = 120  # 2 minutes in seconds
time_remaining = game_duration
timer_running = False
timer_id = None

# Add timer display to game controls frame
timer_label = tk.Label(
    game_controls_frame,
    text="Time: 2:00",
    font=("Bebas Neue", 16),
    bg="crimson",
    fg="white",
)
timer_label.pack(side="left", padx=20, pady=10)


def update_timer():
    """Updates the countdown timer every second, updates the display, and ends the game when the time is up."""
    global time_remaining, timer_running, game_paused, timer_id
    if timer_running and not game_paused:
        time_remaining -= 1

        # Format time as M:SS
        minutes = time_remaining // 60
        seconds = time_remaining % 60
        timer_label.config(text=f"Time: {minutes}:{seconds:02d}")

        if time_remaining <= 0:
            end_game()
        else:
            # Schedule the next call and store the ID
            timer_id = root.after(1050, update_timer)


# Game start function
def start_game():
    """Resets the game state, starts the timer, and begins ball movement to initiate the game."""
    global game_paused, left_score, right_score, timer_running, time_remaining, ball_move_id, timer_id

    # Cancel any existing game loop
    if ball_move_id is not None:
        root.after_cancel(ball_move_id)
        ball_move_id = None

    # Cancel any existing timer
    if timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None

    # Reset game state
    left_score = 0
    right_score = 0
    time_remaining = game_duration
    update_score_display()

    # Clear any existing canvas text
    canvas.delete("win_text")
    canvas.delete("pause_text")

    # Reset ball and start game
    reset_ball()
    game_paused = False

    # Start timer
    timer_running = True
    update_timer()

    # Start ball movement
    move_ball()
    show_frame(game_frame)


def end_game():
    """Ends the game, stops the timer, and displays the winner or a tie along with the final score."""
    global timer_running, game_paused
    timer_running = False
    game_paused = True

    # Determine winner based on score
    if left_score > right_score:
        winner = "Player 1"
    elif right_score > left_score:
        winner = "Player 2"
    else:
        winner = "Tie"

    # Display end game message
    if winner != "Tie":
        canvas.create_text(
            400,
            250,
            text=f"{winner} Wins!",
            fill="white",
            font=("Bebas Neue", 36),
            tags="win_text",
        )
        canvas.create_text(
            400,
            300,
            text=f"Final Score: {left_score} - {right_score}",
            fill="white",
            font=("Bebas Neue", 24),
            tags="win_text",
        )
        # Prompt winner for leaderboard entry
        if winner == "Player 1":
            prompt_winner(left_score)
        else:
            prompt_winner(right_score)
    else:
        canvas.create_text(
            400,
            250,
            text="Game Over - It's a Tie!",
            fill="white",
            font=("Bebas Neue", 36),
            tags="win_text",
        )
        canvas.create_text(
            400,
            300,
            text=f"Final Score: {left_score} - {right_score}",
            fill="white",
            font=("Bebas Neue", 24),
            tags="win_text",
        )


# Function to reset the game after it ends
def reset_game():
    """Resets the game state and score, and navigates to the leaderboard screen after the game ends."""
    global player1_score, player2_score
    player1_score = 0
    player2_score = 0
    ball_speed_x = initial_ball_speed_x
    ball_speed_y = initial_ball_speed_y
    # Reset positions, ball, and other game state here
    show_frame(leaderboard_frame)  # Navigate to leaderboard


# Example of where to call `check_game_end` in your game loop
def update_score(player):
    """Increases the score for the specified player, checks if the game should end, and updates the score display."""
    global player1_score, player2_score
    if player == 1:
        player1_score += 1
    elif player == 2:
        player2_score += 1

    end_game()  # Check if the game should end
    update_score_display()  # Function to update the score display (if applicable)


# Call update_resume_button when showing main menu
show_frame(main_frame)
update_resume_button()

# Key bindings for player controls
root.bind(f"<{left_up_key}>", move_left_paddle_up)
root.bind(f"<{left_down_key}>", move_left_paddle_down)
root.bind(f"<{right_up_key}>", move_right_paddle_up)
root.bind(f"<{right_down_key}>", move_right_paddle_down)

# Update key bindings dynamically
def update_key_bindings():
    """Unbinds the current key bindings and rebinds the keys to their respective paddle movement functions."""
    root.unbind(f"<{left_up_key}>")
    root.unbind(f"<{left_down_key}>")
    root.unbind(f"<{right_up_key}>")
    root.unbind(f"<{right_down_key}>")

    root.bind(f"<{left_up_key}>", move_left_paddle_up)
    root.bind(f"<{left_down_key}>", move_left_paddle_down)
    root.bind(f"<{right_up_key}>", move_right_paddle_up)
    root.bind(f"<{right_down_key}>", move_right_paddle_down)


# Start by showing the main menu
show_frame(main_frame)

# Run the Tkinter event loop
root.mainloop()