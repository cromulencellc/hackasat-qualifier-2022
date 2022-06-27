
#[cfg(test)]
mod tests { 
    use std::collections::HashMap;
    use client::comms::CommManager;
    use net2::{TcpBuilder, unix::UnixTcpBuilderExt}; 
    use std::net::TcpStream;

    use std::thread;
    use std::sync::{Arc, Mutex, mpsc::sync_channel};

    use server::router::router;
    use server::client_handler::accept_connections;
    
    use messages::{route::Route, messages::{Message, MessageBody}};

    #[test]
    fn test_comms() {
        // Setup Server
        let listener = TcpBuilder::new_v4().unwrap()
                                    .reuse_address(true).unwrap()
                                    .reuse_port(true).unwrap()
                                    .bind("0.0.0.0:3333").expect("Could not bind address")
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

        let _t3 = thread::spawn(move || {
            let sat_id = 1;
            let stream = TcpStream::connect("localhost:3333").unwrap();
            Message::new_hello(sat_id).send(&stream);
            thread::sleep(std::time::Duration::from_millis(100));

            Message::new_network_check_msg(sat_id, 2).send(&stream);
        });

        let t4 = thread::spawn(move || {
            let sat_id = 2 ;
            let stream = TcpStream::connect("localhost:3333").unwrap();
            Message::new_hello(sat_id).send(&stream);
            let msg = Message::recv(&stream).expect("Failed to receieve").unwrap();
            assert_eq!(msg, 
                Message::new_network_check_msg(1, 2));
        });

        t4.join().unwrap();
    }

    #[test]
    fn test_comms_routing() {
        // Setup Server
        let listener = TcpBuilder::new_v4().unwrap()
                                    .reuse_address(true).unwrap()
                                    .reuse_port(true).unwrap()
                                    .bind("0.0.0.0:3334").expect("Could not bind address")
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

        let _sat1 = thread::spawn(move || {
            let sat_id = 1;
            let stream = TcpStream::connect("localhost:3334").unwrap();
            Message::new_hello(sat_id).send(&stream);
            thread::sleep(std::time::Duration::from_millis(100));

            Message::new_network_check_msg(sat_id, 3).send(&stream);
        });

        let _sat20 = thread::spawn(move || {
            let sat_id = 20;
        
            let stream = TcpStream::connect("localhost:3334").unwrap();
            Message::new_hello(sat_id).send(&stream);
            let msg = Message::recv(&stream).expect("Failed to receieve").unwrap();
            assert_eq!(msg, Message::new_network_check_msg(1, 3));
        });

        let sat3 = thread::spawn(move || {
            let sat_id = 3;
            let stream = TcpStream::connect("localhost:3334").unwrap();
            Message::new_hello(sat_id).send(&stream);
            thread::sleep(std::time::Duration::from_millis(100));

            Message::new_network_check_msg(sat_id, 2).send(&stream);
        });


        sat3.join().unwrap();
    }

    #[test]
    fn test_comms_network_check() {
        let listener = TcpBuilder::new_v4().unwrap()
                                    .reuse_address(true).unwrap()
                                    .reuse_port(true).unwrap()
                                    .bind("0.0.0.0:3335").expect("Could not bind address")
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

        let sat1 = thread::spawn(move || {
            let sat_id = 1;
        
            let stream = TcpStream::connect("localhost:3335").unwrap();
            Message::new_hello(sat_id).send(&stream);
            thread::sleep(std::time::Duration::from_millis(100));

            // Check if we can get to Sat 12, it won't respond, but will test by itself 
            // if a message was recieved...
            Message::new_network_check_msg(sat_id, 12).send(&stream);

            // Meanwhile, check network to 2,3,20
            for target_id in vec![2,3,20].iter() {
                Message::new_network_check_msg(sat_id, *target_id).send(&stream);
                if let Ok(Some(msg)) = Message::recv(&stream) { 
                    assert_eq!(msg.body, MessageBody::NetworkCheckAck(*target_id));
                    assert_eq!(msg.get_src(), match target_id { 2 => 2, _ => 20}); 
                    if let Some(dst_id) = msg.get_next_dst() { 
                        assert_eq!(dst_id, sat_id);
                    } else { 
                        panic!("Empty destination route");
                    }
                } else { 
                    panic!("Failed to get message");
                }
            }
        });

        let _sat2 = thread::spawn(move || {
            let sat_id = 2;
            let stream = TcpStream::connect("localhost:3335").unwrap();
            let mut mgr = CommManager::new(sat_id, stream, None);
            mgr.start_communication();
        });

        let _sat3 = thread::spawn(move || {
            let sat_id = 3;
            let stream = TcpStream::connect("localhost:3335").unwrap();
            let mut mgr = CommManager::new(sat_id, stream, None);
            mgr.start_communication();
        });
        let _sat20 = thread::spawn(move || {
            let sat_id = 20;
            let stream = TcpStream::connect("localhost:3335").unwrap();
            let mut mgr = CommManager::new(sat_id, stream, None);
            mgr.start_communication();
        });

        let sat12 = thread::spawn(move || {
            let sat_id = 12;
        
            let stream = TcpStream::connect("localhost:3335").unwrap();
            Message::new_hello(sat_id).send(&stream);
            
            let msg = Message::recv(&stream).expect("Failed to receive").unwrap();
            assert_eq!(msg.body, MessageBody::NetworkCheckReq(1));
        });


        sat12.join().unwrap();
        sat1.join().unwrap();
    }

