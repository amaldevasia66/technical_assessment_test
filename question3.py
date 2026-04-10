import math

class GarmentMatcher:

    def __init__(self,database):
        self.database=database
        self.weights={'chest':2,'waist':1,'hip':1}

    #function to make a scoring criteria and assign score to each garment pattern
    def calculate_score(self,user,garment):
        #penalty is used to create the score,the lower the penalty the higher the score
        total_penalty=0
        
        for feature,weights in self.weights.items():
            g_val=garment[feature]
            u_val=user[feature]
            diff=g_val-u_val #difference b/w user measurement and the measurement in garment pattern

            if diff<=-2:
                return 0 #since garment shorter than 2 cms is unwearable we will make it have zero score
            if -2<diff<=0:
                penalty=(abs(diff)**2)*5 #asymmetric penalty,shorter garment measurement gets high penalty
            if diff >0:
                penalty=diff*5 #asymmetric penalty,longer garment measurement is considered relaxed fit and only gets comparitively lower penalty
            
            total_penalty+=penalty*weights #the total penalty based on each measurement
        
        score=100*math.exp(-total_penalty/100) #creating a score based on total penalty

        return round(score,3)
    
    #function to assign top fits based on the score of each garment pattern
    def top_fits_finder(self,user):
        results=[]

        garments=self.database

        for garment in garments:
            score=self.calculate_score(user,garment)

            if score>0: #only adding score if its wearable
                results.append({'id':garment["id"],'label':garment["label"],'score':score})

        results.sort(key=lambda x: x['score'],reverse=True) #sorting the resultant list based on descending order of score

        return results[:3] #returning only the top 3 fits

garment_db=[
    {"id": 1, "label": "Size S ", "chest": 90, "waist": 80, "hip": 90}, 
    {"id": 2, "label": "Size S ", "chest": 93, "waist": 88, "hip": 90},
    {"id": 3, "label": "Size S ", "chest": 92, "waist": 92, "hip": 93},
    {"id": 4, "label": "Size M ", "chest": 97, "waist": 95, "hip": 98},
    {"id": 5, "label": "Size M", "chest": 98, "waist": 98, "hip": 98},
    {"id": 6, "label": "Size M ", "chest": 96, "waist": 93, "hip": 98}, 
    {"id": 7, "label": "Size L ", "chest": 100, "waist": 98, "hip": 103},
    {"id": 8, "label": "Size L ", "chest": 104, "waist": 98, "hip": 106},
    {"id": 9, "label": "Size L ", "chest": 102, "waist": 100, "hip": 105},
    {"id": 10, "label": "Size XL ", "chest": 109, "waist": 104, "hip": 110}, 
    {"id": 11, "label": "Size XL ", "chest": 110, "waist": 102, "hip": 112},
    {"id": 12, "label": "Size XL ", "chest": 111, "waist": 109, "hip": 111}
] #mock database


#entering user measurements
ch=float(input("Enter chest measurement:"))
w=float(input("Enter waist measurement:"))
h=float(input("Enter hip measurement:"))
user_measurement={'chest':ch,'waist':w,'hip':h}

gm=GarmentMatcher(garment_db)
top_3_fit=gm.top_fits_finder(user_measurement)

for fit in top_3_fit:#output
    print(fit)
if len(top_3_fit)==0:
    print("No wearable garment found")

    

#I have explained the efficiency optimization for database of 1 million items in README.md
#The explanation is right under the logic for question 3 and above the "how to run" and "requirements" section in README.md
