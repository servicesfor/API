from apps import app


from views import *


APP_CONFIG={
    'host': '0.0.0.0',
    'port': 9006,
    'debug': True
}

if __name__ == '__main__':
    app.register_blueprint(app_user.blue)
    app.register_blueprint(app_doctor.blue)
    app.register_blueprint(app_medicine.blue)
    app.register_blueprint(app_oneask.blue)
    app.register_blueprint(app_cart.blue)
    app.register_blueprint(app_hospital.blue)
    app.register_blueprint(app_diseases.blue)
    app.register_blueprint(app_order.blue)
    app.register_blueprint(app_article.blue)
    app.register_blueprint(app_receive.blue)
    app.register_blueprint(app_search.blue)

    app.run(**APP_CONFIG)





