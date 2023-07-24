use macroquad::prelude::*;

const WINDOW_W: i32 = 800;
const WINDOW_H: i32 = 600;
const TIMESTEP: f64 = 1.0 / 60.0;

struct Paddle {
    position: Vec2,
}

impl Paddle {
    const W: f32 = (WINDOW_W / 60) as f32;
    const H: f32 = (WINDOW_H / 6) as f32;
    const SPEED: f32 = 10.0;
}

struct Ball {
    position: Vec2,
    velocity: Vec2,
    collision: bool,
}

impl Ball {
    const SIDE: f32 = Paddle::W;
    const SPEED: f32 = 8.0;
}

enum State {
    Serve { velocity: Vec2 },
    InPlay,
    Quit,
}

struct Context {
    state: State,
    p1: Paddle,
    p2: Paddle,
    ball: Ball,
    p1_score: usize,
    p2_score: usize,
}

impl Context {
    fn new(screen_w: f32, screen_h: f32) -> Context {
        Context {
            state: State::Serve {
                velocity: Vec2 {
                    x: Ball::SPEED,
                    y: 0.0,
                },
            },
            p1: Paddle {
                position: Vec2 {
                    x: Paddle::W,
                    y: screen_h / 2.0 - Paddle::H / 2.0,
                },
            },
            p2: Paddle {
                position: Vec2 {
                    x: screen_w - 2.0 * Paddle::W,
                    y: screen_h / 2.0 - Paddle::H / 2.0,
                },
            },
            ball: Ball {
                position: Vec2 {
                    x: screen_w / 2.0 - Ball::SIDE / 2.0,
                    y: screen_h / 2.0 - Ball::SIDE / 2.0,
                },
                velocity: Vec2::ZERO,
                collision: true,
            },
            p1_score: 0,
            p2_score: 0,
        }
    }
}

fn conf() -> Conf {
    Conf {
        window_title: String::from("Pong"),
        window_width: WINDOW_W,
        window_height: WINDOW_H,
        window_resizable: false,
        ..Default::default()
    }
}

fn update(ctx: &mut Context) {
    let screen_w = screen_width();
    let screen_h = screen_height();
    // Some systems (e.g. Ubuntu WSL on Windows 10) ignore the false window resizable property.
    // Verify that the screen dimensions match the expected window configuration.
    let resized = screen_w != WINDOW_W as f32 || screen_h != WINDOW_H as f32;
    if resized {
        eprintln!("Window was unexpectedly resized! Exiting...");
        std::process::exit(1);
    }

    if is_key_down(KeyCode::Escape) {
        ctx.state = State::Quit;
        return;
    }

    if is_key_down(KeyCode::A) {
        ctx.p1.position.y -= Paddle::SPEED;
    }
    if is_key_down(KeyCode::Z) {
        ctx.p1.position.y += Paddle::SPEED;
    }
    if ctx.p1.position.y < 0.0 {
        ctx.p1.position.y = 0.0;
    }
    if ctx.p1.position.y > screen_h - Paddle::H {
        ctx.p1.position.y = screen_h - Paddle::H;
    }

    if is_key_down(KeyCode::Up) || is_key_down(KeyCode::K) {
        ctx.p2.position.y -= Paddle::SPEED;
    }
    if is_key_down(KeyCode::Down) || is_key_down(KeyCode::J) {
        ctx.p2.position.y += Paddle::SPEED;
    }
    if ctx.p2.position.y < 0.0 {
        ctx.p2.position.y = 0.0;
    }
    if ctx.p2.position.y > screen_h - Paddle::H {
        ctx.p2.position.y = screen_h - Paddle::H;
    }

    if let State::Serve { velocity: v } = ctx.state {
        if !is_key_down(KeyCode::Space) && !is_key_down(KeyCode::Enter) {
            return;
        }
        ctx.ball.velocity = v;
        ctx.state = State::InPlay;
    }

    ctx.ball.position.x += ctx.ball.velocity.x;
    ctx.ball.position.y += ctx.ball.velocity.y;
    let ball_rect = Rect::new(
        ctx.ball.position.x,
        ctx.ball.position.y,
        Ball::SIDE,
        Ball::SIDE,
    );

    let rebound = 30.0f32.to_radians();

    let p1_rect = Rect::new(ctx.p1.position.x, ctx.p1.position.y, Paddle::W, Paddle::H);
    if ctx.ball.collision && ball_rect.overlaps(&p1_rect) {
        let intersect = p1_rect.center().y - ball_rect.center().y;
        let normalized = intersect / (Paddle::H / 2.0);
        let angle = normalized * rebound;
        ctx.ball.velocity.x = Ball::SPEED * angle.cos() * 1.0;
        ctx.ball.velocity.y = Ball::SPEED * angle.sin() * -1.0;
    }

    let p2_rect = Rect::new(ctx.p2.position.x, ctx.p2.position.y, Paddle::W, Paddle::H);
    if ctx.ball.collision && ball_rect.overlaps(&p2_rect) {
        let intersect = p2_rect.center().y - ball_rect.center().y;
        let normalized = intersect / (Paddle::H / 2.0);
        let angle = normalized * rebound;
        ctx.ball.velocity.x = Ball::SPEED * angle.cos() * -1.0;
        ctx.ball.velocity.y = Ball::SPEED * angle.sin() * -1.0;
    }

    ctx.ball.collision = !ball_rect.overlaps(&p1_rect) && !ball_rect.overlaps(&p2_rect);

    if ctx.ball.position.y <= 0.0 || ctx.ball.position.y >= screen_h - Ball::SIDE {
        ctx.ball.velocity.y = -ctx.ball.velocity.y;
    }

    if ctx.ball.position.x + Ball::SIDE < 0.0 {
        ctx.ball.position.x = screen_w / 2.0;
        ctx.ball.position.y = screen_h / 2.0;
        ctx.ball.velocity = Vec2::ZERO;
        ctx.p2_score += 1;
        ctx.state = State::Serve {
            velocity: Vec2 {
                x: Ball::SPEED,
                y: 0.0,
            },
        };
    }
    if ctx.ball.position.x >= screen_w {
        ctx.ball.position.x = screen_w / 2.0;
        ctx.ball.position.y = screen_h / 2.0;
        ctx.ball.velocity = Vec2::ZERO;
        ctx.p1_score += 1;
        ctx.state = State::Serve {
            velocity: Vec2 {
                x: -Ball::SPEED,
                y: 0.0,
            },
        };
    }
}

