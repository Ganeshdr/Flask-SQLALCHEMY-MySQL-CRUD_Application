from flask import make_response, jsonify, abort, current_app
from werkzeug.http import HTTP_STATUS_CODES
import sys
import os
import traceback

'''
Helper for making API returns consistent
'''
def _make_json_response(response, code=200):
   #if response type is not defined, use default HTTP status name
   if code is not 200 and not response['errors']['type']:
      response['errors']['type'] = HTTP_STATUS_CODES[code]
   
   return make_response(jsonify(response), code)

def make_success_resp(msg=None):
   response = {
      'success': True,
      'message': msg or ''
   }
   return _make_json_response(response)

def make_data_resp(data, msg=None):
   response = {
      'success': True,
      'data'   : data,
      'message': msg or ''
   }
   return _make_json_response(response)
   
def make_error_resp(msg, type=None, code=400):
   response = {
      'errors': {
         'message' : msg or "Something is wrong!",
         'type'     : type,
         'more info': ''
      }
   }
   return _make_json_response(response, code)