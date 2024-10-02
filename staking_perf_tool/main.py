from config import properties
import os
import sys
import typer
import api
import state
import file
import time

app = typer.Typer()

parent_file_location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_file_location)

@app.command()
def latency(validator_count: int):
    data = {
        'network': properties.NETWORK,
        'fee_recipient_address': properties.FEE_RECIPIENT_ADDRESS,
        'withdrawal_address': properties.WITHDRAWAL_ADDRESS,
        'region': properties.REGION,
        'validator_count': validator_count,
        'client_req_id': state.STATE.prefix
    }
    jwt_token = api.create_jwt_token(data, 'v1/ethereum/validators')

    for i in range(properties.SAMPLE_SIZE):
        data_copy = data.copy()
        data_copy['client_req_id'] = f'{data["client_req_id"]}_{i}'
        start_time = time.time()
        result = api.send_staking_request(data_copy, jwt_token )
        end_time = time.time()
        result_obj = state.Result(result[0], result[1], end_time-start_time)
        state.STATE.add_result(i,result_obj)
    file.generate_results(parent_file_location,'latency',state.STATE, validator_count)

@app.command()
def add(a: int, b: int):
    """Add two numbers."""
    typer.echo(f"The sum of {a} and {b} is {a + b}")

if __name__ == "__main__":
    app()