import typer
from rich import print as pprint
from typing_extensions import Annotated

from cloud_latest.cli import args
from cloud_latest.net.mirror import Mirror
from cloud_latest.simplestreams.processor import StreamProcessor

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)


def main() -> None:
    app()


@app.callback()
def help_msg():
    """
    My helpful heredoc.
    """


def _get_url(version, platform, image_type, arch) -> str:
    mirror = Mirror()

    processor_args = {}
    processor_args["version"] = version
    processor_args["platform"] = platform
    processor_args["image_type"] = image_type
    processor_args["arch"] = arch
    processor = StreamProcessor(mirror.stream, **processor_args)

    return mirror.get_download_url(processor.download)


@app.command()
def show(
    version: Annotated[str, args.version] = args.DEFAULT_VERSION,
    platform: Annotated[str, args.platform] = args.DEFAULT_PLATFORM,
    image_type: Annotated[str, args.image_type] = args.DEFAULT_IMAGE_TYPE,
    arch: Annotated[str, args.arch] = args.DEFAULT_ARCH,
) -> None:
    pprint(_get_url(version, platform, image_type, arch))


@app.command()
def download(
    version: Annotated[str, args.version] = args.DEFAULT_VERSION,
    platform: Annotated[str, args.platform] = args.DEFAULT_PLATFORM,
    image_type: Annotated[str, args.image_type] = args.DEFAULT_IMAGE_TYPE,
    arch: Annotated[str, args.arch] = args.DEFAULT_ARCH,
) -> None:
    url = _get_url(version, platform, image_type, arch)  # pyright:ignore  # noqa: F841
    ...
