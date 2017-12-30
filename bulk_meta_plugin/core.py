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

import base64
import logging

from deluge import component
from deluge._libtorrent import lt
from deluge.core.rpcserver import export
from deluge.event import DelugeEvent
from deluge.plugins.pluginbase import CorePluginBase


log = logging.getLogger(__name__)


class MetadataReceivedEvent(DelugeEvent):

    def __init__(self, torrent_id):
        self._args = [torrent_id]


class BulkMetaTrackerErrorEvent(DelugeEvent):

    def __init__(self, torrent_id, tracker_url, error_message, times_in_row,
                 status_code, error):
        self._args = [
            torrent_id, tracker_url, error_message, times_in_row,
            status_code, error]


class Core(CorePluginBase):

    def enable(self):
        self.core = component.get("Core")
        self.session = self.core.session
        self.torrents = self.core.torrentmanager.torrents
        self.pluginmanager = component.get("CorePluginManager")
        self.eventmanager = component.get("EventManager")
        self.alertmanager = component.get("AlertManager")

        self.alertmanager.register_handler(
            "metadata_received_alert", self.on_metadata_received)
        self.alertmanager.register_handler(
            "tracker_error_alert", self.on_tracker_error)

        self.pluginmanager.register_status_field(
            "bulk_meta_has_metadata", self.get_has_metadata)
        self.pluginmanager.register_status_field(
            "bulk_meta_upload_mode", self.get_upload_mode)

    def disable(self):
        self.alertmanager.deregister_handler(self.on_metadata_received)
        self.alertmanager.deregister_handler(self.on_tracker_error)

        self.pluginmanager.deregister_status_field("bulk_meta_has_metadata")
        self.pluginmanager.deregister_status_field("bulk_meta_upload_mode")

    def update(self):
        pass

    @export
    def get_metadata(self, torrent_id):
        torrent = self.torrents[torrent_id]
        if torrent.handle.has_metadata():
            ti = torrent.handle.get_torrent_info()
            return ti.metadata()

    @export
    def set_upload_mode(self, torrent_id, upload_mode):
        torrent = self.torrents[torrent_id]
        return torrent.handle.set_upload_mode(upload_mode)

    def get_has_metadata(self, torrent_id):
        torrent = self.torrents[torrent_id]
        return torrent.handle.has_metadata()

    def get_upload_mode(self, torrent_id):
        torrent = self.torrents[torrent_id]
        return torrent.handle.status().upload_mode

    def on_metadata_received(self, alert):
        torrent_id = str(alert.handle.info_hash())
        self.eventmanager.emit(MetadataReceivedEvent(torrent_id))

    def on_tracker_error(self, alert):
        try:
            torrent_id = str(alert.handle.info_hash())
            tracker_url = alert.tracker_url()
            error_message = alert.error_message()
            times_in_row = alert.times_in_row
            status_code = alert.status_code
            e = alert.error
            error = {"message": e.message(), "value": e.value()}
            self.eventmanager.emit(BulkMetaTrackerErrorEvent(
                torrent_id, tracker_url, error_message, times_in_row,
                status_code, error))
        except:
            raise
