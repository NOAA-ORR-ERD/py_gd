cmake_minimum_required(VERSION 3.15...4.0)
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

find_library (libgd
              gd
              REQUIRED
              )
message (STATUS "libgd found at ${libgd}")

find_path (gd_include_path
           "gd.h"
           REQUIRED)

message (STATUS "gd.h found at ${gd_include_path}")

cython_transpile(py_gd/py_gd.pyx
   LANGUAGE C
   OUTPUT_VARIABLE py_gd_c)

python_add_library(py_gd MODULE "${py_gd_c}" WITH_SOABI)
target_link_libraries(py_gd PUBLIC "${libgd}" Python::NumPy)
target_include_directories(py_gd PUBLIC "${gd_include_path}")
install(TARGETS py_gd DESTINATION py_gd)


cython_transpile(py_gd/spline.pyx LANGUAGE C OUTPUT_VARIABLE spline_c)

python_add_library(spline MODULE "${spline_c}" WITH_SOABI)
target_link_libraries(spline PUBLIC Python::NumPy)
install(TARGETS spline DESTINATION py_gd)


