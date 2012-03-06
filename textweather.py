#!/bin/python

# Copyright (C) 2011 sricola me@sricola.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), 
# to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above
# copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED "AS IS",
# WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import urllib2
import cherrypy
import wsgiref.handlers
from xml.dom.minidom import parse, parseString


class bitlysms:
    
    def index(self, Body, **kwargs):
        if Body == "" or Body == "help" or Body == "Help":
            return_text = "Please text a zipcode or location name to get weather details. eg. send \"washington dc\" to get the weather in Washington DC"
        else:
            url = urllib2.urlopen("http://www.google.com/ig/api?weather="+Body)
            try:
                data = url.readline()
                dom1 = parseString(data)
                city = dom1.getElementsByTagName("forecast_information")[0].getElementsByTagName("city")[0].getAttribute("data")
                currently = dom1.getElementsByTagName("current_conditions")[0].getElementsByTagName("condition")[0].getAttribute("data")
                current_temp = dom1.getElementsByTagName("current_conditions")[0].getElementsByTagName("temp_f")[0].getAttribute("data")
                current_temp_c = dom1.getElementsByTagName("current_conditions")[0].getElementsByTagName("temp_c")[0].getAttribute("data")
                current_humidity = dom1.getElementsByTagName("current_conditions")[0].getElementsByTagName("humidity")[0].getAttribute("data")
                current_wind = dom1.getElementsByTagName("current_conditions")[0].getElementsByTagName("wind_condition")[0].getAttribute("data")
                
                today_low = dom1.getElementsByTagName("forecast_conditions")[0].getElementsByTagName("low")[0].getAttribute("data")
                today_high = dom1.getElementsByTagName("forecast_conditions")[0].getElementsByTagName("high")[0].getAttribute("data")
                today_condition = dom1.getElementsByTagName("forecast_conditions")[0].getElementsByTagName("condition")[0].getAttribute("data")
                
                tomorrow_day = dom1.getElementsByTagName("forecast_conditions")[1].getElementsByTagName("day_of_week")[0].getAttribute("data")
                tomorrow_low = dom1.getElementsByTagName("forecast_conditions")[1].getElementsByTagName("low")[0].getAttribute("data")
                tomorrow_high = dom1.getElementsByTagName("forecast_conditions")[1].getElementsByTagName("high")[0].getAttribute("data")
                tomorrow_condition = dom1.getElementsByTagName("forecast_conditions")[1].getElementsByTagName("condition")[0].getAttribute("data")
                
                return_text = "Current weather at "+city+": "+current_temp+"F("+current_temp_c+"C)/"+current_humidity+"/"+current_wind+" ... Today: "+today_high+"F/"+today_low+"F/"+today_condition+" ... "+tomorrow_day+": "+tomorrow_high+"F/"+tomorrow_low+"F/"+tomorrow_condition
                
            except IndexError, e:
                return_text = "Oppsie! '" + Body + "' is not a location I recognize. Please try a more precise name or zipcode."    

        return "<?xml version=\"1.0\" encoding=\"UTF-8\" ?><Response><Sms>%s</Sms></Response>" % return_text
                        
    index.exposed = True


app = cherrypy.tree.mount(bitlysms(), "/")
wsgiref.handlers.CGIHandler().run(app)


