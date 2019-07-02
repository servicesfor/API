from apps import app


from views import app_user, app_doctor, app_medicine, app_oneask, app_cart

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

    app.run(**APP_CONFIG)





