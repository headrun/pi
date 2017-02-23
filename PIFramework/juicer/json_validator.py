import os
import json
import jsonschema
from jsonschema import Draft4Validator

def get_validator_obj():
        par_dir = os.path.abspath(os.pardir)
        json_file_path = os.path.join(par_dir, 'scripts/availability_info_schema.json')
        jf = open(json_file_path)
        validator = Draft4Validator(json.loads(jf.read()))
        jf.close()

        return validator

def validate_json_record(rec):
        status = True
        validator = get_validator_obj()

        try:
            validator.validate(rec)
        except (jsonschema.ValidationError, jsonschema.SchemaError) as e:
            status = False
            print str(e.message)

        return status
