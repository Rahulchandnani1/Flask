from flask import Flask, request, render_template
import requests, random, phonenumbers
from flask_cors import CORS, cross_origin
from flask import jsonify

app = Flask(__name__)
CORS(app)
MSG91_API_KEY = '415468AhzConnQK67b65e832e9P1'

@app.route('/')
def index():
    return jsonify({"message":"Working bhai"})

@app.route('/send_otp', methods=['POST'])
@cross_origin()

def send_otp():
    data = request.json
    phone_number = data["phNo"]
    country_code = "+91"
    full_number = country_code + phone_number
    reference_otp = generate_otp()
    response = requests.get(f"https://api.msg91.com/api/v5/otp?authkey={MSG91_API_KEY}&template_id=65effbe9d6fc053c6c19f882&mobile=+91{phone_number}&otp={reference_otp}")
    result = phonenumbers.is_valid_number(phonenumbers.parse(full_number))
    if result:
        return jsonify({"message": "OTP send successfully!", "status": "success"})
    else:
        return jsonify({"message": "PLEASE ENTER THE VALID NUMBER", "status": "error"})

def generate_otp():
    otp = ''.join(random.choices('0123456789', k=4))
    return otp

@app.route('/verify_otp', methods=['POST'])
@cross_origin()
def verify_otp():
    data = request.json
    phone_number = data["phNo"]
    otp = data["otp"]
    response = requests.get(f"https://control.msg91.com/api/v5/otp/verify?otp={otp}&mobile=+91{phone_number}&authkey={MSG91_API_KEY}")
    if 'message' in response.json() and response.json()['message'] == 'OTP verified success':
        return jsonify({"message": "OTP verified successfully!", "status": "success"})
    else:
        return jsonify({"message": "OTP verification failed!", "status": "error"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
