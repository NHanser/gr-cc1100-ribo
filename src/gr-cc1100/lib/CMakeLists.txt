# Copyright 2011,2012 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

########################################################################
# Setup library
########################################################################
include(GrPlatform) #define LIB_SUFFIX

include_directories(${Boost_INCLUDE_DIR})
link_directories(${Boost_LIBRARY_DIRS})

list(APPEND cc1100_sources
    cc1100_packet_decoder_impl.cc
)

set(cc1100_sources "${cc1100_sources}" PARENT_SCOPE)
if(NOT cc1100_sources)
	MESSAGE(STATUS "No C++ sources... skipping lib/")
	return()
endif(NOT cc1100_sources)

add_library(gnuradio-cc1100 SHARED ${cc1100_sources})
target_link_libraries(gnuradio-cc1100 ${Boost_LIBRARIES} ${GNURADIO_ALL_LIBRARIES})
set_target_properties(gnuradio-cc1100 PROPERTIES DEFINE_SYMBOL "gnuradio_cc1100_EXPORTS")

if(APPLE)
    set_target_properties(gnuradio-cc1100 PROPERTIES
        INSTALL_NAME_DIR "${CMAKE_INSTALL_PREFIX}/lib"
    )
endif(APPLE)

########################################################################
# Install built library files
########################################################################
install(TARGETS gnuradio-cc1100
    LIBRARY DESTINATION lib${LIB_SUFFIX} # .so/.dylib file
    ARCHIVE DESTINATION lib${LIB_SUFFIX} # .lib file
    RUNTIME DESTINATION bin              # .dll file
)

########################################################################
# Build and register unit test
########################################################################
include(GrTest)

include_directories(${CPPUNIT_INCLUDE_DIRS})

list(APPEND test_cc1100_sources
    ${CMAKE_CURRENT_SOURCE_DIR}/test_cc1100.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/qa_cc1100.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/qa_cc1100_packet_decoder.cc
)

add_executable(test-cc1100 ${test_cc1100_sources})

target_link_libraries(
  test-cc1100
  ${GNURADIO_RUNTIME_LIBRARIES}
  ${Boost_LIBRARIES}
  ${CPPUNIT_LIBRARIES}
  gnuradio-cc1100
)

GR_ADD_TEST(test_cc1100 test-cc1100)
