"""
AI智能推荐系统API路由
简仪科技锐视测控平台专用
"""

from flask import Blueprint, request, jsonify
import logging
from typing import Dict, Any
from models.recommendation import intelligent_recommendation

logger = logging.getLogger(__name__)

# 创建推荐系统蓝图
recommendation_bp = Blueprint('recommendation', __name__, url_prefix='/api/recommendation')

@recommendation_bp.route('/analyze', methods=['POST'])
def analyze_user_intent():
    """
    分析用户意图
    
    POST /api/recommendation/analyze
    {
        "question": "用户问题",
        "context": {可选的上下文信息}
    }
    """
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({
                'success': False,
                'error': '缺少必要参数：question'
            }), 400
        
        question = data['question'].strip()
        if not question:
            return jsonify({
                'success': False,
                'error': '问题不能为空'
            }), 400
        
        context = data.get('context', {})
        
        # 分析用户意图
        intent_result = intelligent_recommendation.analyze_user_intent(question, context)
        
        return jsonify({
            'success': True,
            'data': intent_result,
            'message': '用户意图分析完成'
        })
        
    except Exception as e:
        logger.error(f"用户意图分析失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '用户意图分析失败，请稍后重试'
        }), 500

@recommendation_bp.route('/products', methods=['POST'])
def recommend_products():
    """
    推荐产品
    
    POST /api/recommendation/products
    {
        "intent_data": {用户意图分析结果},
        "limit": 5
    }
    """
    try:
        data = request.get_json()
        if not data or 'intent_data' not in data:
            return jsonify({
                'success': False,
                'error': '缺少必要参数：intent_data'
            }), 400
        
        intent_data = data['intent_data']
        limit = data.get('limit', 5)
        
        # 验证limit参数
        if not isinstance(limit, int) or limit < 1 or limit > 20:
            limit = 5
        
        # 推荐产品
        recommendations = intelligent_recommendation.recommend_products(intent_data, limit)
        
        return jsonify({
            'success': True,
            'data': {
                'recommendations': recommendations,
                'total_count': len(recommendations),
                'intent_confidence': intent_data.get('confidence_score', 0.0)
            },
            'message': f'成功生成{len(recommendations)}个产品推荐'
        })
        
    except Exception as e:
        logger.error(f"产品推荐失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '产品推荐失败，请稍后重试'
        }), 500

@recommendation_bp.route('/solution', methods=['POST'])
def generate_solution():
    """
    生成完整解决方案
    
    POST /api/recommendation/solution
    {
        "products": [推荐产品列表],
        "intent_data": {用户意图分析结果}
    }
    """
    try:
        data = request.get_json()
        if not data or 'products' not in data or 'intent_data' not in data:
            return jsonify({
                'success': False,
                'error': '缺少必要参数：products 和 intent_data'
            }), 400
        
        products = data['products']
        intent_data = data['intent_data']
        
        if not isinstance(products, list) or len(products) == 0:
            return jsonify({
                'success': False,
                'error': '产品列表不能为空'
            }), 400
        
        # 生成解决方案配置
        solution_config = intelligent_recommendation.generate_solution_config(products, intent_data)
        
        return jsonify({
            'success': True,
            'data': solution_config,
            'message': '解决方案生成成功'
        })
        
    except Exception as e:
        logger.error(f"解决方案生成失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '解决方案生成失败，请稍后重试'
        }), 500

@recommendation_bp.route('/complete', methods=['POST'])
def complete_recommendation():
    """
    一站式推荐服务：从问题分析到完整解决方案
    
    POST /api/recommendation/complete
    {
        "question": "用户问题",
        "context": {可选的上下文信息},
        "product_limit": 5
    }
    """
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({
                'success': False,
                'error': '缺少必要参数：question'
            }), 400
        
        question = data['question'].strip()
        if not question:
            return jsonify({
                'success': False,
                'error': '问题不能为空'
            }), 400
        
        context = data.get('context', {})
        product_limit = data.get('product_limit', 5)
        
        # 验证product_limit参数
        if not isinstance(product_limit, int) or product_limit < 1 or product_limit > 20:
            product_limit = 5
        
        # 步骤1：分析用户意图
        intent_result = intelligent_recommendation.analyze_user_intent(question, context)
        
        # 步骤2：推荐产品
        recommendations = intelligent_recommendation.recommend_products(intent_result, product_limit)
        
        # 步骤3：生成解决方案（如果有推荐产品）
        solution_config = None
        if recommendations:
            solution_config = intelligent_recommendation.generate_solution_config(recommendations, intent_result)
        
        return jsonify({
            'success': True,
            'data': {
                'intent_analysis': intent_result,
                'product_recommendations': recommendations,
                'solution_config': solution_config,
                'summary': {
                    'confidence_score': intent_result.get('confidence_score', 0.0),
                    'detected_categories': len(intent_result.get('detected_categories', [])),
                    'recommended_products': len(recommendations),
                    'has_solution': solution_config is not None
                }
            },
            'message': '完整推荐分析完成'
        })
        
    except Exception as e:
        logger.error(f"完整推荐服务失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '推荐服务失败，请稍后重试'
        }), 500

