from typer.testing import CliRunner

from cloud_latest.cli.commands import app

cli_app = app
cli_runner = CliRunner()
