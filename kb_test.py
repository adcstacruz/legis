from neo4j import GraphDatabase

class Congraph:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))


    def close(self):
        self.driver.close()


    def update_author(self, author):

        #  name, province, district, representative, party, term, bloc
        with self.driver.session() as session: 
            session.write_transaction(self._create_author, author)
            print('created author!!!')

    def _check_author():
        pass

    @staticmethod
    def _create_author(tx, author):
        tx.run(
            "CREATE (a:Author)"
            "SET a.name = $name",
            name = author.name
            )

    def _update_author(tx, author):
        pass


    def print_greeting(self, message):
        with self.driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]


if __name__ == "__main__":
    greeter = Congraph("bolt://localhost:7687", "neo4j", "test")
    greeter.print_greeting("hello, world")
    greeter.print_greeting("TRIAL")
    greeter.close()