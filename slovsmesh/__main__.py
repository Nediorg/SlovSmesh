from .app import create_app
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)s %(levelname)s: %(message)s'
)

app = create_app()
app.run(host='0.0.0.0', port=1234)
