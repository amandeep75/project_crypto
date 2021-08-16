# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
import pandas as pd
import json
from logging import info, warn, error

WAZIRX_API = 'https://api.wazirx.com'

def market_ticker(market_list=None):
    """

    Parameters
    ----------
    market_list : TYPE, MANDATORY
        DESCRIPTION. The default is 'None'.

    Returns
    -------
    price_change_df : TYPE
        Returns Ticker for the market.
    
    """

    if market_list == None:
        endPoint = '/uapi/v1/tickers/24hr'
        response = requests.get( WAZIRX_API + endPoint) 
        json_data = json.loads(response.text)
        price_change_df = pd.DataFrame(json_data) 
        price_change_df = price_change_df.set_index('at')             
        return price_change_df
    
    else:
        endPoint = '/uapi/v1/ticker/24hr'
        json_data_list = []
        for market in market_list:
            params = {'market':market}
            response = requests.get( WAZIRX_API + endPoint, params=params) 
            json_data = json.loads(response.text)
            json_data_list.append(json_data)
        
        price_change_df = pd.DataFrame(json_data_list) 
        price_change_df = price_change_df.set_index('at')             
        return price_change_df

def is_server_ok():
    """
    

    Returns
    dictionary 
        keys- status, message
    -------
    DESCRIPTION - Health checks server.

    """
    response = requests.get( WAZIRX_API +'/uapi/v1/systemStatus')
    json_data = json.loads(response.text)
    info(json_data['message'])
    if (json_data['status'] == 'normal'):
        return True
    else:
        return False

def order_book(market='btcinr'):
    """
    

    Parameters
    ----------
    market : str, MANDATORY
        DESCRIPTION. The default is 'btcinr'.

    Returns
    -------
    order_book_df : TYPE
        DESCRIPTION.

    """
    endPoint = '/uapi/v1/depth'    
    params = {'market':market}
    response = requests.get( WAZIRX_API + endPoint, params=params) 
    json_data = json.loads(response.text)
    order_book_df = pd.DataFrame(json_data)    
    return order_book_df

def market_status():
    """
    

    Parameters
    ----------
    market : str, MANDATORY
    DESCRIPTION. Market Status" will give your an overview of markets and assets. 
    This is helpful when you want to track the configuration of our markets, track
    fees or status of withdrawal deposit, market configuration and more. 
    This response is not recommended for price polling because accurate realtime
    price is not guaranteed as there could be some delays. We recommend using price
    ticker API for all price tracking activity..

    Returns
    -------
    market_status_df : TYPE
        DESCRIPTION.

    """
    endPoint = '/api/v2/market-status'    
    response = requests.get( WAZIRX_API + endPoint) 
    json_data = json.loads(response.text)
    assets_status_df = pd.DataFrame(json_data['assets'])  
    market_status_df = pd.DataFrame(json_data['markets'])  
    return market_status_df, assets_status_df