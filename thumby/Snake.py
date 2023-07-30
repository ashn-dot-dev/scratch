# /Games/Snake/Snake.py
import random
import thumby
import time

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        assert type(self) == type(other)
        return (self.x, self.y) == (other.x, other.y)

    def __repr__(self):
        return f"Position({self.x}, {self.y})"

class Velocity:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        assert type(self) == type(other)
        return (self.x, self.y) == (other.x, other.y)

    def __repr__(self):
        return f"Velocity({self.x}, {self.y})"

class Snake:
    def __init__(self, body, velocity):
        self.body = body
        self.velocity = velocity

    def head(self):
        return self.body[0]

    def tail(self):
        return self.body[len(self.body)-1]

class State:
    def __init__(self):
        self.done = False
        self.frame = 0
        self.snake = Snake([
            Position(thumby.display.width // 2 - BLOCK * 1, thumby.display.height // 2 - BLOCK),
            Position(thumby.display.width // 2 - BLOCK * 2, thumby.display.height // 2 - BLOCK),
            Position(thumby.display.width // 2 - BLOCK * 3, thumby.display.height // 2 - BLOCK),
        ], Velocity(+BLOCK, +0))
        self.fruit = Position(self.snake.head().x + BLOCK * 8, self.snake.head().y)
        self.direction = Velocity(self.snake.velocity.x, self.snake.velocity.y)

BLACK = 0
WHITE = 1

BLOCK = 4

VELOCITY_U = Velocity(+0, -BLOCK)
VELOCITY_D = Velocity(+0, +BLOCK)
VELOCITY_L = Velocity(-BLOCK, +0)
VELOCITY_R = Velocity(+BLOCK, +0)

FONT_W = 8
FONT_H = 8
FONT_SPACE = 0
thumby.display.setFont("/lib/font8x8.bin", FONT_W, FONT_H, FONT_SPACE)

FRAMES_PER_SECOND = 60
FRAMES_PER_UPDATE_MAX = 15
FRAMES_PER_UPDATE_MIN = 5
thumby.display.setFPS(FRAMES_PER_SECOND)

def wait_for_any_input():
    while not thumby.inputJustPressed():
        pass

def draw_text_centered(text):
    x = thumby.display.width // 2 - len(text) * FONT_W // 2
    y = thumby.display.height // 2 - FONT_H // 2
    thumby.display.drawText(text, x, y, WHITE)

def update(state):
    if thumby.buttonU.justPressed() and state.snake.velocity != VELOCITY_D:
        state.direction = VELOCITY_U
    if thumby.buttonD.justPressed() and state.snake.velocity != VELOCITY_U:
        state.direction = VELOCITY_D
    if thumby.buttonL.justPressed() and state.snake.velocity != VELOCITY_R:
        state.direction = VELOCITY_L
    if thumby.buttonR.justPressed() and state.snake.velocity != VELOCITY_L:
        state.direction = VELOCITY_R

    frames_per_update = FRAMES_PER_UPDATE_MAX - len(state.snake.body) // 6
    frames_per_update = max(frames_per_update, FRAMES_PER_UPDATE_MIN)
    if state.frame % frames_per_update != 0:
        return

    state.snake.velocity.x = state.direction.x
    state.snake.velocity.y = state.direction.y
    last = Position(state.snake.tail().x, state.snake.tail().y)

    next_x = (state.snake.head().x + state.snake.velocity.x) % thumby.display.width
    next_y = (state.snake.head().y + state.snake.velocity.y) % thumby.display.height
    if Position(next_x, next_y) in state.snake.body[:-1]:
        state.done = True
        return

    for i in reversed(range(1, len(state.snake.body))):
        state.snake.body[i].x = state.snake.body[i-1].x
        state.snake.body[i].y = state.snake.body[i-1].y
    state.snake.head().x = next_x
    state.snake.head().y = next_y

    if state.snake.head() in state.snake.body[1:]:
        state.done = True
        return

    if state.snake.head() == state.fruit:
        state.snake.body.append(last)
        # Select a new random position in the play area as the location for the
        # next fruit spawn. If that area is occupied by any segment of the
        # snake's body, then discard that position repeat the selection.
        while True:
            state.fruit.x = random.randint(0, (thumby.display.width-1) // BLOCK) * BLOCK
            state.fruit.y = random.randint(0, (thumby.display.height-1) // BLOCK) * BLOCK
            if not state.fruit in state.snake.body:
                break

def render(state):
    thumby.display.fill(BLACK if not state.done else WHITE)
    color = WHITE if not state.done else BLACK
    # Head
    thumby.display.drawFilledRectangle(state.snake.head().x, state.snake.head().y, BLOCK, BLOCK, color)
    if state.snake.velocity == VELOCITY_U:
        thumby.display.drawFilledRectangle(state.snake.head().x,             state.snake.head().y, 1, 1, color ^ 1)
        thumby.display.drawFilledRectangle(state.snake.head().x + BLOCK - 1, state.snake.head().y, 1, 1, color ^ 1)
    if state.snake.velocity == VELOCITY_D:
        thumby.display.drawFilledRectangle(state.snake.head().x,             state.snake.head().y + BLOCK - 1, 1, 1, color ^ 1)
        thumby.display.drawFilledRectangle(state.snake.head().x + BLOCK - 1, state.snake.head().y + BLOCK - 1, 1, 1, color ^ 1)
    if state.snake.velocity == VELOCITY_L:
        thumby.display.drawFilledRectangle(state.snake.head().x, state.snake.head().y,             1, 1, color ^ 1)
        thumby.display.drawFilledRectangle(state.snake.head().x, state.snake.head().y + BLOCK - 1, 1, 1, color ^ 1)
    if state.snake.velocity == VELOCITY_R:
        thumby.display.drawFilledRectangle(state.snake.head().x + BLOCK - 1, state.snake.head().y,             1, 1, color ^ 1)
        thumby.display.drawFilledRectangle(state.snake.head().x + BLOCK - 1, state.snake.head().y + BLOCK - 1, 1, 1, color ^ 1)
    # Body
    for pos in state.snake.body[1:]:
        thumby.display.drawFilledRectangle(pos.x, pos.y, BLOCK, BLOCK, color)
    # Fruit
    thumby.display.drawRectangle(state.fruit.x, state.fruit.y, BLOCK, BLOCK, color)
    thumby.display.update()

def game_init():
    thumby.display.fill(BLACK)
    draw_text_centered("SNAKE")
    thumby.display.update()
    wait_for_any_input()
    # Flash to indicate the game is starting.
    for c in (WHITE, BLACK, WHITE):
        thumby.display.fill(c)
        for _ in range(FRAMES_PER_UPDATE_MAX):
            thumby.display.update()
    return State()

def game_main(state):
    while not state.done:
        update(state)
        render(state)
        state.frame += 1

def game_fini(state):
    time.sleep(1)
    thumby.display.fill(BLACK)
    draw_text_centered(f"SCORE {len(state.snake.body)}")
    thumby.display.update()
    time.sleep(1)
    wait_for_any_input()

def main():
    state = game_init()
    game_main(state)
    game_fini(state)
    thumby.reset()

main()
