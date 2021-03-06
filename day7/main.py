import re
from collections import defaultdict
from functools import lru_cache

def part_one(filename='input.txt', target='shiny gold'):
    
    # Simple directed graph stored with out edges as a list at each node
    graph = defaultdict(list)
    
    for line in open(filename):
        # First get rid of the word bag(s) since the pluralization will just
        # cause headaches and then split on the word contain
        tokens = line.replace('bags', 'bag').replace('bag', '').split('contain')
        
        container = tokens[0].strip()
        
        for item in tokens[1].split(','):
            contained_in = re.sub('[0-9]|\.', '', item).strip()
            graph[contained_in].append(container)
    
    things_holding_target_bag = set()
    items_to_check = graph[target]
    while len(items_to_check):
        item = items_to_check.pop()
        things_holding_target_bag.add(item)
        items_to_check.extend(graph[item])
    
    return len(things_holding_target_bag)

print(f'Part One: {part_one()}')

def part_two(filename='input.txt', target='shiny gold'):

    # Note, I am swapping the key and value of this dictionary. In this part,
    # I want the key to be the bag containing things and the value to be a tuple
    # of what it contains and how many.
    graph = defaultdict(list)
    
    for line in open(filename):
        if 'no other bags' in line:
            continue
        
        tokens = line.replace('bags', 'bag').replace('bag', '').split('contain')
        
        container = tokens[0].strip()
        
        for item in tokens[1].split(','):
            subtokens = item.strip().split(' ', 1)
            count = int(subtokens[0])
            contained_in = subtokens[1].replace('.', '').strip()
            graph[container].append((contained_in, count))
        
    # This looks ripe for memoization. We are going to be computing partial
    # solutions over and over again. Here is a recursive function that will
    # memorize previously computed answers and preload them rather than compute
    # them again.
    @lru_cache(maxsize=None)
    def count_contents(x):
        things_in_bag = 0
        items_to_check = graph[x]
        for item, count in items_to_check:
            # Add one to account for the containing bag itself
            things_in_bag += count*(count_contents(item)+1)
        return things_in_bag
            
    return count_contents(target)
    
print(f'Part Two: {part_two()}')