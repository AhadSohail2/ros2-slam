#include <rclcpp/rclcpp.hpp>
#include <utility>

#include <nav_msgs/msg/occupancy_grid.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>

#include <nav_msgs/msg/path.hpp>

#include "tf2_ros/buffer.h"
#include "tf2_ros/transform_listener.h"

namespace bumperbot_planning
{

    struct GraphNode
    {
        int x;
        int y;
        int cost;
        std::shared_ptr<GraphNode> prev;

        GraphNode(int in_x, int in_y) : x(in_x), y(in_y), cost(0) {};
        GraphNode() : GraphNode(0, 0) {};

        bool operator>(const GraphNode &other) const
        {
            return cost > other.cost;
        }

        bool operator==(const GraphNode &other) const
        {
            return x == other.x && y == other.y;
        }

        GraphNode operator+(std::pair<int, int> const &other)
        {
            GraphNode result;

            result.x = x + other.first;
            result.y = y + other.second;

            return result;
        }
    };

    class DijkstraPlanner : public rclcpp::Node
    {
    public:
        DijkstraPlanner();

    private:
        rclcpp::Subscription<nav_msgs::msg::OccupancyGrid>::SharedPtr map_sub_;
        rclcpp::Subscription<geometry_msgs::msg::PoseStamped>::SharedPtr pose_sub_;

        rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr path_pub_;
        rclcpp::Publisher<nav_msgs::msg::OccupancyGrid>::SharedPtr map_pub_;

        nav_msgs::msg::OccupancyGrid::SharedPtr map_;
        nav_msgs::msg::OccupancyGrid visited_map_;

        std::shared_ptr<tf2_ros::Buffer> tf_buffer_;
        std::shared_ptr<tf2_ros::TransformListener> tf_listener_;

        void mapCallback(const nav_msgs::msg::OccupancyGrid::SharedPtr msg);
        void goalCallback(const geometry_msgs::msg::PoseStamped::SharedPtr msg);

        GraphNode worldToGrid(const geometry_msgs::msg::Pose &pose);
        bool poseOnMap(const GraphNode &node);
        unsigned int poseToCell(const GraphNode &node);

        geometry_msgs::msg::Pose gridToWorld(const GraphNode &node);

        nav_msgs::msg::Path plan(const geometry_msgs::msg::Pose &start, const geometry_msgs::msg::Pose &goal);
    };

} // namespace bumperbot_planning