cmake_minimum_required(VERSION 3.24...4.0)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C)

option(BUILD_DEPS OFF)

find_package(
  Python
  COMPONENTS Interpreter Development.Module NumPy
  REQUIRED)

include(UseCython)
include(GNUInstallDirs)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/cmake")

if(ENV{VCPKG_ROOT})
  message(STATUS "VCPKG_ROOT: $ENV{VCPKG_ROOT}")
  set(CMAKE_TOOLCHAIN_FILE "$env{VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake")
endif()

# We do not use FetchContent because the CMakeLists of GD is terrible
if(BUILD_DEPS)
    include(BuildGD)
else()
    find_package(GD MODULE REQUIRED)
endif()

cython_transpile(py_gd/py_gd.pyx LANGUAGE C OUTPUT_VARIABLE py_gd_c)
python_add_library(py_gd MODULE "${py_gd_c}" WITH_SOABI)
target_link_libraries(py_gd PUBLIC GD::GD Python::NumPy)
install(TARGETS py_gd DESTINATION py_gd)

get_filename_component(GD_LIBRARY_DIR "${GD_LIBRARIES}" DIRECTORY)
set_target_properties(py_gd PROPERTIES INSTALL_RPATH "${GD_LIBRARY_DIR}")

cython_transpile(py_gd/spline.pyx LANGUAGE C OUTPUT_VARIABLE spline_c)
python_add_library(spline MODULE "${spline_c}" WITH_SOABI)
target_link_libraries(spline PUBLIC Python::NumPy)
install(TARGETS spline DESTINATION py_gd)


