// Publishes a counting string message on /chatter once per second.
//
// This is the C++ equivalent of demo/python/talker.py — same pattern
// (node -> publisher -> timer callback), different language. Compare the
// two side by side to see what's language-specific (memory management,
// syntax) vs. what's the actual ROS2 concept (publisher, timer, spin).

#include <chrono>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;  // lets us write "1s" for 1 second

class Talker : public rclcpp::Node
{
public:
  Talker() : Node("talker"), count_(0)
  {
    // create_publisher<MsgType>(topic_name, queue_size) — same shape as
    // rclpy's create_publisher, just templated on the message type
    // instead of taking it as a positional argument.
    publisher_ = this->create_publisher<std_msgs::msg::String>("chatter", 10);

    // create_wall_timer binds this->publish_message() as the callback,
    // fired every 1 second. `this` is captured so the lambda can call
    // back into the node's members.
    timer_ = this->create_wall_timer(
      1s, std::bind(&Talker::publish_message, this));
  }

private:
  void publish_message()
  {
    auto msg = std_msgs::msg::String();
    msg.data = "Hello, ROS2! count=" + std::to_string(count_);
    RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", msg.data.c_str());
    publisher_->publish(msg);
    count_++;
  }

  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  size_t count_;
};

int main(int argc, char * argv[])
{
  // rclcpp::init is the C++ equivalent of rclpy.init() — sets up the
  // communication layer before any node is constructed.
  rclcpp::init(argc, argv);

  // spin() blocks here and drives the timer callback until Ctrl+C
  // (rclcpp::shutdown gets called internally on SIGINT).
  rclcpp::spin(std::make_shared<Talker>());

  rclcpp::shutdown();
  return 0;
}
