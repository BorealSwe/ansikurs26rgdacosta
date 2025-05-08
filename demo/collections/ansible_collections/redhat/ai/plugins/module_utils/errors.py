# -*- coding: utf-8 -*-
# Copyright: (c) 2025, XLAB Steampunk <steampunk@xlab.si>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ILabError(Exception):
    """Errors that we should catch in the main method."""


class ILabAssertionError(ILabError):
    """Errors because of bug in code"""


class ILabRunCommandError(ILabError):
    """Errors when running external program"""
