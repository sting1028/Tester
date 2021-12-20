from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
from pathlib import Path
from datetime import datetime
from run_case import main, list_case_name
from flash_mcu import flashMcu
import click
import os,logging,sys,json


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version="0.1", title="Case Execution API", description="Case Execution API for Acqer",)

ns = api.namespace("Cexer", path='/api/Cexer/',description="Case Execution API for Acqer")

status = api.model(
    "status", {"status": fields.String(required=True, description="The status of case running")}
)

case = api.model(
    "case", {"case": fields.String(required=True, description="The name of case")}
)

run_cases = api.model(
    "run_cases",
    {
        "case": fields.Nested(case, description="cases name"),
    },
)

def log_config(debug):
    date_time = datetime.now().strftime('%Y.%m%d.%H%M')
    log_folder = Path('log/')
    print(log_folder.exists())
    if not log_folder.exists():
        log_folder.mkdir()
    log_filename = f"{Path(f'log/{date_time}')}.log"
    if debug:
        lev = logging.DEBUG
    else:
        lev = logging.INFO
    logging.basicConfig(
        level=lev,
        format=
        '{asctime} - {levelname} - {name} - {lineno} - {funcName} ::: {message}',
        filename=log_filename,
        style='{')
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

@click.command()
@click.option(
    '--debug',
    default=False,
    help='set debug for log more infomation',
    is_flag=True,
)
def start(debug):
    log_config(debug)
    app.run(host="0.0.0.0", port=8383, debug=debug)

@ns.route("/v1/case")
class Runcase(Resource):
    # @api.expect(status)
    def get(self):
        """Get supported case name"""
        try:
            response = list_case_name()
        except Exception as e:
                logger.error(f'Error occurred:{e}')
                api.abort(502, e)
        else:
            return response


    @api.expect(run_cases)
    def post(self):
        """Run a case or cases"""
        try:
            case = request.json['case']['case']
            response = main(case_name=case)
        except Exception as e:
                logger.error(f'Error occurred:{e}')
                api.abort(502, e)
        else:
            return response

@ns.route("/v1/flash")
class Flash(Resource):
    # @api.expect(status)
    def post(self):
        """Run a case or cases"""
        try:
            response = flashMcu()
        except Exception as e:
                logger.error(f'Error occurred:{e}')
                api.abort(502, e)
        else:
            return response



if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    start()
    
