"""Module to set up a database in neo4j"""
from neo4j import GraphDatabase


def createDb(uri, usr, pwd):
    """Function to create a neo4j database
    uri: local machine with designated port from neo4j
    user: your username
    password: your password

    Note - I have no idea why I needed to split the relationship
    creation into three separate queries, but trying to do them at once 
    just does not work, this way did. 
    """

    uri = 'bolt://127.0.0.1:7687'
    user = 'neo4j'
    password = 'root'

    driver = GraphDatabase.driver(uri, auth=(user, password))
    nodeCreate = """
        load csv with headers from 'file:///OccupantAddresses_CT_NewHaven_2005.csv' as row
        with row.State as state, row.City as city,  row.Occupant as occupant, row.Address as address, toInteger(row.ZipCode) as zipcode, toInteger(row.phone) as phone
        where occupant is not NULL
        merge (s: State {name: state})
        merge (c: City {name: city})
        merge (a: Address {street: address})
        merge (o: Occupant {tenant: occupant})
        """
    stateCityRel = """
        load csv with headers from 'file:///OccupantAddresses_CT_NewHaven_2005.csv' as row
        match (s: State {name: row.State})
        match (c: City {name: row.City})
        merge (s)-[:CONTAIN]->(c)
        """
    cityAddRel = """
        load csv with headers from 'file:///OccupantAddresses_CT_NewHaven_2005.csv' as row
        match (c: City {name: row.City})
        match (a: Address {street: row.Address})
        merge (c)-[:HAS]->(a)
        """
    addOccRel = """
        load csv with headers from 'file:///OccupantAddresses_CT_NewHaven_2005.csv' as row
        match (a: Address {street: row.Address})
        match (o: Occupant {tenant: row.Occupant})
        merge (o)-[:RESIDES_IN]->(a)
        """
    with driver.session() as conn:
        conn.run('CREATE CONSTRAINT ON (s:State) ASSERT s.name IS UNIQUE')
        conn.run('CREATE CONSTRAINT ON (c:City) ASSERT c.name IS UNIQUE')
        conn.run('CREATE CONSTRAINT ON (z:ZipCode) ASSERT z.zipcode IS UNIQUE')
        conn.run(nodeCreate)
        conn.run(stateCityRel)
        conn.run(cityAddRel)
        conn.run(addOccRel)
