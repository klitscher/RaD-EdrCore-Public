import csv
import neo4j
import re
import sys


path = sys.argv[1]
loadCsv = 'LOAD CSV WITH HEADERS FROM $path AS row\n'
dbCreds = ('neo4j', 'yhack2019')
dbUrl = 'bolt://localhost:7687'
pattern = re.compile(
    r'^\s*' +
    r'(\d+(\s+\d+/\d+)?)\s+' +
    r'([\w\s]+?)' +
    r'(\s+\#\s*([\w-]+))?' +
    r'\s*$',
    re.VERBOSE
)


def makeIndexes(session):
    session.run('CREATE CONSTRAINT ON (o:Occupant) ASSERT o.id IS UNIQUE')
    session.run('CREATE CONSTRAINT ON (s:State) ASSERT s.name IS UNIQUE')
    session.run('CREATE CONSTRAINT ON (y:Year) ASSERT y.year IS UNIQUE')
    session.run('CREATE CONSTRAINT ON (z:ZipCode) ASSERT z.code IS UNIQUE')
    session.run('CREATE INDEX ON :City(name)')
    session.run('CREATE INDEX ON :Street(name)')
    session.run('CREATE INDEX ON :House(number)')
    session.run('CREATE INDEX ON :Unit(number)')


if __name__ == '__main__':
    db = neo4j.Driver(dbUrl, auth=dbCreds)
    with db.session() as session:
        makeIndexes(session)
        query = loadCsv + 'WITH row WHERE row.State IS NOT NULL\n'
        query += 'MERGE (:State {name: row.State})'
        session.run(query, {'path': path})
        print('loaded states')
        query = loadCsv + 'WITH row WHERE row.City IS NOT NULL\n'
        query += 'MERGE (:City {name: row.City})'
        session.run(query, {'path': path})
        print('loaded cities')
        query = loadCsv + 'WITH row WHERE row.State IS NOT NULL AND row.City IS NOT NULL\n'
        query += 'MATCH (s:State {name: row.State})\n'
        query += 'MATCH (c:City {name: row.City})\n'
        query += 'MERGE (s)-[:CONTAINS]->(c)'
        session.run(query, {'path': path})
        print('joined states and cities')
        query = loadCsv + 'WITH row WHERE row.ZipCode IS NOT NULL\n'
        query += 'MERGE (:ZipCode {code: row.ZipCode})'
        session.run(query, {'path': path})
        print('loaded zip codes')
        query = loadCsv + 'WITH row WHERE row.ZipCode IS NOT NULL AND row.City IS NOT NULL\n'
        query += 'MATCH (c:City {name: row.City})\n'
        query += 'MATCH (z:ZipCode {code: row.ZipCode})\n'
        query += 'MERGE (c)-[:CONTAINS]->(z)'
        session.run(query, {'path': path})
        print('joined zip codes and cities')
        
