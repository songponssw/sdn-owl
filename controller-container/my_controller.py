# Copyright (C) 2016 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from operator import attrgetter

from ryu.app import simple_switch_13
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub

import time
import json
import array


class SimpleMonitor13(simple_switch_13.SimpleSwitch13):

    def __init__(self, *args, **kwargs):
        super(SimpleMonitor13, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)

    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(3)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def _switch_features_handler(self, ev):
        sw_addr = ev.msg.datapath.address
        return sw_addr
        # print("switch_features" + str(ev.msg.datapath.address))

    def _request_stats(self, datapath):
        self.logger.debug('send stats request: %016x', datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        # print(datapath.address)
        # print(datapath.is_active)

        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)

        # self.logger.info('=========================================\n')

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):

        body = ev.msg.body
        # print(body)
        self.logger.debug('Receive Message : ' +
                          time.strftime("%Y-%m-%d %H:%M:%S"))
        self.logger.debug('datapath         '
                          'in-port  eth-dst           '
                          'out-port packets  bytes')
        self.logger.debug('---------------- '
                          '-------- ----------------- '
                          '-------- -------- --------')
        for stat in sorted([flow for flow in body if flow.priority == 1],
                           key=lambda flow: (flow.match['in_port'],
                                             flow.match['eth_dst'])):
            self.logger.debug('%016x %8x %17s %8x %8d %8d',
                              ev.msg.datapath.id,
                              stat.match['in_port'], stat.match['eth_dst'],
                              stat.instructions[0].actions[0].port,
                              stat.packet_count, stat.byte_count)

    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev):
        body = ev.msg.body
        # sw = ev.msg.datapath.address
        # print (sw)
        # print(body)
        # print(json.dumps(body))

        
        for stat in ev.msg.body:
            ports = []
            x = []
            ports.append('port_no=%d '
                         'rx_packets=%d tx_packets=%d '
                         'rx_bytes=%d tx_bytes=%d '
                         'rx_dropped=%d tx_dropped=%d '
                         'rx_errors=%d tx_errors=%d '
                         'rx_frame_err=%d rx_over_err=%d rx_crc_err=%d '
                         'collisions=%d duration_sec=%d duration_nsec=%d ' %
                         (stat.port_no,
                          stat.rx_packets, stat.tx_packets,
                          stat.rx_bytes, stat.tx_bytes,
                          stat.rx_dropped, stat.tx_dropped,
                          stat.rx_errors, stat.tx_errors,
                          stat.rx_frame_err, stat.rx_over_err,
                          stat.rx_crc_err, stat.collisions,
                          stat.duration_sec, stat.duration_nsec))
            # ports = ports.append('sw_ip=%s ' % str(ev.msg.datapath.address))
            x.append('PortStats: %s '
                     'ip_switch: %s '
                     'time: %s' %
                     (ports,
                      str(ev.msg.datapath.address[0]),
                      time.strftime("%Y-%m-%d %H:%M:%S.%f"[:-3])
                      ))
            # return json
            print(json.dumps(x))
        
        # print(json.dumps(ports))
        # x = 'PortStats: %s',ports
        # print(ports)
        # x = []
    def addToInflux(host='db', port=8086):
        """Instantiate a connection to the InfluxDB."""
        user = 'root'
        password = 'root'
        dbname = 'ovs1'
        dbuser = 'smly'
        dbuser_password = 'my_secret_password'
        # query = 'select * from cpu_load_short;'
        json_body = [
            {
                "measurement": "ovs1",
                "tags": {
                    "host": "ovs01",
                    "region": "us-west"
                },
                "fields": {
                    "ofport_1": 0.64,
                    "ofport_2": 3,
             
                }
            }
        ]

        client = InfluxDBClient(host, port, user, password, dbname)

        # print("Create database: " + dbname)
        # client.create_database(dbname)

        # print("Create a retention policy")
        # client.create_retention_policy('awesome_policy', '3d', 3, default=True)

        print("Switch user: " + dbuser)
        client.switch_user(dbuser, dbuser_password)

        print("Write points: {0}".format(json_body))
        client.write_points(json_body)

        # print("Querying data: " + query)
        # result = client.query(query)

        print("Result: {0}".format(result))

    
