cmake_minimum_required(VERSION 3.5)
project(cpr_orchard_gazebo)

find_package(ament_cmake REQUIRED)

install(DIRECTORY launch meshes rviz urdf worlds
  DESTINATION share/${PROJECT_NAME}
)

install(FILES model.config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
