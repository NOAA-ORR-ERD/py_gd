find_package(PkgConfig)
if(PKG_CONFIG_FOUND)
  pkg_check_modules(PC_GD QUIET GD)
endif()

find_path(GD_INCLUDE_DIR
  NAMES gd.h
  HINTS "${PC_GD_INCLUDE_DIRS}"
  REQUIRED
)

find_library(GD_LIBRARY
  NAMES gd
  HINTS "${PC_GD_INCLUDE_DIRS}"
  REQUIRED
)

cmake_path(ABSOLUTE_PATH GD_LIBRARY)
cmake_path(ABSOLUTE_PATH GD_INCLUDE_DIR)

message (STATUS "libgd found at ${GD_LIBRARY}, ${GD_INCLUDE_DIR}")

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(GD
  REQUIRED_VARS
    GD_LIBRARY
    GD_INCLUDE_DIR
  VERSION_VAR GD_VERSION
)

if(GD_FOUND)
  set(GD_LIBRARIES "${GD_LIBRARY}")
  set(GD_INCLUDE_DIRS "${GD_INCLUDE_DIR}")
  set(Foo_DEFINITIONS ${PC_GD_CFLAGS_OTHER})
endif()

if(GD_FOUND AND NOT TARGET GD::GD)
  add_library(GD::GD UNKNOWN IMPORTED)
  set_target_properties(GD::GD PROPERTIES
    IMPORTED_LOCATION "${GD_LIBRARY}"
    INTERFACE_COMPILE_OPTIONS "${PC_GD_CFLAGS_OTHER}"
    INTERFACE_INCLUDE_DIRECTORIES "${GD_INCLUDE_DIR}"
  )
endif()

mark_as_advanced(
  GD_INCLUDE_DIR
  GD_LIBRARY
)

