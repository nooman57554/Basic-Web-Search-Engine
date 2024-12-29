import networkx as nx
from sqlalchemy.orm import sessionmaker
from web_crawler import Page, engine

Session = sessionmaker(bind=engine)
session = Session()

def calc_pagerank():
    pages = session.query(Page).all()
    
    Graph = nx.DiGraph()
    
    for page in pages:
        Graph.add_node(page.url)

        if page.outgoing_links:
            for link in page.outgoing_links:
                if link.startswith("http"):
                    Graph.add_edge(page.url, link)
        
    pagerank = nx.pagerank(Graph)

    for page in pages:
        if page.url in pagerank:
            page.pagerank = pagerank[page.url]
            print(f"updated pagerank for- {page.url} : {page.pagerank}")
        else:
            print(f"PageRank for {page.url} not found in PageRank calculation.")
            
    session.commit()


if __name__ == "__main__":
    calc_pagerank()

    
