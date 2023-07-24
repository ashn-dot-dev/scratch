import random
import thumby

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

thumby.display.setFPS(60)

def init():
    # Flash the screen at boot time to indicate the game is starting.
    for c in (WHITE, BLACK, WHITE):
        thumby.display.fill(c)
        for _ in range(10):
            thumby.display.update()
    # Return the initial game state.
    return State()

def update(state):
    if thumby.buttonU.justPressed() and state.snake.velocity != VELOCITY_D:
        state.direction = VELOCITY_U
    if thumby.buttonD.justPressed() and state.snake.velocity != VELOCITY_U:
        state.direction = VELOCITY_D
    if thumby.buttonL.justPressed() and state.snake.velocity != VELOCITY_R:
        state.direction = VELOCITY_L
    if thumby.buttonR.justPressed() and state.snake.velocity != VELOCITY_L:
        state.direction = VELOCITY_R

    if state.frame % 10 != 0:
        return

    state.snake.velocity.x = state.direction.x
    state.snake.velocity.y = state.direction.y
    last = Position(state.snake.tail().x, state.snake.tail().y)

    for i in reversed(range(1, len(state.snake.body))):
        state.snake.body[i].x = state.snake.body[i-1].x
        state.snake.body[i].y = state.snake.body[i-1].y
    state.snake.head().x += state.snake.velocity.x
    state.snake.head().y += state.snake.velocity.y
    state.snake.head().x %= thumby.display.width
    state.snake.head().y %= thumby.display.height

    if state.snake.head() in state.snake.body[1:]:
        state.done = True

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
    for pos in state.snake.body:
        thumby.display.drawFilledRectangle(pos.x, pos.y, BLOCK, BLOCK, color)
    thumby.display.drawRectangle(state.fruit.x, state.fruit.y, BLOCK, BLOCK, color)
    thumby.display.update()

def main():
    state = init()
    while not state.done:
        update(state)
        render(state)
        state.frame += 1

main()