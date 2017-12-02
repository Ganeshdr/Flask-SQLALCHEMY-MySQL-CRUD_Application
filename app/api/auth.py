from flask import Blueprint, Flask, send_from_directory, request, redirect, url_for, g
from flask import jsonify, render_template, abort
from flask_login import login_user, current_user, logout_user, confirm_login, login_fresh
import os
import json
import subprocess
import ssl
from .employee_data import EMPLOYEE_DATA
from ..users import User, UserAuth, BlacklistToken
from ..common import Response
from functools import wraps

auth = Blueprint('auth', __name__)
print("auth:",__name__)
employee_data = EMPLOYEE_DATA()
def login_required(api_method):
    @wraps(api_method)
    def check_login(*args, **kwargs):
        userid = request.headers.get('Authorization')
        if userid:
            userid = userid.replace('Bearer ', '', 1)
            try:
                userid = UserAuth.UserActions.decode_auth_token(userid)
            except Exception as e:
                print('Exception:', e)
                # abort(401, e)
                return route_error(401, str(e))
            if userid:
                return api_method(*args, **kwargs)
        return route_error(401, 'Unauthorized user')

    return check_login


def route_error(code, message):
    print('Error!:', code, message)
    response = jsonify({'message': message})
    response.status_code = code
    return response

@auth.route('/api/login', methods=['POST'])
def login():
    print("login called")
    # if current_user.is_authenticated:
    #     return Response.make_success_resp(msg="You are already logged in")
    username = request.json['uname']
    password = request.json['pwd']
    registered_user, authenticated = User.authenticate(username, password)
    if registered_user:
        if authenticated:
            auth_token = UserAuth.UserActions.encode_auth_token(
                registered_user.id)
            if auth_token:
              login_user(registered_user, remember=False)
              responseObject = {
                  'status': 'success',
                  'message': 'Successfully logged in',
                  'userid': registered_user.id,
                  'role':'admin',
                  'token': auth_token
              }
              print('User Logged in!')
              return jsonify(responseObject)
              # return Response.make_data_resp(data=responseObject, msg="You have successfully logged in")
        else:
          responseObject = {
              'status': 'fail',
              'message': 'Invalid credentials'
          }
          return Response.make_error_resp(msg="Invalid username or password", type="Wrong Authentication", code=422)
    return Response.make_error_resp(msg="Invalid User", type="Wrong Authentication", code=422)

@auth.route('/api/logout')
@login_required
def logout():
    auth_header = request.headers.get('Authorization')
    auth_token = auth_header.replace('Bearer ', '', 1)
    blacklist_token = BlacklistToken(token=auth_token)
    BlacklistToken.blacklisted_tokens.append(blacklist_token)
    return jsonify({'data': 'successfully logged out'})


@auth.route('/api/authenticate_user', methods=['POST'])
@login_required
def auth_user():
    print('Authenticating User....')
    currentUser = request.json
    user = User.authenticate_user(int(currentUser['userid']))
    if user:
        # if user.role != currentUser['role']:
            # return route_error(401, 'Role Unauthorized')
        return jsonify({'data': 'authorized'})
    return route_error(401, 'User not found!')


@auth.route('/api/employees', methods=['GET'])
@login_required
def getAllEmployees():
    return employee_data.getAllEmployees()


@auth.route('/api/employees/<int:employeeId>', methods=['GET'])
@login_required
def getEmployee(employeeId):
    return employee_data.getEmployee(employeeId)


@auth.route('/api/employees/<int:employeeId>', methods=['PUT'])
@login_required
def updateEmployee(employeeId):
    return employee_data.updateEmployee(employeeId, request.json)


@auth.route('/api/employees', methods=['POST'])
@login_required
def createEmployee():
    # if user:
        # if user.role != currentUser['role']:
            # return route_error(401, 'Role Unauthorized')
        # return jsonify({'data': 'authorized'})
    # return route_error(401, 'User not found!')
    return employee_data.createEmployee(request.json)


@auth.route('/api/employees/<int:id>', methods=['DELETE'])
@login_required
def deleteEmployee(id):
    if(employee_data.deleteEmployee(id)):
        return "success"
    else:
        return "error while deleting"

    
@auth.route('/api/employees/', methods=['GET'])
@login_required
def searchEmployee():
    return jsonify({'data': employee_data.searchEmployee(request.args)})
