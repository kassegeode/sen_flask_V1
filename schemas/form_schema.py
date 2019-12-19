from functools import wraps

from flask import request, jsonify
from jsonschema import Draft4Validator

schemas_degradation = {

    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://geojson.org/schema/Point.json",
    "title": "GeoJSON Point",
    "type": "object",
    "required": [
        "type",
        "coordinates"
    ],
    "properties": {
        "type": {
            "type": "string",
            "enum": [
                "Point"
            ]
        },
        "coordinates": {
            "type": "array",
            "minItems": 2,
            "items": {
                "type": "number"
            }
        },
        "bbox": {
            "type": "array",
            "minItems": 4,
            "items": {
                "type": "number"
            }
        }
    }
}

js_schemas1 = {
    "type": "object",
    "required": [
        "age"
    ],
    "properties": {
        "firstName": {
            "type": "string",
            "minLength": 2,
            "maxLength": 20
        },
        "lastName": {
            "type": "string",
            "minLength": 5,
            "maxLength": 15
        },
        "age": {
            "type": "integer",
            "minimum": 18,
            "maximum": 100
        },
        "gender": {
            "type": "string",
            "enum": [
                "Male",
                "Female",
                "Undisclosed"
            ]
        },
        "height": {
            "type": "number"
        },
        "dateOfBirth": {
            "type": "string",
            "format": "date"
        },
        "rating": {
            "type": "integer"
        },
        "committer": {
            "type": "boolean"
        },
        "address": {
            "type": "object",
            "properties": {
                "street": {
                    "type": "string"
                },
                "streetnumber": {
                    "type": "string"
                },
                "postalCode": {
                    "type": "string"
                },
                "city": {
                    "type": "string"
                }
            }
        }
    }
}

schema_degradation = {
    "schema": {
        "uuid": {
            "type": "string"
        },
        "status": {
            "type": "string",
            "title": "status",
            "enum": ["BON", "FAIBLE DEGRADATION", "FORTE DEGRADATION", "CRITIQUE", "NON TRAITEE"]
        },
        "description": {
            "type": "string",
            "title": "description",
            "format": "text",
            "description": "Veuillez Mettre ici la description ..."
        },
        "coordinates": {
            "type": "array",
            "minItems": 4,
            "items": {
                "type": "number"
            }
        }
    },
    "form": [
        {
            "key": "status",
            "titleMap": {
                "Good": "Good",
                "Low Degradation": "Low Degradation",
                "Critical": "Critical",
                "Strong degradation": "Strong degradation",
                "NOT TREATED": "NOT TREATED"
            }
        },
        {
            "key": "description"
        },
        {
            "key": "coordinates"
        },
        {
            "title": "save",
            "type": "submit"
        }
    ]

}

input_form_schema = {"schema": {
    "status": {
        "type": "string",
        "title": "status",
        "enum": ["BON", "FAIBLE DEGRADATION", "FORTE DEGRADATION", "CRITIQUE", "NON TRAITEE"]
    },

    "description": {
        "type": "string",
        "title": "description"
    }
},
    "form": [{
        "key": "status",
        "options": {
            "": "Please select",
            "BON": "BON",
            "FAIBLE DEGRADATION": "FAIBLE DEGRADATION",
            "FORTE DEGRADATION": "FORTE DEGRADATION",
            "CRITIQUE": "CRITIQUE",
            "NON TRAITEE": "NON TRAITEE"

        }
    }, {
        "key": "description"
    }, {
        "title": "Submit",
        "type": "submit"
    }]
}

input_form_schema_fr = {"schema": {
    "statut": {
        "type": "string",
        "title": "statut",
        "enum": ["BON", "FAIBLE DEGRADATION", "FORTE DEGRADATION", "CRITIQUE", "NON TRAITÉE"],
        "required": True
    },
    "description": {
        "type": "string",
        "title": "description"
    }
},
    "form": [{
        "key": "statut",
        "titleMap": {
            "BON": "BON",
            "FAIBLE DEGRADATION": "FAIBLE DEGRADATION",
            "FORTE DEGRADATION": "FORTE DEGRADATION",
            "CRITIQUE": "CRITIQUE",
            "NON TRAITÉE": "NON TRAITÉE"
        },
    }, {
        "key": "description"
    }, {
        "title": "Valider",
        "type": "submit"
    }]
}

input_form_schema_en = {"schema": {
    "status": {
        "type": "string",
        "title": "status",
        "enum": ["Good", "Low Degradation", "Strong degradation", "Critical", "NOT TREATED"],
        "required": True
    },

    "description": {
        "type": "string",
        "title": "description"
    }
},
    "form": [{
        "key": "status",
        "titleMap": {
            "Good": "Good",
            "Low Degradation": "Low Degradation",
            "Critical": "Critical",
            "Strong degradation": "Strong degradation",
            "NOT TREATED": "NOT TREATED"
        }
    }, {
        "key": "description"
    }, {
        "title": "Validated",
        "type": "submit"
    }]
}


input_form_schema_degrade = 1222


init_report_data = {
    'report_data_moz': [],
    'report_data_rec': []
}

format_report_data = {
    'FR': [],
    'EN': []
}

format_get_data = {
    'FR': {},
    'EN': {}
}


json_schemas = {
    'FR': input_form_schema_fr,
    'EN': input_form_schema_en
}
