import os
c = get_config()
c.ServerApp.ip = "0.0.0.0"
c.ServerApp.port = 8888
c.ServerApp.open_browser = False
c.ServerApp.root_dir = "/course"
c.ServerApp.allow_remote_access = True
c.ServerApp.allow_origin = os.environ["SITE_ORIGIN"]
c.ServerApp.allow_headers = "Authorization,Content-Type"
c.IdentityProvider.token = os.environ["JUPYTER_TOKEN"]
