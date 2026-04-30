### Efficiency Optimization for database of 1 million items

For large scale optimization (1M+ garment patterns), I would replace the linear scan with a KD Tree.In this case,a KD Tree recursively partitions the 3D space by splitting along one dimension at a time.Then instead of searching the entire database we can search through nearest neighbour search,thus only small portion of the region is searched through.After retrieving nearest candidates using KD tree, the asymmetric penalty scoring is applied only on shortlisted garments to ensure accuracy while maintaining efficiency thus forming a two stage retrieval system.

Also KD Tree is chosen because it works the best among low dimensional spaces,so in our case it appears to be a better fit than using vector database.The time complexity of searching is decreased from O(N) to O(log N)

## How to Run

python question1.py
python question2.py
python question3.py

## Requirements

- numpy
- trimesh
- python 3.x
