import streamlit as st
import numpy as np
import pandas as pd
import warnings 
warnings.filterwarnings("ignore")
import pickle
from streamlit_option_menu import option_menu
# importing laptop prediction files
with open("D:\\endtoend\\Laptop Price Prediction\\fle\\ct.pkl", "rb") as file:
    ct= pickle.load(file)
with open("D:\\endtoend\\Laptop Price Prediction\\fle\\model.pkl", "rb") as md:
    model= pickle.load(md)
with open("D:\\endtoend\\Laptop Price Prediction\\fle\\df.pkl", "rb") as d:
    df= pickle.load(d)

# importing mobile prediction file
with open("D:\\endtoend\\Laptop Price Prediction\\fle\\mobile\\ctmobile.pkl", "rb") as file:
    mobile_ct= pickle.load(file)

with open("D:\\endtoend\\Laptop Price Prediction\\fle\\mobile\\mobiledata.pkl", "rb") as d:
    mobile_df= pickle.load(d)

mobile_model= pickle.load(open("D:\\endtoend\\Laptop Price Prediction\\fle\\mobile\\mobilePricemodel.pkl", "rb"))

# importing car price prediction file
with open("D:\\endtoend\\Laptop Price Prediction\\fle\\Car\\carct.pkl", "rb") as file:
    car_ct= pickle.load(file)
with open("D:\\endtoend\\Laptop Price Prediction\\fle\\Car\\carmodel.pkl", "rb") as file:
    car_model= pickle.load(file)
with open("D:\\endtoend\\Laptop Price Prediction\\fle\\Car\\cardata.pkl", "rb") as file:
    car_df= pickle.load(file)


def main():
    with st.sidebar:
        selected= option_menu("Commodity Price Prediction",
                            ["Laptop Price Prediction", "Mobile Price Prediction","Car Price Prediction"],icons=["laptop", "phone", "car-front-fill"], default_index=0)
    if selected=="Laptop Price Prediction":
    
        st.title("Laptop Price Prediction")

        left, right= st.columns(2)
        company = left.selectbox('Brand',df['Company'].unique())

        # type of laptop
        type = right.selectbox('Type',df['TypeName'].unique())

        #ram
        Ram= left.selectbox("Ram (in GB)", [2, 4, 6, 8, 12, 16, 24, 32, 64])

        # operating system
        os = right.selectbox('OS',df['OpSys'].unique())

        # Weight
        Weight= left.number_input("Weight of the Laptop")
        # Touchscreen
        Touchscreen =right.selectbox('touchscreen',["Yes", "No"])
        if Touchscreen =="Yes":
            Touchscreen= 1
        else:
            Touchscreen= 0


        # IPS
        ips = left.selectbox('IPS',['No','Yes'])
        if ips =="Yes":
            ips= 1
        else:
            ips= 0

        # screen size
        screen_size = right.number_input('Screen Size')

        #resolution
        resolution = left.selectbox('Screen Resolution',['1920x1080','1366x768',
                                                '1600x900','3840x2160','3200x1800','2880x1800','2560x1600','2560x1440','2304x1440'])
        #cpu
        cpu = right.selectbox('CPU',df['cpu Brand'].unique())
        #hdd
        hdd = left.selectbox('HDD(in GB)',[0,128,256,512,1024,2048])
        #ssd
        ssd = right.selectbox('SSD(in GB)',[0,8,128,256,512,1024])
        #gpu
        gpu = left.selectbox('GPU',df['Gpu Brand'].unique())
        
        Predict_Button= st.button("Predict")
        if Predict_Button:
            ppi =None
            X_res = int(resolution.split('x')[0])
            Y_res = int(resolution.split('x')[1])
            ppi = ((X_res**2) + (Y_res**2))**0.5/screen_size
            
            a=pd.DataFrame([{"Company":company, "TypeName":type, "Ram":Ram,"OpSys": os, "Weight":Weight, "Touchscreen":Touchscreen,
                            "Ips":ips,
                        "ppi":ppi,"cpu Brand": cpu,
            "HDD": hdd, "SSD": ssd, "Gpu Brand": gpu}])
            a= ct.transform(a)
            result=model.predict(a)
            st.title("The predicted price of this configuration is " + str(int(np.exp(result[0]))))
    if selected=="Mobile Price Prediction":
        st.title("Mobile Price Prediction")
        left, right= st.columns(2)
        Name =left.selectbox("Select Mobile Brand", mobile_df["Name"].unique())
        ram =right.selectbox("Select RAM Capacity (GB)", mobile_df["ram"].unique())
        Rom =left.selectbox("Select ROM Capacity (GB)", mobile_df["Rom"].unique())
        display=right.number_input("Enter Display Size (cm)")
        HD=left.selectbox("HD Display Support", mobile_df["HD"].unique())
        Front_Camera_Resolution_MP= right.selectbox("Select Front Camera Resolution (MP)", mobile_df["Front_Camera_Resolution_MP"].unique())
        Back_Camera=left.selectbox("Select Back Camera Type", mobile_df["Back/Rare Camera"].unique())
        Battery=right.selectbox("Select Battery Capacity (mAh)", mobile_df["Battery"].unique())
        Predict_Button= st.button("Predict")
        if Predict_Button:
        
            
            a=pd.DataFrame([{"Name": Name, "ram": ram, "Rom": Rom, "display": display, "HD": HD, "Front_Camera_Resolution_MP":
                            Front_Camera_Resolution_MP, "Back/Rare Camera": Back_Camera,
            "Battery": Battery}])
            a= mobile_ct.transform(a)
            result=mobile_model.predict(a)
            st.title("The predicted price of Mobile is " + str(int(np.exp(result[0]))))


    if selected=="Car Price Prediction":
        st.title("Car Price Prediction")
        left, right= st.columns(2)
        Location =  left.selectbox("Select location", car_df["Location"].unique())
        Kilometers_Driven=  right.number_input("Enter kilometer Driven", step=0, value=0)
        Fuel_Type=  left.selectbox("Select Feul Type", car_df["Fuel_Type"].unique())
        Transmission=  right.selectbox("Select Transmission Type", car_df["Transmission"].unique())
        Owner_Type  =  left.selectbox("Select Owner Type", car_df["Owner_Type"].unique()) 
        Mileage = right.number_input("Enter Mileage (km/l)")
        Engine=  left.number_input("Enter Engine Capacity (cc)", value=0, step=0)
        Power = right.number_input("Enter Power (bhp)")
        Seats=  left.selectbox("Select Number of Seats", car_df["Seats"].unique())
        Brand=  right.selectbox("Select location", car_df["Brand"].unique())
        Age=  left.number_input("Enter Age of Car (years)", value=0, step=0)
        Predict_Button= st.button("Predict")
        if Predict_Button:
        
            
            a=pd.DataFrame([{"Location":Location, "Kilometers_Driven": Kilometers_Driven, "Fuel_Type": Fuel_Type, 
                             "Transmission": Transmission, "Owner_Type":Owner_Type,
                             "Mileage": Mileage, "Engine": Engine, "Power": Power, "Seats":Seats,
                               "Brand":Brand, "Age": Age}])
            a= car_ct.transform(a)
            result=car_model.predict(a)
            st.title("The predicted price of car is " + str(round(float(np.exp(result[0])),2)))
    





if __name__== "__main__":
    main()
