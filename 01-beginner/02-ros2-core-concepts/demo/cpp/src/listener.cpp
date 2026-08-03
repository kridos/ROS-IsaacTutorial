// Subscribes to /chatter and logs every message it receives.
//
// C++ equivalent of demo/python/listener.py.

#include <functional>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using std::placeholders::_1;  // used below to bind the callback's one argument

class Listener : public rclcpp::Node
{
public:
  Listener() : Node("listener")
  {
    // create_subscription<MsgType>(topic_name, qos_depth, callback).
    // std::bind(&Listener::on_message, this, _1) creates a callable that,
    // when invoked with one argument, calls this->on_message(that_arg) —
    // the C++ way of registering a member function as a callback.
    subscription_ = this->create_subscription<std_msgs::msg::String>(
      "chatter", 10, std::bind(&Listener::on_message, this, _1));
  }

private:
  void on_message(const std_msgs::msg::String & msg) const
  {
    RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg.data.c_str());
  }

  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Listener>());
  rclcpp::shutdown();
  return 0;
}
