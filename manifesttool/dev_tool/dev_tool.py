# ----------------------------------------------------------------------------
# Copyright 2019-2020 Pelion
#
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------------

import argparse
import enum
import logging
import sys

from manifesttool import __version__
from manifesttool.dev_tool.actions import create
from manifesttool.dev_tool.actions import init, update
from manifesttool.mtool.asn1.v1 import ManifestAsnCodecV1
from manifesttool.mtool.asn1.v3 import ManifestAsnCodecV3

logger = logging.getLogger('manifest-dev-tool')


class DevActions(enum.Enum):
    INIT = 'init'

    CREATE = 'create'
    CREATE_V1 = 'create-v1'

    UPDATE = 'update'
    UPDATE_V1 = 'update-v1'


def get_parser():
    parser = argparse.ArgumentParser(
        description='FOTA developer flow helper'
    )

    actions_parser = parser.add_subparsers(dest='action')
    actions_parser.required = True

    init_parser = actions_parser.add_parser(
        DevActions.INIT.value,
        help='Create a Pelion Device management update certificate.'
    )
    init.register_parser(init_parser)

    create_parser = actions_parser.add_parser(
        DevActions.CREATE.value,
        help='Helper tool for creating a manifest using manifest schema '
             'version v3.',
        add_help=False
    )
    create.register_parser(create_parser, ManifestAsnCodecV3.get_name())

    create_parser = actions_parser.add_parser(
        DevActions.CREATE_V1.value,
        help='Helper tool for creating a manifest using manifest schema '
             'version v1.',
        add_help=False
    )
    create.register_parser(create_parser, ManifestAsnCodecV1.get_name())

    update_parser = actions_parser.add_parser(
        DevActions.UPDATE.value,
        help='Perform Pelion Device management update operations using '
             'manifest schema version v3.',
        add_help=False
    )
    update.register_parser(update_parser, ManifestAsnCodecV3.get_name())

    update_parser = actions_parser.add_parser(
        DevActions.UPDATE_V1.value,
        help='Perform Pelion Device management update operations using '
             'manifest schema version v1',
        add_help=False
    )
    update.register_parser(update_parser, ManifestAsnCodecV1.get_name())

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Show exception info on error.'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='Manifest-Tool version {}'.format(__version__)

    )

    return parser


def entry_point(argv=sys.argv[1:]):  # pylint: disable=dangerous-default-value
    logging.basicConfig(
        stream=sys.stdout,
        format='%(asctime)s %(levelname)s %(message)s',
        level=logging.INFO
    )
    parser = get_parser()
    args = parser.parse_args(argv)

    if args.debug:
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)

    try:
        action = DevActions(args.action)

        if action == DevActions.INIT:
            init.entry_point(args)
        # ---------------------------------------------------------------------
        elif action == DevActions.CREATE:
            create.entry_point(args, ManifestAsnCodecV3)
        elif action == DevActions.CREATE_V1:
            create.entry_point(args, ManifestAsnCodecV1)
        # ---------------------------------------------------------------------
        elif action == DevActions.UPDATE:
            update.entry_point(args, ManifestAsnCodecV3)
        elif action == DevActions.UPDATE_V1:
            update.entry_point(args, ManifestAsnCodecV1)
        # ---------------------------------------------------------------------
        else:
            raise AssertionError('unknown action')
    except Exception as ex:  # pylint: disable=broad-except
        logger.error(
            str(ex),
            exc_info=args.debug
        )
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(entry_point())
