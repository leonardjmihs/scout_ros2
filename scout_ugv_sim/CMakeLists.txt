cmake_minimum_required(VERSION 3.5)
project(scout_ugv_sim)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)

install(DIRECTORY launch worlds params
  DESTINATION share/${PROJECT_NAME}/)
ament_export_dependencies(ros_gz_bridge)
ament_export_dependencies(ros_gz_sim)
ament_package()
