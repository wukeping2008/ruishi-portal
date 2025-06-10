"""
Knowledge Base Routes for Ruishi Control Platform
知识库管理和文档上传路由
"""

from flask import Blueprint, request, jsonify, send_from_directory
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import hashlib
from models.knowledge import knowledge_base
from models.llm_models import model_selector

knowledge_bp = Blueprint('knowledge', __name__, url_prefix='/api/knowledge')

# 允许的文件类型
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'md'}

def allowed_file(filename):
    """检查文件类型是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@knowledge_bp.route('/documents')
def get_documents():
    """获取文档列表"""
    try:
        category = request.args.get('category', '')
        search = request.args.get('search', '')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # 使用数据库知识库搜索文档
        if search:
            all_docs = knowledge_base.search_documents(search, limit=100)
        else:
            # 由于新的数据库知识库没有get_all_documents方法，我们使用空搜索来获取所有文档
            all_docs = knowledge_base.search_documents('', limit=1000)
        
        # 分类筛选
        if category:
            all_docs = [doc for doc in all_docs if doc.get('category') == category]
        
        # 转换为API格式
        documents = []
        for doc in all_docs:
            documents.append({
                'doc_id': doc.get('id'),
                'filename': doc.get('original_filename', doc.get('title', 'Unknown')),
                'title': doc.get('title'),
                'doc_type': doc.get('category', 'general'),
                'file_size': f"{doc.get('file_size', 0) / 1024:.1f} KB" if doc.get('file_size') else "Unknown",
                'upload_time': doc.get('upload_time'),
                'content_summary': doc.get('content_summary', ''),
                'category': doc.get('category', 'general')
            })
        
        # 分页
        total = len(documents)
        start = (page - 1) * per_page
        end = start + per_page
        documents = documents[start:end]
        
        return jsonify({
            "success": True,
            "documents": documents,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "pages": (total + per_page - 1) // per_page
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"获取文档列表失败: {str(e)}"
        }), 500

@knowledge_bp.route('/document/<doc_id>')
def get_document(doc_id):
    """获取文档详情"""
    try:
        doc = knowledge_base.find_document_by_id(doc_id)
        if not doc:
            return jsonify({
                "success": False,
                "error": "文档不存在"
            }), 404
        
        doc_dict = doc.to_dict()
        doc_dict.update({
            'file_size': f"{len(doc.content) / 1024:.1f} KB",
            'keywords': doc.content[:100].split()[:10],  # 提取关键词
            'content_summary': doc.content[:500] + "..." if len(doc.content) > 500 else doc.content
        })
        
        return jsonify({
            "success": True,
            "document": doc_dict
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"获取文档详情失败: {str(e)}"
        }), 500

@knowledge_bp.route('/categories')
def get_categories():
    """获取文档分类"""
    try:
        all_docs = knowledge_base.get_all_documents()
        
        # 统计各分类的文档数量
        category_counts = {}
        for doc in all_docs:
            category_counts[doc.doc_type] = category_counts.get(doc.doc_type, 0) + 1
        
        categories = [
            {"id": "system_architecture", "name": "系统架构", "count": category_counts.get("system_architecture", 0)},
            {"id": "product_specs", "name": "产品规格", "count": category_counts.get("product_specs", 0)},
            {"id": "software_development", "name": "软件开发", "count": category_counts.get("software_development", 0)},
            {"id": "application_notes", "name": "应用笔记", "count": category_counts.get("application_notes", 0)},
            {"id": "troubleshooting", "name": "故障排除", "count": category_counts.get("troubleshooting", 0)},
            {"id": "general", "name": "通用文档", "count": category_counts.get("general", 0)}
        ]
        
        return jsonify({
            "success": True,
            "categories": categories
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"获取分类失败: {str(e)}"
        }), 500

@knowledge_bp.route('/search')
def search_documents():
    """搜索文档内容"""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({
                "success": False,
                "error": "搜索关键词不能为空"
            })
        
        # 使用知识库搜索
        results = knowledge_base.search_documents(query, limit=20)
        
        # 转换为API格式
        formatted_results = []
        for doc in results:
            doc_dict = doc.to_dict()
            
            # 计算相关性分数（简单实现）
            query_lower = query.lower()
            content_lower = doc.content.lower()
            filename_lower = doc.filename.lower()
            
            score = content_lower.count(query_lower) + filename_lower.count(query_lower) * 2
            
            doc_dict.update({
                'relevance_score': score,
                'file_size': f"{len(doc.content) / 1024:.1f} KB",
                'content_summary': doc.content[:300] + "..." if len(doc.content) > 300 else doc.content,
                'matches': [
                    {"field": "filename", "text": doc.filename} if query_lower in filename_lower else None,
                    {"field": "content", "text": doc.content[:200]} if query_lower in content_lower else None
                ]
            })
            doc_dict['matches'] = [m for m in doc_dict['matches'] if m is not None]
            
            formatted_results.append(doc_dict)
        
        return jsonify({
            "success": True,
            "query": query,
            "results": formatted_results,
            "count": len(formatted_results)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"搜索失败: {str(e)}"
        }), 500

@knowledge_bp.route('/upload', methods=['POST'])
def upload_document():
    """上传文档"""
    try:
        if 'file' not in request.files:
            return jsonify({
                "success": False,
                "error": "没有选择文件"
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                "success": False,
                "error": "没有选择文件"
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                "success": False,
                "error": f"不支持的文件类型，支持的类型：{', '.join(ALLOWED_EXTENSIONS)}"
            }), 400
        
        # 获取表单数据
        category = request.form.get('category', 'general')
        
        # 使用知识库上传文档
        result = knowledge_base.upload_document(file, category)
        
        if result['success']:
            return jsonify({
                "success": True,
                "message": result['message'],
                "document": result['document']
            })
        else:
            return jsonify({
                "success": False,
                "error": result['error']
            }), 400
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"上传失败: {str(e)}"
        }), 500

@knowledge_bp.route('/delete/<doc_id>', methods=['DELETE'])
def delete_document(doc_id):
    """删除文档"""
    try:
        result = knowledge_base.delete_document(doc_id)
        
        if result['success']:
            return jsonify({
                "success": True,
                "message": result['message']
            })
        else:
            return jsonify({
                "success": False,
                "error": result['error']
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"删除失败: {str(e)}"
        }), 500

@knowledge_bp.route('/ask-document', methods=['POST'])
def ask_document():
    """基于文档内容回答问题"""
    try:
        data = request.get_json()
        doc_id = data.get('doc_id')
        question = data.get('question')
        
        if not doc_id or not question:
            return jsonify({
                "success": False,
                "error": "文档ID和问题不能为空"
            }), 400
        
        # 查找文档
        doc = knowledge_base.find_document_by_id(doc_id)
        if not doc:
            return jsonify({
                "success": False,
                "error": "文档不存在"
            }), 404
        
        # 构建基于文档的问题
        context_question = f"""基于以下文档内容回答问题：

