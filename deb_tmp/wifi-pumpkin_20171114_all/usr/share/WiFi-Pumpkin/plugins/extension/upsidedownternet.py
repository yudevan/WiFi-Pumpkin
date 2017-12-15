import io
from PIL import Image
from plugins.extension.plugin import PluginTemplate

"""
Description:
    This program is a core for wifi-pumpkin.py. file which includes functionality
    plugins for Pumpkin-Proxy.

Copyright:
    Copyright (C) 2015-2016 Marcos Nesster P0cl4bs Team
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
"""


class upsidedownternet(PluginTemplate):
    meta = {
        'Name'      : 'upsidedownternet',
        'Version'   : '1.0',
        'Description' : 'flip image from website request mitmproxy ',
        'Author'    : 'from mitmproxy scripts'
    }
    def __init__(self):
        for key,value in self.meta.items():
            self.__dict__[key] = value
        self.ConfigParser = False
    def request(self, flow):
        pass

    def response(self, flow):
        if flow.response.headers.get("content-type", "").startswith("image"):
            try:
                s = io.StringIO(flow.response.content)
                img = Image.open(s).rotate(180)
                s2 = io.StringIO()
                img.save(s2, "png")
                flow.response.content = s2.getvalue()
                flow.response.headers["content-type"] = "image/png"
                self.send_output.emit('[{}][*] flip image from website request'.format(self.Name))
            except:  # Unknown image types etc.
                pass