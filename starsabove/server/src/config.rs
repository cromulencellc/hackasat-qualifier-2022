use std::env; 
#[derive(Clone)]
pub struct Config {
    pub server: String,
    pub flag: String,
    pub src_id: u16,
    pub dst_id: u16
}

pub fn get_config() -> Config {
    let server = match env::var("SERVER") { 
        Ok(addr) => addr,
        Err(_) => String::from("0.0.0.0:31337")
    };
    
    let flag = match env::var("FLAG") { 
        Ok(flag) => flag,
        Err(_) => String::from("FLAG{Test_Flag}")
    };

    let mut cmd_args = env::args();
    let src_id:u16 = match cmd_args.nth(1) {
        Some(src_id) => src_id.parse().unwrap_or(2),
        None => 2
    };

    let dst_id:u16 = match cmd_args.next() {
        Some(dst_id) => dst_id.parse().unwrap_or(8),
        None => 8
    };

    Config {
        server, 
        flag, 
        src_id, 
        dst_id
    }
}

