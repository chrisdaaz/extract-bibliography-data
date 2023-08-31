#!/usr/bin/python3

import re
import pypandoc
import yaml

class BibliographicCitation:
    """Generic bibiliographic citation data

    Attributes:
        authors(string): the author or authors of a work 
        year(int): the year of publication
        title(string): the title of the work
    """

    def __init__(self, authors, year, title):
        self.authors = authors
        self.year = year
        self.title = title

class Book(BibliographicCitation):
    """Subclass of BibliographicCitation, representing a Book citation

    Attributes:
        publisher(string): The publisher of the book
        publisher(location): The city where the book was published
    """

    def __init__(self, authors, year, title, publisher, publisher_location):
        BibliographicCitation.__init__(self, authors, year, title)
        self.publisher = publisher
        self.publisher_location = publisher_location

class JournalArticle(BibliographicCitation):
    """Subclass of BibliographicCitation, representing a journal article citation

    Attributes:
        journal_title(string): The title of the journal
        doi(string): The digital object identifier
    """

    def __init__(self, authors, year, title, journal_title, doi=None):
        BibliographicCitation.__init__(self, authors, year, title)
        self.journal_title = journal_title
        self.doi = doi

def convert(input, output):
    """
    Calls Pandoc to convert the Microsoft Word file to HTML for parsing
    """
    pypandoc.convert_file(input, 'html', extra_args=['--wrap=none'], outputfile=output)

def get_authors(entry):
    author_pattern = r'<p>(.*?)\.'
    author_match = re.search(author_pattern, entry)
    return author_match.group(1)

def get_year(entry):
    year_pattern = r'\b\d{4}\b' 
    year_match = re.search(year_pattern, entry)
    year = year_match.group()
    return year

def get_title(entry):
    article_title_pattern = r'[“”"]([^“”"]*)[“”"]'
    article_title_match = re.search(article_title_pattern, entry)
    if article_title_match:
        title = article_title_match.group(1)
        return title
    else:
        title_pattern = r'<em>(.*?)</em>'
        title_match = re.search(title_pattern, entry)
        title = title_match.group(1)
        return title
    
def get_publisher(entry):
    if check_type(entry) == "Book":
        publisher_pattern = r'([A-Za-z]+):\s([A-Za-z\s]+)\.'
        publisher_match = re.search(publisher_pattern, citation)
        if publisher_match:
            publisher_location = publisher_match.group(1)
            publisher_name = publisher_match.group(2)
            return publisher_location, publisher_name
        
def get_journal_title(entry):
    journal_title_pattern = r'<em>(.*?)</em>'
    journal_title_match = re.search(journal_title_pattern, entry)
    journal_title = journal_title_match.group(1)
    return journal_title

def get_doi(entry):
    doi_pattern = r'doi\.org/([^"]+)'
    doi_match = re.search(doi_pattern, entry)
    doi = doi_match.group(1)
    return doi

def check_type(entry):
    """
    Checks if there's a pattern in the string indicative of a journal article
    """
    journal_pattern = r'[“”"]([^“”"]*)[“”"]'
    if re.search(journal_pattern, entry):
        return "Journal"
    else:
        return "Book"
    
def get_raw_citations(file_path):
    raw_citations = []
    with open(file_path, "r") as file:
        for line in file:
            raw_citations.append(line)
        return raw_citations

bibliography_html = "./example/bibliography.html"
bibliography_docx = "./example/bibliography.docx"

convert(bibliography_docx, bibliography_html)
unstructured_citations = get_raw_citations(bibliography_html)

bib_data_list = []

for citation in unstructured_citations:
    authors = get_authors(citation)
    title = get_title(citation)
    year = get_year(citation)

    if check_type(citation) == "Journal":
        journal_title = get_journal_title(citation)
        doi = None
        article_reference = JournalArticle(authors, year, title, journal_title, doi)
        bib_data_list.append(article_reference)
    else:
        publisher_location = get_publisher(citation)[0]
        publisher = get_publisher(citation)[1]
        book_reference = Book(authors, year, title, publisher, publisher_location)
        bib_data_list.append(book_reference)

yaml_data = []

for data in bib_data_list:
    
    yaml_data.append({
        "title": data.title,
        "authors": data.authors,
        "year": data.year        
    })

with open("bibliography.yaml", "w") as yaml_file:
    yaml.dump(yaml_data, yaml_file)