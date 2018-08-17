

*****
Comments:
Our heuristic works by first finding the tile which is closest
to all the targets in our problem, obviously the tile is checked
to be a valid tile to put on a piece (by the rules of blokus), and then the heuristic returns the manhattan distance of that tile to all the REMAINING targets. It is consistent because first h(goal) is equal to 0 because if there is no valid tile to put on a piece the heuristic returns 0 (it doesn't enter the loop).
furthermore the heuristics points the search to have as less distance possible to all remaining targets, as we parse further onto the search tree we have tiles that are closer to all remaining targets which means their distance is less. it is consistent therefore admissible.
I decrease the manhattan distance by one every time because when I have more than one target then when I calculate the manhattan distance of the tile to every target I count each time the tile itsself which might overestimate the cost, so I decrease one and eventually returns +1 just for the tile itsself one time.
