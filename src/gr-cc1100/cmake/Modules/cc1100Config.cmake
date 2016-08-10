INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_CC1100 cc1100)

FIND_PATH(
    CC1100_INCLUDE_DIRS
    NAMES cc1100/api.h
    HINTS $ENV{CC1100_DIR}/include
        ${PC_CC1100_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    CC1100_LIBRARIES
    NAMES gnuradio-cc1100
    HINTS $ENV{CC1100_DIR}/lib
        ${PC_CC1100_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(CC1100 DEFAULT_MSG CC1100_LIBRARIES CC1100_INCLUDE_DIRS)
MARK_AS_ADVANCED(CC1100_LIBRARIES CC1100_INCLUDE_DIRS)

