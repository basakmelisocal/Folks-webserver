from flask import Flask
from flask import request
import json

from sources.account_manager import accountmanager
from sources.trip_manager import tripmanager
from sources.recommendation_manager import recomendation_manager
from sources.contacts_manager import contacts_manager
# from utils.validation.validation import validate_request

from utils.base_response import base_resp as BaseResponse

app = Flask(__name__)


@app.before_request
def before_request():
    if request.method == 'GET':
        request.data = request.args.to_dict()
    elif request.method == 'POST' or request.method == 'PUT':
        request.data = json.loads(request.data.replace("\\", r"\\").replace("\n", ""))
    # if 'signup' not in request.path or 'login' not in request.path:
    #     if not accountmanager.AccountManager.user_operations.auth_user(args=request.data):
    #         return BaseResponse({},403,'User not authorized')


@app.route("/")
def hello():
    return "<h1 style='color:blue'>Dude trying to send request to /user/register, this is not the server you are looking for.</h1>"


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        req = request.data
        resp = accountmanager.AccountManager.registration_operations.login(req)
        if resp:
            return BaseResponse(resp, 200)
        else:
            return BaseResponse({}, 404)
    return BaseResponse({}, 404)


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        req = request.data
        resp = accountmanager.AccountManager.registration_operations.signup(req)
        if resp and not resp.get('error', None):
            return BaseResponse(resp, 200)
        elif resp and resp.get('error', None):
            return BaseResponse(resp, 407)
        else:
            return BaseResponse({}, 404)
    return BaseResponse({}, 404)


@app.route('/signup2', methods=['POST'])
def signup_cntd():
    if request.method == 'POST':
        req = request.data
        resp = accountmanager.AccountManager.registration_operations.alter_user(req)
        if resp:
            return BaseResponse(resp, 200)
        else:
            return BaseResponse({}, 404)
    return BaseResponse({}, 404)


@app.route('/userinfo', methods=['GET'])
def usr_info():
    if request.method == 'GET':
        req = request.args.to_dict()
        resp = accountmanager.AccountManager.user_operations.get_user_info(args=req)
        if resp:
            return BaseResponse(resp, 200)
    return BaseResponse({}, 404)


@app.route('/interests-list', methods=['GET'])
def get_interests():
    if request.method == 'GET':
        resp = tripmanager.TripManager.interests_operations.get_main_interests()
        if resp:
            return BaseResponse({"data": resp}, 200)
        else:
            return BaseResponse({}, 204)
    return BaseResponse({}, 405)


@app.route('/user-interests', methods=['GET', 'POST', 'DELETE'])
def interest_oper():
    if request.method == 'GET':
        req = request.args.to_dict()
        if not req['user_id']:
            return BaseResponse({}, 404)
        resp = tripmanager.TripManager.interests_operations.get_user_interests(args=req)
    elif request.method == 'POST':
        req = request.data
        resp = tripmanager.TripManager.interests_operations.add_interests_to_user(args=req)
    elif request.method == 'DELETE':
        req = request.data
        resp = tripmanager.TripManager.interests_operations.delete_interests_of_user(args=req)
    else:
        return BaseResponse({}, 405)

    if resp:
        return BaseResponse({"data": resp}, 200)
    return BaseResponse({}, 204)


@app.route('/hometown', methods=['GET'])
def getHometownRecommendations():
    req = request.args.to_dict()
    resp = recomendation_manager.RecomendationManager.recommendation_operations.get_hometown_reccomendations(args=req)
    return BaseResponse({'data': resp}, 200)


@app.route('/trips', methods=['GET', 'POST', 'PUT', 'DELETE'])
def trips():
    resp = None
    if request.method == 'GET':
        req = request.args.to_dict()
        if not req['user_id']:
            return BaseResponse({}, 404)
        resp = tripmanager.TripManager.trip_oper.get_trips_of_user(req)
        if resp:
            return BaseResponse({'data': resp}, 200)
        return BaseResponse({}, 204, error_message="no data")
    elif request.method == 'POST':
        req = request.data
        resp = tripmanager.TripManager.trip_oper.add_trip_to_user(req)
    elif request.method == 'DELETE':
        req = request.args.to_dict()
        resp = tripmanager.TripManager.trip_oper.delete_trip_of_user(req)
    if resp:
        return BaseResponse({"data": resp}, 200)
    return BaseResponse({}, 404, error_message="No data found")

@app.route('/delete-trip', methods=['POST'])
def delete_trip():
    req = request.data
    resp = tripmanager.TripManager.trip_oper.delete_trip_of_user(req)
    return BaseResponse({"data": resp}, 200)

