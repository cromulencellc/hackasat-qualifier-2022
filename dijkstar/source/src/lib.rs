extern crate csv;
extern crate serde;
#[macro_use]
extern crate serde_derive;
#[macro_use]
extern crate lazy_static;
use std::sync::{Mutex};

use std::error::Error;
use std::collections::HashMap;
use pathfinding::directed::dijkstra::dijkstra;
use ordered_float::OrderedFloat;

#[derive(Debug, Deserialize)]
#[serde(rename_all = "PascalCase")]
struct DataRow {
    source: String,
    dest: String,
    range: f64,
}
lazy_static! {
    static ref NODES: Mutex<HashMap<String, Node>> = Mutex::new(HashMap::new());
}

pub unsafe fn run(args: Args) -> Result<(), Box<dyn Error>>{
    // Read in the data files
    let mut gateway_rdr = csv::Reader::from_path(args.gateway_file)?;
    let mut sats_rdr = csv::Reader::from_path(args.satellite_file)?;
    let mut users_rdr = csv::Reader::from_path(args.users_file)?;
    

    // NOTE: The Gateway File's source and dest need to be reversed, hence the bool parameter
    parse_reader_file(&mut gateway_rdr, true).expect("Error Parsing Gateway Data.");
    parse_reader_file(&mut sats_rdr, false).expect("Error Parsing Sat Data.");
    parse_reader_file(&mut users_rdr, false).expect("Error Parsing User Data.");

    let starting_node = NODES.lock().unwrap().get(&args.src_user).unwrap().clone();

    // // Perform the a-star algorithm to find the shortest path from start to fin
    let shortest_path = dijkstra(&starting_node,
                              |cur_node| get_neighbours(cur_node),
                              |fin| (*fin).node_name == args.dst_gateway);

    for node in shortest_path.unwrap().0 {
        println!("{:?}", node.node_name);
    }
    Ok(())
}


// unsafe fn get_estimate_cost(curNode: &Node) -> OrderedFloat<f64>
// {
//     let mut ret_val = OrderedFloat(2000.0);
//     if target_map.contains_key(&curNode)
//     {
//         for targ in target_map.get(&curNode).unwrap().iter()
//         {
//             if targ.target_name == endNode
//             {
//                 ret_val = OrderedFloat(targ.get_target_traversal_cost());
//                 break;
//             }
//         }
//     }
//     ret_val
// }

unsafe fn get_neighbours(node: &Node) -> Vec<(Node, OrderedFloat<f64>)>{
    let mut neighbour_list: Vec<(Node, OrderedFloat<f64>)> = Vec::new();
    for neighbour in node.node_neighbours.iter() {
        neighbour_list.push((NODES.lock().unwrap().get(&neighbour.0).unwrap().clone(), neighbour.1.clone()));
    }
    neighbour_list
}

unsafe fn parse_reader_file(rdr: &mut csv::Reader<std::fs::File>,
                            reverse:bool) -> Result<(), Box<dyn Error>> {
    for result in rdr.deserialize() {
        let data_row: DataRow = result?;
        let src = if reverse { &data_row.dest } else {&data_row.source};
        let dst = if reverse { &data_row.source } else {&data_row.dest};
        let range = data_row.range;
        if NODES.lock().unwrap().contains_key(src)
        {
            if NODES.lock().unwrap().contains_key(dst)
            {
                NODES.lock().unwrap().get_mut(src)
                    .expect("Invalid Key!")
                    .node_neighbours
                    .push((dst.clone(), get_target_traversal_cost(OrderedFloat(range), determine_target_type(dst))));
            }
            else {
                NODES.lock().unwrap().insert(dst.clone(), Node::new(dst.clone(), Vec::new()));
            }
        }
        else {
            NODES.lock().unwrap().insert(src.clone(), 
                             Node::new(src.clone(), 
                                       Vec::new()
                                       ));

            if NODES.lock().unwrap().contains_key(dst)
            {
                NODES.lock().unwrap().get_mut(src)
                    .expect("Invalid Key!")
                    .node_neighbours
                    .push((dst.clone(), get_target_traversal_cost(OrderedFloat(range), determine_target_type(dst))));
            }
            else {
                NODES.lock().unwrap().insert(dst.clone(), Node::new(dst.clone(), Vec::new()));
            }
        }
    }
    Ok(())
}

// #[derive(Clone, Debug, PartialOrd)]
// struct Range {
//     dist: f64
// }

// impl Range {
//     fn new(d: f64) -> Range {
//         Range {
//             dist: d
//         }
//     }
// }


#[derive(Eq, PartialEq, Hash, Clone, Debug)]
struct Node{
    node_name: String,
    node_neighbours: Vec<(String, OrderedFloat<f64>)>
}

impl Node {
    fn new(n_name: String, n_neighbours: Vec<(String, OrderedFloat<f64>)>) -> Node {
        Node{
            node_name: n_name,
            node_neighbours: n_neighbours
        }
    }
}

fn get_target_traversal_cost(t_distance: OrderedFloat<f64>, t_type: TargetType) -> OrderedFloat<f64> {
    OrderedFloat(t_distance.into_inner() * determine_type_weight(&t_type))
}

fn determine_target_type(target_name: &String) -> TargetType {
    let last_num = target_name[target_name.len()-1..].parse::<i32>();
    let type_num = match last_num {
        Ok(last_num) => last_num%3,
        Err(_) => 3
    };

    match type_num {
        0 => TargetType::Starmander,
        1 => TargetType::Starmeleon,
        2 => TargetType::Starzard,
        _ => TargetType::UserOrGatewayStation,
    }
    
}


#[derive(Eq, PartialEq, Hash, Clone, Debug)]
pub enum TargetType {
    Starmander,
    Starmeleon,
    Starzard,
    UserOrGatewayStation
}

pub fn determine_type_weight(t_type: &TargetType) -> f64 {
    match t_type {
        TargetType::Starmander => 2.718,
        TargetType::Starmeleon => 3.141,
        TargetType::Starzard => 4.04,
        TargetType::UserOrGatewayStation => 1999.9
    }
}

pub struct Args {
    pub src_user: String,
    pub dst_gateway: String,
    pub gateway_file: String,
    pub satellite_file: String,
    pub users_file: String,
}

impl Args { 
    pub fn new(args: &[String]) -> Result<Args, &'static str> {
        if args.len() != 6 {
            return Err("Not the correct number of input arguments. Number of input arguments should be 5.");
        }
        let src_user       = args[1].clone();
        let dst_gateway    = args[2].clone();
        let gateway_file   = args[3].clone();
        let satellite_file = args[4].clone();
        let users_file     = args[5].clone();

    Ok(Args{src_user, dst_gateway, gateway_file, satellite_file, users_file})
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn one_result() {
        let query = "duct";
        let contents = "\
Rust:
safe, fast, productive.
Pick three.";

        assert_eq!(vec!["safe, fast, productive."], search(query, contents));
    }
}