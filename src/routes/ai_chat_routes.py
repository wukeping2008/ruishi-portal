"""
AI聊天相关API路由
"""

from flask import Blueprint, request, jsonify
from models.product_manager import product_manager
from models.recommendation import intelligent_recommendation
import json
import re

ai_chat_bp = Blueprint('ai_chat', __name__)

# 使用全局推荐系统实例
recommendation_engine = intelligent_recommendation

@ai_chat_bp.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    """AI聊天接口"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        context = data.get('context', 'general')
        filters = data.get('filters', {})
        
        if not message.strip():
            return jsonify({
                'success': False,
                'error': '消息不能为空'
            }), 400
        
        # 分析用户意图
        intent = analyze_user_intent(message)
        
        # 根据意图生成回复
        response_data = generate_ai_response(message, intent, context, filters)
        
        return jsonify({
            'success': True,
            'response': response_data['response'],
            'recommendations': response_data.get('recommendations', []),
            'intent': intent
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'AI聊天服务暂时不可用: {str(e)}'
        }), 500

def analyze_user_intent(message):
    """分析用户意图"""
    message_lower = message.lower()
    
    # 产品搜索意图
    if any(keyword in message_lower for keyword in ['找', '搜索', '查找', '需要', '想要', '推荐']):
        if any(keyword in message_lower for keyword in ['pxi', 'daq', '数据采集', '控制器', '模块']):
            return 'product_search'
    
    # 产品对比意图
    if any(keyword in message_lower for keyword in ['对比', '比较', '区别', '差异']):
        return 'product_compare'
    
    # 技术咨询意图
    if any(keyword in message_lower for keyword in ['怎么', '如何', '什么是', '原理', '技术']):
        return 'technical_inquiry'
    
    # 价格咨询意图
    if any(keyword in message_lower for keyword in ['价格', '多少钱', '费用', '成本']):
        return 'price_inquiry'
    
    # 规格咨询意图
    if any(keyword in message_lower for keyword in ['规格', '参数', '性能', '指标']):
        return 'specification_inquiry'
    
    # 应用场景咨询
    if any(keyword in message_lower for keyword in ['应用', '场景', '用途', '适合']):
        return 'application_inquiry'
    
    return 'general_inquiry'

def generate_ai_response(message, intent, context, filters):
    """生成AI回复"""
    response_data = {
        'response': '',
        'recommendations': []
    }
    
    if intent == 'product_search':
        response_data = handle_product_search(message, filters)
    elif intent == 'product_compare':
        response_data = handle_product_compare(message)
    elif intent == 'technical_inquiry':
        response_data = handle_technical_inquiry(message)
    elif intent == 'price_inquiry':
        response_data = handle_price_inquiry(message)
    elif intent == 'specification_inquiry':
        response_data = handle_specification_inquiry(message)
    elif intent == 'application_inquiry':
        response_data = handle_application_inquiry(message)
    else:
        response_data = handle_general_inquiry(message)
    
    return response_data

def handle_product_search(message, filters):
    """处理产品搜索请求"""
    # 提取关键词
    keywords = extract_keywords(message)
    
    # 搜索产品
    products = []
    for keyword in keywords:
        search_results = product_manager.search_products(keyword)
        products.extend(search_results)
    
    # 去重
    unique_products = []
    seen_ids = set()
    for product in products:
        if product['id'] not in seen_ids:
            unique_products.append(product)
            seen_ids.add(product['id'])
    
    # 生成推荐
    recommendations = []
    for product in unique_products[:5]:  # 最多推荐5个
        recommendations.append({
            'product_id': product['id'],
            'name': product.get('name', product.get('part_number', '')),
            'description': product.get('description', ''),
            'price_range': format_price_range(product.get('price', 0)),
            'recommendation_score': 0.8  # 简单的推荐分数
        })
    
    if recommendations:
        response = f"根据您的需求，我为您找到了 {len(recommendations)} 个相关产品。这些产品都符合您提到的关键词：{', '.join(keywords)}。"
    else:
        response = "抱歉，没有找到符合您需求的产品。您可以尝试使用其他关键词搜索，或者告诉我更具体的需求。"
    
    return {
        'response': response,
        'recommendations': recommendations
    }

def handle_product_compare(message):
    """处理产品对比请求"""
    response = "产品对比功能可以帮您详细比较不同产品的规格和特性。您可以在产品列表中选择要对比的产品，然后点击'开始对比'按钮。我可以为您分析产品在以下方面的差异：\n\n• 技术规格参数\n• 价格和性价比\n• 应用场景适配\n• 性能优势对比\n\n请告诉我您想对比哪些具体产品？"
    
    return {
        'response': response,
        'recommendations': []
    }

def handle_technical_inquiry(message):
    """处理技术咨询"""
    # 简单的技术问答
    tech_responses = {
        'pxi': 'PXI（PCI eXtensions for Instrumentation）是一种基于PC的测量和自动化平台，结合了PCI总线的电气特性和CompactPCI的机械封装。PXI系统具有高性能、模块化、可扩展的特点，广泛应用于测试测量、数据采集和工业自动化领域。',
        'daq': '数据采集（DAQ）是将模拟信号转换为数字信号的过程，包括信号调理、模数转换、数字信号处理等步骤。DAQ系统通常包括传感器、信号调理电路、ADC转换器和计算机软件。',
        '控制器': 'PXI控制器是PXI系统的核心，负责系统控制、数据处理和通信。控制器通常基于工业级计算机平台，具有高可靠性、实时性能和丰富的I/O接口。'
    }
    
    message_lower = message.lower()
    response = "这是一个很好的技术问题。"
    
    for keyword, tech_response in tech_responses.items():
        if keyword in message_lower:
            response = tech_response
            break
    else:
        response += "我建议您查看我们的技术文档或联系技术支持团队获取更详细的信息。您也可以具体说明您想了解的技术细节，我会尽力为您解答。"
    
    return {
        'response': response,
        'recommendations': []
    }

def handle_price_inquiry(message):
    """处理价格咨询"""
    response = "产品价格会根据具体型号、配置和采购数量有所不同。我建议您：\n\n• 查看产品详情页面的参考价格\n• 联系我们的销售团队获取准确报价\n• 考虑批量采购的优惠政策\n\n如果您有特定的预算范围，我可以为您推荐合适的产品。请告诉我您的预算区间？"
    
    return {
        'response': response,
        'recommendations': []
    }

def handle_specification_inquiry(message):
    """处理规格咨询"""
    response = "产品规格是选择合适设备的重要依据。我可以帮您了解：\n\n• 技术参数详细说明\n• 性能指标对比\n• 兼容性要求\n• 应用限制条件\n\n请告诉我您关心的具体规格参数，比如采样率、精度、通道数等，我会为您详细介绍。"
    
    return {
        'response': response,
        'recommendations': []
    }

def handle_application_inquiry(message):
    """处理应用场景咨询"""
    response = "我们的产品广泛应用于多个领域：\n\n• 汽车测试：发动机测试、排放检测、耐久性试验\n• 航空航天：飞行器测试、结构分析、环境模拟\n• 工业自动化：生产线监控、质量检测、过程控制\n• 科研教育：实验室测量、教学演示、研究开发\n\n请告诉我您的具体应用场景，我可以为您推荐最适合的产品解决方案。"
    
    return {
        'response': response,
        'recommendations': []
    }

def handle_general_inquiry(message):
    """处理一般咨询"""
    response = "您好！我是简仪科技的AI产品助手。我可以帮助您：\n\n• 🔍 搜索和推荐产品\n• 📊 对比产品规格\n• 💡 解答技术问题\n• 💰 提供价格信息\n• 🎯 推荐应用方案\n\n请告诉我您需要什么帮助，我会尽力为您提供专业的建议。"
    
    return {
        'response': response,
        'recommendations': []
    }

def extract_keywords(message):
    """从消息中提取关键词"""
    # 产品相关关键词
    product_keywords = [
        'pxi', 'pxie', 'daq', 'controller', 'module',
        '控制器', '模块', '数据采集', '测量', '测试',
        'ni-9', 'pxie-', 'pxi-', 'cdaq', 'compactdaq'
    ]
    
    keywords = []
    message_lower = message.lower()
    
    for keyword in product_keywords:
        if keyword in message_lower:
            keywords.append(keyword)
    
    # 提取型号
    model_pattern = r'(ni-\d+|pxie?-\d+|cdaq-\d+)'
    models = re.findall(model_pattern, message_lower)
    keywords.extend(models)
    
    return list(set(keywords)) if keywords else ['daq']  # 默认搜索DAQ产品

def format_price_range(price):
    """格式化价格范围"""
    if not price or price == 0:
        return "询价"
    elif price < 5000:
        return "¥5,000以下"
    elif price < 15000:
        return "¥5,000-15,000"
    elif price < 50000:
        return "¥15,000-50,000"
    else:
        return "¥50,000以上"

@ai_chat_bp.route('/api/ai/product-recommendations', methods=['POST'])
def get_ai_product_recommendations():
    """基于AI的产品推荐"""
    try:
        data = request.get_json()
        user_requirements = data.get('requirements', {})
        context = data.get('context', {})
        
        # 使用推荐引擎分析用户意图并推荐产品
        intent_data = recommendation_engine.analyze_user_intent(
            question=user_requirements.get('description', ''),
            context=context
        )
        
        # 基于意图推荐产品
        recommendations = recommendation_engine.recommend_products(intent_data)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ai_chat_bp.route('/api/ai/analyze-requirements', methods=['POST'])
def analyze_requirements():
    """分析用户需求"""
    try:
        data = request.get_json()
        description = data.get('description', '')
        
        # 简单的需求分析
        analysis = {
            'categories': [],
            'specifications': {},
            'budget_range': '',
            'application_area': ''
        }
        
        description_lower = description.lower()
        
        # 分析产品类别
        if any(keyword in description_lower for keyword in ['pxi', 'pxie']):
            analysis['categories'].append('PXI/PXIe')
        if any(keyword in description_lower for keyword in ['daq', '数据采集']):
            analysis['categories'].append('数据采集')
        if any(keyword in description_lower for keyword in ['controller', '控制器']):
            analysis['categories'].append('控制器')
        
        # 分析规格需求
        channel_match = re.search(r'(\d+)\s*(?:通道|channel)', description_lower)
        if channel_match:
            analysis['specifications']['channels'] = int(channel_match.group(1))
        
        # 分析预算
        budget_patterns = [
            (r'(\d+)万以下', lambda x: f"¥{int(x)*10000}以下"),
            (r'(\d+)-(\d+)万', lambda x, y: f"¥{int(x)*10000}-{int(y)*10000}"),
            (r'(\d+)k以下', lambda x: f"¥{int(x)*1000}以下")
        ]
        
        for pattern, formatter in budget_patterns:
            match = re.search(pattern, description_lower)
            if match:
                analysis['budget_range'] = formatter(*match.groups())
                break
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
