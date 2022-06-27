
use std::collections::HashMap;

use std::net::TcpStream;
use std::sync::mpsc::Receiver;
use std::sync::{Arc, Mutex};

use debug_print::{debug_println}; 

use messages::route::Detour;
use routelib::can_reach;
use messages::messages::{Message, MessageBody};
use client::comms::validate_message;

pub fn router(route_queue: Receiver<Message>, clients_mutex:Arc<Mutex<HashMap<u16, TcpStream>>>) {        
    let mut faker = Faker::new(); 
    loop { 
        if let Ok(mut msg) = route_queue.recv() { 
            if let Some(dst_id) = msg.get_next_dst() {
                // Lock the clients to find the postbox
                let clients = clients_mutex.lock().unwrap();
                if !can_reach(msg.get_src(), dst_id) {
                    println!("Message dropped by 'physics'...");
                    if let MessageBody::NetworkCheckReq(resp_id) =  msg.body {
                        if let Some(stream) = clients.get(&dst_id) { 
                            Message::new_network_check_response_msg(99, resp_id).send(stream);
                        }
                    }
                } else if let Some(stream) = clients.get(&dst_id) { 
                    msg.send(stream);
                } else {
                    loop { 
                        msg = if let Some(next_msg) = faker.route(msg) {
                            let dst_id = next_msg.get_next_dst().unwrap();
                            debug_println!("Fake Forwarding: {:?}", next_msg);
                            if !can_reach(next_msg.get_src(), dst_id) {
                                debug_println!("Faker Dropping Message due to physics {:?}", next_msg);
                                break;
                            } else if let Some(stream) = clients.get(&dst_id) { 
                                debug_println!("Found real client to send to: {}", dst_id);
                                next_msg.send(stream);
                                break;
                            } 
                            next_msg
                        } else {
                            break;
                        };
                    }
                } 
            }
        } else {
            debug_println!("Route Queue disconnected, dying");
            break;
        }
    }
}

struct Faker {
    detours: HashMap<u16, Vec<Detour>>
}
impl Faker { 
    pub fn new() -> Faker {
        Faker {detours: HashMap::new()}
    }

    pub fn route(&mut self, msg: Message) -> Option<Message>{ 
        let curr_id = msg.get_next_dst().unwrap();

        match validate_message(curr_id, msg) {
            Some((msg, true)) => {
                self.handle_message(msg)
            }, 
            Some((mut msg, false)) => { 
                let next_sat_id = msg.forward();

                if let Some(detours) = self.detours.get(&curr_id) { 
                    if let Some(&r) = detours.iter().find(|detour| detour.original == next_sat_id) {
                        msg.reroute(r.reroute);
                    }
                } 
                
                // Send the message to the next guy!
                Some(msg)
            },
            None => None
        }
    }

    fn handle_message(&mut self, msg:Message) -> Option<Message> {
        debug_println!("Fake Handling: {:?}", msg);
        let sat_id = msg.get_next_dst().unwrap(); 

        match msg.body {
            MessageBody::NetworkCheckReq(return_addr) => { 
                Some(Message::new_network_check_response_msg(sat_id, return_addr))
            },
            MessageBody::DetourReq(original,reroute) => {
                debug_println!("Registering Detour for {}:  {}->{}", sat_id, original, reroute);
                if let Some(detours) = self.detours.get_mut(&sat_id) {
                    detours.push(Detour { original, reroute});
                } else { 
                    self.detours.insert(sat_id, vec![Detour {original, reroute}]);
                }
                None
            },
            _ => None
        } 
    }
}

