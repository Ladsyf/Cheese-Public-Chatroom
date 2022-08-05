pip uninstall gunicorn
pip uninstall eventlet
pip install gunicorn==20.1.0
pip install eventlet==0.33.1

web: gunicorn --worker-class eventlet -w 1 app:app