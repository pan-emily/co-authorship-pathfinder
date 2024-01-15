from scholarly import scholarly, ProxyGenerator
from cachetools import cached, TTLCache


cache = TTLCache(maxsize=100, ttl=86400)
pg = ProxyGenerator()
# success = pg.FreeProxies()
success = pg.ScraperAPI(API_KEY)

scholarly.use_proxy(pg)

print('proxy complete')


def get_coauthors(author_id, publication_limit, k):
    """
    Gets all k coauthors from Google Scholar's Coauthors sidebar. 
    """
    author = scholarly.search_author_id(author_id, publication_limit=publication_limit)
    coauthors = [auth['scholar_id'] for auth in scholarly.fill(author, sections=['coauthors'], publication_limit=publication_limit)['coauthors']]
    return coauthors[:k]

def get_exhaustive_coauthors(author_id, publication_limit, k):
    """
    Gets all coauthors in the first publication_limit publications.

    TODO: limit to k coauths
    """
    try:
        author = scholarly.search_author_id(author_id, publication_limit=publication_limit)
        titles = [pub['bib']['title'] for pub in scholarly.fill(author, sections=['publications'], publication_limit=publication_limit)['publications']]
        # titles = ['Perception of physical stability and center of mass of 3D objects']
        coauthors = set() 
        for title in titles:
            authors = scholarly.search_single_pub(title)
            auths = [auth for auth in scholarly.fill(authors, sections=['author_id'], publication_limit=1)['author_id']]
            for a in auths:
                coauthors.add(a)
        return coauthors
    except:
        return None

    
def id_to_name(author_id):
    author = scholarly.search_author_id(author_id)
    return author['name']

# author_id = "FZOxxvcAAAAJ"
# print(get_exhaustive_coauthors(author_id, 3, 10))






