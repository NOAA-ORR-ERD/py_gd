include_guard(GLOBAL)

include(ExternalProject)

set(DEP_INSTALL_DIR ${CMAKE_BINARY_DIR}/_deps/install)
ExternalProject_Add(
  libpng_ep
  URL http://prdownloads.sourceforge.net/libpng/libpng-1.6.50.tar.gz?download
  URL_HASH SHA256=708f4398f996325819936d447f982e0db90b6b8212b7507e7672ea232210949a
  CMAKE_ARGS
    "-DCMAKE_INSTALL_PREFIX=${DEP_INSTALL_DIR}"
)

set(GD_LIBRARIES "${DEP_INSTALL_DIR}/${CMAKE_INSTALL_LIBDIR}/libgd${CMAKE_SHARED_LIBRARY_SUFFIX}")
set(GD_INCLUDE_DIR "${DEP_INSTALL_DIR}/include")

ExternalProject_Add(
  GD_ep
  GIT_REPOSITORY https://github.com/libgd/libgd.git
  GIT_TAG gd-2.3.3
  BUILD_BYPRODUCTS
    "${GD_LIBRARIES}"
    "${GD_INCLUDE_DIR}"
  CMAKE_ARGS
    "-DCMAKE_INSTALL_PREFIX=${DEP_INSTALL_DIR}"
    -DENABLE_PNG=1
)
add_library(GD::GD SHARED IMPORTED GLOBAL)
file(MAKE_DIRECTORY "${GD_INCLUDE_DIR}")
set_target_properties(GD::GD PROPERTIES
  IMPORTED_LOCATION "${GD_LIBRARIES}"
  INTERFACE_INCLUDE_DIRECTORIES "${GD_INCLUDE_DIR}"
)
add_dependencies(GD_ep libpng_ep)
add_dependencies(GD::GD GD_ep)
