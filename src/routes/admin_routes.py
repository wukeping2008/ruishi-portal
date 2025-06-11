"""
管理员后台路由
Admin backend routes for Ruishi Control Platform
"""

from flask import Blueprint, request, jsonify, session, send_file, render_template_string
from functools import wraps
import os
import json
import logging
from models.database import user_manager, document_manager, db_manager
from models.ai_conversation import ai_conversation_manager

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
        
        # 使用新的AI对话管理器获取统计
        ai_stats = ai_conversation_manager.get_conversation_statistics()
        stats.update(ai_stats)
        
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

@admin_bp.route('/ai-statistics', methods=['GET'])
@require_admin
def get_ai_statistics():
    """获取详细的AI统计信息"""
    try:
        # 获取AI对话统计
        conversation_stats = ai_conversation_manager.get_conversation_statistics()
        
        # 获取AI提供商性能统计
        provider_performance = ai_conversation_manager.get_provider_performance()
        
        # 获取最近的对话记录
        recent_conversations = ai_conversation_manager.get_recent_conversations(limit=20)
        
        return jsonify({
            'success': True,
            'conversation_statistics': conversation_stats,
            'provider_performance': provider_performance,
            'recent_conversations': recent_conversations
        })
        
    except Exception as e:
        logger.error(f"获取AI统计信息失败: {e}")
        return jsonify({'error': '获取AI统计信息失败'}), 500

@admin_bp.route('/ai-conversations/<int:conversation_id>/rate', methods=['POST'])
@require_admin
def rate_conversation(conversation_id):
    """为AI对话评分"""
    try:
        data = request.json
        rating = data.get('rating')
        
        if not rating or rating not in [1, 2, 3, 4, 5]:
            return jsonify({'error': '评分必须是1-5之间的整数'}), 400
        
        success = ai_conversation_manager.rate_conversation(conversation_id, rating)
        
        if success:
            return jsonify({
                'success': True,
                'message': '评分成功'
            })
        else:
            return jsonify({'error': '对话不存在或评分失败'}), 404
            
    except Exception as e:
        logger.error(f"对话评分失败: {e}")
        return jsonify({'error': '对话评分失败'}), 500

@admin_bp.route('/comprehensive-statistics', methods=['GET'])
@require_admin
def get_comprehensive_statistics():
    """获取综合统计信息"""
    try:
        comprehensive_stats = ai_conversation_manager.get_comprehensive_statistics()
        
        return jsonify({
            'success': True,
            'statistics': comprehensive_stats
        })
        
    except Exception as e:
        logger.error(f"获取综合统计信息失败: {e}")
        return jsonify({'error': '获取综合统计信息失败'}), 500

@admin_bp.route('/keyword-statistics', methods=['GET'])
@require_admin
def get_keyword_statistics():
    """获取关键词统计"""
    try:
        limit = int(request.args.get('limit', 50))
        keyword_stats = ai_conversation_manager.get_keyword_statistics(limit=limit)
        
        return jsonify({
            'success': True,
            'keyword_statistics': keyword_stats
        })
        
    except Exception as e:
        logger.error(f"获取关键词统计失败: {e}")
        return jsonify({'error': '获取关键词统计失败'}), 500

@admin_bp.route('/user-statistics', methods=['GET'])
@require_admin
def get_user_statistics():
    """获取用户统计"""
    try:
        user_stats = ai_conversation_manager.get_user_statistics()
        
        return jsonify({
            'success': True,
            'user_statistics': user_stats
        })
        
    except Exception as e:
        logger.error(f"获取用户统计失败: {e}")
        return jsonify({'error': '获取用户统计失败'}), 500

@admin_bp.route('/document-usage-statistics', methods=['GET'])
@require_admin
def get_document_usage_statistics():
    """获取文档使用统计"""
    try:
        document_stats = ai_conversation_manager.get_document_usage_statistics()
        
        return jsonify({
            'success': True,
            'document_statistics': document_stats
        })
        
    except Exception as e:
        logger.error(f"获取文档使用统计失败: {e}")
        return jsonify({'error': '获取文档使用统计失败'}), 500

