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
Create configuration for model Cisco-IOS-XR-aaa-lib-cfg.

usage: gn-create-xr-aaa-lib-cfg-20-ydk.py [-h] [-v] device

positional arguments:
  device         gNMI device (http://user:password@host:port)

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.path import Repository
from ydk.services import CRUDService
from ydk.gnmi.providers import gNMIServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_aaa_lib_cfg \
    as xr_aaa_lib_cfg
import os
import logging


YDK_REPO_DIR = os.path.expanduser("~/.ydk/")

def config_aaa(aaa):
    """Add config data to aaa object."""
    username = aaa.usernames.Username()
    username.ordering_index = 20
    username.name = "sysadmin"
    username.secret = "$1$AQ9U$6iYrri084f6crrBmPeN0q."
    # task group
    usergroup_under_username = username.usergroup_under_usernames.UsergroupUnderUsername()
    usergroup_under_username.name = "sysadmin"
    username.usergroup_under_usernames.usergroup_under_username.append(usergroup_under_username)
    aaa.usernames.username.append(username)


if __name__ == "__main__":
    """Execute main program."""
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    parser.add_argument("device",
                        help="gNMI device (http://user:password@host:port)")
    args = parser.parse_args()
    device = urlparse(args.device)

    # log debug messages if verbose argument specified
    if args.verbose:
        logger = logging.getLogger("ydk")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                                      "%(levelname)s - %(message)s"))
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # create gNMI provider
    repository = Repository(YDK_REPO_DIR+device.hostname)
    provider = gNMIServiceProvider(repo=repository,
                                   address=device.hostname,
                                   port=device.port,
                                   username=device.username,
                                   password=device.password)
    # create CRUD service
    crud = CRUDService()

    aaa = xr_aaa_lib_cfg.Aaa()  # create object
    config_aaa(aaa)  # add object configuration

    # create configuration on gNMI device
    crud.create(provider, aaa)

    exit()
# End of script
