from typer.testing import CliRunner
from modernizer.main import app
from modernizer.strategies.reactive import WebFluxStrategy

runner = CliRunner()

def test_help_command():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Interactive Migration Pipeline" in result.stdout

def test_strategy_detection():
    # Test our logic without needing the CLI
    strategy = WebFluxStrategy()
    code = "public class MyVerticle extends AbstractVerticle"
    assert strategy.needs_migration(code) is True
    
    clean_code = "public class MyService"
    assert strategy.needs_migration(clean_code) is False