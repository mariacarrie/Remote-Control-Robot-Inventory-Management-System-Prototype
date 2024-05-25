#app.wsgi
#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/Applications/phpstudy/WWW/Smart_Inventory_Sys")


from app import app as application
application.secret_key = b'\xbe\xfe\x96\x06\x80\xfd\xd1\x8e\xd9p$D\xdeW\xd9\x9e\xa4R\xb1\xd8\xb2\xca/\xf4'  # 生成的密钥
