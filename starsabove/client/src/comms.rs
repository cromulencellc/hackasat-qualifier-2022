use std::{net::TcpStream};
use std::sync::mpsc::SyncSender;
use messages::messages::{Message, MessageBody};
use messages::route::{Route, Detour};
use debug_print::debug_println;

use crate::config::get_config;

pub struct CommManager {
    sat_id  : u16,
    stream  : TcpStream,
    detours : Vec<Detour>,
    spy     : Option<SyncSender<Message>>
}

impl CommManager {
    pub fn new(sat_id: u16, stream: TcpStream, spy:Option<SyncSender<Message>>) -> CommManager {
        CommManager { sat_id, stream, detours: Vec::new(), spy }
    }

    pub fn start_communication(&mut self) {
        // Say hello so the server knows who we are
        Message::new_hello(self.sat_id).send(&self.stream);

        loop {
            if let Some(msg) = match Message::recv(&self.stream) {
                Ok(result) => result,
                Err(_) => break
            } {
                if let Some(spy) = &self.spy {
                    _ = spy.send(msg.clone());
                }
                match validate_message(self.sat_id, msg) {
                    Some((msg, true)) => {
                        // Is this the final destination of the packet?
                        if let Some(msg) = self.handle_message(msg) {
                            msg.send(&self.stream);
                        }
                    },
                    Some((mut msg, false)) => {
                        // Nope! Forward it along then!
                        let next_sat_id = msg.forward();

                        if let Some(&r) = self.detours.iter().find(|detour| detour.original == next_sat_id) {
                            msg.reroute(r.reroute);
                        }

                        // Send the message to the next guy!
                        msg.send(&self.stream);
                    },
                    None => continue
                }
            }
        }
        debug_println!("Shutdown")
    }

    fn handle_message(&mut self, msg:Message) -> Option<Message> {
        debug_println!("Handling: {:?}", msg);
        match msg.body {
            MessageBody::NetworkCheckReq(return_addr) => {
                Some(Message::new_network_check_response_msg(self.sat_id, return_addr))
            },
            MessageBody::DetourReq(original,reroute) => {
                self.detours.push(Detour { original, reroute});
                None
            },
            MessageBody::Flag(_flag) => { 
                debug_println!("Got Flag {_flag}");
                None
            },
            MessageBody::SendFlag => {
                if !self.network_check() {
                    println!("Sat_{}: Network Check Failed! Goodbye...", self.sat_id);
                    None
                } else {
                    let config = get_config();
                    println!("Sat_{}: Network Check Succeeded! Sending Flag to {}...", self.sat_id, config.flag_dst);

                    Some(Message {
                        route: Route::full_route(self.sat_id, config.flag_dst),
                        body: MessageBody::Flag(config.flag)
                    })
                }
            }
            _ => None
        }
    }

    fn network_check(&self) -> bool {
        println!("Sat_{}: Starting Network Check...", self.sat_id);

        for target_id in 1..=12 {
            if target_id == self.sat_id {
                continue;
            }
            if !self.send_and_recv_network_check(target_id) {
                println!("Sat_{}: Network Check Failed! Goodbye...", self.sat_id);
            }
        }
        true
    }

    fn send_and_recv_network_check(&self, target_id: u16) -> bool {
        Message::new_network_check_msg(self.sat_id, target_id).send(&self.stream);
        std::thread::sleep(std::time::Duration::from_millis(50));
        match Message::recv(&self.stream)
        {
            Ok(Some(msg)) => {
                if let MessageBody::NetworkCheckAck(resp_id) = msg.body {
                    resp_id == target_id
                }
                else {
                    false
                }
            },
            _ => {
                false
            }
        }
    }
}



pub fn validate_message(sat_id: u16, msg: Message) -> Option<(Message,bool)> {
    // Were we supposed to get this message?
    if !msg.validate_recv_id(sat_id) {
        debug_println!("Bad Route, {:?}, dropping", msg);
        None
    }
    else {
        let at_destination = msg.at_destination();
        Some((msg, at_destination))
    }
}

#[cfg(test)]
mod test {
    use super::*;
    use std::thread;
    use net2::{TcpBuilder, unix::UnixTcpBuilderExt};
    use messages::{route::Route, messages::MessageBody};

