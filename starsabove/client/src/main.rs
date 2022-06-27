use std::io::BufRead;
use std::net::{Shutdown,TcpStream};
use std::thread;
use std::sync::mpsc::sync_channel;
use hex::{FromHex};

use messages::messages::Message;

mod comms;
use comms::CommManager;

mod config;
use config::{get_config,Config};


fn chomp(s: &mut String) { 
    if s.ends_with('\n') {
        s.pop();
        if s.ends_with('\r') {
            s.pop();
        }
    }
}

fn main() {
    let config:Config = get_config();
    thread::sleep(std::time::Duration::from_millis(1000));

    let stream = TcpStream::connect(config.server).expect("Failed to connect to 'space'"); 
        
    let stream_clone = stream.try_clone().expect("Could not clone");

    if config.sat_id != 5 {
        thread::spawn(|| {
            let config = get_config();
            let mut mgr = CommManager::new(config.sat_id, stream_clone, None);
            mgr.start_communication();
        }).join().expect("Could not wait for message");

    } else { 
        let (spy_tx, spy_rx) = sync_channel::<Message>(1);
    
        let _t1 = thread::spawn(|| {
            let config = get_config();
            let mut mgr = CommManager::new(config.sat_id, stream_clone, Some(spy_tx));
            mgr.start_communication();
        });

        println!("Successfully connected to 'space'");

        thread::spawn(move || loop {
            if let Ok(msg) = spy_rx.try_recv() { 
                println!("{:?}", msg);
            }
            thread::sleep(std::time::Duration::from_millis(100));
        });

        // debug_messages()

        for line in std::io::stdin().lock().lines() {
            match line  {
                Ok(mut line) => { 
                        chomp(&mut line);                    
                        if let Ok(bytes) = Vec::from_hex(&line) {
                            if let Some(msg) = Message::from_bytes(bytes) {
                                println!("Sending message {:?}", msg);
                                msg.send(&stream);
                                thread::sleep(std::time::Duration::from_millis(500));
                            } else { 
                                println!("Couldn't decode message from hex...");
                            }
                        } else { 
                            println!("Encountered Non-Hex string, dropping...");
                        }
                }
                Err(_) => break
                
            }
        }
        stream.shutdown(Shutdown::Both).expect("Couldn't shutdown stream");
        println!("Terminated.");    
    }
}

// use hex::ToHex;
// use messages::{route::Route, messages::MessageBody};
// fn debug_messages(stream: &TcpStream) {
//        thread::sleep(std::time::Duration::from_millis(2000));
//         let msg = Message { 
//             route: Route { src:5, dst:vec![30,5]},
//             body : MessageBody::DetourReq(0, 30)
//         };
//         println!("Route: {}", msg.to_bytes().encode_hex::<String>());
//         for (targ, orig, reroute) in [(3,0,4),(20,0,3),(4,0,5)] { 
//             let msg = Message { 
//                 route: Route::full_route(5, targ),
//                 body : MessageBody::DetourReq(orig, reroute)
//             };
//             println!("Route: {}", msg.to_bytes().encode_hex::<String>());
//             msg.send(&stream);
//             thread::sleep(std::time::Duration::from_millis(1000));
//         }

//         let msg = Message {
//             route: Route::full_route(5, 2),
//             body : MessageBody::SendFlag
//         };
//         println!("Send Flag: {}", msg.to_bytes().encode_hex::<String>());
//         msg.send(&stream); 

//         let msg = Message::new_network_check_msg(5,6);
//         println!("Network Check: {}", msg.to_bytes().encode_hex::<String>());
//         msg.send(&stream); 
// }