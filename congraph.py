from neo4j import GraphDatabase

class Congraph:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))


    def close(self):
        self.driver.close()


    def update_author(self, author):
        #  name, province, district, representative, party, term, bloc
        # TODO: if already exists - checker
        with self.driver.session() as session: 
            # 1. check if exsits, 1a create, 1b update
            session.write_transaction(self._create_author, author)
            print(f'Created author node: {author.name}')

    def _check_author():
        pass

    @staticmethod
    def _create_author(tx, author):
        tx.run(
            "MERGE (a:Author {name:$name})",
            name = author.name
            )


    def update_bill(self, bill):
        with self.driver.session() as session:
            session.write_transaction(self._create_bill, bill)
            print(f'Created bill node: {bill.bid}')
    
            session.write_transaction(self._update_bill_relationships, bill)
            print(f'Updated relationships with node: {bill.bid}')

    @staticmethod
    def _create_bill(tx, bill):
        tx.run(
            "MERGE (b:Bill {bid:$bid})",
            # "SET b.bid = $bid",
            bid = bill.bid
            )

    @staticmethod
    def _update_bill_relationships(tx, bill):
        for name in bill.mapped_authors:
            tx.run(
                'MATCH (a:Author),(b:Bill) '
                'WHERE a.name = $name AND b.bid = $bid '
                'MERGE (a)-[:IS_AUTHOR]->(b)',
                name = name,
                bid = bill.bid
                )



    # def _update_author(tx, author):
    #     pass


    # def print_greeting(self, message):
    #     with self.driver.session() as session:
    #         greeting = session.write_transaction(self._create_and_return_greeting, message)
    #         print(greeting)


    # @staticmethod
    # def _create_and_return_greeting(tx, message):
    #     result = tx.run("CREATE (a:Greeting) "
    #                     "SET a.message = $message "
    #                     "RETURN a.message + ', from node ' + id(a)", message=message)
    #     return result.single()[0]


if __name__ == "__main__":
    greeter = Congraph("bolt://localhost:7687", "neo4j", "test")
    greeter.print_greeting("hello, world")
    greeter.print_greeting("TRIAL")
    greeter.close()