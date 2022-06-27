use std::io;
use std::{net::TcpStream};
use serde::{Serialize,Deserialize};

use crate::Shutdown;
use crate::route::{Route};

#[derive(Serialize,Deserialize,Debug,PartialEq,Clone)]
pub enum MessageBody {
    Hello(u16),
    NetworkCheckReq(u16),             // The ID of the return address
    NetworkCheckAck(u16),             // The ID of the responder
    SendFlag,
    Flag(String),
    DetourReq(u16, u16)
}

#[derive(Serialize,Deserialize,Debug,PartialEq,Clone)]
pub struct Message {
    pub route: Route,
    pub body : MessageBody
}

impl Message { 

    pub fn new_hello(sat_id: u16) ->  Message {
        Message { 
            route: Route::new(sat_id, 0),
            body: MessageBody::Hello(sat_id)
        }
    }

    pub fn new_network_check_msg(src:u16, dst:u16) -> Message {
        Message { 
            route: Route::full_route(src, dst),
            body: MessageBody::NetworkCheckReq( src )
        }
    }
    
    pub fn new_network_check_response_msg(src:u16, dst:u16) -> Message {
        Message { 
            route: Route::full_route(src, dst),
            body: MessageBody::NetworkCheckAck( src )
        }
    }
}

impl Message {
    pub fn send(&self, stream: &TcpStream) {
        bincode::serialize_into(stream, &self).expect("failed to write");
    }
    
    pub fn recv(stream: &TcpStream) -> Result<Option<Message>,Shutdown>{
        match bincode::deserialize_from(stream) {
            Ok(msg) => Ok(Some(msg)),
            Err(e) => match *e {
                bincode::ErrorKind::Io(ref e2) => match e2.kind() {
                    io::ErrorKind::WouldBlock =>  Ok(None),
                    io::ErrorKind::UnexpectedEof => Err(Shutdown),
                    _ => panic!("Unhandled IO Error")
                }
                _ => panic!("Unhandled bincode Error")
            }
        }
    }
    
    pub fn to_bytes(&self) -> Vec<u8> {
        match bincode::serialize(self) { 
            Ok(bytes) => bytes,
            Err(_) => panic!("Couldn't pack into bytes")
        }
    }
    pub fn from_bytes(bytes: Vec<u8>) -> Option<Message> { 
        match bincode::deserialize(&bytes) { 
            Ok(msg) => Some(msg),
            Err(_) => None
        }
    }

    pub fn get_src(&self) -> u16 {
        self.route.src
    }
    pub fn get_next_dst(&self) -> Option<u16> {
        self.route.dst.get(0).copied()
    }

    pub fn validate_recv_id(&self, id:u16) -> bool { 
        if self.route.dst.is_empty() { 
            false
        } else {
            id == *self.route.dst.get(0).unwrap()
        }
    }

    pub fn validate_send_id(&self, id:u16) -> bool { 
        id == self.route.src
    }

    pub fn at_destination(&self) -> bool { 
        self.route.dst.len() == 1
    }

    pub fn forward(&mut self) -> u16 { 
        if self.route.dst.is_empty() {
            panic!("No where left to send the message")
        }
        self.route.src = self.route.dst.remove(0);
        self.get_next_dst().unwrap() 
    }

    pub fn reroute(&mut self, detour:u16) {
        if self.route.dst.is_empty() { 
            panic!("Cannot reroute, route list is empty");
        }
        self.route.dst.insert(0, detour);
    }
}
