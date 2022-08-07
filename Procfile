pip uninstall dnspython
pip uninstall eventlet
pip uninstall gunicorn
pip install gunicorn==20.1.0
pip install eventlet==0.30.2
pip install dnspython==1.16.0
pip install https://github.com/eventlet/eventlet/archive/master.zip

web: gunicorn -k eventlet -w 1 app:app