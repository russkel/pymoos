///////////////////////////////////////////////////////////////////////////
//
//   pyMOOS - An interface to the Mission Oriented Operating Suite  - see
//   http://www.robots.ox.ac.uk/~mobile/MOOS/wiki/pmwiki.php
//
//   This program is free software; you can redistribute it and/or
//   modify it under the terms of the GNU General Public License as
//   published by the Free Software Foundation; either version 2 of the
//   License, or (at your option) any later version.
//
//   This program is distributed in the hope that it will be useful,
//   but WITHOUT ANY WARRANTY; without even the implied warranty of
//   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
//   General Public License for more details.
//
//   You should have received a copy of the GNU General Public License
//   along with this program; if not, write to the Free Software
//   Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
//   02111-1307, USA.
//
//////////////////////////    END_GPL    //////////////////////////////////

#ifdef _WIN32
#pragma warning(disable : 4786)
#endif

#include <boost/python.hpp>

#include <MOOS/libMOOS/Comms/MOOSMsg.h>
#include <MOOS/libMOOS/Utils/MOOSException.h>
#include <MOOS/libMOOS/Utils/MOOSPlaybackStatus.h>
#include <MOOS/libMOOS/Utils/MOOSUtils.h>

#include <cmath>
#include <cstring>
#include <iomanip>
#include <iostream>
#include <sstream>

using namespace boost::python;

BOOST_PYTHON_MODULE(CMOOSMsg) {
  class_<CMOOSMsg>("MOOSMsg", "MOOS Message Class.")
      .def(init<char, std::string, double, double>())
      .def(init<char, std::string, std::string, double>())
      .def("IsDataType", &CMOOSMsg::IsDataType)
      .def("IsDouble", &CMOOSMsg::IsDouble)
      .def("IsString", &CMOOSMsg::IsString)
      .def("IsBinary", &CMOOSMsg::IsBinary)
      .def("IsSkewed", &CMOOSMsg::IsSkewed)
      .def("IsYoungerThan", &CMOOSMsg::IsYoungerThan)
      .def("IsType", &CMOOSMsg::IsType)
      .def("GetBinaryDataSize", &CMOOSMsg::GetBinaryDataSize)
      .def("GetTime", &CMOOSMsg::GetTime)
      .def("GetDouble", &CMOOSMsg::GetDouble)
      .def("GetString", &CMOOSMsg::GetString,
           return_value_policy<copy_const_reference>())
      //.def("GetBinaryData", &CMOOSMsg::GetBinaryData,
      //     return_internal_reference<>())
      .def("GetKey", &CMOOSMsg::GetKey,
           return_value_policy<copy_const_reference>())
      .def("GetName", &CMOOSMsg::GetName,
           return_value_policy<copy_const_reference>())
      .def("GetSource", &CMOOSMsg::GetSource,
           return_value_policy<copy_const_reference>())
      .def("GetSourceAux", &CMOOSMsg::GetSourceAux,
           return_value_policy<copy_const_reference>())
      .def("GetCommunity", &CMOOSMsg::GetCommunity,
           return_value_policy<copy_const_reference>())
      .def("GetAsString", &CMOOSMsg::GetAsString)
      .def("Trace", &CMOOSMsg::Trace)
      .def("SetSourceAux", &CMOOSMsg::SetSourceAux)
      .def("SetDouble", &CMOOSMsg::SetDouble)

      // Attributes
      .def_readwrite("m_dfVal", &CMOOSMsg::m_dfVal)
      .def_readwrite("m_sSrc", &CMOOSMsg::m_sSrc)
      .def_readwrite("m_sKey", &CMOOSMsg::m_sKey);
}
