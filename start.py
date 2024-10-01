# import os
# from flask import Flask
# import threading

# app = Flask(__name__)

# @app.route('/health', methods=['GET'])
# def health_check():
#     return 'OK', 200

# def run_health_check():
#     app.run(host='0.0.0.0', port=8443)

# if __name__ == "__main__":

#     health_thread = threading.Thread(target=run_health_check)
#     health_thread.start()
#     os.system("python -m Bot")



import os
os.system("python -m Bot")


