import itertools
from math import ceil
from pathlib import Path

import yaml
import numpy as np
import pandas as pd


def main():
    """
    main function
    """
    data_file = Path("characters.yml")
    with data_file.open("rb") as stream:
        characters = yaml.safe_load(stream)
    for char, data in characters.items():
        print(char)
        ultimate = data.pop('ultimate')
        smalls = [k for k,v in data.items() if v < 5]
        bigs ={k: v for k,v in data.items() if k not in smalls}
        base_turns = ceil( ultimate / min(bigs.values()))
        if len(smalls) > 0:
            base_turns += 4
        print(f"base turns: {base_turns}")
        rates = []
        for r in range(base_turns):
            cap = r + 1
            combos = list(itertools.combinations_with_replacement([k for k in data.keys() if k != 'ultimate'], cap))
            space = max(len(repr(c)) for c in combos if str(c)) + len("    : ")
            
            for combo in combos:
                if len([c for c in combo if c is not None]) == 0:
                    continue

                energy_gain = sum(data[c] for c in combo if c in data)
                if energy_gain > ultimate:
                    continue
                required_rate = (ultimate / energy_gain) - 1
                
                if _smalls := [s for s in smalls if s in combo]:
                    _combo = [c for c in combo if c not in smalls]
                    counts = []
                    for s in _smalls:
                        count = combo.count(s)
                        counts.append(count)
                        _combo.append(f"{s} x {count}")
                    if any(c > 4 for c in counts):
                        continue
                    rates.append((required_rate, _combo))
                else:
                    rates.append((required_rate, combo))
        if len(rates) == 0:
            continue
            # print([len(repr(t)) for _, t in rates])
        rates = [(r,", ".join(c)) for r,c in rates]
        space = max(len(t) for _, t in rates) + len("    :  ")
        
        def sort_items(d):
            rate, seq = d
            if isinstance(seq, str):
                big_parts = 1 if seq in bigs else 0
            else:
                big_parts = len([s for s in seq if s in bigs])
            return rate, big_parts
        
        for rate, combo in sorted(rates, key=sort_items):
            if rate >= 0.35 or rate < 0:
                continue
            else:
                left_str = f"    {combo}: ".ljust(space)
                right_str = f"{rate:.2%}"
                print(left_str + right_str)
        print()
        
    

if __name__ == "__main__":
    main()