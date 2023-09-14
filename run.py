from app import app
from configs.server_config import server_cfg

import api.routes.auth.controller
import api.routes.client.controller
import api.routes.todos.controller
import api.error.error_register


cfg = server_cfg('staging')

if __name__ == '__main__':
	app.run(host=cfg['HOST'], port=cfg['PORT'])
