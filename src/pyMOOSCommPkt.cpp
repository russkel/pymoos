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
#pragma warning(disable : 4503)
#endif

#include <boost/python.hpp>

#include <MOOS/libMOOS/Comms/MOOSCommPkt.h>
#include <MOOS/libMOOS/Comms/MOOSMsg.h>
#include <MOOS/libMOOS/Utils/MOOSPlaybackStatus.h>
#include <MOOS/libMOOS/Utils/MOOSUtils.h>

#include <assert.h>
#include <cstring>
#include <iostream>

using namespace boost::python;

bool Serialize(CMOOSCommPkt &Pkt, PyObject *obj, bool bToStream = true,
               bool bNoNULL = false, double *pdfPktTime = NULL);
bool Serialize(CMOOSCommPkt &Pkt, PyObject *obj, bool bToStream, bool bNoNULL,
               double *pdfPktTime) {

  if (bToStream) {
    boost::python::object o(boost::python::borrowed(obj));

    std::size_t n = len(o);
    MOOSMSG_LIST List;

    for (unsigned int i = 0; i < n; i++) {
      CMOOSMsg a = extract<CMOOSMsg>(o[i]);
      List.push_back(a);
    }

    return (Pkt.Serialize(List, bToStream, bNoNULL, pdfPktTime));
  } else {
    MOOSMSG_LIST List;

    if (Pkt.Serialize(List, bToStream, bNoNULL, pdfPktTime)) {
      boost::python::list pylist;

      size_t s = List.size();

      for (unsigned int i = 0; i < s; i++) {
        pylist.append(List.front());
        PyList_Insert(obj, i, object(List.front()).ptr());
        List.pop_front();
      }

      return true;
    } else
      return false;
  }

  return false;
}

BOOST_PYTHON_MODULE(CMOOSCommPkt) {
  class_<CMOOSCommPkt>("CMOOSCommPkt", "MOOS Packet Class.")
      .def("Serialize", &Serialize)
      .def("GetStreamLength", &CMOOSCommPkt::GetStreamLength)
      .def("GetBytesRequired", &CMOOSCommPkt::GetBytesRequired);
}
