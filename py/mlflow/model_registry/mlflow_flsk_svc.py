from flask import Flask, jsonify, request
import os
import mlflow
from mlflow.tracking import MlflowClient

app = Flask(__name__)
API_CALLS = ["/api/listModels, /api/help, "
             "/api/deleteModel/<model_name>,"
             "/api/echoJson"]


@app.route('/api/help')
def help():
   return jsonify(result=API_CALLS)

@app.route('/')
def hello():
   # greet the user
   return (f"Hello {os.getlogin()}! To get the list of REST endpoints, use '/api/help'")

@app.route('/api/listModels')
def list_models():

   # Get a list of all registered models
   lst = None
   for rm in client.list_registered_models():
      lst = [(f"run_id={mv.run_id}",f"status={mv.current_stage}",
          f"version={mv.version}", f"name={mv.name}") for mv in rm.latest_versions]

   res = jsonify(result=lst) if lst is not None else jsonify(result="Registry Empty")
   return res

@app.route('/api/deleteModel/<string:model_name>')
def delete_model(model_name=None):

   if model_name is None:
      return "Model name not specified"

   print(f"Deleting model {model_name} and all its versions and data")

   client.delete_registered_model(model_name)
   return f"Model {model_name} deleted!"

@app.route('/api/echoJson', methods=['POST'])
def echo_json():
   # use curl to send POST request
   # curl -X POST -H 'Content-Type: application/json' http://127.0.0.1:5000/api/echoJson -d '{"name": "Alice"}'
    data = request.get_json()
    # ... do your business logic, and return some response
    # e.g., below we're just echo-ing back the received JSON data
    return jsonify(data)

# main driver function
if __name__ == '__main__':
   # set the registry path and creat MLflowClient
   local_registry = "sqlite:///mlruns.db"
   mlflow.set_tracking_uri(local_registry)
   client = MlflowClient()
   # run() method of Flask class runs the application
   # on the local development server.
   app.run()
