from flask import request

def socket_connected():
    user_ip = request.remote_addr
    user_sid = request.sid
    print(f"[NEW CONNECTION] new user \nSID: {user_sid} \nIP: {user_ip}")