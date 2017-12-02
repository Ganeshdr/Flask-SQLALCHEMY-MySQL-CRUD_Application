from app.common.helpers import JsonSerializer, get_current_time, get_user_serialized
from app.extensions import db
from flask_login import UserMixin
from sqlalchemy import inspect
from flask import jsonify
from sqlalchemy.ext.declarative import declarative_base
from app.users import UserConstants
from ..common import Response

Base = declarative_base()


class UserJsonSerializer(JsonSerializer):
    __json_public__ = ['id', 'name']
    __json_modifiers__ = {}


class EMPLOYEE_DATA(Base, db.Model, UserMixin, UserJsonSerializer):

    __bind_key__ = 'login'
    __tablename__ = "employee_details"

    def __repr__(self):
        return '<EMPLOYEE_DATA %r>' % (self.name)

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(UserConstants.STRING_LEN), nullable=False)
    updated_date = db.Column(
        db.DateTime, nullable=False, default=get_current_time)
    date_of_joining = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fixed_ctc = db.Column(db.Integer, nullable=False)
    var_ctc = db.Column(db.Integer, nullable=True)
    joining_bonus = db.Column(db.Integer, nullable=True)
    relocation_charges = db.Column(db.Integer, nullable=True)
    var_ctc_frequency = db.Column(db.String, nullable=True)
    buyout = db.Column(db.Integer, nullable=True)
    role = db.Column(db.String(UserConstants.STRING_LEN), default='admin')

    # methods
    @classmethod
    def getAllEmployees(self):
        try:
            employees = EMPLOYEE_DATA.query.all()
            return Response.make_data_resp(self.map_as_list(employees))
        except Exception as e:
            return Response.make_error_resp(msg="Something went wrong", type=e.args, code=500)

    def getEmployee(self, employeeId):
        try:
            employee = EMPLOYEE_DATA.query.filter(
            db.or_(EMPLOYEE_DATA.id == employeeId)).first()
            return Response.make_data_resp(self.map_as_dict(employee))
        except Exception as e:
            return Response.make_error_resp(msg="Something went wrong", type=e.args, code=500)

    def updateEmployee(self, employeeId, employeeData):
        try:
            print("empl update:", employeeData, get_current_time)
            EMPLOYEE_DATA.query.filter(db.or_(EMPLOYEE_DATA.id == employeeId)).update(
                {
                  "fixed_ctc":employeeData["fixed_ctc"],
                  "var_ctc":employeeData["var_ctc"],
                  "joining_bonus":employeeData["joining_bonus"],
                  "relocation_charges":employeeData["relocation_charges"],
                  "var_ctc_frequency":employeeData["var_ctc_frequency"],
                  "buyout":employeeData["buyout"],
                  "updated_date":get_current_time()
                })
            db.session.commit()
            return Response.make_success_resp(msg="employee updated!")
        except Exception as e:
            return Response.make_error_resp(msg="Something went wrong", type=e.args, code=500)

    def createEmployee(self, employeeData):
        try:
            non_mandatory_keys = ['var_ctc', 'joining_bonus', 'var_ctc_frequency','relocation_charges', 'buyout'];
            for key in non_mandatory_keys:
                  if(key not in employeeData):
                        employeeData[key] = None;
            new_employee = EMPLOYEE_DATA(
                id=employeeData["id"],
                name=employeeData['name'],
                date_of_joining=employeeData["date_of_joining"],
                email=employeeData["email"],
                fixed_ctc=employeeData["fixed_ctc"],
                var_ctc=employeeData["var_ctc"],
                joining_bonus=employeeData["joining_bonus"],
                relocation_charges=employeeData["relocation_charges"],
                var_ctc_frequency=employeeData["var_ctc_frequency"],
                buyout=employeeData["buyout"]
            )
            db.session.add(new_employee)
            db.session.commit()
            return Response.make_success_resp(msg="employee added!")
        except Exception as e:
            return Response.make_error_resp(msg="Something went wrong", type=e.args, code=500)

    def deleteEmployee(self, employeeId):
        try:
            print('delete ', employeeId)
            EMPLOYEE_DATA.query.filter(
                db.or_(EMPLOYEE_DATA.id == employeeId)).delete()
            db.session.commit()
            return True
        except:
            return False

    @classmethod
    def map_as_list(cls, obj):
        lst = []
        for employee in obj:
            lst.append({
                "id": employee.id,
                "name": employee.name,
                "updated_date": employee.updated_date,
                "date_of_joining": employee.date_of_joining,
                "email": employee.email,
                "fixed_ctc": employee.fixed_ctc,
                "var_ctc": employee.var_ctc,
                "joining_bonus": employee.joining_bonus,
                "relocation_charges": employee.relocation_charges,
                "var_ctc_frequency": employee.var_ctc_frequency,
                "buyout": employee.buyout,
                "role": employee.role
            })
        return lst

    def map_as_dict(cls, employee):
        return {
            "id": employee.id,
            "name": employee.name,
            "updated_date": employee.updated_date,
            "date_of_joining": employee.date_of_joining,
            "email": employee.email,
            "fixed_ctc": employee.fixed_ctc,
            "var_ctc": employee.var_ctc,
            "joining_bonus": employee.joining_bonus,
            "relocation_charges": employee.relocation_charges,
            "var_ctc_frequency": employee.var_ctc_frequency,
            "buyout": employee.buyout,
            "role": employee.role
        }


# def searchEmployee(self, request_dict):
#       name = request_dict.get('name')
#       employees = []
#       for employee in self.employees:
#             if name.lower() in employee['name'].lower():
#                   employees.append(employee)
#       return employees
