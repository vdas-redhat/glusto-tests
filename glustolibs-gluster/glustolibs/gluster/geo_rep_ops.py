#  Copyright (C) 2017-2018  Red Hat, Inc. <http://www.redhat.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
   Description: Library for gluster geo-replication operations
"""

from glusto.core import Glusto as g


def create_shared_storage(mnode):
    """Create shared volume which is necessary for the setup of
       a geo-rep session

    Args:
        mnode(str): Node on which command is to be executed

    Returns:
        tuple: Tuple containing three elements (ret, out, err).
            The first element 'ret' is of type 'int' and is the return value
            of command execution.

            The second element 'out' is of type 'str' and is the stdout value
            of the command execution.

            The third element 'err' is of type 'str' and is the stderr value
            of the command execution.

    """
    cmd = "gluster volume set all cluster.enable-shared-storage enable"
    return g.run(mnode, cmd)


def georep_createpem(mnode):
    """ Creates a common pem pub file on all the nodes in the master and
        is used to implement the passwordless SSH connection
    Args:
        mnode (str): Node on which cmd is to be executed
    Returns:
        tuple: Tuple containing three elements (ret, out, err).
            The first element 'ret' is of type 'int' and is the return value
            of command execution.

            The second element 'out' is of type 'str' and is the stdout value
            of the command execution.

            The third element 'err' is of type 'str' and is the stderr value
            of the command execution.

    """
    cmd = "gluster system:: execute gsec_create"
    return g.run(mnode, cmd)


def georep_create(mnode, mastervol, slaveip, slavevol, user=None, force=False):
    """Pushes the keys to all the slave nodes and creates a geo-rep session
    Args:
        mnode (str) : Node on which cmd is to be executed
        mastervol (str) : The name of the mastervol
        slaveip (str): SlaveIP
        slavevol (str) The name of the slave volume
    kwargs:
        force (bool): If this option is set to True, then create geo-rep
            session will be executed with the force option.
            If it is set to False, then the geo-rep session is created
            without the force option
        user (str): If not set, the default is a root-user
            If specified, non-root user participates in the geo-rep
            session

    Returns:
        tuple: Tuple containing three elements (ret, out, err).
            The first element 'ret' is of type 'int' and is the return value
            of command execution.

            The second element 'out' is of type 'str' and is the stdout value
            of the command execution.

            The third element 'err' is of type 'str' and is the stderr value
            of the command execution.

    """
    if user:
        if force:
            cmd = "gluster volume geo-replication %s %s@%s::%s create push-pem \
                   force" % (mastervol, user, slaveip, slavevol)
        else:
            cmd = "gluster volume geo-replication %s %s@%s::%s create \
                   push-pem" % (mastervol, user, slaveip, slavevol)
    else:
        if force:
            cmd = "gluster volume geo-replication %s %s::%s create push-pem \
                   force" % (mastervol, slaveip, slavevol)
        else:
            cmd = "gluster volume geo-replication %s %s::%s create \
                   push-pem" % (mastervol, slaveip, slavevol)
    return g.run(mnode, cmd)
