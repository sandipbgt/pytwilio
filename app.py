from urllib.parse import urlencode
import json
import os
from flask import Flask, jsonify, url_for, request, make_response
from twilio import TwilioRestException
from twilio.rest import TwilioRestClient
import requests

app = Flask(__name__)

# Configuration
CONFIG = {
    'ENVIRONMENT': os.environ.get('PYTWILIO_ENVIRONMENT', 'production'),
    'TWILIO_ACCOUNT_SID': os.environ.get('TWILIO_ACCOUNT_SID', None),
    'TWILIO_AUTH_TOKEN': os.environ.get('TWILIO_AUTH_TOKEN', None),
    'TWILIO_FROM_PHONE': os.environ.get('TWILIO_FROM_PHONE', None),
    'NGROK_URL': os.environ.get('TWIPODCAST_NGROK_URL', None),
}

# 400 bad request error message
def bad_request(message):
    response = jsonify({'status': 400, 'error': 'bad request',
                        'message': message})
    response.status_code = 400
    return response

# 404 not found error message
def not_found(message):
    response = jsonify({'status': 404, 'error': '404 not found',
                        'message': message})
    response.status_code = 404
    return response

# CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# Main Index
@app.route('/', methods=['GET'])
def get_home():
    return jsonify({
            'author': 'Sandip Bhagat',
            'author_url': 'http://sandipbgt.github.io',
            'project_name': 'pytwilio',
            'project_url': 'https://github.com/sandipbgt/pytwilio',
        })

# API Index
@app.route('/api', methods=['GET'])
def get_api_home():
    return jsonify({
            'sms': '/api/sms',
            'call': '/api/call',
        })

# send sms usig Twilio API
@app.route('/api/sms', methods=['POST'])
def send_message():
    data = request.get_json(force=True)

    account_sid = CONFIG.get('TWILIO_ACCOUNT_SID', None)
    if account_sid is None:
        return bad_request('Twilio account_sid environment variable is not set.')

    auth_token = CONFIG.get('TWILIO_AUTH_TOKEN', None)
    if auth_token is None:
        return bad_request('Twilio auth token environment variable is not set.')

    from_phone = CONFIG.get('TWILIO_FROM_PHONE', None)
    if from_phone is None:
        return bad_request('Twilio from phone environment variable is not set.')

    to_phone = data.get('to_phone', None)
    if to_phone is None:
        return bad_request('To phone number is required.')

    body = data.get('body', None)
    if body is None:
        return bad_request('Message body is required.')

    try:
        client = TwilioRestClient(account_sid, auth_token)
        message = client.messages.create(body=body, to=to_phone, from_=from_phone)
        return jsonify({
            'message_id': message.sid
        })
    except TwilioRestException as e:
        return bad_request(e.msg)

# get TwiML response for Twilio Calls API
@app.route('/api/call/say', methods=['GET', 'POST'])
def say():
    text = request.args.get('text', None)
    if text is None:
        return bad_request('Voice text is required.')

    media_url = request.args.get('media_url', None)
    if media_url is None:
        return bad_request('Media url is required.')

    body ="""<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say voice="alice">{message}</Say>
        <Play>{media_url}</Play>
    </Response>
    """

    response = make_response(body.format(message=text, media_url=media_url))
    response.headers['Content-Type'] = 'text/xml'
    return response

# create a call via Twilio API
@app.route('/api/call', methods=['POST'])
def call_phone():
    data = request.get_json(force=True)

    account_sid = CONFIG.get('TWILIO_ACCOUNT_SID', None)
    if account_sid is None:
        return bad_request('Twilio account_sid environment variable is not set.')

    auth_token = CONFIG.get('TWILIO_AUTH_TOKEN', None)
    if auth_token is None:
        return bad_request('Twilio auth token environment variable is not set.')

    from_phone = CONFIG.get('TWILIO_FROM_PHONE', None)
    if from_phone is None:
        return bad_request('Twilio from phone environment variable is not set.')

    to_phone = data.get('to_phone', None)
    if to_phone is None:
        return bad_request('To phone number is required.')

    text = data.get('text', None)
    if text is None:
        return bad_request('Voice text is required.')

    media_url = data.get('media_url', None)
    if media_url is None:
        return bad_request('Media url is required.')

    if CONFIG['ENVIRONMENT'] == 'development':
        query_params = urlencode({'text': text, 'media_url': media_url})
        url = "%s/api/calls/say?%s" % (CONFIG['NGROK_URL'], query_params)
    else:
        url = url_for('say', text=text, media_url=media_url, _external=True)
    try:
        client = TwilioRestClient(account_sid, auth_token)
        call = client.calls.create(
                url=url,
                to=to_phone,
                from_=from_phone
            )

        return jsonify({
            'call_id': call.sid
        })
    except TwilioRestException as e:
        return bad_request(e.msg)


# Fire up our Flask app
if __name__ == '__main__':
    if CONFIG['ENVIRONMENT'] == 'development':
        app.run(debug=True)
    else:
        app.run()