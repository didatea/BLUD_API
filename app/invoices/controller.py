import ast
import os
from datetime import datetime, date
from multiprocessing import Process
from pathlib import Path
from flask import request, send_from_directory
from flask_restx import Resource, Namespace, fields, reqparse, inputs
from app.invoices import service as invoice
from app.invoices.service import get_valuetype
from app.utils import logger, getDatabaseSelectorUrl

api = Namespace("export", description="For dynamic Invoices get, with invoice name & dynamic parameter")
rpt_folder = 'app/invoices/rpt_files/'


def genResponse(rpt_name="yourFilename", code=None):
    responses = [
        {'status': True, 'code': 200, 'message': "Download File"},
        {'status': False, 'code': 404, 'message': "File Not Found!",
         'reason': f"Make sure the '{rpt_name}.rpt' file is exist in the folder '{rpt_folder}'"},
        {'status': False, 'code': 403.14, 'message': "Folder Not Found!",
         'reason': f"Make sure this folder exists : '{rpt_folder}'"},
        {'status': False, 'code': 404.7, 'message': "Unsupported output_type!",
         'reason': "Supported output_type = 'pdf' or 'xls' or 'csv'"},
        {'status': False, 'code': 403.10, 'message': "Failed to open the connection!",
         'reason': "Problem with database connection.Connection on params 'dataYear' selector or Connection in rpt file. Try to change 'dataYear' or verify in the rpt file"},
        {'status': False, 'code': 403.2, 'message': "Invoice Failed Connection!",
         'reason': f"Make sure the file:'{rpt_name}.rpt' have some connection to database"},
        {'status': False, 'code': 500, 'message': "Failed!.", "reason": "Failed to Generate Invoice File."}
    ]
    newResponses = {}
    for row in responses:
        if not code:
            if 'reason' in row and row['reason'] != '':
                modelDef = {
                    "status": fields.Boolean(default=row['status']),
                    "code": fields.Integer(default=row['code']),
                    "message": fields.String(default=row['message']),
                    "reason": fields.String(default=row['reason'])
                }
                newResponses[row['code']] = (
                row['message'], api.model(f"invoice_{row['code']}_response_object", modelDef))

            else:
                newResponses[row['code']] = row['message']
        else:
            for row in responses:
                if row['code'] == code:
                    new_Responses = {
                        'status': row['status'],
                        "code": row['code'],
                        'message': row['message'],
                        'reason': row['reason']
                    }
                    newResponses = new_Responses, int(str(row['code']).split('.')[0])
    return newResponses


parser = reqparse.RequestParser()
# parser.add_argument('rpt_name',
#                     type=int,
#                     default='sample',
#                     location="path",
#                     help='Name of a Report File. For testing, fill With : "sample"')
parser.add_argument('as_attachment',
                    type=inputs.boolean,
                    default="False",
                    help='get response file as attachment. For Testing set this argument = true')
parser.add_argument('dataYear',
                    type=int,
                    default=date.today().year,
                    help='set data filter by year.')
parser.add_argument('par_UNITKEY',
                    type=int,
                    default='123',
                    help='sample of dynamic param for match param @UNITKEY in rpt file. Prefix with "par_". Note: The name of param is case sensitive')
parser.add_argument('par_SAMPLE',
                    type=str,
                    default='Test',
                    help='sample of dynamic param for match param @SAMPLE in rpt file. Prefix with "par_". Note: The name of param is case sensitive')


@api.route("/<string:module_name>/<string:rpt_name>/<string:output_type>", endpoint='invoice')
class ExportRpt(Resource):
    # method_decorators = {'get': [tblUser.auth_apikey_privilege]}
    @api.doc(
        params={
            'module_name': 'Name of a module.',
            'rpt_name': 'Name of a Report File. For testing, fill With : "sample"',
            'output_type': 'Document Extension Type to Display the Report. Fill With : pdf or xls or csv',
        }
    )
    @api.doc("Get Invoice by Name.", responses=genResponse())
    @api.expect(parser)
    def get(self, module_name, rpt_name, output_type):
        if not module_name:
            return genResponse(rpt_name=rpt_name, code=404)
            
        if output_type not in ['pdf', 'xls', 'csv']:
            return genResponse(rpt_name=rpt_name, code=404.7)

        try:
            connections = os.environ.get('DATABASE_URL')
            # logger.info(connections)
            args_params_state = False
            args_params = {}
            if request.args:
                argsKeys = request.args.to_dict(flat=True)
                for row in argsKeys:
                    if row[0:4] == 'par_':
                        fixKey = row.replace("par_", "")
                        args_params[fixKey] = argsKeys[row]
                        args_params_state = True
            print(args_params)
            logger.info(rpt_folder + module_name + '/' + rpt_name + '.rpt')
            
            r = invoice.connect(rpt_folder + module_name + '/' + rpt_name + '.rpt', connections)
            
            params = invoice.get_params(r)
            if args_params_state:
                # values = invoice.get_literals(request.args.get('values'))
                values = args_params
                # logger.info(values)
                for each in params:
                    reportParamName = each.Name.replace('{', '').replace('?', '').replace('@', '').replace('}', '')
                    parType = get_valuetype(each)
                    # logger.info(reportParamName, parType)
                    # logger.info(values.get(reportParamName))
                    if values.get(reportParamName):
                        each.ClearCurrentValueAndRange()
                        if parType == 'datetime':
                            each.AddCurrentValue(datetime.fromisoformat(values.get(reportParamName, "")))
                        else:
                            each.AddCurrentValue(values.get(reportParamName, ""))
                    else:
                        if parType == 'string':
                            each.AddCurrentValue("")
                        elif parType == 'number':
                            each.AddCurrentValue(0)
                        elif parType == 'datetime':
                            each.AddCurrentValue(datetime.now())

            filename = invoice.set_exportoption(r, output_type, rpt_name)
            #logger.error('sadsadsad')
            # r.Database.Verify()
            logger.info(filename)
            r.Export(promptUser=False)
        except Exception as e:
            logger.error(e)
            #logger.error(e.excepinfo[2].split("."))[0]
            if 'Invalid directory.' in str(e):
                return genResponse(rpt_name=rpt_name, code=403.14)
            if 'Failed to open the connection.' in str(e):
                return genResponse(rpt_name=rpt_name, code=403.10)
            if 'File not found.' in str(e):
                return genResponse(rpt_name=rpt_name, code=404)
            if "-2147352567, 'Exception occurred.'" in str(e):
                return genResponse(rpt_name=rpt_name, code=403.2)
            return genResponse(rpt_name=rpt_name, code=500)
        else:
            thread = Process(target=remove_after_response, args=('app/static/invoice_output/', filename,))
            thread.start()

            return send_from_directory('static/invoice_output', filename,
                                       as_attachment=request.args.get('as_attachment') or False)


def remove_after_response(pathx, filename, current_user=None):
    files = sorted(Path(pathx).iterdir(), key=os.path.getmtime)
    files.sort(key=os.path.getctime)
    for filenamex in files[:-7]:
        os.remove(filenamex)

    # if current_user:
    #     UserActivityAdd = UserActivity(
    #         id_user=user.id,
    #         id_activityCategory=1,
    #         created_by=user.id,
    #         attributes=deviceInfo
    #     )
    #     db.session.add(UserActivityAdd)
    #     db.session.commit()


def copyf(dictlist, key, valuelist):
    return [dictio for dictio in dictlist if dictio[key] in valuelist][0]['ParamStrValue']