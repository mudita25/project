from flask import Flask, render_template, json, request, jsonify	
from myModules import StockPrice as sc
reload(sc)

app = Flask(__name__)

class MyIterator:
   
    def __init__(self, data):
        self.data = data
        self.length = len(data)
        self.index = 0

    def __iter__(self):
        return self

    def next(self):
        if self.index == self.length:
            raise StopIteration
        value  = self.data[self.index].strip(" ")  
        self.index = self.index + 1
        return value

class StockPredictionMain():

    @app.route("/")
    def main():
        return render_template('index.html')

    @app.route('/getValue', methods=['POST'])
    def getValue(): 
        _name = request.form['companyName']
        try:
            if _name:
                obj = sc.PricePrediction(_name)
                obj.predict_and_plot()
                numberOfdays = 45
                obj.predict_future_stock(numberOfdays)         
                return jsonify(status='success',name=_name, xAxis=obj.get_date_data(), yAxis=obj.get_price_data(), regrValues=obj.get_regression_values(), futureValues=obj.get_futurePrice_data())
            else:
                return json.dumps({'html':'<span>Enter the required fields</span>'}) 
        except sc.DataNotFoundError:
            return jsonify(status='error',message='Invalid Input, Data Not Found')
            
    @app.route('/compare', methods=['POST'])
    def compare(): 
        _data = []
        _name = request.form['companyName']
        _name = _name.split(",")
        _companyCode = MyIterator(_name)
        iter(_companyCode)
        for item in _companyCode:
                _dataCurr = {}
                try:
                    obj = sc.PricePrediction(item)
                    obj.predict_and_plot()
                    _dataCurr['name'] = item 
                    _dataCurr['xAxis'] = obj.get_date_data()               
                    _dataCurr['yAxis'] = obj.get_price_data() 
                    _data.append(json.dumps(_dataCurr)) 
                except sc.DataNotFoundError:
                    return jsonify(status='error',message='Invalid Input, Data Not Found') 
                                  
        return jsonify(status='success',data=_data)
        
    @app.errorhandler(sc.DataNotFoundError)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
  
    if __name__ == "__main__":
        app.run()
