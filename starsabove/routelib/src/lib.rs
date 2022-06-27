use std::{error::Error, fmt};

#[derive(Debug)]
pub struct Unreachable;
impl Error for Unreachable {} 
impl fmt::Display for Unreachable {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "No Route between nodes")
    }
}


enum Node {
    End(u16,u16),
    Gateway(u16,u16,u16),
    Root
}

struct Hop { 
    id: u16,
    n: Node,
    default: u16
}

const ROUTE_TABLE:[Hop; 17] = [
    Hop { id :  0, n: Node::Root, default : 0 },

    Hop { id :  1, n: Node::End(12, 2), default : 20 },
    Hop { id :  2, n: Node::End( 1, 3), default : 20 },
    Hop { id :  3, n: Node::End( 2, 4), default : 20 },

    Hop { id :  4, n: Node::End( 3, 5), default : 30 },
    Hop { id :  5, n: Node::End( 4, 6), default : 30 },
    Hop { id :  6, n: Node::End( 5, 7), default : 30 },
    
    Hop { id :  7, n: Node::End( 6, 8), default : 40 },
    Hop { id :  8, n: Node::End( 7, 9), default : 40 },
    Hop { id :  9, n: Node::End( 8,10), default : 40 },

    Hop { id : 10, n: Node::End( 9,11), default : 50 },
    Hop { id : 11, n: Node::End(10,12), default : 50 },
    Hop { id : 12, n: Node::End(11, 1), default : 50 },

    Hop { id : 20, n: Node::Gateway( 1, 2, 3), default : 0 },
    Hop { id : 30, n: Node::Gateway( 4, 5, 6), default : 0 },
    Hop { id : 40, n: Node::Gateway( 7, 8, 9), default : 0 },
    Hop { id : 50, n: Node::Gateway(10,11,12), default : 0 },
];

fn lookup_route(src: u16) -> Result<&'static Hop,Unreachable> {
    match src {
        0..=12 => Ok(ROUTE_TABLE.get(src as usize).unwrap()),
        20 => Ok(ROUTE_TABLE.get(13).unwrap()),
        30 => Ok(ROUTE_TABLE.get(14).unwrap()),
        40 => Ok(ROUTE_TABLE.get(15).unwrap()),
        50 => Ok(ROUTE_TABLE.get(16).unwrap()),
        _ => Err(Unreachable)
    }
}

impl Hop { 
    pub fn get_next(&self, dst: u16) -> Result<u16,Unreachable>{
        match self.n { 
            Node::End(d1,d2) => { 
                if d1 == dst || d2 == dst { 
                    Ok(dst)
                } else { 
                    Ok(self.default)
                } 
            }, 
            Node::Gateway(d1, d2, d3) => {
                if d1 == dst || d2 == dst || d3 == dst {
                    Ok(dst)
                } else { 
                    Ok(self.default)
                }            
            }, 
            Node::Root => match dst { 
                1..=3   => Ok(20),
                4..=6   => Ok(30),
                7..=9   => Ok(40),
                10..=12 => Ok(50),
                20|30|40|50 => Ok(dst),
                _ => Err(Unreachable)
            }
        }
    }
}

pub fn get_route(src:u16, dst:u16) -> Result<Vec<u16>, Unreachable> {
    let mut next_node = lookup_route(src)?;
    let mut route:Vec<u16> = Vec::new();
    loop {
        let node = lookup_route(next_node.get_next(dst)?)?;
        route.push(node.id);

        if node.id == dst { 
            break
        }
        next_node = node;
    }
    Ok(route)
}

pub fn can_reach(src:u16, dst:u16) -> bool {
    match lookup_route(src) { 
        Ok(node) => match node.get_next(dst) {
            Ok(next_id) => next_id == dst,
            Err(_) => false
        }
        Err(_) => false
    }
}

#[cfg(test)]
mod tests {
    use super::{get_route,can_reach};
    #[test]
    fn call_can_reach() { 
        assert!( !can_reach(1, 4) );
        assert!(  can_reach(1, 2) );
        assert!(  can_reach(1, 12) );
        assert!(  can_reach(1, 20) );
        assert!( !can_reach(1, 0) );
        assert!( !can_reach(1, 30) );
        assert!( !can_reach(1, 1) );

        assert!( can_reach(20,0));
        assert!( can_reach(20,1));
        assert!( can_reach(20,2));
        assert!( can_reach(20,3));
        assert!( !can_reach(20,30));

        assert!( can_reach(0,20));
        assert!( can_reach(0,30));
        assert!( can_reach(0,40));
        assert!( can_reach(0,50));
        
        assert!( !can_reach(0,1));
    }
    
    #[test]
    fn check_connectivity() {
        for src in 1..=12 { 
            for dst in 1..=12 {
                if src != dst {
                    let route = get_route(src, dst).expect("Bad Route");
                    assert_ne!(0, route.len());
                    assert!(route.len() <= 4);
                }
            }
        }
    }
    #[test]
    fn check_routes() {
        assert_eq!(get_route(1, 2).expect("Bad Route"),  vec![2u16]);
        assert_eq!(get_route(1, 12).expect("Bad Route"), vec![12u16]);
        assert_eq!(get_route(1, 20).expect("Bad Route"), vec![20u16]);
        
        assert_eq!(get_route(1, 3).expect("Bad Route"), vec![20u16, 3u16]);
        assert_eq!(get_route(1, 4).expect("Bad Route"), vec![20u16, 0u16, 30u16, 4u16]);
        
        assert_eq!(get_route(1, 4).expect("Bad Route"), vec![20u16, 0u16, 30u16, 4u16]);
        assert_eq!(get_route(1, 8).expect("Bad Route"), vec![20u16, 0u16, 40u16, 8u16]);
        assert_eq!(get_route(2, 0).expect("Bad Route"), vec![20u16, 0u16]);

    }
}
