#!/bin/bash

# Copyright(C) 2014, Stamus Networks
# All rights reserved
# Part of Debian SELKS scripts
# Written by Peter Manev <pmanev@stamus-networks.com>
#
# Please run on Debian
#
# This script comes with ABSOLUTELY NO WARRANTY!
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.



echo -e "\n Adjusting kernel parameters in /etc/sysctl.conf ... \n";

  if grep --quiet "### STAMUS Networks" /etc/sysctl.conf 
    then
      sed -i -e  '/### STAMUS Networks/,/### STAMUS Networks/d' /etc/sysctl.conf
  fi



echo '### STAMUS Networks ' >> /etc/sysctl.conf
echo '' >> /etc/sysctl.conf
echo 'net.core.netdev_max_backlog=250000' >> /etc/sysctl.conf
echo 'net.core.rmem_max=16777216' >> /etc/sysctl.conf
echo 'net.core.rmem_default=16777216' >> /etc/sysctl.conf
echo 'net.core.optmem_max=16777216' >> /etc/sysctl.conf
echo '' >> /etc/sysctl.conf
echo '### STAMUS Networks ' >> /etc/sysctl.conf

/sbin/sysctl -p
echo -e "\n DONE adjusting kernel parameters in /etc/sysctl.conf \n";