文档标题：{doc.filename}
文档内容：
{doc.content[:2000]}...

用户问题：{question}

请基于上述文档内容提供准确的回答，如果文档中没有相关信息，请明确说明。"""
        
        # 使用AI模型回答
        response = model_selector.ask_question(
            question=context_question,
            provider=None,  # 自动选择
            model=None,
            options={}
        )
        
        if response.get('content'):
            return jsonify({
                "success": True,
                "question": question,
                "answer": response['content'],
                "source_document": {
                    "id": doc.doc_id,
                    "filename": doc.filename,
                    "doc_type": doc.doc_type
                },
                "confidence": 0.85,
                "provider_used": response.get('provider', 'unknown')
            })
        else:
            return jsonify({
                "success": False,
                "error": "AI回答生成失败"
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"文档问答失败: {str(e)}"
        }), 500

@knowledge_bp.route('/ask-knowledge', methods=['POST'])
def ask_knowledge():
    """基于整个知识库回答问题"""
    try:
        data = request.get_json()
        question = data.get('question')
        
        if not question:
            return jsonify({
                "success": False,
                "error": "问题不能为空"
            }), 400
        
        # 获取相关文档内容
        relevant_content = knowledge_base.get_relevant_content(question, max_docs=3)
        
        if relevant_content:
            # 构建包含知识库内容的问题
            context_question = f"""基于简仪科技锐视测控平台的知识库内容回答问题：

相关文档内容：
{relevant_content}

用户问题：{question}

请基于上述知识库内容提供专业的PXI测控技术回答。如果知识库中没有直接相关的信息，请结合PXI技术的一般知识进行回答，并建议用户访问简仪科技官网 www.jytek.com 获取更多信息。"""
        else:
            # 没有相关文档时的通用问题
            context_question = f"""作为简仪科技锐视测控平台的AI助手，请回答以下PXI技术问题：

{question}

请提供专业的技术回答，并在适当时候推荐简仪科技的PXI产品和解决方案。如需更详细信息，建议访问官网 www.jytek.com。"""
        
        # 使用AI模型回答
        response = model_selector.ask_question(
            question=context_question,
            provider=None,  # 自动选择
            model=None,
            options={}
        )
        
        if response.get('content'):
            # 查找相关文档
            related_docs = knowledge_base.search_documents(question, limit=3)
            
            return jsonify({
                "success": True,
                "question": question,
                "answer": response['content'],
                "has_knowledge_base_content": bool(relevant_content),
                "related_documents": [
                    {
                        "id": doc.doc_id,
                        "filename": doc.filename,
                        "doc_type": doc.doc_type
                    } for doc in related_docs
                ],
                "provider_used": response.get('provider', 'unknown')
            })
        else:
            return jsonify({
                "success": False,
                "error": "AI回答生成失败"
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"知识库问答失败: {str(e)}"
        }), 500

@knowledge_bp.route('/stats')
def get_knowledge_stats():
    """获取知识库统计信息"""
    try:
        all_docs = knowledge_base.get_all_documents()
        
        # 统计信息
        total_docs = len(all_docs)
        total_content_size = sum(len(doc.content) for doc in all_docs)
        
        # 按类型统计
        type_stats = {}
        for doc in all_docs:
            type_stats[doc.doc_type] = type_stats.get(doc.doc_type, 0) + 1
        
        # 最近上传的文档
        recent_docs = sorted(all_docs, key=lambda x: x.upload_time, reverse=True)[:5]
        
        return jsonify({
            "success": True,
            "stats": {
                "total_documents": total_docs,
                "total_content_size_kb": round(total_content_size / 1024, 2),
                "document_types": type_stats,
                "recent_uploads": [
                    {
                        "filename": doc.filename,
                        "doc_type": doc.doc_type,
                        "upload_time": doc.upload_time
                    } for doc in recent_docs
                ]
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"获取统计信息失败: {str(e)}"
        }), 500
