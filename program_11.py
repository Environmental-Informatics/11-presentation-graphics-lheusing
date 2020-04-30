#!/bin/env python
# Add your own header comments
#Created by ;logan Heusinger 4/24/2020
#this lab will generate figures for presentaion using two files given within the directory.
#the code leans heavily on lab 10 for code as it uses much of the same stats created there
#uses anual and monthly metrics within the  same directory

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import rcParams


def ReadData( fileName ): #in additino to Clip data bpth taken directly from ;lab 10
    """This function takes a filename as input, and returns a dataframe with
    raw data read from that file in a Pandas DataFrame.  The DataFrame index
    should be the year, month and day of the observation.  DataFrame headers
    should be "agency_cd", "site_no", "Date", "Discharge", "Quality". The 
    "Date" column should be used as the DataFrame index. The pandas read_csv
    function will automatically replace missing values with np.NaN, but needs
    help identifying other flags used by the USGS to indicate no data is 
    availabiel.  Function returns the completed DataFrame, and a dictionary 
    designed to contain all missing value counts that is initialized with
    days missing between the first and last date of the file."""
    
    # define column names
    colNames = ['agency_cd', 'site_no', 'Date', 'Discharge', 'Quality']

    # open and read the file
    DataDF = pd.read_csv(fileName, header=1, names=colNames,  
                         delimiter=r"\s+",parse_dates=[2], comment='#',
                         na_values=['Eqp'])
    DataDF = DataDF.set_index('Date')
    
    #check for negative values
    DataDF['Discharge'].loc[(DataDF['Discharge']<0)] = np.nan
    
    # quantify the number of missing values
    MissingValues = DataDF["Discharge"].isna().sum()
    
    return( DataDF, MissingValues )
    
    

def ClipData( DataDF, startDate, endDate ):
    """This function clips the given time series dataframe to a given range 
    of dates. Function returns the clipped dataframe and and the number of 
    missing values."""
   
    #clip dF to start end values
    DataDF = DataDF.loc[startDate:endDate]
    
     # quantify the number of missing values
    MissingValues = DataDF["Discharge"].isna().sum()
    
    return( DataDF, MissingValues )
    
    

def ReadMetrics( csv ):
    """This function takes a filename as input, and returns a dataframe with
    the metrics from the assignment on descriptive statistics and 
    environmental metrics.  Works for both annual and monthly metrics. 
    Date column should be used as the index for the new dataframe.  Function 
    returns the completed DataFrame."""
    #read in the CSV and place it into a DF
    MetricsDF = pd.read_csv(csv, header = 0, delimiter = "," , parse_dates = ["Date"], comment = "#", index_col = ["Date"])
    return( MetricsDF )
    
    
def GetMonthlyStatistics(DataDF1):
    """This function calculates monthly descriptive statistics and metrics 
    for the given streamflow time series.  Values are returned as a dataframe
    of monthly values for each year."""
  
    #setup monthly data frame and index for it
    monthly_index = DataDF1.resample('MS').mean()
    resampleMDF = DataDF1.resample('MS')
    MoDataDF = pd.DataFrame(index = monthly_index.index, columns = ['Discharge'] )
    
    #monthly statistics
    MoDataDF['Discharge']= resampleMDF.Discharge.mean()
    
    months = MoDataDF.index.month
    MoDataDF = MoDataDF.groupby(months).mean()
     
     
    return ( MoDataDF )


# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.
# put the main routines from your code after this conditional check.

