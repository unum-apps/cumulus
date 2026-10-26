#!/usr/bin/env python

import service

app = service.build()

service.route(app)

app.run(host='0.0.0.0', port=80)
