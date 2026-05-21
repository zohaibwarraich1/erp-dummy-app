from flask import Flask, jsonify
import os
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Add custom metric for DB connectivity
db_status_metric = metrics.info(
    'erp_db_connected',
    'Database connection status',
    version='1.0.0'
)


@app.route('/')
def hello():
    tenant = os.environ.get('TENANT_NAME', 'Unknown Tenant')
    db_host = os.environ.get('DATABASE_HOST', 'Not Configured')
    db_name = os.environ.get('DATABASE_NAME', 'Not Configured')
    db_pass = os.environ.get('POSTGRES_PASSWORD', 'Not Configured')
    # Utilizing the APP_ENV from ConfigMap
    app_env = os.environ.get('APP_ENV', 'production')

    # Simulating the database connection status
    is_db_configured = (
        db_host != "Not Configured" and db_pass != "Not Configured"
    )
    db_status = "Connected" if is_db_configured else "Disconnected"

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
    # Run the Flask app without debug mode for security compliance
    app.run(host='0.0.0.0', port=5000)
