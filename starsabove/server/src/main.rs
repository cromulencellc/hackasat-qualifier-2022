use std::collections::HashMap;
use std::thread;
use std::net::{TcpListener, TcpStream};
use std::sync::{Arc, Mutex};
use std::sync::mpsc::sync_channel;
use debug_print::debug_println; 

use messages::messages::{Message};

use server::router::router;
use server::client_handler::accept_connections; 
use server::config::get_config; 

fn main() {

    let config = get_config();
    let listener = TcpListener::bind(&config.server).unwrap();

    // accept connections and process them, spawning a new thread for each one
    debug_println!("Server 1 listening on port {}", config.server);
    
    let (route_req, route_queue) = sync_channel::<Message>(32);
    let clients_mtx:Arc<Mutex<HashMap<u16,TcpStream>>> = Arc::new(Mutex::new(HashMap::new()));
    let clients_mtx_clone = Arc::clone(&clients_mtx);
    
    thread::spawn(move || { 
        router(route_queue, clients_mtx);
    });

    accept_connections(&listener, clients_mtx_clone, route_req);

    // close the socket server
    drop(listener);
}


#[cfg(test)]
mod tests { 
    use super::*;
    use net2::{TcpBuilder, unix::UnixTcpBuilderExt}; 
    use std::net::TcpStream; 

    #[test]
    fn try_clients() {
        
        let listener = TcpBuilder::new_v4().unwrap()
                                .reuse_address(true).unwrap()
                                .reuse_port(true).unwrap()
                                .bind("0.0.0.0:2222").expect("Could not bind address")
                                .listen(32).unwrap();

        let (route_req, route_queue) = sync_channel::<Message>(32);
        
        let clients_mtx:Arc<Mutex<HashMap<u16,TcpStream>>> = Arc::new(Mutex::new(HashMap::new()));
        let clients_mtx_clone = Arc::clone(&clients_mtx);

        let _t1 = thread::spawn(move || { 
            router(route_queue, clients_mtx);
        });
    
        let _t2 = thread::spawn(move || {
            accept_connections(&listener, clients_mtx_clone, route_req);
        });

        struct Client{
            id: u16,
            stream: TcpStream
        }

        let mut clients:Vec<Client> = Vec::new();
        for client_id in 1..=12 { 
            let client = Client { 
                id:client_id, 
                stream:TcpStream::connect("localhost:2222").unwrap() 
            };
            let msg = Message::new_hello(client.id);
            msg.send(&client.stream);  

            clients.push(client);
        }
        
        for client_id in vec![20u16,30u16,40u16,50u16,0u16].iter() { 
            let client = Client { 
                id:*client_id, 
                stream:TcpStream::connect("localhost:2222").unwrap() 
            };
            let msg = Message::new_hello(client.id);
            msg.send(&client.stream);  

            clients.push(client);
        }

        thread::sleep(std::time::Duration::from_millis(100));

        for (c1,c2) in vec![(1,2),(3,20), (20,0)].iter() {
            let client1 = clients.iter().find(|c| c.id == *c1).unwrap();
            let client2 = clients.iter().find(|c| c.id == *c2).unwrap();

            let msg = Message::new_network_check_msg(client1.id, client2.id);
            msg.send(&client1.stream);

            match Message::recv(&client2.stream) {
                Ok(Some(msg2)) => {

                    assert_eq!(msg, msg2)
                },
                _ => panic!("Didn't get message back")
            };

        }
    }
}