import functions_framework
from OrchestadorProc1 import Orchestador1
from OrchestadorProc2 import Orchestador2

@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'data' in request_json and 'proc' in request_json:
        data = request_json['data']
        proceso = request_json['proc']

    elif request_args and 'data' in request_args and 'proc' in request_args:
        data = request_args['data']
        proceso = request_args['proc']

    else:
        return f'Not Found\n'
    
    try:
        if(proceso == 1):
            return Orchestador1(data)
            
        elif(proceso == 2):
            return Orchestador2(data)
        
        else:
            return f'Proceso {proceso}not found'

    except Exception as e:
        return f'Error: {e}'
