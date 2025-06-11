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
    from routes.knowledge_routes import knowledge_bp
    from routes.product_routes import product_bp
    from routes.admin_routes import admin_bp
    
    # Register blueprints
    app.register_blueprint(llm_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(knowledge_bp)
    app.register_blueprint(admin_bp)
    
    print("基础蓝图已成功注册")
except ImportError as e:
    print(f"导入基础模块失败: {e}")
    print("将以简化模式运行")

# Try to import prompt routes separately
try:
    from routes.prompt_routes import prompt_bp
    app.register_blueprint(prompt_bp)
    print("提示词蓝图已成功注册")
except ImportError as e:
    print(f"导入提示词模块失败: {e}")
    print("提示词功能将不可用")

# Try to initialize LLM providers
try:
    from models.llm_models import initialize_llm_providers
    print("LLM模块导入成功")
except ImportError as e:
    print(f"导入LLM模块失败: {e}")

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

# 简化的提示词API端点
@app.route('/api/prompt/modes')
def get_prompt_modes():
    """获取提示词模式"""
    user_level = request.args.get('user_level', 'basic')
    
    modes = {
        'simple': {
            'name': '简单模式',
            'description': '快速配置，适合新手',
            'difficulty': 1,
            'features': ['一键生成', '基础配置', '快速上手']
        },
        'template': {
            'name': '模板模式',
            'description': '可视化编辑，日常维护',
            'difficulty': 2,
            'features': ['模板编辑', '变量替换', '实时预览']
        },
        'json': {
            'name': 'JSON模式',
            'description': '高级配置，批量管理',
            'difficulty': 3,
            'features': ['JSON配置', '批量导入', '复杂规则']
        },
        'intelligent': {
            'name': '智能模式',
            'description': 'AI驱动，自动优化',
            'difficulty': 2,
            'features': ['意图分析', '智能优化', '效果跟踪']
        },
        'expert': {
            'name': '专家模式',
            'description': '分层架构，企业级',
            'difficulty': 4,
            'features': ['分层管理', '继承规则', '权限控制']
        }
    }
    
    return jsonify({
        'success': True,
        'data': {
            'modes': modes,
            'user_level': user_level,
            'total_modes': len(modes)
        }
    })

@app.route('/api/prompt/build', methods=['POST'])
def build_prompt():
    """构建提示词"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        mode = data.get('mode', 'simple')
        context = data.get('context', {})
        
        if not question:
            return jsonify({
                'success': False,
                'error': '问题不能为空'
            }), 400
        
        # 简化的提示词生成逻辑
        if mode == 'simple':
            prompt = f"""你是简仪科技（JYTEK）锐视测控平台的专业AI助手。

我们的主要产品是锐视测控平台，专注于PXI系统、数据采集等领域。

用户问题：{question}

请提供专业、准确的回答，重点介绍我们的技术优势和产品特色。"""
        
        elif mode == 'template':
            prompt = f"""你是简仪科技技术专家。

{context.get('knowledge_content', '')}

用户问题：{question}

请根据问题类型提供专业的技术解答。"""
        
        else:
            prompt = f"""你是简仪科技的AI助手。

用户问题：{question}

请提供专业回答。"""
        
        return jsonify({
            'success': True,
            'data': {
                'prompt': prompt,
                'mode': mode,
                'question': question,
                'length': len(prompt)
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/prompt/test', methods=['POST'])
def test_prompt():
    """测试提示词"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        mode = data.get('mode', 'simple')
        
        if not question:
            return jsonify({
                'success': False,
                'error': '测试问题不能为空'
            }), 400
        
        # 生成测试提示词
        prompt = f"""你是简仪科技的AI助手。

用户问题：{question}

请提供专业回答。"""
        
        # 分析提示词
        analysis = {
            'length': len(prompt),
            'estimated_tokens': len(prompt.split()) * 1.3,
            'complexity_score': 2.5,
            'has_knowledge_content': False
        }
        
        return jsonify({
            'success': True,
            'data': {
                'prompt': prompt,
                'analysis': analysis,
                'test_question': question,
                'mode': mode
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Enable CORS for development
@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Debug information - moved to startup
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
    
    # Call debug info
    debug_info()
    
    port = int(os.getenv('PORT', 8083))
    print(f"服务器将在端口 {port} 启动")
    print(f"访问地址: http://localhost:{port}")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=port, debug=True)
