# Assessment Submission

Logic to all 3 questions and efficiency requirement for 3rd question is written here.

---

## Question 1

### Logic

1. Load the given SMPL mesh using trimesh 2. Create a function calculate_circumference with mesh and target_z as the parameters. 1. Detect the vertical axis using mesh.extents. 2. Calculate the normal to the cutting plane(through upaxis) and the height at which the plane is to be cut(through target_z).I assumed 60% of the height of the body to be the desired cutting height according to standard body measurements. 3. Slice the mesh through the computed plane at the computed height. 4. Due to the presence of both arms,3 loops could be formed by the slicing.Since arms aren't considered while calculating the waist circumference,only the loop that had the highest circumference is considered. 5. The length of this loop is calculated as the waist circumference.The length of each segment in the loop is added and summed. 6. Close the loop using np.vstack and load the circumference using trimesh.load_path for visual representation. 7. Both the cicumference and the visual loop is returned 3. The height of the body is found by subtracting the highest point and lowest point in the vertical axis which are found using mesh.bounds.60% of this height is assumed to be the height at which the waist is present. 4. Call the function and return the waist circumference value and the visual representation of the waist. 5. Print the waist circumference value. 6. Color the body in grey and the circumference of the waist in red and the visual representation is outputted using trimesh.Scene(the visual presentation is in "question1_output_screenshot.png" file)

---

## Question 2

### Logic

1. Create a class DataSanitizer with raw_data,clean_data,flags and is_inch as its object attributes
2. Create a function normalization for autonormalizing all the values into centimeters
   1. Get the height from the user measurement
   2. Return None if the height is missing or invalid
   3. If height exists and is less than 90,flag it and set is_inch to True
   4. For each value in raw_data, assign the same value \* 2.54 to clean_data if is_inch is True,or assign the same value is is_inch is False.Assign None if value is invalid(<0) or None
3. Create function validation for detecting outliers
   1. Get the height,chest,waist,hip values from the user measurement
   2. Return None if the height is missing or invalid
   3. If waist is greater than or equal to height or if chest measurement is not between 30-80% of height,flag the respective case as an outlier
4. Create a function estimation to estimate non critical values if they are not given properly by the user
   1. Create a dictionary for standard body estimates
   2. Get the height from the user measurement
   3. Return None if the height is missing or invalid
   4. For each None value in clean_data,assign height \*respective ratio from standard body estimate to it
5. Create a function run to call all of the three above functions which returns clean_data and flags
6. Read the user_measurements from the user as a dictionary
7. Create an object of DataSanitizer class to call the run function
8. Output the clean_data and flags

---

## Question 3

### Logic

1. Create a class GarmentMatcher with database(storing the garment patterns) and weights(importance of each measurement in the garment type)as its object attributes
2. Create a function calculate_score which takes user_measurement and garment pattern as its parameters to make a scoring criteria and assign score to each garment pattern
   1. total_penalty is initialised which used to create the score,the lower the penalty the higher the score
   2. difference between user measurement and the measurement in garment pattern is calculated to define the penalty
   3. if difference <-2 we will make score zero since garment shorter than 2 cms is unwearable,if it is between 0 and -2 we give heavy penalty as shorter garments are not preferred however if difference>0 we consider it as relaxed fits so we will only slightly increase the penalty.
   4. total_penalty is the summation of penalties at each measurement.
   5. Based on penalties a score is created which is percentage of exponent of negative of total_penalty divided by 100
   6. The score is returned
3. Create a function top_fits_finder to assign top fits based on the score of each garment pattern which takes user_measurement as its parameter and returns the top 3 fits
   1. For each garment pattern in the database,calculate_function score is called and the score is returned.
   2. We append the score to a list called result only if its positive
   3. We sort the result in decreasing order of score and return the top 3 rows.
4. A database of garment patterns is stored in garment_db
5. The user enters the user_measurement
6. An object gm of class GarmentMatcher is initialised which is used to call the top_fits_finder function and the returned list is stored in top_3_fit
   7 .The top_3_fit list is then outputted

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
