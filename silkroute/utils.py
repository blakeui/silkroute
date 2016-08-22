# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:

import glob
from os import remove


def clean_temp(name=None):
    if not name:
        map(remove, glob.glob("/tmp/silkroute-*.db"))
    else:
        map(remove, glob.glob(name))
