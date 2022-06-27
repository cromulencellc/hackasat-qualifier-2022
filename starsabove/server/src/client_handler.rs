use std::thread;
use std::net::{TcpStream, TcpListener};
use std::sync::{Arc, Mutex};
use std::sync::mpsc::{SyncSender};
use debug_print::{debug_println}; 

use std::collections::HashMap;

use messages::{Shutdown, messages::{Message, MessageBody}};

pub fn accept_connections(listener: &TcpListener, clients_mutex:Arc<Mutex<HashMap<u16, TcpStream>>>, message_router:SyncSender<Message>) { 

    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                if let Ok(_addr) = stream.peer_addr() { 
                    debug_println!("New connection: {}", _addr);
                } else {
                    debug_println!("Unknown Client Connected");
                }

                if let Ok(Some(msg)) = Message::recv(&stream) {
                    
                    if let MessageBody::Hello(sat_id) = &msg.body { 
                        let mut clients = clients_mutex.lock().expect("Couldn't get Mutex");
                        let stream_clone = stream.try_clone().expect("Could not clone TCP Socket");
                        clients.insert(*sat_id, stream_clone);
                    } else {
                        debug_println!("Unknown Message body, dropped, {:?}", msg);
                    }
                } else { 
                    debug_println!("Failed to receive from new client!")
                }

                let router_copy =  message_router.clone();
                thread::spawn(move|| {
                    // connection succeeded
                    handle_client(stream, router_copy)
                });
            }
            Err(_e) => {
                debug_println!("Error: {}", _e);
                /* connection failed */
            }
        }
    }
}    

fn handle_client(stream: TcpStream, msg_router: SyncSender<Message>) {
    loop { 
        if let Some(msg) = match Message::recv(&stream) { 
                Ok(result) => result,
                Err(Shutdown) => break
        } {
            if msg_router.send(msg).is_err() { 
                break;
            }
        } 
    }
}