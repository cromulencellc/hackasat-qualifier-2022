use std::env;
use std::process;
use once_unop_a_dijkstar::Args;

fn main() {
    // Read in the std arguments
    let args: Vec<String> = env::args().collect();
    let parsed_args = Args::new(&args).unwrap_or_else(|err| {
        println!("Problem parsing arguments: {}", err);
        process::exit(1);
    });

    unsafe {
        if let Err(e) = once_unop_a_dijkstar::run(parsed_args) {
            println!("Error: {}", e);

            process::exit(1);
        }
    }

}

