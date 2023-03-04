from bs4 import BeautifulSoup

def detectAbstractParagraph(response):
    
    # # Parse the TEI XML response using BeautifulSoup 
    soup = BeautifulSoup(response.text, "xml")
    
    # find the abstract element
    abstract_element = soup.find('abstract')

    # extract the text content of the abstract element
    abstract_text = abstract_element.text.strip()

    print("Abstract "+"\n\n"+abstract_text)
    
    paragraphs_list=[]
    #Find the paragrph text inside <p> element
    paragraphs = soup.find_all("p")

    for paragraph in paragraphs:
        paragraphs_list.append(paragraph.get_text())

    #Concat the abstract and paragraph text
    paraText =  str(abstract_text) + ("\n\n").join(paragraphs_list)
    
    return abstract_text,paraText