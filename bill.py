class BillList:
    def __init__(self):
        pass


class Bill:
    def __init__(self, congress, file_path):
        self.file_path = file_path
        self.congress = congress
        self.authors = None
        
        with open(file_path, 'r') as bill:
            self.bill_texts = bill.read().split('\n')

        self._extract_bill_id()
        self._extract_description()
        self._extract_short_title()
        self._extract_authors()
        self._process_authors()
    
    def _extract_bill_id(self):
        for bill_text in self.bill_texts:
            bid = re.findall(bid_pattern, bill_text)[0]
            if bid:
                self.bid = bid
                return
            
        # TODO: trigger push to bin
        return None 

    
    def _extract_description(self):
        # TODO: this might be faulty, check this in the future
        self.description = self.bill_texts[1]
        return 

    
    def _extract_short_title(self):
        for bill_text in self.bill_texts:
            try: 
                key, value = bill_text.split(':')
            except:
                continue
            
            if key in short_title_keys:
                self.short_title = value.strip()
                return
            
        # TODO: trigger push to bin
        return None 
    
    
    def _extract_authors(self):
        for bill_text in self.bill_texts:
            try:
                key, authors = bill_text.split(':')
            except:
                continue
            
            if key in author_keys:
                authors = authors.split(';')
                self.raw_authors = list(map(str.strip, authors))
                return
            
        # TODO: trigger push to bin
        return None 


    # CHANGE PROCESS AUTHORS
    def _process_authors(self):
        authors = []
        for author in self.raw_authors:
            authors.append(Author(author, self.congress))
        
        self.authors = authors