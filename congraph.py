from neo4j import GraphDatabase


class Congraph:
    ###########################
    ### Fundamental Methods ###
    ###########################

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))


    def close(self):
        self.driver.close()


    @staticmethod
    def _reset_graph(tx):
        tx.run(
            'MATCH (n)-[r]->() DELETE n,r'
        )

        tx.run(
            'MATCH (n) DELETE n'
        )
    

    def clear_graph(self):
        with self.driver.session() as session:
            session.write_transaction(self._reset_graph)
            print(f'Finished resetting the graph!')
    

    ######################
    ### Author Methods ###
    ######################

    def update_auth_nodes(self, author):
        #  name, province, district, representative, party, term, bloc
        # TODO: if already exists - checker
        with self.driver.session() as session: 
            # 1. check if exsits, 1a create, 1b update
            session.write_transaction(self._create_author_node, author)
            print(f'Created author node: {author.name}')


    @staticmethod
    def _create_author_node(tx, author):
        tx.run(
            "MERGE (a:Author {name:$name})",
            name = author.name
            )

    def get_author():
        pass


    ########################
    ### Location Methods ###
    ########################

    # TODO: this should be based on a master list of locations; loc data should be matched to this master list
    def update_loc_nodes(self, author):
        with self.driver.session() as session: 
            session.write_transaction(
                self._create_province_node, 
                prov_name=author.province
                )
            print(f'Created province node: {author.province}')

            # TODO: add province and relationship


    @staticmethod
    def _create_province_node(tx, prov_name):
        tx.run(
            "MERGE (p:Province {name:$name})",
            name = prov_name
            )
    

    def update_loc_auth_rels(self, author):
        with self.driver.session() as session: 
            # 1. check if exsits, 1a create, 1b update
            session.write_transaction(
                self._update_loc_auth_rels, 
                auth_name=author.name,
                prov_name=author.province
                )
            print(f'Updated relationship of a:{author.name} and p:{author.province}')


    @staticmethod
    def _update_loc_auth_rels(tx, auth_name, prov_name):
        tx.run(
            'MATCH (a:Author),(p:Province) '
            'WHERE a.name = $a_name AND p.name = $p_name '
            'MERGE (a)-[:IS_REP]->(p)',
            a_name = auth_name,
            p_name = prov_name
            )



    ####################
    ### Bill Methods ###
    ####################

    def update_bill_nodes(self, bill):
        with self.driver.session() as session:
            session.write_transaction(
                self._update_bill_node, 
                bill = bill,
                )
            print(f'Created bill node: {bill.bid}')


    @staticmethod
    def _update_bill_node(tx, bill):
        tx.run(
            'MERGE (b:Bill {bid:$bid})',
            bid = bill.bid,
            )



    def update_bill_auth_rels(self, bill):
        with self.driver.session() as session:
            for auth in bill.authors_list:
                # check if auth exists in KG
                auth_exists = session.write_transaction(
                    self._check_auth_exists,
                    auth,
                )

                # create node if it does not exist
                if not auth_exists:
                    session.write_transaction(
                        self._create_author_node,
                        auth,
                    )
                    print(f'Created author node: {auth.name}')
            
                # create relationship
                session.write_transaction(
                    self._update_bill_auth_rels, 
                    bill = bill, 
                    auth = auth)
                print(f'Updated auth-bill relationships with node: {bill.bid}\n')


    @staticmethod
    def _check_auth_exists(tx, auth):
        match_result = tx.run(
            'MATCH (a:Author) '
            'WHERE a.name = $name '
            'RETURN a',
            name = auth.name #Jose Tejada
        )
        # for match in match_result:
        #     if match['name'] > 0:
        #         return True
        
        # return False
        return bool(match_result.single())


    @staticmethod
    def _update_bill_auth_rels(tx, bill, auth):
        tx.run(
            'MATCH (a:Author),(b:Bill) '
            'WHERE a.name = $name AND b.bid = $bid '
            'MERGE (a)-[:IS_AUTH]->(b) ',
            name = auth.name,
            bid = bill.bid,
            #rel = author.author_type,
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