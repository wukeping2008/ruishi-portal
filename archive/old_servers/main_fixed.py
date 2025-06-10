"""
锐视测控平台 - 简仪科技JYTEK专业PXI测控解决方案
Main entry point for the Ruishi Control Platform Flask application
"""

import sys
import os
import json
from flask import Flask, render_template, send_from_directory, request, jsonify

# Ensure proper import paths
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Create Flask app with proper static folder configuration
app = Flask(__name__, 
           static_folder=os.path.join(current_dir, 'static'), 
           static_url_path='')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file upload

# Import routes after Flask app creation
try:
    from routes.llm_routes import llm_bp
    from routes.product_routes import product_bp
    from routes.knowledge_routes import knowledge_bp
    from models.llm_models import initialize_llm_providers
    
    # Register blueprints
    app.register_blueprint(llm_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(knowledge_bp)
    
    print("所有蓝图已成功注册")
except ImportError as e:
    print(f"导入模块失败: {e}")
    print("将以简化模式运行")

# Load configuration
def load_config():
    """Load configuration from environment or config file"""
    config_path = os.path.join(current_dir, 'config.json')
    config = {}
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                print(f"Successfully loaded config from {config_path}")
        except Exception as e:
            print(f"Error loading config file: {e}")
    
    # 如果config.json不存在或加载失败，使用环境变量作为后备
    if not config:
        config = {
            'claude': {
                'api_key': os.getenv('CLAUDE_API_KEY', ''),
                'default_model': 'claude-3-sonnet-20240229'
            },
            'gemini': {
                'api_key': os.getenv('GEMINI_API_KEY', ''),
                'default_model': 'gemini-1.5-flash'
            },
            'default_provider': 'claude'
        }
        print("Using environment variables for configuration")
    
    return config

# Initialize LLM providers
try:
    config = load_config()
    initialize_llm_providers(config)
    print("LLM providers initialized successfully")
except Exception as e:
    print(f"LLM initialization failed: {e}")

# Routes
@app.route('/')
def index():
    """Serve the main application page"""
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except Exception as e:
        print(f"Error serving index.html: {e}")
        return f"<h1>锐视测控平台</h1><p>静态文件加载错误: {e}</p><p>静态文件夹: {app.static_folder}</p>"

@app.route('/<path:filename>')
def serve_static_files(filename):
    """Serve static files"""
    try:
        return send_from_directory(app.static_folder, filename)
    except Exception as e:
        print(f"Error serving {filename}: {e}")
        return f"文件未找到: {filename}", 404

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': '锐视测控平台 API 运行正常',
        'platform': 'JYTEK Ruishi Control Platform',
        'static_folder': app.static_folder,
        'files_exist': os.path.exists(os.path.join(app.static_folder, 'index.html'))
    })

@app.route('/api/company-info')
def company_info():
    """Get company information"""
    return jsonify({
        'name': '简仪科技',
        'english_name': 'JYTEK',
        'platform': '锐视测控平台',
        'website': 'https://www.jytek.com',
        'description': '专业的PXI模块化测控解决方案提供商'
    })

# Enable CORS for development
@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Debug information
@app.before_first_request
def debug_info():
    print(f"Flask app static folder: {app.static_folder}")
    print(f"Static folder exists: {os.path.exists(app.static_folder)}")
    if os.path.exists(app.static_folder):
        files = os.listdir(app.static_folder)
        print(f"Files in static folder: {files}")
        index_path = os.path.join(app.static_folder, 'index.html')
        print(f"index.html exists: {os.path.exists(index_path)}")

# Run the application
if __name__ == '__main__':
    print("=" * 50)
    print("启动锐视测控平台")
    print("=" * 50)
    print(f"当前目录: {current_dir}")
    print(f"静态文件夹: {app.static_folder}")
    print(f"静态文件夹存在: {os.path.exists(app.static_folder)}")
    
    if os.path.exists(app.static_folder):
        print(f"静态文件列表: {os.listdir(app.static_folder)}")
    
    port = int(os.getenv('PORT', 8083))
    print(f"服务器将在端口 {port} 启动")
    print(f"访问地址: http://localhost:{port}")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=port, debug=True)
