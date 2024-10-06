from config import properties
import os
import sys
import typer
import api
import state
import file
import time
import asyncio

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


    print(jwt_token)
    for i in range(properties.SAMPLE_SIZE):
        data_copy = data.copy()
        data_copy['client_req_id'] = f'{data["client_req_id"]}_{i}'
        start_time = time.time()
        result = api.send_staking_request(data_copy, jwt_token )
        end_time = time.time()
        result_obj = state.Result(result[0], result[1], end_time-start_time)
        state.STATE.add_result(i,result_obj)
    file.generate_results(parent_file_location,'latency',state.STATE, validator_count)



async def send_staking_requests_async(data:dict, jwt_token: str, index: int):
    start_time = time.time()
    local_time = time.localtime(start_time)
    print(f'Started sending msg {index} at time {time.strftime("%y%m%d %H%M%S",local_time)}.{int((start_time - int(start_time)) * 1000)}')
    result = await api.send_staking_request_async(data, jwt_token )
    end_time = time.time()
    local_time = time.localtime(end_time)
    #print(f'Ended Processing msg {index} at time {time.strftime("%y%m%d %H%M%S", local_time)}.{int((end_time - int(end_time)) * 1000)}')
    result_obj = state.Result(result[0], result[1], end_time-start_time)
    state.STATE.add_result(index,result_obj)


async def throughput_async(msgs_per_min:int):
    data = {
        'network': properties.NETWORK,
        'fee_recipient_address': properties.FEE_RECIPIENT_ADDRESS,
        'withdrawal_address': properties.WITHDRAWAL_ADDRESS,
        'region': properties.REGION,
        'validator_count': properties.THROUGHPUT_TEST_VALIDATOR_COUNT,
        'client_req_id': state.STATE.prefix
    }
    jwt_token = api.create_jwt_token(data, 'v1/ethereum/validators')
    sleep_time = 60/msgs_per_min

    running_tasks = []
    # Launch each task, then sleep between launching them
    for i in range(properties.SAMPLE_SIZE):
        data_copy = data.copy()
        data_copy['client_req_id'] = f'{data["client_req_id"]}_{i}'
        task = asyncio.create_task(send_staking_requests_async(data_copy, jwt_token, i))
        running_tasks.append(task)
        await asyncio.sleep(sleep_time)  # Sleep before launching the next task
    
    # Gather results after all tasks have been launched
    results = await asyncio.gather(*running_tasks)
    
    file.generate_results(parent_file_location,'throughput',state.STATE, properties.THROUGHPUT_TEST_VALIDATOR_COUNT, msgs_per_min)
    

@app.command()
def throughput(msgs_per_min:int):
    asyncio.run(throughput_async(msgs_per_min))
   

if __name__ == "__main__":
    app()