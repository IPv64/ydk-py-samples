#!/usr/bin/env python
#
# Copyright 2016 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Encode configuration for model Cisco-IOS-XE-native.

usage: cd-encode-xe-native-router-ospf-34-ydk.py [-h] [-v]

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.services import CodecService
from ydk.providers import CodecServiceProvider
from ydk.models.cisco_ios_xe import Cisco_IOS_XE_native \
    as xe_native
from ydk.types import Empty
import logging


def config_native(native):
    """Add config data to native object."""
    # OSPF process
    ospf = native.router.Ospf()
    ospf.id = 172
    ospf.router_id = "172.16.255.1"

    ospf.passive_interface.interface = "Loopback0"

    network = ospf.Network()
    network.ip = "172.16.0.0"
    network.mask = "0.0.0.255"
    network.area = 0

    ospf.network.append(network)

    network = ospf.Network()
    network.ip = "172.16.1.0"
    network.mask = "0.0.0.255"
    network.area = 1

    ospf.network.append(network)

    # OSPF stub Area
    area = ospf.Area()
    area.id = 1
    stub = area.Stub()
    stub.no_summary = Empty()
    area.stub = stub
    ospf.area.append(area)

    native.router.ospf.append(ospf)


if __name__ == "__main__":
    """Execute main program."""
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    args = parser.parse_args()

    # log debug messages if verbose argument specified
    if args.verbose:
        logger = logging.getLogger("ydk")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                                      "%(levelname)s - %(message)s"))
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # create codec provider
    provider = CodecServiceProvider(type="xml")

    # create codec service
    codec = CodecService()

    native = xe_native.Native()  # create object
    config_native(native)  # add object configuration

    # encode and print object
    print(codec.encode(provider, native))

    exit()
# End of script