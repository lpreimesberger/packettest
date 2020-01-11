
This is really basic Python 3 - just install the requirements.txt and run the server with python with using the
flask module.  configuration.json has the defined user names in it.

Tests are under ./tests and are plain old unittest script.  Probably need to drop and re-generate database for
each run depending.


    /connections?query=location_name&value=PDX
    Args:
        Requires http parameters:
        - query: query type in supported_queries (location_name, location_city, customer_name, connection_speed, connection_status
        - value: value to search for

    Returns:
        JSON in format { "data": [] } or http code with error.  no result is empty [] (not 404)


    /connection
    does very basic checking for valid input - not safe for multiple calls and doesnt flag duplicates
    Args:
        Requires POST body in JSON form:
            {
              "description": "Test",
              "customer_id": 1,
              "location_id": 1
            }

    Returns:
        Normal HTTP codes - invalid POST body will get a 400 from flask
