fn fizzbuzz_loop(count: usize) {
    for n in 1..count+1 {
        if n % 3 == 0 && n % 5 == 0 {
            println!("fizzbuzz");
        } else if n % 3 == 0 {
            println!("fizz");
        } else if n % 5 == 0 {
            println!("buzz");
        } else {
            println!("{n}");
        }
    }
}

fn fizzbuzz_iter(count: usize) {
    (1..count+1).for_each(|n| {
        if n % 3 == 0 && n % 5 == 0 {
            println!("fizzbuzz");
        } else if n % 3 == 0 {
            println!("fizz");
        } else if n % 5 == 0 {
            println!("buzz");
        } else {
            println!("{n}");
        }
    });
}

fn fizzbuzz_iter_match(count: usize) {
    (1..count+1).for_each(|n| {
        match (n % 3 == 0, n % 5 == 0) {
            (false, false) => println!("{n}"),
            (true, false) => println!("fizz"),
            (false, true) => println!("buzz"),
            (true, true) => println!("fizzbuzz"),
        }
    });
}

fn main() {
    println!("for loop:");
    fizzbuzz_loop(20);
    println!("");
    println!("iterator:");
    fizzbuzz_iter(20);
    println!("");
    println!("iterator with match:");
    fizzbuzz_iter_match(20);
}
