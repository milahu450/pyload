# -*- coding: utf-8 -*-

import re
from module.plugins.Crypter import Crypter


class MultiloadCz(Crypter):
    __name__ = "MultiloadCz"
    __version__ = "0.4"
    __type__ = "crypter"

    __pattern__ = r'http://(?:[^/]*\.)?multiload.cz/(stahnout|slozka)/.*'
    __config__ = [("usedHoster", "str", "Prefered hoster list (bar-separated) ", ""),
                  ("ignoredHoster", "str", "Ignored hoster list (bar-separated) ", "")]

    __description__ = """Multiload.cz decrypter plugin"""
    __author_name__ = "zoidberg"
    __author_mail__ = "zoidberg@mujmail.cz"

    FOLDER_PATTERN = r'<form action="" method="get"><textarea[^>]*>([^>]*)</textarea></form>'
    LINK_PATTERN = r'<p class="manager-server"><strong>([^<]+)</strong></p><p class="manager-linky"><a href="([^"]+)">'


    def decrypt(self, pyfile):
        self.html = self.load(pyfile.url, decode=True)

        if re.match(self.__pattern__, pyfile.url).group(1) == "slozka":
            found = re.search(self.FOLDER_PATTERN, self.html)
            if found is not None:
                self.urls.extend(found.group(1).split())
        else:
            found = re.findall(self.LINK_PATTERN, self.html)
            if found:
                prefered_set = set(self.getConfig("usedHoster").split('|'))
                self.urls.extend([x[1] for x in found if x[0] in prefered_set])

                if not self.urls:
                    ignored_set = set(self.getConfig("ignoredHoster").split('|'))
                    self.urls.extend([x[1] for x in found if x[0] not in ignored_set])

        if not self.urls:
            self.fail('Could not extract any links')
