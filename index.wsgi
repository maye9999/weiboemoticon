import sae  
from weiboemoticon import wsgi  
application = sae.create_wsgi_app(wsgi.application)  