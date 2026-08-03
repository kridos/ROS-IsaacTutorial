// A service server that adds two integers on request.
// C++ equivalent of demo/python/add_two_ints_server.py.

#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

using AddTwoInts = example_interfaces::srv::AddTwoInts;

class AddTwoIntsServer : public rclcpp::Node
{
public:
  AddTwoIntsServer() : Node("add_two_ints_server")
  {
    // create_service takes the service name and a callback that receives
    // shared_ptrs to the request and response — in rclcpp, unlike rclpy,
    // the response is filled in through a pointer rather than returned.
    service_ = this->create_service<AddTwoInts>(
      "add_two_ints",
      std::bind(&AddTwoIntsServer::handle_request, this,
        std::placeholders::_1, std::placeholders::_2));
    RCLCPP_INFO(this->get_logger(), "add_two_ints service ready");
  }

private:
  void handle_request(
    const std::shared_ptr<AddTwoInts::Request> request,
    std::shared_ptr<AddTwoInts::Response> response)
  {
    response->sum = request->a + request->b;
    RCLCPP_INFO(this->get_logger(), "Incoming request: %ld + %ld = %ld",
      request->a, request->b, response->sum);
  }

  rclcpp::Service<AddTwoInts>::SharedPtr service_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<AddTwoIntsServer>());
  rclcpp::shutdown();
  return 0;
}
