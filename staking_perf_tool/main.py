from config import properties
import os
import sys
import typer
import api

app = typer.Typer()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@app.command()
def latency(validator_count: int):
    """Say hello to a user by name."""
    typer.echo(f"Hello {validator_count}")
    print(properties.SAMPLE_SIZE)
    api.send_staking_request(validator_count)

@app.command()
def add(a: int, b: int):
    """Add two numbers."""
    typer.echo(f"The sum of {a} and {b} is {a + b}")

if __name__ == "__main__":
    app()