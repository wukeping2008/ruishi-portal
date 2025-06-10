"""
管理员后台路由
Admin backend routes for Ruishi Control Platform
"""

from flask import Blueprint, request, jsonify, session, send_file, render_template_string
from functools import wraps
import os
import logging
from models.database import user_manager, document_manager, db_manager

logger = logging.getLogger(__name__)

# 创建管理员蓝图
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def require_admin(f):
    """管理员权限装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 检查会话中的用户信息
        session_token = request.headers.get('Authorization') or request.cookies.get('admin_session')
        
        if not session_token:
            return jsonify({'error': '未登录', 'code': 'NOT_AUTHENTICATED'}), 401
        
        # 验证会话
        user = user_manager.verify_session(session_token)
        if not user or user['role'] != 'admin':
            return jsonify({'error': '权限不足', 'code': 'INSUFFICIENT_PERMISSIONS'}), 403
        
        # 将用户信息添加到请求上下文
        request.current_user = user
        return f(*args, **kwargs)
    
    return decorated_function

@admin_bp.route('/login', methods=['POST'])
def admin_login():
    """管理员登录"""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': '用户名和密码不能为空'}), 400
        
        # 验证用户
        user = user_manager.authenticate(username, password)
        if not user:
            return jsonify({'error': '用户名或密码错误'}), 401
        
        if user['role'] != 'admin':
            return jsonify({'error': '权限不足，需要管理员权限'}), 403
        
        # 创建会话
        session_token = user_manager.create_session(user['id'])
        if not session_token:
            return jsonify({'error': '创建会话失败'}), 500
        
        response = jsonify({
            'success': True,
            'message': '登录成功',
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role']
            }
        })
        
        # 设置会话cookie
        response.set_cookie('admin_session', session_token, 
                          max_age=24*60*60, httponly=True, secure=False)
        
        return response
        
    except Exception as e:
        logger.error(f"管理员登录失败: {e}")
        return jsonify({'error': '登录失败，请稍后重试'}), 500

@admin_bp.route('/logout', methods=['POST'])
@require_admin
def admin_logout():
    """管理员登出"""
    try:
        session_token = request.headers.get('Authorization') or request.cookies.get('admin_session')
        if session_token:
            user_manager.logout(session_token)
        
        response = jsonify({'success': True, 'message': '登出成功'})
        response.set_cookie('admin_session', '', expires=0)
        return response
        
    except Exception as e:
        logger.error(f"管理员登出失败: {e}")
        return jsonify({'error': '登出失败'}), 500

@admin_bp.route('/profile', methods=['GET'])
@require_admin
def get_admin_profile():
    """获取管理员信息"""
    return jsonify({
        'success': True,
        'user': request.current_user
    })

@admin_bp.route('/documents', methods=['GET'])
@require_admin
def get_documents():
    """获取文档列表"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        result = document_manager.get_all_documents(page, per_page)
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        logger.error(f"获取文档列表失败: {e}")
        return jsonify({'error': '获取文档列表失败'}), 500

