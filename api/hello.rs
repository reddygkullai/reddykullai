use std::io::Write;

fn main() {
    let mut stdout = std::io::stdout();
    write!(stdout, "Hello from Rust on Vercel!").unwrap();
}
