# -*- coding: UTF-8 -*-
import json
import psycopg2 as psycopg2
from flask import logging, request, Flask, Response


# there are frameworks for this - but request is to be basic as possible - plain old flask
app = Flask(__name__)
the_connection: psycopg2 = None
the_log = logging.create_logger(app)
THE_VERSION: float = 1.00
# let the server optimize instead of bunches of joins in code - these tables are full of scans anyway
# but this would a bunch of ugly SQL without
CREATE_TEMP_VIEW = """
create temporary view denormalize as
select distinct customer.id as customer_id,
    customer.name as customer_name,
    connection.id as connection_id,
    connection.descripton as connection_description,
    location.id as location_id,
    location.name as location_name,
    location.city as location_city,
    (select value from connection_attribute
     where connection_attribute.connection_id=connection.id and connection_attribute.name='speed') as connection_speed,
    (select value from connection_attribute
     where connection_attribute.connection_id=connection.id and connection_attribute.name='status') as connection_status,
    (select value from connection_attribute
     where connection_attribute.connection_id=connection.id and connection_attribute.name='maintenance') as connection_maintenance
    from connection, customer, location, connection_attribute
where connection.customer_id = customer.id and connection.location_id = location.id
"""


@app.route('/connections', methods=['GET'])
def connections():
    """Connection query handler - real world there's a jwt or auth decorator and preflight for CORS
    /connections?query=location_name&value=PDX
    Args:
        Requires http parameters:
        - query: query type in supported_queries (location_name, location_city, customer_name, connection_speed, connection_status
        - value: value to search for

    Returns:
        JSON in format { "data": [] } or http code with error.  no result is empty [] (not 404)
    """
    supported_queries = {
        "location_name": "SELECT * from denormalize where location_name = %s;",
        "location_city": "SELECT * from denormalize where location_city = %s;",
        "customer_name": "SELECT * from denormalize where customer_name = %s;",
        "connection_speed": "SELECT * from denormalize where connection_speed = %s;",
        "connection_status": "SELECT * from denormalize where connection_status = %s;"}
    query = request.args.get("query")
    value = request.args.get("value")
    if query is None or value is None:
        return Response("Missing parameters - query and value are required", status=400)
    if query not in supported_queries.keys():
        return Response("invalid query value", status=400)
    # no ORM - being simple - not a fan of sqlalchemy anyway
    cursor = the_connection.cursor()
    print(supported_queries[query], value)
    # not a typo, really need a tuple for param
    cursor.execute(supported_queries[query], (value,))
    rows = cursor.fetchall()
    return_value = []
    for row in rows:
        print(row)
        return_value.append({"customer_id": row[0], "customer_name": row[1], "connection_id": row[2],
                             "connection_description": row[3], "location_id": row[4], "location_name": row[5],
                             "location_city": row[6]})
    cursor.close()
    # you can't send arrays - that's a browser hijack vector - wrap in an object
    return {"data": return_value}


@app.route('/connection', methods=['POST'])
def add_connection():
    """Connection add handler - real world there's a jwt or auth decorator and preflight for CORS
    does very basic checking for valid input - not safe for multiple calls
    Args:
        Requires POST body in JSON form:
            {
              "description": "Test",
              "customer_id": 1,
              "location_id": 1
            }

    Returns:
        Normal HTTP codes - invalid POST body will get a 400 from flask
    """

    content = request.get_json()  # we just let the key exceptions return 500
    # this is hokey - the database should enforce this or we should have values from the jwt
    cursor = the_connection.cursor()
    cursor.execute("SELECT * from customer where id=%s", (str(content["customer_id"]),))
    rows = cursor.fetchall()
    if len(rows) == 0:
        return Response("Invalid customer_id", status=400)
    cursor.close()
    cursor = the_connection.cursor()
    cursor.execute("SELECT * from location where id=%s", (str(content["location_id"]),))
    rows = cursor.fetchall()
    if len(rows) == 0:
        return Response("Invalid location_id", status=400)
    cursor.close()
    cursor = the_connection.cursor()
    # this is really ghetto - the database isn't set up right, should have autoincrement on
    cursor.execute("SELECT max(id)+1 from connection")
    rows = cursor.fetchone()
    print(rows)
    cursor = the_connection.cursor()
    cursor.execute("INSERT INTO connection(id,descripton,customer_id,location_id) values(%s,%s,%s,%s)",
                   (str(rows[0]), str(content["description"]), str(content["customer_id"]), str(content["location_id"]),))
    the_connection.commit()
    cursor.close()
    return {"data": "success"}


# it's annoying to not know what version is running someplace
the_log.debug("Starting PacketFabric 'Test' %.02f", THE_VERSION)
# grab the config, yaml and includes can introduce random code or bugs
# ini and xml are annoying to parse and can have weird chars (BOM) included if people use
# the wrong editors.   just let it fail since trace is self-explanatory for devop guys :)
with open("configuration.json", "rt") as file_handle:
    the_configuration = json.load(file_handle)
try:
    the_log.debug("Connecting to postgresql %s@%s", the_configuration["host"], the_configuration["user"])
    the_connection = psycopg2.connect(
        host=the_configuration["host"],
        database=the_configuration["database"],
        user=the_configuration["user"],
        password=the_configuration["password"])
    cur = the_connection.cursor()
    # there are a lot of joins, preoptimize and remove the spaghetti queries
    cur.execute(CREATE_TEMP_VIEW)
    the_connection.commit()
    cur.close()
except (Exception, psycopg2.DatabaseError) as error:
    the_log.fatal(str(error))
    raise
the_log.debug("Starting listener...")
if __name__ == "__main__":
    app.run()