@admin_bp.route('/documents/upload', methods=['POST'])
@require_admin
def upload_document():
    """上传文档"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': '没有选择文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        # 获取表单数据
        category = request.form.get('category', 'general')
        title = request.form.get('title')
        description = request.form.get('description')
        
        # 检查文件大小（16MB限制）
        file_data = file.read()
        if len(file_data) > 16 * 1024 * 1024:
            return jsonify({'error': '文件大小不能超过16MB'}), 400
        
        # 检查文件类型
        allowed_extensions = {'.pdf', '.doc', '.docx', '.txt', '.md', '.ppt', '.pptx', '.xls', '.xlsx'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in allowed_extensions:
            return jsonify({'error': f'不支持的文件类型: {file_ext}'}), 400
        
        # 保存文档
        document_id = document_manager.save_document(
            file_data=file_data,
            filename=file.filename,
            user_id=request.current_user['id'],
            category=category,
            title=title,
            description=description
        )
        
        if document_id:
            return jsonify({
                'success': True,
                'message': '文档上传成功',
                'document_id': document_id
            })
        else:
            return jsonify({'error': '文档保存失败'}), 500
            
    except Exception as e:
        logger.error(f"文档上传失败: {e}")
        return jsonify({'error': '文档上传失败，请稍后重试'}), 500

@admin_bp.route('/documents/<int:document_id>', methods=['DELETE'])
@require_admin
def delete_document(document_id):
    """删除文档"""
    try:
        success = document_manager.delete_document(document_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': '文档删除成功'
            })
        else:
            return jsonify({'error': '文档不存在或删除失败'}), 404
            
    except Exception as e:
        logger.error(f"删除文档失败: {e}")
        return jsonify({'error': '删除文档失败'}), 500

@admin_bp.route('/documents/search', methods=['GET'])
@require_admin
def search_documents():
    """搜索文档"""
    try:
        query = request.args.get('q', '')
        category = request.args.get('category')
        limit = int(request.args.get('limit', 20))
        
        results = document_manager.search_documents(query, category, limit)
        
        return jsonify({
            'success': True,
            'documents': results,
            'total': len(results)
        })
        
    except Exception as e:
        logger.error(f"搜索文档失败: {e}")
        return jsonify({'error': '搜索文档失败'}), 500

@admin_bp.route('/documents/<int:document_id>/content', methods=['GET'])
@require_admin
def get_document_content(document_id):
    """获取文档内容"""
    try:
        content = document_manager.get_document_content(document_id)
        
        if content is not None:
            return jsonify({
                'success': True,
                'content': content
            })
        else:
            return jsonify({'error': '文档不存在'}), 404
            
    except Exception as e:
        logger.error(f"获取文档内容失败: {e}")
        return jsonify({'error': '获取文档内容失败'}), 500

@admin_bp.route('/statistics', methods=['GET'])
@require_admin
def get_statistics():
    """获取系统统计信息"""
    try:
        conn = db_manager.get_connection()
        
        # 获取各种统计数据
        stats = {}
        
        # 文档统计
        cursor = conn.execute('SELECT COUNT(*) as total FROM documents WHERE is_active = 1')
        stats['total_documents'] = cursor.fetchone()['total']
        
        cursor = conn.execute('''
            SELECT category, COUNT(*) as count 
            FROM documents WHERE is_active = 1 
            GROUP BY category
        ''')
        stats['documents_by_category'] = {row['category']: row['count'] for row in cursor.fetchall()}
        
        cursor = conn.execute('''
            SELECT file_type, COUNT(*) as count 
            FROM documents WHERE is_active = 1 
            GROUP BY file_type
        ''')
        stats['documents_by_type'] = {row['file_type']: row['count'] for row in cursor.fetchall()}
        
        # 用户统计
        cursor = conn.execute('SELECT COUNT(*) as total FROM users WHERE is_active = 1')
        stats['total_users'] = cursor.fetchone()['total']
        
        # AI对话统计
        cursor = conn.execute('SELECT COUNT(*) as total FROM ai_conversations')
        stats['total_conversations'] = cursor.fetchone()['total']
        
        cursor = conn.execute('''
            SELECT ai_provider, COUNT(*) as count 
            FROM ai_conversations 
            GROUP BY ai_provider
        ''')
        stats['conversations_by_provider'] = {row['ai_provider']: row['count'] for row in cursor.fetchall()}
        
        # 最近上传的文档
        cursor = conn.execute('''
            SELECT original_filename, upload_time, category
            FROM documents 
            WHERE is_active = 1 
            ORDER BY upload_time DESC 
            LIMIT 10
        ''')
        stats['recent_documents'] = [
            {
                'filename': row['original_filename'],
                'upload_time': row['upload_time'],
                'category': row['category']
            }
            for row in cursor.fetchall()
        ]
        
        conn.close()
        
        return jsonify({
            'success': True,
            'statistics': stats
        })
        
    except Exception as e:
        logger.error(f"获取统计信息失败: {e}")
        return jsonify({'error': '获取统计信息失败'}), 500

@admin_bp.route('/dashboard', methods=['GET'])
def admin_dashboard():
    """管理员后台首页"""
    try:
        with open(os.path.join(os.path.dirname(__file__), '..', 'static', 'admin.html'), 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return '''
        <h1>管理员后台</h1>
        <p>管理员后台页面文件未找到</p>
        <p>请访问 <a href="/admin.html">admin.html</a></p>
        ''', 404
