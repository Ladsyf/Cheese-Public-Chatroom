pip uninstall gunicorn
pip uninstall eventlet
pip install gunicorn==20.1.0
pip install eventlet==0.30.2

gunicorn --worker-class eventlet -w 1 app:app