if __name__ == '__main__':
    
    DataDF = {}
    MissingValues = {}
    MetricsDF = {}
    
    # define full river names as a dictionary so that abbreviations are not used in figures
    riverName = { "Wildcat": "Wildcat Creek",
                  "Tippe": "Tippecanoe River" }
    #define filenames in dict format
    fileName = { "Wildcat": "WildcatCreek_Discharge_03335000_19540601-20200315.txt",
                 "Tippe": "TippecanoeRiver_Discharge_03331500_19431001-20200315.txt" }
    
    #define csvs in dict format
    csv = {"Annual" : "Annual_Metrics.csv" , "Monthly" : "Monthly_Metrics.csv"}
    
   # runthrough txt files to get data
    for file in fileName.keys():
         
        DataDF[file], MissingValues[file] = ReadData(fileName[file])
        DataDF[file], MissingValues[file] = ClipData(DataDF[file], '1969-10-01' , '2019-09-30')
   
    
    #run through csv to get metrics
    for file1 in csv.keys(): 
        MetricsDF[file1] = ReadMetrics(csv[file1])
        
    tippe = MetricsDF['Annual'].loc[MetricsDF['Annual']['Station']=='Tippe']
    wildcat = MetricsDF['Annual'].loc[MetricsDF['Annual']['Station']=='Wildcat']
    
    
    #### PLOT Daily Flow
    plt.plot(DataDF['Tippe']['2014-10-01':'2019-09-30']['Discharge'], label='Tippecanoe River')
    plt.plot(DataDF['Wildcat']['2014-10-01':'2019-09-30']['Discharge'], label='Wildcat Creek')
    plt.legend()
    plt.xlabel('Date',fontsize = 13)
    plt.ylabel('Discharge (cfs)')
    plt.title('Wildcat Creek and Tippecanoe River Daily Flow')
    rcParams['figure.figsize'] = 7, 5 #inches (width, height)
    plt.savefig('DailyFlow.png', dpi = 96)
    plt.close()    
    
    
    ##Plot Coef of Var
    plt.plot(tippe["Coeff Var"],  label='Tippecanoe River')
    plt.plot(wildcat["Coeff Var"],  label='Wildcat Creek')
    plt.legend(loc = 'upper right')
    plt.xlabel('Date',fontsize = 13)
    plt.ylabel('Coefficient of Variation (unitless)')
    plt.title('Annual Coefficient of Variation for \nWildcat Creek and Tippecanoe River')
    rcParams['figure.figsize'] = 7, 5 #inches (width, height)
    plt.savefig('CoeffVar.png', dpi = 96)
    plt.close()  
    
     ##Plot TQ mean
    plt.plot(tippe["Tqmean"],  label='Tippecanoe River')
    plt.plot(wildcat["Tqmean"],  label='Wildcat Creek')
    plt.legend()
    plt.xlabel('Date',fontsize = 13)
    plt.ylabel('Time (Days)')
    plt.title('T-Q mean - Days which Flow Exceeds Mean Annual Flow (Fractional)')
    rcParams['figure.figsize'] = 7, 5 # in inches (width, height)
    plt.savefig('Tqmean.png', dpi = 96)
    plt.close()  
    
    ##plot RB index
    plt.plot(tippe["R-B Index"],  label='Tippecanoe River')
    plt.plot(wildcat["R-B Index"],  label='Wildcat Creek')
    plt.legend()
    plt.xlabel('Date',fontsize = 13)
    plt.ylabel('Flashiness Index (cfs/cfs)')
    plt.title('Richards Baker Flashiness Index')
    rcParams['figure.figsize'] = 7, 5 # inches (width, height)
    plt.savefig('RBindex.png', dpi = 96)
    plt.close()  
    
    #Get monthly stats
    Motippe = DataDF['Tippe']['Discharge'].to_frame() #store monthlys in dataframe
    Motippe = GetMonthlyStatistics(Motippe)
    Mowildcat = DataDF['Wildcat']['Discharge'].to_frame()
    Mowildcat = GetMonthlyStatistics(Mowildcat)
    
    
    #Annual average of monthly flow 
    plt.plot(Motippe["Discharge"],  label='Tippecanoe River')
    plt.plot(Mowildcat["Discharge"],  label='Wildcat Creek')
    plt.legend()
    plt.xlabel('Months',fontsize = 13)
    plt.xticks(np.arange(1,13,1)) #label x axis with 12
    plt.ylabel('Discharge (cfs)')
    plt.title('Average Annual Monthly Flow ')
    rcParams['figure.figsize'] = 7, 5 # inches (width, height)
    plt.savefig('Annual Average monthly flow.png', dpi = 96)
    plt.close() 
    
    
    #formate wilcat and tippe for ranking
   
    #sort
    rankedtippe = tippe.sort_values('Peak Flow' , ascending = False)
    rankedwildcat = wildcat.sort_values('Peak Flow' , ascending = False)
    
    #rank them
    rankedtippe.rank = np.arange(1,51,1)
    rankedwildcat.rank= np.arange(1,51,1)
    
    #exceedence
    rankedtippe.prob = rankedtippe.rank / 51
    rankedwildcat.prob = rankedwildcat.rank / 51
    
    
    #Aplot of exceedence probability
    plt.plot(rankedtippe.prob, rankedtippe['Peak Flow'], label='Tippecanoe River')
    plt.plot(rankedwildcat.prob, rankedwildcat['Peak Flow'] , label='Wildcat Creek')
    plt.legend()
    plt.xlabel('Exceedence Probability' ,fontsize = 13)
    plt.xlim(1,0) #reverse order of x axis
    plt.ylabel('Peak Discharge (cfs)')
    plt.title('Exceedence Probability')
    rcParams['figure.figsize'] = 7, 5 # nches (width, height)
    plt.savefig('exceedenceprobability.png', dpi = 96)
    plt.close() 
    