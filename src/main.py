"""
锐视测控平台 - 简仪科技JYTEK专业PXI测控解决方案
Main entry point for the Ruishi Control Platform Flask application
"""

import sys
import os
import json
from flask import Flask, render_template, send_from_directory, request, jsonify

# Ensure proper import paths
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from routes.llm_routes import llm_bp
from routes.product_routes import product_bp
from routes.knowledge_routes import knowledge_bp
from models.llm_models import initialize_llm_providers

# Create Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file upload

# Register blueprints
app.register_blueprint(llm_bp)
app.register_blueprint(product_bp)
app.register_blueprint(knowledge_bp)

# Load configuration
def load_config():
    """Load configuration from environment or config file"""
    config = {
        'openai': {
            'api_key': os.getenv('OPENAI_API_KEY', ''),
            'default_model': os.getenv('OPENAI_DEFAULT_MODEL', 'gpt-4o')
        },
        'deepseek': {
            'api_key': os.getenv('DEEPSEEK_API_KEY', ''),
            'default_model': os.getenv('DEEPSEEK_DEFAULT_MODEL', 'deepseek-chat')
        },
        'qianwen': {
            'api_key': os.getenv('QIANWEN_API_KEY', ''),
            'secret_key': os.getenv('QIANWEN_SECRET_KEY', ''),
            'default_model': os.getenv('QIANWEN_DEFAULT_MODEL', 'ERNIE-Bot-4')
        },
        'default_provider': os.getenv('DEFAULT_LLM_PROVIDER', 'claude')
    }
    
    # For development, try to load from config file if exists
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                file_config = json.load(f)
                # Update config with file values
                for key, value in file_config.items():
                    if key in config and isinstance(value, dict):
                        config[key].update(value)
                    else:
                        config[key] = value
        except Exception as e:
            print(f"Error loading config file: {e}")
    
    return config

# Initialize LLM providers
config = load_config()
initialize_llm_providers(config)

# Routes
@app.route('/')
def index():
    """Serve the main application page"""
    return send_from_directory('static', 'index.html')

@app.route('/products')
def products():
    """Serve the products page"""
    return send_from_directory('static', 'products.html')

@app.route('/solutions')
def solutions():
    """Serve the solutions page"""
    return send_from_directory('static', 'solutions.html')

@app.route('/about')
def about():
    """Serve the about page"""
    return send_from_directory('static', 'about.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('static', path)

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files with explicit static prefix"""
    return send_from_directory('static', filename)

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': '锐视测控平台 API 运行正常',
        'platform': 'JYTEK Ruishi Control Platform'
    })

@app.route('/api/company-info')
def company_info():
    """Get company information"""
    return jsonify({
        'name': '简仪科技',
        'english_name': 'JYTEK',
        'platform': '锐视测控平台',
        'website': 'https://www.jytek.com',
        'description': '专业的PXI模块化测控解决方案提供商',
        'specialties': [
            'PXI模块化仪器',
            '自动化测试系统',
            '数据采集系统',
            '测控软件开发',
            '定制化解决方案'
        ]
    })

# Enable CORS for development
@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Run the application
if __name__ == '__main__':
    # For development
    port = int(os.getenv('PORT', 8083))
    app.run(host='0.0.0.0', port=port, debug=True)
