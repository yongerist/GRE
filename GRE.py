from app import app, db
from app.models import User


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}               # 添加数据库实例和模型