// #[cfg(test)]
// mod tests { 
//     use super::*;
//     use std::thread;
//     use std::sync::mpsc::sync_channel;
//     use messages::route::{Route};

    // #[test]
    // fn try_router() {
    //     let (route_req, route_queue) = sync_channel::<Message>(32);
        
    //     let clients_mtx:Arc<Mutex<HashMap<u16,TcpStream>>> = Arc::new(Mutex::new(HashMap::new()));
    //     let clients_mtx_clone = Arc::clone(&clients_mtx);

    //     thread::spawn(move || { 
    //         router(route_queue, clients_mtx_clone);
    //     });
    
    //     let (tx1, rx1) = sync_channel::<Message>(0);
    //     let (tx2, rx2) = sync_channel::<Message>(0);

    //     {
    //         let mut clients = clients_mtx.lock().unwrap();
    //         clients.insert(1, tx1);
    //         clients.insert(2, tx2);
    //     }

    //     let msg1 = Message::new_network_check_msg(2,1);
    //     route_req.send(msg1).expect("Couldn't send to router");

    //     let msg2 = rx1.recv().unwrap();
    //     assert_eq!(Message::new_network_check_msg(2,1),msg2);        

    //     let msg1 = Message::new_network_check_msg(1,2);
    //     route_req.send(msg1).expect("Couldn't send to router");

    //     let msg2 = rx2.recv().unwrap();
    //     assert_eq!(Message::new_network_check_msg(1,2),msg2);
    // }
    // #[test]
    // fn try_fakers() { 
    //     let (route_req, route_queue) = sync_channel::<Message>(32);
        
    //     let clients_mtx:Arc<Mutex<HashMap<u16,SyncSender<Message>>>> = Arc::new(Mutex::new(HashMap::new()));
    //     let clients_mtx_clone = Arc::clone(&clients_mtx);

    //     thread::spawn(move || { 
    //         router(route_queue, clients_mtx_clone);
    //     });
    
    //     let (tx1, rx1) = sync_channel::<Message>(0);
    //     let (tx2, rx2) = sync_channel::<Message>(0);

    //     {
    //         let mut clients = clients_mtx.lock().unwrap();
    //         clients.insert(1, tx1);
    //         clients.insert(3, tx2);
    //     }

    //     let msg1 = Message::new_network_check_msg(3,1);
    //     route_req.send(msg1).expect("Couldn't send to router");

    //     let msg2 = rx1.recv().unwrap();
    //     assert_eq!(msg2, Message { 
    //         route: Route::new(20,1),
    //         body : MessageBody::NetworkCheckReq(3)
    //     });        

    //     let msg1 = Message::new_network_check_msg(1,3);
    //     route_req.send(msg1).expect("Couldn't send to router");

    //     let msg2 = rx2.recv().unwrap();
    //     assert_eq!(msg2, Message { 
    //         route: Route::new(20,3),
    //         body : MessageBody::NetworkCheckReq(1)
    //     });

    //     let msg3 = Message::new_network_check_msg(1, 9);
    //     route_req.send(msg3).expect("Failed to send message");
 
    //     let msg4 = rx1.recv().unwrap();
    //     assert_eq!(msg4, Message { 
    //         route: Route::new(20,1),
    //         body : MessageBody::NetworkCheckAck(9)
    //     }); 
    // }

    // #[test]
    // fn try_fakers_detour() { 
    //     let (route_req, route_queue) = sync_channel::<Message>(32);
        
    //     let clients_mtx:Arc<Mutex<HashMap<u16,TcpStream>>> = Arc::new(Mutex::new(HashMap::new()));
    //     let clients_mtx_clone = Arc::clone(&clients_mtx);

    //     thread::spawn(move || { 
    //         router(route_queue, clients_mtx_clone);
    //     });
    
    //     let (tx1, rx1) = sync_channel::<Message>(0);
    //     {
    //         let mut clients = clients_mtx.lock().unwrap();
    //         clients.insert(1, tx1);
    //     }

    //     route_req.send(Message { 
    //         route: Route::full_route(1, 20),
    //         body : MessageBody::DetourReq(3, 2)
    //     }).expect("Failed to send");

    //     let msg1 = Message::new_network_check_msg(1,3);
    //     route_req.send(msg1).expect("Couldn't send to router");

    //     let msg2 = rx1.recv().unwrap();
    //     assert_eq!(msg2, Message { 
    //         route: Route::new(20,1),
    //         body : MessageBody::NetworkCheckAck(3)
    //     }); 
    // }
// }
