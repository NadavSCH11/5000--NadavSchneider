"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from _5000__NadavSchnieder import app
import pandas as pd 
from flask import render_template, redirect, request
from _5000__NadavSchnieder.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines

#------------------------------------------------------------------------
        

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
#------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#------------------------------------------------------------------------
import json 
import requests
#------------------------------------------------------------------------
import io
import base64
#------------------------------------------------------------------------
from os import path
#------------------------------------------------------------------------
from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError
#------------------------------------------------------------------------

from _5000__NadavSchnieder.Models.QueryFormStructure import LoginFormStructure 
from _5000__NadavSchnieder.Models.QueryFormStructure import UserRegistrationFormStructure 
from _5000__NadavSchnieder.Models.QueryFormStructure import DataQueryFormStructure 
from _5000__NadavSchnieder.Models.DataQuery import plot_to_img
from _5000__NadavSchnieder.Models.DataQuery import get_year
from _5000__NadavSchnieder.Models.DataQuery import get_country_choices
#------------------------------------------------------------------------
db_Functions = create_LocalDatabaseServiceRoutines() 

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'Home.html',
        title='Home Page',
        year=datetime.now().year,
    )
 #------------------------------------------------------------------------
@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='My contact page.'
    )
 #------------------------------------------------------------------------
@app.route('/about')
def about():
    """Renders the contact page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='My about page.'
    )
 #------------------------------------------------------------------------
@app.route('/DataModel')
def DataModel():
    """Renders the contact page."""
    return render_template(
        'DataModel.html',
        title='Data Model',
        year=datetime.now().year,
        message='This is how I will present my data.'
    )
 #------------------------------------------------------------------------
@app.route('/Dataset1')
def Dataset1():
    """Renders the contact page."""
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/Data/GlobalLandTemperaturesByMajorCity.csv'),low_memory= False)
    raw_data_table = df.sample(20).to_html(classes = 'table table-hover')
   

 
    return render_template(
        'DataSet1.html',
        title='This is Dataset 1 page',
        raw_data_table = raw_data_table,
        year=datetime.now().year,
        message='In this page we will display the dataset'
    )
 #------------------------------------------------------------------------
@app.route('/Dataset2')
def Dataset2():
    """Renders the contact page."""
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/Data/waves.csv'))
    raw_data_table = df.sample(20).to_html(classes = 'table table-hover')
   

 
    return render_template(
        'DataSet2.html',
        title='This is Dataset 2 page',
        raw_data_table = raw_data_table,
        year=datetime.now().year,
        message='In this page we will display the datasets we are going to use in order to answer ARE THERE UFOs'
    )


    # -------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
           
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )

 #------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            return redirect('DataQuery')
        else:
            flash('Error, please try again')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to analyze data!',
        year=datetime.now().year,
        repository_name='Pandas',
        )


 #------------------------------------------------------------------------

@app.route('/DataQuery', methods=['GET','POST'])
def DataQuery():

    chart = ''
    form = ''
    
    #------------------------------------------------------------------------
    #Creates a DataFrame from a "CSV" file
    #------------------------------------------------------------------------
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/Data/GlobalLandTemperaturesByMajorCity.csv'))
    
    #------------------------------------------------------------------------
    #Makes a form with multiple choices the puts the user's input into a list
    #------------------------------------------------------------------------
    form = DataQueryFormStructure(request.form)
    form.countries.choices = get_country_choices()         
    country_list = form.countries.data

    raw_data_table = df.sample(20).to_html(classes = 'table table-hover')
 
     
    if (request.method == 'POST' ):
       
        #------------------------------------------------------------------------
        #Leaves the DataFrame with the selected columns
        #------------------------------------------------------------------------
        df = df[['City', 'Country', 'AverageTemperature','dt']]

        #---------------------------------------------------------------
        #uses the "get_year"  to make values in the 'dt' column year only
        #---------------------------------------------------------------
        df['dt'] = df['dt'].apply(lambda x:get_year(x)) 
        df['dt'] = df['dt'].astype(int) 
       
        #------------------------------------------------------------------------
        #Sets up a new empty DataFrame with the year indexed
        #------------------------------------------------------------------------
        df = df[df['dt']>1920]
        df1 = df.set_index('Country')
        df1 = df1.groupby('dt').mean() 
        df1 = df1.rename(columns = {'AverageTemperature': 'Côte D\'Ivoire'}) 
        df1 = df1.drop('Côte D\'Ivoire',1) 

        #------------------------------------------------------------------------
        #The loop runs for every user selected country, each time adding columns of 
        #the countries with their average yearly temperatures to the emptry DataFrame
        #------------------------------------------------------------------------
    
        for country in country_list: 
            df2 = df[df['Country'] == country]
            df2 = df2.set_index('Country')
            df2 = df2.groupby('dt').mean()
            df1[country] = df2['AverageTemperature'] #T#השורה הראשונה משאירה בעמודה 'country' רק את המדינות של המשתמש, השורה השנייה עושה אותן האינדקס, השורה השלישית עושה ממוצע שנתי לכל הטמפ', והשורה הרביעית מכניסה עמודות בשם של מדינות המשתמש עם ערכים של טמפ' עובר על כל שנה בשביל כל מדינה שהמשתמש בוחר, ומכניס את זה לדטהפריים כאשר העמודות בשם של 
          
     
        #------------------------------------------------------------------------
        #Fills NaN values with 0's
        #------------------------------------------------------------------------
        df1 = df1.fillna(value = 0)


        
        #------------------------------------------------------------------------
        #Plots the DataFrame and coverts it into an image
        #------------------------------------------------------------------------
        fig = plt.figure()
        ax = fig.add_subplot()
        df1.plot(ax=ax, kind = 'line')
        chart = plot_to_img(fig)


    return render_template(
        'DataQuery.html', 
         form = form,
         chart = chart,
         title='Login Succesful! please select to analyze',
         year=datetime.now().year,
         message='This page will use the web forms to get user input'


   

     
 )