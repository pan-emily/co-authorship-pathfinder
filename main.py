#!/usr/bin/python
from scholarly import scholarly 
from collections import deque 
from coauthor_scraper import get_coauthors, id_to_name, get_exhaustive_coauthors
from datetime import datetime

def traverse(author_id, target_id, publication_limit, maximum_depth, k):
    seen_ids = set()

    queue = deque([(author_id, [id_to_name(author_id)])])
    # queue = deque([(author_id, [author_id])])

    seen_ids.add(author_id)
    
    while queue:
        author, path = queue.popleft()
        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        print(path)

        if author == target_id:
            print('found')
            return path 
        
        if len(path) > maximum_depth:
            print("maximum depth exceeded; aborting path")
            return 
        
        # coauthors = get_exhaustive_coauthors(author, publication_limit, k)
        coauthors = get_coauthors(author, publication_limit, k)
        if not coauthors:
            coauthors = get_exhaustive_coauthors(author, publication_limit, k)
        if not coauthors:
            return 
        
        for coauthor in coauthors:
            if coauthor not in seen_ids:
                seen_ids.add(coauthor)
                queue.append((coauthor, path+[id_to_name(coauthor)]))
                # queue.append((coauthor, path+[coauthor]))

    print("not found")

def main():
    # author_name = "Eric Mazumdar"
    author_id = "FZOxxvcAAAAJ"
    # target_id = "LVPkbeYAAAAJ" # 1 person away 
    target_id = "4bahYMkAAAAJ"

    maximum_depth = 20
    publication_limit = 3
    k = 5

    found = traverse(author_id, target_id, publication_limit, maximum_depth, k)
    
    # turn this into actual people names 
    # path = [id_to_name(auth) for auth in found]

    f = open("eric_rudolf_path2.txt", "a")
    f.write(", ".join(found))
    f.close()

if __name__ == '__main__':
  main()