@admin_bp.route('/trigger-statistics', methods=['GET'])
@require_admin
def get_trigger_statistics():
    """获取触发类型统计"""
    try:
        trigger_stats = ai_conversation_manager.get_trigger_type_statistics()
        
        return jsonify({
            'success': True,
            'trigger_statistics': trigger_stats
        })
        
    except Exception as e:
        logger.error(f"获取触发类型统计失败: {e}")
        return jsonify({'error': '获取触发类型统计失败'}), 500

@admin_bp.route('/detailed-conversations', methods=['GET'])
@require_admin
def get_detailed_conversations():
    """获取详细的对话记录"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        user_type = request.args.get('user_type')
        ai_provider = request.args.get('ai_provider')
        
        conn = db_manager.get_connection()
        
        # 构建查询条件
        where_conditions = []
        params = []
        
        if user_type:
            where_conditions.append('user_type = ?')
            params.append(user_type)
        
        if ai_provider:
            where_conditions.append('ai_provider = ?')
            params.append(ai_provider)
        
        where_clause = ' AND '.join(where_conditions)
        if where_clause:
            where_clause = 'WHERE ' + where_clause
        
        # 获取总数
        count_sql = f'SELECT COUNT(*) as total FROM ai_conversations {where_clause}'
        cursor = conn.execute(count_sql, params)
        total = cursor.fetchone()['total']
        
        # 获取分页数据
        offset = (page - 1) * per_page
        data_sql = f'''
            SELECT 
                ac.id, ac.user_type, ac.user_ip, ac.question, ac.ai_provider, ac.ai_model,
                ac.trigger_type, ac.keywords, ac.document_names, ac.created_at, 
                ac.response_time, ac.rating, ac.related_documents
            FROM ai_conversations ac
            {where_clause}
            ORDER BY ac.created_at DESC 
            LIMIT ? OFFSET ?
        '''
        params.extend([per_page, offset])
        
        cursor = conn.execute(data_sql, params)
        conversations = []
        
        for row in cursor.fetchall():
            # 解析JSON字段
            keywords = []
            document_names = []
            related_files = []
            
            try:
                if row['keywords']:
                    keywords = json.loads(row['keywords'])
            except (json.JSONDecodeError, TypeError):
                pass
            
            try:
                if row['document_names']:
                    document_names = json.loads(row['document_names'])
            except (json.JSONDecodeError, TypeError):
                pass
            
            # 获取关联文档的原始文件名
            try:
                if row['related_documents']:
                    related_docs = json.loads(row['related_documents'])
                    if related_docs:
                        # 获取文档的原始文件名
                        doc_ids = [str(doc.get('id')) for doc in related_docs if doc.get('id')]
                        if doc_ids:
                            placeholders = ','.join(['?' for _ in doc_ids])
                            doc_cursor = conn.execute(f'''
                                SELECT original_filename 
                                FROM documents 
                                WHERE id IN ({placeholders}) AND is_active = 1
                            ''', doc_ids)
                            related_files = [doc_row['original_filename'] for doc_row in doc_cursor.fetchall()]
            except (json.JSONDecodeError, TypeError):
                pass
            
            conversations.append({
                'id': row['id'],
                'user_type': row['user_type'],
                'user_ip': row['user_ip'],
                'question': row['question'][:200] + '...' if len(row['question']) > 200 else row['question'],
                'ai_provider': row['ai_provider'],
                'ai_model': row['ai_model'],
                'trigger_type': row['trigger_type'],
                'keywords': keywords,
                'document_names': document_names,
                'related_files': related_files,  # 新增：关联的原始文件名
                'created_at': row['created_at'],
                'response_time': row['response_time'],
                'rating': row['rating']
            })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'conversations': conversations,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        })
        
    except Exception as e:
        logger.error(f"获取详细对话记录失败: {e}")
        return jsonify({'error': '获取详细对话记录失败'}), 500

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
