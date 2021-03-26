regexes = {
    'email': "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])",
    'password': "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}",
}

validation_scheme = {
    # 'GET': {
    #     'uinfo': {
    #
    #     },
    #     'interests-list': {
    #         'user_id': int
    #     },
    #     'user-interests': {},
    #     'hometown': {},
    #     'trips': {}
    #
    # },
    'POST': {
        'login': {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "pattern": regexes['email']
                },
                "password": {
                    "type": "string",
                    "pattern": regexes['password']

                },

            },
            "required": ["email", "password"]
        },
        'signup': {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "pattern": regexes['email']
                },
                "password": {
                    "type": "string",
                    "pattern": regexes['password']
                },

            },
            "required": ["email", "password"]
        },
    }
    #     'signup2': {
    #         'user_id': int,
    #         'firstname': basestring,
    #         'surname': basestring,
    #         'occupation': basestring,
    #         'gender': basestring,
    #         'homecity': basestring
    #
    #     },
    #     'user-interests': {
    #         'user_id': int,
    #         'interests': [basestring]
    #     },
    #     'trips': {
    #         'user_id': int,
    #         'city_id': int,
    #         'start_date': basestring,
    #         'end_date': basestring
    #     }
    #
    # },
    # 'PUT': {
    #     'trips': {
    #         'user_id': int,
    #         'city_id': int,
    #         'start_date': basestring,
    #         'end_date': basestring,
    #         'trip_id': int
    #     }
    #
    # },
    # 'DELETE': {
    #     'user-interests': {},
    #     'trips': {}
    # }
}