    #[test]
    fn test_forward() {
        let listener = TcpBuilder::new_v4().unwrap()
                            .reuse_address(true).unwrap()
                            .reuse_port(true).unwrap()
                            .bind("0.0.0.0:1111").expect("Could not bind address")
                            .listen(32).unwrap();

        let t1 = thread::spawn(move || {
            for stream in listener.incoming() {
                match stream {
                    Ok(stream) => {
                        if Message::recv(&stream).expect("Didn't receive").is_some() {
                            println!("Got Hello, carry on...");
                        } else {
                            panic!("Didn't get hello");
                        }

                        let msg = Message {
                            route: Route { src: 0, dst: vec![1,2]},
                            body: MessageBody::Hello(0)
                        };

                        // Send the forwardable packet
                        msg.send(&stream);

                        if let Some(msg2) = Message::recv(&stream).expect("Didn't receive") {
                            assert_eq!(msg2, Message {
                                route: Route { src: 1, dst: vec![2]},
                                body: MessageBody::Hello(0)
                            });
                        } else {
                            panic!("Didn't get a message");
                        }
                        break;
                    },
                    _ => {
                        panic!("Bad connect");
                    }
                }
            }
        });


        let _t2 = thread::spawn(move || {
            let stream = TcpStream::connect("localhost:1111").unwrap();
            let mut mgr = CommManager::new(1, stream, None);
            mgr.start_communication();
        });

        t1.join().unwrap();
    }

    #[test]
    fn test_channel() {
        let listener = TcpBuilder::new_v4().unwrap()
                            .reuse_address(true).unwrap()
                            .reuse_port(true).unwrap()
                            .bind("0.0.0.0:1112").expect("Could not bind address")
                            .listen(32).unwrap();

        let t1 = thread::spawn(move || {
            for stream in listener.incoming() {
                match stream {
                    Ok(stream) => {
                        if Message::recv(&stream).expect("Didn't receive").is_some() {
                            println!("Got Hello, carry on...");
                        } else {
                            panic!("Didn't get hello");
                        }

                        // Send the forwardable packet

                        if let Some(msg2) = Message::recv(&stream).expect("Didn't receive") {
                            assert_eq!(msg2, Message {
                                route: Route { src: 1, dst: vec![2]},
                                body: MessageBody::Hello(0)
                            });
                        } else {
                            panic!("Didn't get a message");
                        }
                        break;
                    },
                    _ => {
                        panic!("Bad connect");
                    }
                }
            }
        });

        let stream = TcpStream::connect("localhost:1112").unwrap();
        let stream_clone = stream.try_clone().expect("Could not clone");

        let _t2 = thread::spawn(move || {
            let mut mgr = CommManager::new(1, stream_clone, None);
            mgr.start_communication();
        });

        thread::sleep(std::time::Duration::from_millis(100));
        Message {
            route: Route { src: 1, dst: vec![2]},
            body: MessageBody::Hello(0)
        }.send(&stream);

        t1.join().unwrap();
    }

    #[test]
    fn test_network_check() {
        let listener = TcpBuilder::new_v4().unwrap()
                            .reuse_address(true).unwrap()
                            .reuse_port(true).unwrap()
                            .bind("0.0.0.0:1113").expect("Could not bind address")
                            .listen(32).unwrap();

        let t1 = thread::spawn(move || {
            for stream in listener.incoming() {
                match stream {
                    Ok(stream) => {
                        if Message::recv(&stream).expect("Didn't receive").is_some() {
                            println!("Got Hello, carry on...");
                        } else {
                            panic!("Didn't get hello");
                        }

                        // Send the Network check request packet
                        Message::new_network_check_msg(2, 1).send(&stream);

                        if let Some(msg2) = Message::recv(&stream).expect("Didn't receive") {
                            assert_eq!(msg2, Message {
                                route: Route { src: 1, dst: vec![2]},
                                body: MessageBody::NetworkCheckAck(1)
                            });
                        } else {
                            panic!("Didn't get a message");
                        }
                        break;
                    },
                    _ => {
                        panic!("Bad connect");
                    }
                }
            }
        });

        let _t2 = thread::spawn(move || {
            let stream = TcpStream::connect("localhost:1113").unwrap();
            let mut mgr = CommManager::new(1, stream, None);
            mgr.start_communication();
        });

        t1.join().unwrap();
    }
}