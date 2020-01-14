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
#include <boost/python/exception_translator.hpp>

#include <MOOS/libMOOS/Comms/MOOSCommObject.h>
#include <MOOS/libMOOS/Comms/MOOSCommPkt.h>
#include <MOOS/libMOOS/Comms/XPCTcpSocket.h>
#include <MOOS/libMOOS/Utils/MOOSException.h>

#include <iostream>
#include <memory>
#include <string>

class CMOOSCommObjectProxy : public CMOOSCommObject {
public:
  CMOOSCommObjectProxy(){};
  bool ProxySendPkt(XPCTcpSocket *pSocket, CMOOSCommPkt &PktTx) {
    return SendPkt(pSocket, PktTx);
  }

  bool ProxyReadPkt(XPCTcpSocket *pSocket, CMOOSCommPkt &PktRx,
                    int nSecondsTimeOut) {
    return ReadPkt(pSocket, PktRx);
  }

  bool ProxySendMsg(XPCTcpSocket *pSocket, CMOOSMsg &Msg) {
    return SendMsg(pSocket, Msg);
  }

  bool ProxyReadMsg(XPCTcpSocket *pSocket, CMOOSMsg &Msg) {
    return ReadMsg(pSocket, Msg);
  }
};

void translate_cmoos_exception(const CMOOSException &e) {
  // Use the Python 'C' API to set up an exception object
  PyErr_SetString(PyExc_RuntimeError, e.m_sReason);
  return;
}

using namespace boost::python;

BOOST_PYTHON_MODULE(CMOOSCommObject) {

  register_exception_translator<CMOOSException>(&translate_cmoos_exception);

  object a = class_<CMOOSCommObjectProxy>("MOOSCommObject",
                                          "MOOS Communications Object.")
                 .def("SendPkt", &CMOOSCommObjectProxy::ProxySendPkt)
                 .def("ReadPkt", &CMOOSCommObjectProxy::ProxyReadPkt)
                 .def("SendMsg", &CMOOSCommObjectProxy::ProxySendMsg)
                 .def("ReadMsg", &CMOOSCommObjectProxy::ProxyReadMsg);
}
