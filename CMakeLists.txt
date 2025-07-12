cmake_minimum_required(VERSION 3.20...4.0)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C)

find_package(
  Python
  COMPONENTS Interpreter Development.Module NumPy
  REQUIRED)
include(UseCython)

# FetchContent_Declare(
#   gd
#   URL https://github.com/libgd/libgd/releases/download/gd-2.3.3/
#   URL_HASH stuff
# )

# FetchContent_MakeAvailable(gd)

set(CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/cmake")

find_package(GD
             MODULE
             REQUIRED
             )
cython_transpile(py_gd/py_gd.pyx
   LANGUAGE C
   OUTPUT_VARIABLE py_gd_c)

python_add_library(py_gd MODULE "${py_gd_c}" WITH_SOABI)
target_link_libraries(py_gd PUBLIC GD::GD Python::NumPy)
install(TARGETS py_gd DESTINATION py_gd)

get_filename_component(GD_LIBRARY_DIR "${GD_LIBRARIES}" DIRECTORY)
set_target_properties(py_gd PROPERTIES INSTALL_RPATH "${GD_LIBRARY_DIR}")

cython_transpile(py_gd/spline.pyx LANGUAGE C OUTPUT_VARIABLE spline_c)

python_add_library(spline MODULE "${spline_c}" WITH_SOABI)
target_link_libraries(spline PUBLIC Python::NumPy)
install(TARGETS spline DESTINATION py_gd)


