use serde::{Serialize,Deserialize};
use routelib::get_route; 

#[derive(Serialize,Deserialize,PartialEq,Debug,Clone)]
pub struct Route { 
    pub src: u16,
    pub dst: Vec<u16>
}
impl Route {
    pub fn new(src:u16, dst:u16) -> Route { 
        Route { src, dst: vec![dst]}
    }
    pub fn from_vec(src:u16, dst:Vec<u16>) -> Route{ 
        Route {src, dst}
    }
    pub fn full_route(src:u16, dst:u16) -> Route {
        match get_route(src, dst){
            Ok(route) => Route {src, dst: route},
            Err(_) => Route {src, dst: vec![99]}
        }
    }
}

#[derive(Serialize, Deserialize, Clone, Copy)]
pub struct Detour {
    pub original: u16,
    pub reroute : u16
}
