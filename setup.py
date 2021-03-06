#
# -*- coding: utf-8 -*-#

# Copyright (C) 2016 AllSeeingEyeTolledEweSew <allseeingeyetolledewesew@protonmail.com>
#
# Basic plugin template created by:
# Copyright (C) 2008 Martijn Voncken <mvoncken@gmail.com>
# Copyright (C) 2007-2009 Andrew Resch <andrewresch@gmail.com>
# Copyright (C) 2009 Damien Churchill <damoxc@gmail.com>
# Copyright (C) 2010 Pedro Algarvio <pedro@algarvio.me>
#
# This file is part of YATFS and is licensed under GNU General Public License 3.0, or later, with
# the additional special exception to link portions of this program with the OpenSSL library.
# See LICENSE for more details.
#

from setuptools import setup, find_packages

__plugin_name__ = "BulkMetaRpc"
__author__ = "AllSeeingEyeTolledEweSew"
__author_email__ = "allseeingeyetolledewesew@protonmail.com"
__version__ = "1.0.0"
__url__ = "https://github.com/AllSeeingEyeTolledEweSew/Deluge-BulkMeta-Helper-Plugin"
__license__ = "GPLv3"
__description__ = "Helper plugin for the BTN bulk metadata downloader."

setup(
    name=__plugin_name__,
    version=__version__,
    description=__description__,
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    license=__license__,

    packages=find_packages(),

    entry_points="""
    [deluge.plugin.core]
    %(plugin_name)s = %(plugin_module)s:CorePlugin
    """ % dict(plugin_name=__plugin_name__, plugin_module="bulk_meta_plugin")
)