fn render(ctx: &Context, interpolation: f32) {
    assert!(0.0 <= interpolation || interpolation <= 1.0);
    clear_background(BLACK);

    draw_rectangle(
        ctx.p1.position.x,
        ctx.p1.position.y,
        Paddle::W,
        Paddle::H,
        WHITE,
    );
    draw_rectangle(
        ctx.p2.position.x,
        ctx.p2.position.y,
        Paddle::W,
        Paddle::H,
        WHITE,
    );
    draw_rectangle(
        ctx.ball.position.x + ctx.ball.velocity.x * interpolation,
        ctx.ball.position.y + ctx.ball.velocity.y * interpolation,
        Ball::SIDE,
        Ball::SIDE,
        WHITE,
    );

    let font_size: u16 = 16;
    let text = format!("FPS: {}", get_fps());
    let size = measure_text(text.as_str(), None, font_size, 1.0);
    draw_text(text.as_str(), 2.0, 2.0 + size.height, font_size as f32, RED);

    let screen_w = screen_width();
    let screen_h = screen_height();

    const SCORE_OFFSET_X: f32 = 50.0;
    const SCORE_OFFSET_Y: f32 = 10.0;
    let font_size: u16 = 128;
    let text = format!("{}", ctx.p1_score);
    let size = measure_text(text.as_str(), None, font_size, 1.0);
    draw_text(
        text.as_str(),
        screen_w * 0.5 - size.width - SCORE_OFFSET_X,
        SCORE_OFFSET_Y + size.height,
        font_size as f32,
        WHITE,
    );
    let text = format!("{}", ctx.p2_score);
    let size = measure_text(text.as_str(), None, font_size, 1.0);
    draw_text(
        text.as_str(),
        screen_w * 0.5 + SCORE_OFFSET_X,
        SCORE_OFFSET_Y + size.height,
        font_size as f32,
        WHITE,
    );

    if let State::Serve { velocity: _ } = &ctx.state {
        let font_size: u16 = 64;
        let text = &"PRESS SPACE";
        let size = measure_text(text, None, font_size, 1.0);
        draw_text(
            text,
            screen_w * 0.5 - size.width * 0.5,
            screen_h * 0.5 - size.height * 0.5,
            font_size as f32,
            WHITE,
        );
    }
}

#[macroquad::main(conf)]
async fn main() {
    let mut ctx = Context::new(screen_width(), screen_height());

    let mut time = get_time();
    let mut accumulator = 0.0;
    loop {
        let now = get_time();
        let elapsed = now - time;
        time = now;

        accumulator += elapsed;

        while accumulator > TIMESTEP {
            update(&mut ctx);
            accumulator -= TIMESTEP;
        }

        render(&ctx, (accumulator / TIMESTEP) as f32);
        match ctx.state {
            State::Quit => return,
            _ => next_frame().await,
        }
    }
}
