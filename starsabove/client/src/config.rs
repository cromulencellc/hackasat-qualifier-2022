use std::env; 
#[derive(Clone)]
pub struct Config {
    pub server: String,
    pub flag: String,
    pub sat_id: u16,
    pub flag_dst: u16
}

pub fn get_config() -> Config {
    let server = match env::var("SERVER") { 
        Ok(addr) => addr,
        Err(_) => String::from("localhost:31337")
    };
    
    let flag = match env::var("FLAG") { 
        Ok(flag) => flag,
        Err(_) => String::from("FLAG{Sorry, your flag is on another satallite...}")
    };


    let sat_id:u16 = env::args().nth(1)
                        .expect("Missing Commandline Arg")
                        .parse().expect("Invalid Satellite Number");

    let flag_dst:u16 = env::args().nth(2)
                        .expect("Missing Commandline Arg")
                        .parse().expect("Invalid Satellite Number");
                        
    Config {
        server, 
        flag, 
        sat_id,
        flag_dst
    }
}

