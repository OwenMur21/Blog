from app import create_app,db
from flask_script import Manager,Server



#Creating app instance
app = create_app('development')
# app = create_app('production')
# app = create_app('test')
manager = Manager(app)
manager.add_command('server',Server)



@manager.shell
def make_shell_context():
    return dict(app = app, db = db)
if __name__ == '__main__':
    manager.run()