@app.route('/uinfo', methods=['GET'])
def user_info():
    if request.method == 'GET':
        req = request.args.to_dict()
        respuinfo = accountmanager.AccountManager.user_operations.get_user_info(args=req)
        respcontacts = contacts_manager.ContactsManager.contacts.get_contacts(args=req)
        resppendingreq = contacts_manager.ContactsManager.contacts.get_pending_requests(args=req)
        resptrips = tripmanager.TripManager.trip_oper.get_trips_of_user(req)
        respconvo = contacts_manager.ContactsManager.message.get_conversation_list(args=req)
        resphometown_rec = recomendation_manager.RecomendationManager.recommendation_operations.get_hometown_reccomendations(args=req)

        return BaseResponse({'profilepage': respuinfo, 'hometown': resphometown_rec,
                             'trips': resptrips,
                             'contacts': respcontacts,
                             'pending_contacts': resppendingreq, 'conversations_people':respconvo}, 200)
    return


@app.route('/message', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        req = request.args.to_dict()
        resp = contacts_manager.ContactsManager.message.pull_conversation(args=req)
        return BaseResponse({"data": resp}, 200)
    if request.method == 'POST':
        req = request.data
        resp = contacts_manager.ContactsManager.message.push_message_to_db(args=req)
        return BaseResponse({"data": resp}, 200)


@app.route('/conversations', methods=['GET'])
def conversations():
    req = request.args.to_dict()
    resp = contacts_manager.ContactsManager.message.get_conversation_list(args=req)
    return BaseResponse({'data': resp}, 200)


@app.route('/contact_requests', methods=['GET', 'POST'])
def contact_requests():
    if request.method == 'GET':
        req = request.args.to_dict()
        resp = contacts_manager.ContactsManager.contacts.get_pending_requests(args=req)
        return BaseResponse({"data": resp}, 200)
    if request.method == 'POST':
        req = request.data
        resp = contacts_manager.ContactsManager.contacts.accept_or_reject_request(args=req)
        return BaseResponse({"data": resp}, 200)


@app.route('/send_request', methods=['POST'])
def send_request():
    req = request.data
    resp = contacts_manager.ContactsManager.contacts.send_contact_request(args=req)
    return BaseResponse({"data": resp}, 200)

@app.route('/change_image', methods=['POST'])
def add_img():
    req = request.data
    resp = accountmanager.AccountManager.registration_operations.upload_img(args=req)
    return BaseResponse({"data": resp}, 200)

@app.route('/explore', methods=['GET'])
def explore():
    req = request.args.to_dict()
    resp = recomendation_manager.RecomendationManager.recommendation_operations.get_explore_reccomendation(args=req)
    return BaseResponse({"data": resp}, 200)

@app.route('/add_venue_to_trip', methods=['POST'])
def venue_to_trip():
    req = request.data
    resp = tripmanager.TripManager.trip_oper.add_venue_to_trip(args=req)
    return BaseResponse({"data": resp}, 200)

@app.route('/delete_venue_of_trip', methods=['POST'])
def venue_of_trip():
    req = request.data
    resp = tripmanager.TripManager.trip_oper.delete_venue_of_trip(args=req)
    return BaseResponse({"data": resp}, 200)

@app.route('/get_single_trip', methods=['GET'])
def get_specific_trip():
    req = request.args.to_dict()
    resp = tripmanager.TripManager.trip_oper.get_trip_and_contents(args=req)
    return BaseResponse({"data": resp}, 200)

@app.route('/rate_venue', methods=['POST'])
def rate_venue():
    req = request.data
    resp = tripmanager.TripManager.interests_operations.give_rating_to_venue(args=req)
    return BaseResponse({"data": resp}, 200)

@app.route('/rate_user', methods=['POST'])
def rate_user():
    req = request.data
    resp = tripmanager.TripManager.interests_operations.give_rating_to_user(args=req)
    return BaseResponse({"data": resp}, 200)

@app.route('/delete_user', methods=['POST'])
def delete_user():
    req = request.data
    resp = accountmanager.AccountManager.user_operations.delete_user(args=req)
    return BaseResponse({"data": resp}, 200)

@app.route('/edit_user', methods=['POST'])
def edit_user_inf():
    req = request.data
    resp = accountmanager.AccountManager.user_operations.edit_user_info(args=req)
    return BaseResponse({"data": resp}, 200)

@app.route('/get_rated_venues', methods=['GET'])
def get_rated_venues():
    req = request.data
    resp = tripmanager.TripManager.interests_operations.get_rated_venues_of_user(args=req)
    return BaseResponse({"data": resp}, 200)