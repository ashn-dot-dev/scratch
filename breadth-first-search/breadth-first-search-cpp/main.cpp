#include <functional>
#include <iostream>
#include <memory>
#include <queue>
#include <vector>
#include <unordered_set>

struct Node {
    std::string name;
    std::unordered_set<std::shared_ptr<Node>> children;
};

struct Graph {
    std::unordered_set<std::shared_ptr<Node>> nodes;
};

static std::vector<std::shared_ptr<Node>>
bfs(Graph const& graph, std::shared_ptr<Node> root)
{
    auto visited = std::unordered_set<std::shared_ptr<Node>>{};
    auto ordered = std::vector<std::shared_ptr<Node>>{};
    auto queue = std::queue<std::shared_ptr<Node>>{};

    queue.push(root);
    while (!queue.empty()) {
        auto node = queue.front();
        queue.pop();

        if (visited.contains(node)) {
            continue;
        }

        ordered.push_back(node);
        visited.insert(node);
        for (auto child: node->children) {
            queue.push(child);
        }
    }

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
        auto ordered = bfs(graph, b);
        std::cout << "Ordering:" << std::endl;
        for (auto node: ordered) {
            std::cout << node->name << std::endl;
        }
    }
}

