from urllib import urlopen
import datetime
import time
from bs4 import BeautifulSoup
from sklearn import linear_model
import numpy as np

class DataNotFoundError(Exception):
    status_code = 400
    
    def __init__(self, message=None, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        self.payload = payload
        if status_code is not None:
            self.status_code = status_code
            self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class PricePrediction:

    def __init__(self, companyCode):    
        self.__companyCode = companyCode
        self.__dateList = []
        self.__responseDates = []
        self.__closingPrice = [] 
        self.__daysCounter = [] 
        self.__futureDates = []
        self.__futureResponseDates = []
        self.__futureval = []
        self.__currRegressionValues = []
        
    def predict_and_plot(self):
        try:
            self.get_stock_data()
        except DataNotFoundError:
            raise DataNotFoundError()
        return
        
    def get_stock_data(self):
        yahooUrl = 'http://finance.yahoo.com/q/hp?s=' + self.__companyCode
        print yahooUrl
        financeData = urlopen(yahooUrl)
        soup = BeautifulSoup(financeData,"lxml")
        
        try:
            table = soup.find("table", {"class" : "yfnc_datamodoutline1"})
            self.check_data_source(table) 
        except DataNotFoundError:       
            raise DataNotFoundError()   
    
        for row in table.findAll('tr')[1:]:
            table_headers = row.find_all('th')
            table_footers = row.find_all('small')
            
            if table_headers or table_footers:
                pass
            else:
                col = row.findAll('td')
                if len(col) == 7:
                    dt = datetime.datetime.strptime(col[0].string,'%b %d, %Y').date()
                    self.__dateList.append(dt)
                    self.__closingPrice.append(float(col[4].string))
                    self.__responseDates.append(time.mktime(dt.timetuple()) * 1000)
                else:
                    pass

        #reverse the data points
        self.__responseDates.reverse()        
        self.__dateList.reverse()
        self.__closingPrice.reverse()    
        self.__daysCounter = [counter + 1 for counter in range(len(self.__dateList))]                    
        return
        
    def check_data_source(self,table):
        if table == None:
            raise DataNotFoundError()
        else:
            return
      
    def predict_future_stock(self,x):
        linear_mod = linear_model.LinearRegression()
        self.__daysCounter1 = np.reshape(self.__daysCounter,(len(self.__daysCounter),1))
        self.__closingPrice1 = np.reshape(self.__closingPrice,(len(self.__closingPrice),1))
        linear_mod.fit(self.__daysCounter1, self.__closingPrice1)   
        self.__currRegressionValues1 = linear_mod.predict(self.__daysCounter1)
        for i in self.__currRegressionValues1:
            self.__currRegressionValues.append(i[0])

        for i in range(x):
            futureDate = self.__dateList[-1] + datetime.timedelta(days = i + 1)
            if futureDate.strftime("%w") == '6' or futureDate.strftime("%w") == '0':
                pass
            else:
                self.__futureDates.append(futureDate)
                self.__responseDates.append(time.mktime(futureDate.timetuple()) * 1000)
                predictedPrice = linear_mod.predict(self.__daysCounter[-1] + i + 1)
                self.__futureval.append(predictedPrice[0][0])       
        return
        
    def get_date_data(self):    
        return self.__responseDates
              
    def get_price_data(self):
        return self.__closingPrice
    
    def get_regression_values(self):
        return self.__currRegressionValues
              
    def get_futurePrice_data(self):
        return self.__futureval