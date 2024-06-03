#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>

struct Node {
    std::string name;
    std::unordered_set<std::shared_ptr<Node>> children;
};

struct Graph {
    std::unordered_set<std::shared_ptr<Node>> nodes;
};

static std::vector<std::shared_ptr<Node>>
dfs(Graph const& graph)
{
    auto visited = std::unordered_set<std::shared_ptr<Node>>{};
    auto ordered = std::vector<std::shared_ptr<Node>>{};

    std::function<void(std::shared_ptr<Node>)> visit = [&](std::shared_ptr<Node> node) {
        if (visited.find(node) != visited.end()) {
            return;
        }

        visited.insert(node);
        for (auto child: node->children) {
            visit(child);
        }
        ordered.push_back(node);
    };

    for (auto node: graph.nodes) {
        visit(node);
    }

    std::reverse(ordered.begin(), ordered.end());
    return ordered;
}

static std::vector<std::shared_ptr<Node>>
dfs_cycle_detecting(Graph const& graph)
{
    auto visiting = std::unordered_set<std::shared_ptr<Node>>{};
    auto visited = std::unordered_set<std::shared_ptr<Node>>{};
    auto ordered = std::vector<std::shared_ptr<Node>>{};

    std::function<void(std::shared_ptr<Node>)> visit = [&](std::shared_ptr<Node> node) {
        if (visited.find(node) != visited.end()) {
            return;
        }
        if (visiting.find(node) != visited.end()) {
            throw std::runtime_error("cycle detected");
        }

        visiting.insert(node);
        for (auto child: node->children) {
            visit(child);
        }
        visited.insert(node);
        ordered.push_back(node);
    };

    for (auto node: graph.nodes) {
        visit(node);
    }

    std::reverse(ordered.begin(), ordered.end());
    return ordered;
}

int
main()
{
    // B-->E-->A--+
    // |   |   |  |
    // |   v   |  |
    // +-->C<--+  |
    //      |     v
    //      +---->D

    auto a = std::make_shared<Node>(Node{"A"});
    auto b = std::make_shared<Node>(Node{"B"});
    auto c = std::make_shared<Node>(Node{"C"});
    auto d = std::make_shared<Node>(Node{"D"});
    auto e = std::make_shared<Node>(Node{"E"});

    a->children.insert(c);
    a->children.insert(d);

    b->children.insert(c);
    b->children.insert(e);

    c->children.insert(d);

    e->children.insert(a);
    e->children.insert(c);

    {
        auto graph = Graph{{a, b, c, d, e}};
        auto ordered = dfs(graph);
        std::cout << "Topological Ordering:" << std::endl;
        for (auto node: ordered) {
            std::cout << node->name << std::endl;
        }
    }

    // +->W-->X--+
    // |  |   |  |
    // |  |   v  v
    // |  +-->Y->Z
    // |         |
    // +---------+

    auto w = std::make_shared<Node>(Node{"W"});
    auto x = std::make_shared<Node>(Node{"X"});
    auto y = std::make_shared<Node>(Node{"Y"});
    auto z = std::make_shared<Node>(Node{"Z"});

    w->children.insert(x);
    w->children.insert(y);

    w->children.insert(y);
    w->children.insert(z);

    y->children.insert(z);

    z->children.insert(w);

    try {
        auto graph = Graph{{w, x, y, z}};
        auto ordered = dfs_cycle_detecting(graph);
        std::cout << "Topological Ordering:" << std::endl;
        for (auto node: ordered) {
            std::cout << node->name << std::endl;
        }
    }
    catch (std::exception const& e) {
        std::cout << e.what() << std::endl;
    }
}
