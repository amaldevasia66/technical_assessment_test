## Explanation 

This is a body measurement and garment fit recommendation system. It calculates waist circumference directly from a 3D human mesh by extracting a horizontal cross section and forming a closed intersection loop. It also includes a measurement sanitization engine that normalizes user entered values by detecting unit inconsistencies (cm vs inches), flags unrealistic inputs using proportional validation rules, and estimates missing body measurements such as chest, waist, or hip using standard body ratio approximations. Finally, it recommends the top best fitting garment sizes by comparing user measurements against garment spec sheets using a weighted scoring system with asymmetric penalties, where tight fits are heavily penalized and relaxed fits are scored more leniently.

### Efficiency Optimization for database of 1 million items

For large scale optimization (1M+ garment patterns), I would replace the linear scan with a KD Tree.In this case,a KD Tree recursively partitions the 3D space by splitting along one dimension at a time.Then instead of searching the entire database we can search through nearest neighbour search,thus only small portion of the region is searched through.After retrieving nearest candidates using KD tree, the asymmetric penalty scoring is applied only on shortlisted garments to ensure accuracy while maintaining efficiency thus forming a two stage retrieval system.

Also KD Tree is chosen because it works the best among low dimensional spaces,so in our case it appears to be a better fit than using vector database.The time complexity of searching is decreased from O(N) to O(log N)

## How to Run

python body_measurement.py
python normalisation_outlier_detection_and_measurement_estimation.py
python garment_fit_recommendation.py

## Requirements

- numpy
- trimesh
- python 3.x
