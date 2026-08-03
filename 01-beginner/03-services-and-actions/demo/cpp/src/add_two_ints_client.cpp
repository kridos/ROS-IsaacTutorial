// Calls the add_two_ints service once, asynchronously, and prints the
// result. Takes two integers as command-line arguments (defaults 2, 3).
// C++ equivalent of demo/python/add_two_ints_client.py.

#include <chrono>
#include <cstdlib>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

using AddTwoInts = example_interfaces::srv::AddTwoInts;
using namespace std::chrono_literals;

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);

  auto node = rclcpp::Node::make_shared("add_two_ints_client");
  auto client = node->create_client<AddTwoInts>("add_two_ints");

  // Parse optional command-line args, same defaults as the Python client.
  long a = argc > 1 ? std::atol(argv[1]) : 2;
  long b = argc > 2 ? std::atol(argv[2]) : 3;

  // wait_for_service blocks (polled here in 1-second slices) until a
  // server advertises this service name, same reasoning as the Python
  // version: fail loudly and informatively rather than calling into a
  // service that doesn't exist yet.
  while (!client->wait_for_service(1s)) {
    if (!rclcpp::ok()) {
      RCLCPP_ERROR(node->get_logger(), "Interrupted while waiting for service");
      return 1;
    }
    RCLCPP_INFO(node->get_logger(), "Waiting for add_two_ints service...");
  }

  auto request = std::make_shared<AddTwoInts::Request>();
  request->a = a;
  request->b = b;

  // async_send_request returns a future; spin_until_future_complete blocks
  // this thread (safe here since main() isn't itself a callback) while
  // letting the executor process the response when it arrives.
  auto future = client->async_send_request(request);
  if (rclcpp::spin_until_future_complete(node, future) ==
    rclcpp::FutureReturnCode::SUCCESS)
  {
    RCLCPP_INFO(node->get_logger(), "Result: %ld + %ld = %ld",
      a, b, future.get()->sum);
  } else {
    RCLCPP_ERROR(node->get_logger(), "Service call failed");
  }

  rclcpp::shutdown();
  return 0;
}
