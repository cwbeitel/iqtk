#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 The Regents of the University of California
#
# Licensed under the BSD-3-clause license (the "License"); you may not
# use this file except in compliance with the License.
# You are provided a copy of the license in LICENSE.md at the root of
# this project.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Service runner entrypoint for """

import unittest
from inquiry.services import run

class IQTKRegistryTest(unittest.TestCase):

    def test_get_registry(self):
        """By calling runs check that defined services are valid."""
        run.get_iqtk_registry()
