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
"""CLI for uplink utility."""

import time

import click

from uplink.log import Logger
from uplink.util import sync

logger = Logger()


@click.group()
def cli():
    """Specify the top-level CLI object."""
    pass


@cli.command()
@click.option('--local_path', '-l', 'local_path', required=True,
              help='Local path to sync.')
@click.option('--remote_path', '-r', required=True,
              help='Remote bucket to which to sync data.')
@click.option('--sleep_time', '-f', default=30,
              help=('The inter-retry duration, in seconds, with which to '
                    'perform a sync.'))
def main(local_path, remote_path, sleep_time):
    """Specify the primary run loop."""
    logger.info('Starting uplink.')
    while True:
        sync(local_path, remote_path)
        logger.info('sleeping %s seconds before retry' % sleep_time)
        time.sleep(sleep_time)
