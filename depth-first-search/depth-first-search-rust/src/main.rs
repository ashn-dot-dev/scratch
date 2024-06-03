use std::collections::{HashMap, HashSet};
use std::hash::{Hash, Hasher};

#[derive(Debug, Clone)]
struct Node {
    name: String,
    children: HashSet<String>,
}

impl Node {
    fn new<S: Into<String>>(name: S) -> Node {
        Node {
            name: name.into(),
            children: HashSet::new(),
        }
    }
}
impl Hash for Node {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.name.hash(state);
    }
}
impl PartialEq for Node {
    fn eq(&self, other: &Self) -> bool {
        self.name == other.name
    }
}

impl Eq for Node {}

#[derive(Debug)]
struct Graph {
    nodes: HashMap<String, Node>,
}

impl Graph {
    fn new(nodes: HashSet<Node>) -> Graph {
        let mut new = Graph {
            nodes: HashMap::new(),
        };
        nodes.into_iter().for_each(|node| {
            new.nodes.insert(node.name.clone(), node);
        });
        new
    }
    fn get(&self, name: &String) -> Option<&Node> {
        self.nodes.get(name)
    }

    fn get_mut(&mut self, name: &String) -> Option<&mut Node> {
        self.nodes.get_mut(name)
    }
}

fn dfs(graph: &Graph) -> Vec<Node> {
    let mut visited = HashSet::<Node>::new();
    let mut ordered = vec![];

    fn visit(graph: &Graph, node: &Node, visited: &mut HashSet<Node>, ordered: &mut Vec<Node>) {
        if visited.contains(node) {
            return;
        }
        visited.insert(node.clone());
        for child in &node.children {
            visit(graph, graph.get(&child).unwrap(), visited, ordered);
        }
        ordered.push(node.clone());
    }

    for (_, node) in &graph.nodes {
        visit(graph, node, &mut visited, &mut ordered);
    }
    ordered.reverse();
    ordered
}

fn dfs_cycle_detecting(graph: &Graph) -> Vec<Node> {
    let mut visiting = HashSet::<Node>::new();
    let mut visited = HashSet::<Node>::new();
    let mut ordered = vec![];

    fn visit(
        graph: &Graph,
        node: &Node,
        visiting: &mut HashSet<Node>,
        visited: &mut HashSet<Node>,
        ordered: &mut Vec<Node>,
    ) {
        if visited.contains(node) {
            return;
        }
        if visiting.contains(node) {
            panic!("cycle detected");
        }

        visiting.insert(node.clone());
        for child in &node.children {
            visit(
                graph,
                graph.get(&child).unwrap(),
                visiting,
                visited,
                ordered,
            );
        }
        visited.insert(node.clone());
        ordered.push(node.clone());
    }

    for (_, node) in &graph.nodes {
        visit(graph, node, &mut visiting, &mut visited, &mut ordered);
    }
    ordered.reverse();
    ordered
}

fn main() {
    // B-->E-->A--+
    // |   |   |  |
    // |   v   |  |
    // +-->C<--+  |
    //      |     v
    //      +---->D

    let mut a = Node::new("A");
    let mut b = Node::new("B");
    let mut c = Node::new("C");
    let d = Node::new("D");
    let mut e = Node::new("E");

    a.children.insert("C".to_string());
    a.children.insert("D".to_string());

    b.children.insert("C".to_string());
    b.children.insert("E".to_string());

    c.children.insert("D".to_string());

    e.children.insert("A".to_string());
    e.children.insert("C".to_string());

    let graph = Graph::new(HashSet::from([a, b, c, d, e]));
    let ordered = dfs(&graph);
    println!("{ordered:?}");

    // +->W-->X--+
    // |  |   |  |
    // |  |   v  v
    // |  +-->Y->Z
    // |         |
    // +---------+

    let mut w = Node::new("W");
    let mut x = Node::new("X");
    let mut y = Node::new("Y");
    let mut z = Node::new("Z");

    w.children.insert("X".to_string());
    w.children.insert("Y".to_string());

    x.children.insert("Y".to_string());
    x.children.insert("Z".to_string());

    y.children.insert("Z".to_string());

    z.children.insert("W".to_string());

    let graph = Graph::new(HashSet::from([w, x, y, z]));
    let ordered = dfs_cycle_detecting(&graph);
    println!("{ordered:?}");
}
