from tests.cli import cli_app, cli_runner


def test_show_default_args():
    result = cli_runner.invoke(cli_app, ["download"])
    assert result.exit_code == 0
    ...
