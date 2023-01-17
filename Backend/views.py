import datetime
import json

from app import app
from flask_cors import cross_origin
from flask import request
from service import Service

@app.route('/api/optimize', methods=['GET', 'POST'])
@cross_origin()
def optimize():
    #Service().optimize('1',3,[])
    data = json.loads(request.data.decode())
    print()
    default = data['optimization']
    default = '1' if default == 0 else str(default)

    num= data['number_power_plants']
    num = 3 if num == 0 else num


    print(data['graph'])
    changed_values = [] if data['graph'] == '' else data['graph'].split(',')

    changed_values = [int(item) for item in changed_values]

    flag = data['linear_approximtation']

    result = Service.optimize(default,num,changed_values,flag)

    return {'message' : result}


