from the_hive import app
from the_hive.config import app_config

app.config.from_object(app_config['development'])

if __name__ == '__main__':
    app.run(debug=True)
