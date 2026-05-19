from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def hello():
    tenant = os.environ.get('TENANT_NAME', 'Unknown Tenant')
    db_host = os.environ.get('DATABASE_HOST', 'Not Configured')
    db_name = os.environ.get('DATABASE_NAME', 'Not Configured')
    db_pass = os.environ.get('POSTGRES_PASSWORD', 'Not Configured')
    app_env = os.environ.get('APP_ENV', 'production') # Utilizing the APP_ENV from ConfigMap
    
    # Simulating the database connection status
    db_status = "Connected" if db_host != "Not Configured" and db_pass != "Not Configured" else "Disconnected"

    return jsonify({
        "message": f"Welcome to the ERP system for {tenant}!",
        "status": "Healthy",
        "environment": app_env,
        "database": {
            "host": db_host,
            "name": db_name,
            "connection_status": db_status
        }
    })

if __name__ == '__main__':
    # Dynamically enable Flask debug mode based on the environment (APP_ENV)
    app_env = os.environ.get('APP_ENV', 'production')
    debug_mode = True if app_env == 'development' else False
    app.run(host='0.0.0.0', port=80, debug=debug_mode)
