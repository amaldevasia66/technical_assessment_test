class DataSanitizer:

    #Initializing the object using the constructor
    def __init__(self,measurement):
        self.raw_data=measurement
        self.clean_data={}
        self.flags=[]
        self.is_inch=False
    
    #function for auto normalizing the values
    def normalization(self):
        height=self.raw_data.get("height") #getting the height value
    
        #if the height value is none or invalid,then appending the flag
        if height is None or height<=0:
            self.flags.append("CRITICAL: Height value is either missing or not valid.So cannot determine units.")
            return
    
        #if height is less than 90 then assuming the value to be in inches and appending this observation in the flag
        if height and 0<height<90:
            self.flags.append("CONVERSION:Converting data to centi meters")
            self.is_inch=True
    
        #adding the raw data to clean data,but if the values are in inches then converting them to cms before.
        for key,value in self.raw_data.items():
            if value and value>0:
                val=float(value)
                self.clean_data[key]=round(2.54*val,2) if self.is_inch else val
    
            if value is None or value<=0: #adding the none values to clean data
                self.clean_data[key]=None

    #function for detecting outliers
    def validation(self):

        #getting all the measurement values
        height=self.clean_data.get("height")
        if height is None or height<=0: #if height is none or invalid
            return
        
        chest=self.clean_data.get("chest")
        waist=self.clean_data.get("waist")
        hip=self.clean_data.get("hip")

        #if waist>=height then assuming it to be an outlier and flagging it
        if waist:
            if waist>=height:
                self.flags.append("OUTLIER:Waist is higher than or equal to the height")
        #if chest is less than 30% or greater than 80% of height then assuming it to be an outlier and flagging it
        if chest:
            if chest<=(0.3*height):
                self.flags.append("OUTLIER:Chest measurement is too low")
            if chest>=(0.8*height):
                self.flags.append("OUTLIER:Chest measurement is too high")

    #function to estimate non critical values if they are not given properly by the user
    def estimation(self):
        
        #standard body estimates
        ratio_estimates={
            "chest":0.52,
            "waist":0.44,
            "hip":0.54,
            "arm_length":0.35
        }

        height=self.clean_data.get("height")
        if height is None or height<=0:
            return
        
        #estimating values based on standard body estimates.Invalid values were already changed to None before.
        for key,ratio in ratio_estimates.items():
            if self.clean_data[key]==None:
                self.clean_data[key]=round(height*ratio,2)
                self.flags.append(f"MISSING:{key} measurement missing/invalid,estimated value added")
        
    def run(self):
        self.normalization()
        self.validation()
        self.estimation()

        return self.clean_data,self.flags

measurement={}
#reading measurement from user
try:
    ht=float(input("Enter height measurement:").strip())
except ValueError:
    ht=None
try:
    c=float(input("Enter chest measurement:").strip())
except ValueError:
    c=None
try:
    w=float(input("Enter waist measurement:").strip())
except ValueError:
    w=None
try:
    h=float(input("Enter hip measurement:").strip())
except ValueError:
    h=None
try:
    al=float(input("Enter arm length measurement:").strip())
except ValueError:
    al=None

measurement["height"]=ht
measurement["chest"]=c
measurement["waist"]=w
measurement["hip"]=h
measurement["arm_length"]=al

sanitizer=DataSanitizer(measurement)
clean_data,flags=sanitizer.run()

#output
print(f"Values in centimeters:{clean_data}")
print(flags)