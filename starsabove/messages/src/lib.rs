pub mod messages;
pub mod route;

use std::{error::Error, fmt};

#[derive(Debug)]
pub struct Shutdown;
impl Error for Shutdown {} 
impl fmt::Display for Shutdown {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Client Shutdown")
    }
}

