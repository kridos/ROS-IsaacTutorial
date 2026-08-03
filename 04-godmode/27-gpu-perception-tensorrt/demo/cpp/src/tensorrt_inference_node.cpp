// Wraps a TensorRT engine (built by python/build_engine.py) in a ROS2
// node: subscribes to an image topic, runs inference on each incoming
// frame, publishes a result. Written in C++ specifically because
// production perception inference nodes are exactly the case where this
// curriculum's language policy calls for C++ (see the project spec).
//
// GPU buffer allocation happens ONCE in the constructor, not per
// message — see DEEP_DIVE.md for why per-message allocation would waste
// most of TensorRT's speed advantage.

#include <fstream>
#include <memory>
#include <vector>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"
#include "std_msgs/msg/float32_multi_array.hpp"

#include "NvInfer.h"
#include "cuda_runtime_api.h"

// Minimal TensorRT logger — required by the TensorRT API, routes engine
// messages into RCLCPP logging instead of TensorRT's own stdout default.
class TrtLogger : public nvinfer1::ILogger
{
public:
  void log(Severity severity, const char * msg) noexcept override
  {
    if (severity <= Severity::kWARNING) {
      RCLCPP_WARN(rclcpp::get_logger("tensorrt_inference_node"), "[TensorRT] %s", msg);
    }
  }
};

class TensorRTInferenceNode : public rclcpp::Node
{
public:
  TensorRTInferenceNode() : Node("tensorrt_inference_node")
  {
    this->declare_parameter<std::string>("engine_path", "model.engine");
    std::string engine_path = this->get_parameter("engine_path").as_string();

    load_engine(engine_path);
    allocate_buffers();  // once, at startup — see file header comment

    subscription_ = this->create_subscription<sensor_msgs::msg::Image>(
      "camera/image_raw", 10,
      std::bind(&TensorRTInferenceNode::on_image, this, std::placeholders::_1));
    publisher_ = this->create_publisher<std_msgs::msg::Float32MultiArray>(
      "perception/result", 10);

    RCLCPP_INFO(this->get_logger(), "Loaded engine from %s, ready for inference", engine_path.c_str());
  }

  ~TensorRTInferenceNode() override
  {
    cudaFree(input_device_);
    cudaFree(output_device_);
    cudaStreamDestroy(stream_);
  }

private:
  void load_engine(const std::string & engine_path)
  {
    std::ifstream file(engine_path, std::ios::binary | std::ios::ate);
    if (!file) {
      throw std::runtime_error("Could not open engine file: " + engine_path);
    }
    size_t size = file.tellg();
    file.seekg(0);
    std::vector<char> engine_data(size);
    file.read(engine_data.data(), size);

    runtime_.reset(nvinfer1::createInferRuntime(logger_));
    engine_.reset(runtime_->deserializeCudaEngine(engine_data.data(), size));
    context_.reset(engine_->createExecutionContext());
  }

  void allocate_buffers()
  {
    // Fixed sizes matching this demo's placeholder model — a real node
    // would read these from the engine's tensor shapes (as
    // run_inference.py's Python version does) rather than hardcoding
    // them, kept simple here for a focused C++ demo.
    input_size_bytes_ = INPUT_ELEMENTS * sizeof(float);
    output_size_bytes_ = OUTPUT_ELEMENTS * sizeof(float);

    cudaMalloc(&input_device_, input_size_bytes_);
    cudaMalloc(&output_device_, output_size_bytes_);
    cudaStreamCreate(&stream_);

    context_->setTensorAddress(engine_->getIOTensorName(0), input_device_);
    context_->setTensorAddress(engine_->getIOTensorName(1), output_device_);
  }

  void on_image(const sensor_msgs::msg::Image::SharedPtr msg)
  {
    // Real preprocessing (resize, normalize, channel reorder) would
    // convert msg->data into the exact float layout the model expects,
    // then copy it into input_device_ with cudaMemcpyAsync(..., stream_)
    // before running inference below — omitted here since it depends
    // entirely on the specific model's expected input format; this demo
    // focuses on the TensorRT buffer/inference wiring itself, not
    // image preprocessing.
    (void)msg;

    std::vector<float> host_output(OUTPUT_ELEMENTS);

    context_->enqueueV3(stream_);
    cudaMemcpyAsync(host_output.data(), output_device_, output_size_bytes_,
      cudaMemcpyDeviceToHost, stream_);
    cudaStreamSynchronize(stream_);

    auto result_msg = std_msgs::msg::Float32MultiArray();
    result_msg.data = host_output;
    publisher_->publish(result_msg);
  }

  static constexpr size_t INPUT_ELEMENTS = 224 * 224 * 3;
  static constexpr size_t OUTPUT_ELEMENTS = 10;

  TrtLogger logger_;
  std::unique_ptr<nvinfer1::IRuntime> runtime_;
  std::unique_ptr<nvinfer1::ICudaEngine> engine_;
  std::unique_ptr<nvinfer1::IExecutionContext> context_;

  void * input_device_ = nullptr;
  void * output_device_ = nullptr;
  size_t input_size_bytes_ = 0;
  size_t output_size_bytes_ = 0;
  cudaStream_t stream_;

  rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr subscription_;
  rclcpp::Publisher<std_msgs::msg::Float32MultiArray>::SharedPtr publisher_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<TensorRTInferenceNode>());
  rclcpp::shutdown();
  return 0;
}
