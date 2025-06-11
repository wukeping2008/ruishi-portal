"""
产品相关API路由
"""

from flask import Blueprint, request, jsonify
from models.product_manager import product_manager
import json

product_bp = Blueprint('product', __name__)

@product_bp.route('/api/products', methods=['GET'])
def get_products():
    """获取产品列表"""
    try:
        category = request.args.get('category')
        keyword = request.args.get('keyword', '')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        # 搜索产品
        products = product_manager.search_products(keyword, category)
        
        # 分页
        total = len(products)
        start = (page - 1) * per_page
        end = start + per_page
        products_page = products[start:end]
        
        return jsonify({
            'success': True,
            'products': products_page,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@product_bp.route('/api/products/<product_id>', methods=['GET'])
def get_product_detail(product_id):
    """获取产品详情"""
    try:
        product = product_manager.get_product_by_id(product_id)
        if not product:
            return jsonify({'success': False, 'error': '产品不存在'}), 404
        
        # 获取产品规格
        specifications = product_manager.get_product_specification(product_id)
        product['specifications'] = specifications
        
        return jsonify({
            'success': True,
            'product': product
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@product_bp.route('/api/products/categories', methods=['GET'])
def get_categories():
    """获取产品分类"""
    try:
        stats = product_manager.get_categories_stats()
        categories = []
        
        for category_cn, info in stats.items():
            categories.append({
                'name_cn': category_cn,
                'name_en': info['category_en'],
                'count': info['count'],
                'products': info['products']
            })
        
        return jsonify({
            'success': True,
            'categories': categories
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@product_bp.route('/api/products/categories/<category>/products', methods=['GET'])
def get_products_by_category(category):
    """根据分类获取产品"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        products = product_manager.get_products_by_category(category)
        
        # 分页
        total = len(products)
        start = (page - 1) * per_page
        end = start + per_page
        products_page = products[start:end]
        
        return jsonify({
            'success': True,
            'category': category,
            'products': products_page,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@product_bp.route('/api/products/search', methods=['POST'])
def search_products():
    """高级产品搜索"""
    try:
        data = request.get_json()
        keyword = data.get('keyword', '')
        category = data.get('category')
        price_min = data.get('price_min')
        price_max = data.get('price_max')
        stock_status = data.get('stock_status')
        
        # 基础搜索
        products = product_manager.search_products(keyword, category)
        
        # 价格过滤
        if price_min is not None:
            products = [p for p in products if p.get('price', 0) >= price_min]
        if price_max is not None:
            products = [p for p in products if p.get('price', 0) <= price_max]
        
        # 库存状态过滤
        if stock_status:
            products = [p for p in products if p.get('stock_status') == stock_status]
        
        return jsonify({
            'success': True,
            'products': products,
            'total': len(products)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@product_bp.route('/api/products/stats', methods=['GET'])
def get_product_stats():
    """获取产品统计信息"""
    try:
        categories_stats = product_manager.get_categories_stats()
        price_stats = product_manager.get_price_range_stats()
        
        total_products = len(product_manager.products_data.get('products', []))
        total_categories = len(categories_stats)
        
        return jsonify({
            'success': True,
            'stats': {
                'total_products': total_products,
                'total_categories': total_categories,
                'categories': categories_stats,
                'price_ranges': price_stats
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@product_bp.route('/api/products/knowledge-base', methods=['GET'])
def get_ai_knowledge_base():
    """获取AI知识库"""
    try:
        knowledge_base = product_manager.generate_ai_knowledge_base()
        return jsonify({
            'success': True,
            'knowledge_base': knowledge_base
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@product_bp.route('/api/products/import', methods=['POST'])
def import_products():
    """导入产品数据"""
    try:
        data = request.get_json()
        products_data = data.get('products', [])
        
        imported_count = 0
        for product_data in products_data:
            result = product_manager.add_product_from_excel_data(product_data)
            if result:
                imported_count += 1
        
        # 保存数据
        product_manager.save_data()
        
        return jsonify({
            'success': True,
            'message': f'成功导入 {imported_count} 个产品',
            'imported_count': imported_count
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@product_bp.route('/api/products/export', methods=['GET'])
def export_products():
    """导出产品数据"""
    try:
        format_type = request.args.get('format', 'json')
        
        if format_type == 'json':
            return jsonify({
                'success': True,
                'data': product_manager.products_data
            })
        else:
            return jsonify({'success': False, 'error': '不支持的导出格式'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@product_bp.route('/api/products/recommendations', methods=['POST'])
def get_product_recommendations():
    """获取产品推荐"""
    try:
        data = request.get_json()
        user_query = data.get('query', '')
        user_requirements = data.get('requirements', {})
        
        # 基于用户查询和需求推荐产品
        recommendations = []
        
        # 简单的关键词匹配推荐
        if 'pxi' in user_query.lower():
            pxi_products = product_manager.get_products_by_category('PXIe DAQ')
            recommendations.extend(pxi_products[:3])
        
        if 'data acquisition' in user_query.lower() or '数据采集' in user_query:
            daq_products = product_manager.search_products('DAQ')
            recommendations.extend(daq_products[:3])
        
        if 'controller' in user_query.lower() or '控制器' in user_query:
            controller_products = product_manager.get_products_by_category('PXIe Controllers')
            recommendations.extend(controller_products[:3])
        
        # 去重
        seen_ids = set()
        unique_recommendations = []
        for product in recommendations:
            if product['id'] not in seen_ids:
                unique_recommendations.append(product)
                seen_ids.add(product['id'])
        
        return jsonify({
            'success': True,
            'recommendations': unique_recommendations[:5],  # 最多返回5个推荐
            'query': user_query
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