    #[test]
    fn test_detours() {
        let listener = TcpBuilder::new_v4().unwrap()
                                    .reuse_address(true).unwrap()
                                    .reuse_port(true).unwrap()
                                    .bind("0.0.0.0:3336").expect("Could not bind address")
                                    .listen(32).unwrap();

        let (route_req, route_queue) = sync_channel::<Message>(32);

        let clients_mtx:Arc<Mutex<HashMap<u16,TcpStream>>> = Arc::new(Mutex::new(HashMap::new()));
        let clients_mtx_clone = Arc::clone(&clients_mtx);


        let _server1 = thread::spawn(move || { 
            router(route_queue, clients_mtx);
        });

        let _server2 = thread::spawn(move || {
            accept_connections(&listener, clients_mtx_clone, route_req);
        });

        let sat2 = thread::spawn(move || {
            let sat_id = 2;
        
            let stream = TcpStream::connect("localhost:3336").unwrap();
            Message::new_hello(sat_id).send(&stream);
            thread::sleep(std::time::Duration::from_millis(100));

            Message { 
                route: Route { src : sat_id, dst : vec![3] },
                body : MessageBody::DetourReq(20,2)
            }.send(&stream);
            Message { 
                route: Route { src: sat_id, dst: vec![3, 20, 1] },
                body : MessageBody::NetworkCheckReq(2)
            }.send(&stream); 

            let mut next_msg = Message::recv(&stream).expect("Failed to receive").unwrap();
            next_msg.forward();
            next_msg.send(&stream);
        });

        let _sat3 = thread::spawn(move || {
            let sat_id = 3;
            let stream = TcpStream::connect("localhost:3336").unwrap();
            let mut mgr = CommManager::new(sat_id, stream, None);
            mgr.start_communication();
        });

        let _sat20 = thread::spawn(move || {
            let sat_id = 20;
            let stream = TcpStream::connect("localhost:3336").unwrap();
            let mut mgr = CommManager::new(sat_id, stream, None);
            mgr.start_communication();
        });

        let sat1 = thread::spawn(move || {
            let sat_id = 1;
        
            let stream = TcpStream::connect("localhost:3336").unwrap();
            Message::new_hello(sat_id).send(&stream);
            
            let msg = Message::recv(&stream).expect("Failed to receive").unwrap();
            assert_eq!(msg.body, MessageBody::NetworkCheckReq(2));
        });


        sat2.join().unwrap();
        sat1.join().unwrap();
    }

    
    #[test]
    fn test_detours_longer() {
        let listener = TcpBuilder::new_v4().unwrap()
                                    .reuse_address(true).unwrap()
                                    .reuse_port(true).unwrap()
                                    .bind("0.0.0.0:5556").expect("Could not bind address")
                                    .listen(32).unwrap();

        let (route_req, route_queue) = sync_channel::<Message>(32);

        let clients_mtx:Arc<Mutex<HashMap<u16,TcpStream>>> = Arc::new(Mutex::new(HashMap::new()));
        let clients_mtx_clone = Arc::clone(&clients_mtx);


        let _server1 = thread::spawn(move || {
            router(route_queue, clients_mtx);
        });

        let _server2 = thread::spawn(move || {
            accept_connections(&listener, clients_mtx_clone, route_req);
        });

        thread::sleep(std::time::Duration::from_millis(500));

        // Setup Links... 
        let link_ids = [];//[20,30,40,50,4,5,6,7,8,9,10,11,12,50,0,3] ;
        // NOTE: We take advantage of the faking on the server now, much less to do!
        for sat_id in link_ids {
            thread::spawn(move || {
                let stream = TcpStream::connect("localhost:5556").unwrap();
                let mut mgr = CommManager::new(sat_id, stream, None);
                mgr.start_communication();                
            });
        }

        let sat_id = 2;
        let stream = TcpStream::connect("localhost:5556").unwrap();
        Message::new_hello(sat_id).send(&stream);

        for (targ, orig, reroute) in [(4,0,30), (3,0,4), (20,0,3) ] { 
            Message { 
                route: Route::full_route(sat_id, targ),
                body : MessageBody::DetourReq(orig, reroute)
            }.send(&stream);
        }

        thread::sleep(std::time::Duration::from_millis(1000));

        let link_ids = [20,30,40,50,4,5,6,7,8,9,10,11,12,50,0,3] ;

        // Meanwhile, check network to 2,3,20
        for target_id in link_ids.iter() {
            let msg = Message::new_network_check_msg(sat_id, *target_id);
            msg.send(&stream);
            //thread::sleep(std::time::Duration::from_millis(100));
            
            if let Ok(Some(msg)) = Message::recv(&stream) { 
                assert_eq!(msg.body, MessageBody::NetworkCheckAck(*target_id));
                assert!(msg.at_destination());
                if let Some(dst_id) = msg.get_next_dst() { 
                    assert_eq!(dst_id, sat_id);
                } else { 
                    panic!("Empty destination route");
                }
            } else { 
                panic!("Failed to get message");
            }
        }    
    }
    #[test]
    fn test_detours_flag() {
        let listener = TcpBuilder::new_v4().unwrap()
                                    .reuse_address(true).unwrap()
                                    .reuse_port(true).unwrap()
                                    .bind("0.0.0.0:5557").expect("Could not bind address")
                                    .listen(32).unwrap();

        let (route_req, route_queue) = sync_channel::<Message>(32);

        let clients_mtx:Arc<Mutex<HashMap<u16,TcpStream>>> = Arc::new(Mutex::new(HashMap::new()));
        let clients_mtx_clone = Arc::clone(&clients_mtx);


        let _server1 = thread::spawn(move || {
            router(route_queue, clients_mtx);
        });

        let _server2 = thread::spawn(move || {
            accept_connections(&listener, clients_mtx_clone, route_req);
        });

        thread::sleep(std::time::Duration::from_millis(500));

        // Setup Links... 
        let link_ids = [];//[20,30,40,50,4,5,6,7,8,9,10,11,12,50,0,3] ;
        // NOTE: We take advantage of the faking on the server now, much less to do!
        for sat_id in link_ids {
            thread::spawn(move || {
                let stream = TcpStream::connect("localhost:5557").unwrap();
                let mut mgr = CommManager::new(sat_id, stream, None);
                mgr.start_communication();                
            });
        }

        thread::spawn(move || {
            let stream = TcpStream::connect("localhost:5557").unwrap();
            Message::new_hello(8).send(&stream);
        });

        let sat_id = 5;
        
        let stream = TcpStream::connect("localhost:5557").unwrap();
        Message::new_hello(sat_id).send(&stream);

        for (targ, orig, reroute) in [(3,0,4),(20,0,3),(4,0,5)] { 
            Message { 
                route: Route::full_route(sat_id, targ),
                body : MessageBody::DetourReq(orig, reroute)
            }.send(&stream);
        }

        Message {
            route: Route::full_route(sat_id, 2) ,
            body : MessageBody::SendFlag
        }.send(&stream);

        let msg = Message::recv(&stream).expect("Failed to receive").unwrap();
        assert_eq!(msg.body, MessageBody::Flag(String::from("FLAG{Test_Flag}")));

    }
}