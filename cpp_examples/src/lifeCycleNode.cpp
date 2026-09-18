#include <rclcpp/rclcpp.hpp>
#include <rclcpp_lifecycle/lifecycle_node.hpp>

class MyNode : public rclcpp_lifecycle::LifecycleNode
{
public:
    MyNode()
        : LifecycleNode("my_node")
    {}

    CallbackReturn on_configure(
        const rclcpp_lifecycle::State &)
    {
        // Initialize resources
        return CallbackReturn::SUCCESS;
    }

    CallbackReturn on_activate(
        const rclcpp_lifecycle::State &)
    {
        // Start operation
        return CallbackReturn::SUCCESS;
    }

    CallbackReturn on_deactivate(
        const rclcpp_lifecycle::State &)
    {
        // Stop operation
        return CallbackReturn::SUCCESS;
    }
};


int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);

    auto node = std::make_shared<MyNode>();

    rclcpp::spin(node->get_node_base_interface());

    rclcpp::shutdown();

    return 0;
}