@recommendation_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    """
    提交推荐反馈
    
    POST /api/recommendation/feedback
    {
        "recommendation_id": "推荐ID",
        "product_id": "产品ID",
        "rating": 5,
        "feedback": "用户反馈",
        "context": {上下文信息}
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': '缺少请求数据'
            }), 400
        
        recommendation_id = data.get('recommendation_id')
        product_id = data.get('product_id')
        rating = data.get('rating')
        feedback = data.get('feedback', '')
        context = data.get('context', {})
        
        # 验证评分
        if rating is not None:
            if not isinstance(rating, (int, float)) or rating < 1 or rating > 5:
                return jsonify({
                    'success': False,
                    'error': '评分必须在1-5之间'
                }), 400
        
        # 记录反馈到数据库
        # 这里可以扩展为更复杂的反馈处理逻辑
        logger.info(f"收到推荐反馈 - 推荐ID: {recommendation_id}, 产品ID: {product_id}, 评分: {rating}")
        
        return jsonify({
            'success': True,
            'message': '反馈提交成功，感谢您的宝贵意见'
        })
        
    except Exception as e:
        logger.error(f"提交反馈失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '反馈提交失败，请稍后重试'
        }), 500

@recommendation_bp.route('/categories', methods=['GET'])
def get_product_categories():
    """
    获取产品类别信息
    
    GET /api/recommendation/categories
    """
    try:
        categories_info = {}
        
        # 获取产品模式信息
        for category, patterns in intelligent_recommendation.product_patterns.items():
            categories_info[category] = {
                'name': category,
                'keywords': patterns['keywords'][:5],  # 只返回前5个关键词
                'features': patterns['features'],
                'applications': patterns['applications']
            }
        
        # 获取应用场景信息
        application_scenarios = intelligent_recommendation.application_scenarios
        
        return jsonify({
            'success': True,
            'data': {
                'categories': categories_info,
                'application_scenarios': application_scenarios,
                'total_categories': len(categories_info)
            },
            'message': '产品类别信息获取成功'
        })
        
    except Exception as e:
        logger.error(f"获取产品类别失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '获取产品类别失败，请稍后重试'
        }), 500

@recommendation_bp.route('/stats', methods=['GET'])
def get_recommendation_stats():
    """
    获取推荐系统统计信息
    
    GET /api/recommendation/stats
    """
    try:
        # 从数据库获取统计信息
        conn = intelligent_recommendation.db.get_connection()
        
        try:
            # 缓存命中统计
            cursor = conn.execute('''
                SELECT COUNT(*) as total_cache, 
                       SUM(hit_count) as total_hits,
                       AVG(recommendation_score) as avg_score
                FROM recommendation_cache
            ''')
            cache_stats = cursor.fetchone()
            
            # 用户偏好统计
            cursor = conn.execute('''
                SELECT COUNT(DISTINCT session_id) as unique_sessions,
                       COUNT(*) as total_preferences
                FROM user_preferences
            ''')
            preference_stats = cursor.fetchone()
            
            # 产品评分统计
            cursor = conn.execute('''
                SELECT COUNT(*) as total_ratings,
                       AVG(user_rating) as avg_rating
                FROM product_ratings
            ''')
            rating_stats = cursor.fetchone()
            
            stats = {
                'cache_performance': {
                    'total_cached_questions': cache_stats['total_cache'] if cache_stats else 0,
                    'total_cache_hits': cache_stats['total_hits'] if cache_stats else 0,
                    'average_confidence': round(cache_stats['avg_score'] or 0, 2)
                },
                'user_engagement': {
                    'unique_sessions': preference_stats['unique_sessions'] if preference_stats else 0,
                    'total_preferences': preference_stats['total_preferences'] if preference_stats else 0
                },
                'product_feedback': {
                    'total_ratings': rating_stats['total_ratings'] if rating_stats else 0,
                    'average_rating': round(rating_stats['avg_rating'] or 0, 2)
                },
                'system_info': {
                    'supported_categories': len(intelligent_recommendation.product_patterns),
                    'application_scenarios': len(intelligent_recommendation.application_scenarios)
                }
            }
            
            return jsonify({
                'success': True,
                'data': stats,
                'message': '推荐系统统计信息获取成功'
            })
            
        finally:
            conn.close()
        
    except Exception as e:
        logger.error(f"获取推荐统计失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '获取推荐统计失败，请稍后重试'
        }), 500

@recommendation_bp.route('/health', methods=['GET'])
def health_check():
    """
    推荐系统健康检查
    
    GET /api/recommendation/health
    """
    try:
        # 检查数据库连接
        conn = intelligent_recommendation.db.get_connection()
        cursor = conn.execute('SELECT 1')
        cursor.fetchone()
        conn.close()
        
        # 检查推荐系统组件
        health_status = {
            'database': 'healthy',
            'recommendation_engine': 'healthy',
            'cache_system': 'healthy',
            'product_patterns': len(intelligent_recommendation.product_patterns),
            'application_scenarios': len(intelligent_recommendation.application_scenarios),
            'timestamp': '2025-01-02T12:18:00+08:00'
        }
        
        return jsonify({
            'success': True,
            'data': health_status,
            'message': '推荐系统运行正常'
        })
        
    except Exception as e:
        logger.error(f"推荐系统健康检查失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '推荐系统健康检查失败'
        }), 500

# 错误处理
@recommendation_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'API端点不存在',
        'message': '请检查请求URL是否正确'
    }), 404

@recommendation_bp.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': '请求方法不允许',
        'message': '请检查HTTP方法是否正确'
    }), 405

@recommendation_bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': '服务器内部错误',
        'message': '推荐服务暂时不可用，请稍后重试'
    }), 500
