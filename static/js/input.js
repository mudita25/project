var responseData
var seriesOptions = []
$(function(){
    $('#inputButton').click(function(){ 
    inputData = document.getElementById('companyName').value
    inputDataLen = 0
    var arr = inputData.split(',')
    for(i = 0; i< arr.length; i++){
        if(arr[i].trim().length > 0){
            inputDataLen = inputDataLen+1
        }
    }
    
    if(inputDataLen == 0){
        alert("Invalid Input");
    }
    else{
        if(inputDataLen == 1){
            seriesOptions = []
            seriesDataStockPrice = []
            seriesDataRegrValues = []
            seriesDataStockFuturePrice = []
            $.ajax({
                url: 'http://localhost:5000/getValue',
                data: $('form').serialize(),
                type: 'POST',
                success: function(response){          
                    console.log(response);
                    if(response.status == "success"){
                        for (var i=0; i< response.yAxis.length; i++) {
                            seriesDataStockPrice.push([response.xAxis[i], response.yAxis[i]])
                        }
                        for (var i=0; i< response.yAxis.length; i++) {
                            seriesDataRegrValues.push([response.xAxis[i], response.regrValues[i]])
                        }
                        for (var i=0, j=response.yAxis.length; i< response.futureValues.length; i++,j++) {
                            seriesDataStockFuturePrice.push([response.xAxis[j], response.futureValues[i]])
                        }
                        seriesOptions[0] = {
                            name: response.name +' Stock Price',
                            data: seriesDataStockPrice
                        };
                        seriesOptions[1] = {
                            name: 'Regression Values',
                            data: seriesDataRegrValues
                        };
                        seriesOptions[2] = {
                            name: 'Future Values',
                            data: seriesDataStockFuturePrice
                        };
                        plot(seriesOptions)
                    }
                    else if(response.status == "error"){
                        plot(seriesOptions)
                        alert(response.message);
                     }        
                },
                error: function(error){
                    console.log(error);        
                } 
            });
        }
        else{
            seriesOptions = []
            if(arr.length > 5){
                alert("Input Range Excceds Specified Range");
            }
            else{
                $.ajax({
                    url: 'http://localhost:5000/compare',
                    data: $('form').serialize(),
                    type: 'POST',
                    success: function(response){          
                        console.log(response);
                        if(response.status == "success"){
                            for(var i = 0; i< response.data.length;i++){
                                currSeriesDataResponse = JSON.parse(response.data[i])
                                currSeriesData = []                        
                                for (var j=0; j< currSeriesDataResponse.yAxis.length; j++) {
                                    currSeriesData.push([currSeriesDataResponse.xAxis[j], currSeriesDataResponse.yAxis[j]])
                                    seriesOptions[i] = {
                                        name: currSeriesDataResponse['name'],
                                        data: currSeriesData
                                    };
                                }                                           
                            }
                            plot(seriesOptions)   
                        }
                        else if(response.status == "error"){
                            plot(seriesOptions)
                            alert(response.message);
                        } 
                    },
                    error: function(error){
                        console.log(error);        
                    } 
                });
            }
        }
    }
    });
});

function plot(responseData) {
    Highcharts.setOptions({                                            // This is for all plots, change Date axis to local timezone
        global : {
            useUTC : false
        }
    });

    var chart = new Highcharts.Chart({
    
    title : {
                text : 'Stock Price Prediction'
            },
    
    chart : {
                renderTo: 'container',
                zoomType: 'xy'
            }, 

    xAxis : {
                type: 'datetime'
            },

    tooltip :   {
                    pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}USD)<br/>',
                    valueDecimals: 2
                },
                
    series: responseData    
    });
}
