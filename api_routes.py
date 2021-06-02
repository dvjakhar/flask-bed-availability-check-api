from flask import Blueprint
from flask import json
from flask.globals import request
from flask.json import jsonify

api_routes_bp = Blueprint('api_routes', __name__)

@api_routes_bp.route('/')
def home():
  return "<h1>api works</h1>"

# Import db from app
from app import db

# Create a new bed
@api_routes_bp.route('/createNewBed/')
def create_bed():
  bed = {
    'booking_status': 0,# 1: booked, 0: not booked
    'patient_name': '',
    'patient_age': '',
    'guardian_number': '',
    'patient_critical_level': '',
    'pin_code': '',
    'hospital': '',
    'time_slot': ''
  }
  if 'booking_status' in request.args:
    bed['booking_status'] = int(request.args['booking_status'])
  if 'patient_name' in request.args:
    bed['patient_name'] = str(request.args['patient_name'])
  if 'guardian_number' in request.args:
    bed['guardian_number'] = str(request.args['guardian_number'])
  if 'patient_critical_level' in request.args:
    bed["patient_critical_level"] = str(request.args['patient_critical_level'])
  if 'pin_code' in request.args:
    bed["pin_code"] = str(request.args['pin_code'])
  if 'hospital' in request.args:
    bed["hospital"] = str(request.args['hospital'])
  if 'time_slot' in request.args:
    bed["time_slot"] = str(request.args['time_slot'])
  db.beds.insert_one(bed)
  return jsonify(message="Bed created successfully:")

# Get beds with filters
@api_routes_bp.route('/beds')
def get_bed_with_filters():
  queries = {}
  if 'booking_status' in request.args:
    queries['booking_status'] = int(request.args['booking_status'])
  if 'patient_name' in request.args:
    queries['patient_name'] = str(request.args['patient_name'])
  if 'guardian_number' in request.args:
    queries['guardian_number'] = str(request.args['guardian_number'])
  if 'patient_critical_level' in request.args:
    queries["patient_critical_level"] = str(request.args['patient_critical_level'])
  if 'pin_code' in request.args:
    queries["pin_code"] = int(request.args['pin_code'])
  if 'hospital' in request.args:
    queries["hospital"] = str(request.args['hospital'])
  if 'time_slot' in request.args:
    queries["time_slot"] = str(request.args['time_slot'])
  beds = []
  for bed in db.beds.find(queries):
    bed['_id'] = str(bed['_id'])
    beds.append(bed)
  return jsonify(beds)

# Let's book a bed with a pin_code
@api_routes_bp.route('/bookBed')
def book_a_bed():
  data = {}
  data['pin_code'] = request.args['pin_code']
  beds = []
  for bed in db.beds.find(data):
    bed['_id'] = str(bed['_id'])
    beds.append(bed)
  result = {}
  result["message"] = "Below beds are available for booking"
  result["beds_available"] = beds
  return jsonify(result)

# Reschdule booking a bed with given id
@api_routes_bp.route('/reschduleBedBooking')
def reschedule_booking_a_bed():
  id = request.args['id']
  time_slot = request.args['time_slot']
  beds_collection = db.beds
  bed = beds_collection.find_one({"_id": id})
  bed['time_slot'] = time_slot
  beds_collection.save(bed)
  return jsonify(message="Bed rescheduled successfully")

# Unbook a bed using id
@api_routes_bp('/unbookBed')
def unbook_a_bed():
  id = request.args['id']
  beds_collection = db.beds
  bed = beds_collection.find_one({"_id": id})
  bed = {
    'booking_status': 0,# 1: booked, 0: not booked
    'patient_name': '',
    'patient_age': '',
    'guardian_number': '',
    'patient_critical_level': '',
    'pin_code': '',
    'hospital': '',
    'time_slot': ''
  }
  beds_collection.save(bed)
  return jsonify(message="Bed unbooked successfully")