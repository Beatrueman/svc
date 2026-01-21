from flask import Flask
import os
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import config
from models import db, User, File, Question, PasswordReset
from auth import auth_bp, mail  # 导入mail实例
from files import files_bp
from questions import questions_bp
from teacher import teacher_bp

def create_app(config_name=None):
    print("Attempting to create Flask app...")
    """应用工厂函数"""
    
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 邮件配置 - 从环境变量获取，或使用默认值
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT') or 587)
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    
    # 初始化扩展
    db.init_app(app)
    mail.init_app(app)  # 初始化邮件
    Migrate(app, db)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    JWTManager(app)
    
    # 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(questions_bp)
    app.register_blueprint(teacher_bp)
    
    # 健康检查端点
    @app.route('/api/health', methods=['GET'])
    def health():
        return {'code': 200, 'message': 'OK', 'status': 'healthy'}, 200
    
    # 创建数据库表和默认管理员
    with app.app_context():
        db.create_all()
        # 注释掉这一行，因为我们现在使用迁移
        # create_default_admin()
    
    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        return {'code': 404, 'message': '资源不存在'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'code': 500, 'message': '服务器内部错误'}, 500
    
    return app

def create_default_admin():
    """创建默认管理员账户"""
    admin = User.query.filter_by(username='admin').first()
    
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            real_name='系统管理员',
            user_type='admin',
            is_active=True
        )
        admin.set_password('Admin@123456')
        db.session.add(admin)
        db.session.commit()
        print('✓ 默认管理员账户已创建: username=admin, password=Admin@123456')
    else:
        print('✓ 管理员账户已存在')

if __name__ == '__main__':
    try:
        app = create_app()
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        import traceback
        print(f"FATAL: Error during app startup: {e}")
        traceback.print_exc()