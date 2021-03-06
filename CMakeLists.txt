CMAKE_MINIMUM_REQUIRED(VERSION 3.10)
project(pymoos)

set(CMAKE_PROJECT_HOMEPAGE_URL "https://github.com/russkel/pymoos")
set(CMAKE_PROJECT_VERSION_MAJOR 2020)
set(CMAKE_PROJECT_VERSION_MINOR 2)
set(CMAKE_PROJECT_VERSION_PATCH 0)

set(default_build_type "Debug")

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  message(STATUS "Setting build type to '${default_build_type}' as none was specified.")
  set(CMAKE_BUILD_TYPE "${default_build_type}" CACHE
      STRING "Choose the type of build." FORCE)
  # Set the possible values of build type for cmake-gui
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS
    "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

if (CMAKE_VERSION LESS 3.12)
    # to support older cmake versions that don't have FindPython3
    find_package(PythonInterp 3.6 REQUIRED)
    find_package(PythonLibs 3.6 REQUIRED)
    find_package(Boost COMPONENTS python${PYTHON_VERSION_MAJOR} REQUIRED)
    set(PYMOOS_LIB_DEPS Boost::python${PYTHON_VERSION_MAJOR} MOOS::MOOS ${PYTHON_LIBRARIES})
    set(Python3_SITELIB "/usr/lib/python3/dist-packages")  # if this doesn't work for you, upgrade your damn cmake!
    set(Python3_VERSION ${PYTHON_VERSION_STRING})
    include_directories(${PYTHON_INCLUDE_DIRS})
else()
    include(FindPython3)
    find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
    find_package(Boost COMPONENTS python${Python3_VERSION_MAJOR}${Python3_VERSION_MINOR} REQUIRED)
    set(PYMOOS_LIB_DEPS Boost::python${Python3_VERSION_MAJOR}${Python3_VERSION_MINOR} MOOS::MOOS Python3::Python)
endif()


MESSAGE(STATUS "Python: ${Python3_VERSION} SITELIB: ${Python3_SITELIB}")

set( CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/bin )
set( CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/lib )
set( CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/lib )

IF(WIN32)
    ADD_DEFINITIONS(-DWINDOWS_NT -D_CRT_SECURE_NO_DEPRECATE -D_SCL_SECURE_NO_DEPRECATE)
ENDIF(WIN32)

IF(UNIX)
    ADD_DEFINITIONS(-DUNIX)
    IF("${CMAKE_SYSTEM_NAME}" MATCHES "Darwin")
        ADD_DEFINITIONS( -DPLATFORM_DARWIN )

        #some support for macport installed libraries
        SET(CMAKE_LIBRARY_PATH ${CMAKE_LIBRARY_PATH} /opt/local/lib)
        SET(CMAKE_INCLUDE_PATH ${CMAKE_INCLUDE_PATH} /opt/local/include)
        MESSAGE(STATUS "Cmake library path ${CMAKE_LIBRARY_PATH}")

        SET( PLATFORM_DARWIN 1 )
    ENDIF("${CMAKE_SYSTEM_NAME}" MATCHES "Darwin")
    IF("${CMAKE_SYSTEM_NAME}" MATCHES "Linux")
        ADD_DEFINITIONS( -DPLATFORM_LINUX )
        SET( PLATFORM_LINUX 1 )
    ENDIF("${CMAKE_SYSTEM_NAME}" MATCHES "Linux")
ENDIF(UNIX)

SET(Boost_USE_STATIC_LIBS OFF)
SET(Boost_USE_MULTITHREADED ON)
SET(Boost_USE_STATIC_RUNTIME OFF)

FIND_PACKAGE(MOOS 10.5 REQUIRED)

ADD_LIBRARY(CMOOSMsg SHARED src/pyMOOSMsg.cpp)
TARGET_LINK_LIBRARIES(CMOOSMsg ${PYMOOS_LIB_DEPS})
SET_TARGET_PROPERTIES(CMOOSMsg PROPERTIES PREFIX "") # remove 'lib' prefix

ADD_LIBRARY(XPCTcpSocket SHARED src/pyXPCTcpSocket.cpp)
TARGET_LINK_LIBRARIES(XPCTcpSocket ${PYMOOS_LIB_DEPS})
SET_TARGET_PROPERTIES(XPCTcpSocket PROPERTIES PREFIX "")

ADD_LIBRARY(CMOOSCommPkt SHARED src/pyMOOSCommPkt.cpp)
TARGET_LINK_LIBRARIES(CMOOSCommPkt ${PYMOOS_LIB_DEPS})
SET_TARGET_PROPERTIES(CMOOSCommPkt PROPERTIES PREFIX "")

ADD_LIBRARY(CMOOSCommObject SHARED src/pyMOOSCommObject.cpp)
TARGET_LINK_LIBRARIES(CMOOSCommObject ${PYMOOS_LIB_DEPS})
SET_TARGET_PROPERTIES(CMOOSCommObject PROPERTIES PREFIX "")

file(COPY python/MOOSCommClient.py DESTINATION ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})

INSTALL(FILES
    python/MOOSCommClient.py
    python/__init__.py
    ${CMAKE_BINARY_DIR}/lib/CMOOSCommObject.so
    ${CMAKE_BINARY_DIR}/lib/CMOOSCommPkt.so
    ${CMAKE_BINARY_DIR}/lib/CMOOSMsg.so
    ${CMAKE_BINARY_DIR}/lib/XPCTcpSocket.so
    DESTINATION ${Python3_SITELIB}/pymoos/
)

set(CPACK_PACKAGE_CONTACT "russ@rw.id.au")
set(CPACK_DEBIAN_PACKAGE_SHLIBDEPS ON)
include(CPack)
