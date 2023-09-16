# SPDX-FileCopyrightText: 2023-present Alex Wicks <alex@awicks.io>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
CLI arguments.

Arguments are declared here,
to make re-using them across multiple commands easier.
"""

import typer

DEFAULT_ARCH = "amd64"
arch = typer.Option(
    "--arch", "-a",
    rich_help_panel="Image",
    help="""
    CPU architecture to fetch
    """,
)

DEFAULT_PLATFORM = "generic"
platform = typer.Option(
    "--platform", "-p",
    rich_help_panel="Image",
    help="""
    Platform to use - image type pulled will be dictated by this
    """,
)

# Empty string denotes using the default image type for the platform
# See the `Platform` class - the first value of each tuple is the default.
DEFAULT_IMAGE_TYPE = ""
image_type = typer.Option(
    "--image-type", "-t",
    rich_help_panel="Image",
    help="""
    Specify which image type is desired for platforms with more than one type
    """
)

DEFAULT_VERSION = "latest"
version = typer.Option(
    "--version", "-v",
    rich_help_panel="Image",
    help="""
    OS version to fetch
    """,
)
