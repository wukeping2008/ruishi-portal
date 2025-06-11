"""
提示词优化系统路由
Prompt Optimization System Routes
"""

from flask import Blueprint, request, jsonify, render_template
import json
import logging
from typing import Dict, Any
import traceback

from ..models.prompt_system import prompt_system_manager

# 创建蓝图
prompt_bp = Blueprint('prompt', __name__, url_prefix='/api/prompt')

logger = logging.getLogger(__name__)

@prompt_bp.route('/modes', methods=['GET'])
def get_available_modes():
    """获取可用的提示词模式"""
    try:
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
        
        # 根据用户权限过滤模式
        available_modes = {}
        permission_levels = prompt_system_manager.permission_levels
        allowed_modes = permission_levels.get(user_level, ['simple'])
        
        for mode_key in allowed_modes:
            if mode_key in modes:
                available_modes[mode_key] = modes[mode_key]
        
        return jsonify({
            'success': True,
            'data': {
                'modes': available_modes,
                'user_level': user_level,
                'total_modes': len(available_modes)
            }
        })
        
    except Exception as e:
        logger.error(f"获取可用模式失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prompt_bp.route('/build', methods=['POST'])
def build_prompt():
    """构建提示词"""
    try:
        data = request.get_json()
        
        question = data.get('question', '')
        mode = data.get('mode', 'simple')
        user_level = data.get('user_level', 'basic')
        context = data.get('context', {})
        
        if not question:
            return jsonify({
                'success': False,
                'error': '问题不能为空'
            }), 400
        
        # 构建提示词
        prompt = prompt_system_manager.build_prompt(
            question=question,
            mode=mode,
            user_level=user_level,
            context=context
        )
        
        return jsonify({
            'success': True,
            'data': {
                'prompt': prompt,
                'mode': mode,
                'question': question,
                'length': len(prompt)
            }
        })
        
    except PermissionError as e:
        return jsonify({
            'success': False,
            'error': f'权限不足: {str(e)}'
        }), 403
        
    except Exception as e:
        logger.error(f"构建提示词失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prompt_bp.route('/simple/config', methods=['GET', 'POST'])
def simple_config():
    """简单模式配置"""
    try:
        manager = prompt_system_manager.get_mode_manager('simple')
        
        if request.method == 'GET':
            # 获取配置
            config = manager.load_config()
            return jsonify({
                'success': True,
                'data': config
            })
        
        elif request.method == 'POST':
            # 保存配置
            data = request.get_json()
            config = data.get('config', {})
            
            success = manager.save_config(config)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': '配置保存成功'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': '配置保存失败'
                }), 500
                
    except Exception as e:
        logger.error(f"简单模式配置操作失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prompt_bp.route('/template/categories', methods=['GET'])
def get_template_categories():
    """获取模板分类"""
    try:
        manager = prompt_system_manager.get_mode_manager('template')
        config = manager.load_config()
        
        return jsonify({
            'success': True,
            'data': config.get('templates', {})
        })
        
    except Exception as e:
        logger.error(f"获取模板分类失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prompt_bp.route('/template/save', methods=['POST'])
def save_template():
    """保存模板"""
    try:
        data = request.get_json()
        
        category = data.get('category', '')
        template_content = data.get('template_content', '')
        variables = data.get('variables', [])
        
        if not category or not template_content:
            return jsonify({
                'success': False,
                'error': '分类和模板内容不能为空'
            }), 400
        
        manager = prompt_system_manager.get_mode_manager('template')
        success = manager.save_template(category, template_content, variables)
        
        if success:
            return jsonify({
                'success': True,
                'message': '模板保存成功'
            })
        else:
            return jsonify({
                'success': False,
                'error': '模板保存失败'
            }), 500
            
    except Exception as e:
        logger.error(f"保存模板失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prompt_bp.route('/json/config', methods=['GET', 'POST'])
def json_config():
    """JSON配置模式"""
    try:
        manager = prompt_system_manager.get_mode_manager('json')
        
        if request.method == 'GET':
            # 获取配置
            config = manager.load_config()
            return jsonify({
                'success': True,
                'data': config
            })
        
        elif request.method == 'POST':
            # 保存配置
            data = request.get_json()
            config = data.get('config', {})
            
            # 验证JSON格式
            validator = prompt_system_manager.config_validator
            is_valid, errors = validator.validate(config, 'json')
            
            if not is_valid:
                return jsonify({
                    'success': False,
                    'error': '配置格式错误',
                    'details': errors
                }), 400
            
            success = manager.save_config(config)
            
            if success:
                # 保存版本
                version_id = prompt_system_manager.version_manager.save_version(
                    config, 'json', data.get('description', ''), data.get('author', 'system')
                )
                
                return jsonify({
                    'success': True,
                    'message': '配置保存成功',
                    'version_id': version_id
                })
            else:
                return jsonify({
                    'success': False,
                    'error': '配置保存失败'
                }), 500
                
    except Exception as e:
        logger.error(f"JSON配置操作失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prompt_bp.route('/json/validate', methods=['POST'])
def validate_json_config():
    """验证JSON配置"""
    try:
        data = request.get_json()
        config = data.get('config', {})
        
        validator = prompt_system_manager.config_validator
        is_valid, errors = validator.validate(config, 'json')
        
        return jsonify({
            'success': True,
            'data': {
                'valid': is_valid,
                'errors': errors
            }
        })
        
    except Exception as e:
        logger.error(f"验证JSON配置失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prompt_bp.route('/intelligent/analysis', methods=['POST'])
def analyze_question_intent():
    """分析问题意图"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({
                'success': False,
                'error': '问题不能为空'
            }), 400
        
        manager = prompt_system_manager.get_mode_manager('intelligent')
        intent_scores = manager.intent_analyzer.analyze_intent(question)
        
        return jsonify({
            'success': True,
            'data': {
                'question': question,
                'intent_scores': intent_scores,
                'primary_intent': max(intent_scores.items(), key=lambda x: x[1])[0]
            }
        })
        
    except Exception as e:
        logger.error(f"分析问题意图失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prompt_bp.route('/intelligent/optimizations', methods=['GET'])
def get_optimization_suggestions():
    """获取优化建议"""
    try:
        manager = prompt_system_manager.get_mode_manager('intelligent')
        optimizations = manager._get_applicable_optimizations({})
        
        return jsonify({
            'success': True,
            'data': {
                'optimizations': optimizations,
                'total': len(optimizations)
            }
        })
        
    except Exception as e:
        logger.error(f"获取优化建议失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prompt_bp.route('/expert/layers', methods=['GET'])
def get_expert_layers():
    """获取专家模式层级配置"""
    try:
        manager = prompt_system_manager.get_mode_manager('expert')
        config = manager.load_config()
        
        layers_info = {
            'foundation': {
                'name': '基础层',
                'description': '公司核心信息，所有回答的基础',
                'components': ['公司身份', '核心价值观', '回答原则']
            },
            'business': {
                'name': '业务层',
                'description': '场景特定的专业提示词',
                'components': ['产品咨询', '技术支持', '教育培训']
            },
            'personalization': {
                'name': '个性化层',
                'description': '用户自定义和偏好设置',
                'components': ['用户偏好', '行业定制', '个人设置']
            }
        }
        
        return jsonify({
            'success': True,
            'data': {
                'layers': layers_info,
                'config': config
            }
        })
        
    except Exception as e:
        logger.error(f"获取专家模式层级失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prompt_bp.route('/versions', methods=['GET'])
def get_config_versions():
    """获取配置版本列表"""
    try:
        config_type = request.args.get('type')
        versions = prompt_system_manager.version_manager.get_versions(config_type)
        
        return jsonify({
            'success': True,
            'data': {
                'versions': versions,
                'total': len(versions)
            }
        })
        
    except Exception as e:
        logger.error(f"获取配置版本失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prompt_bp.route('/backup', methods=['POST'])
def create_backup():
    """创建备份"""
    try:
        data = request.get_json()
        trigger = data.get('trigger', 'manual')
        
        backup_file = prompt_system_manager.backup_manager.create_backup(trigger)
        
        if backup_file:
            return jsonify({
                'success': True,
                'message': '备份创建成功',
                'backup_file': backup_file
            })
        else:
            return jsonify({
                'success': False,
                'error': '备份创建失败'
            }), 500
            
    except Exception as e:
        logger.error(f"创建备份失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prompt_bp.route('/test', methods=['POST'])
def test_prompt():
    """测试提示词效果"""
    try:
        data = request.get_json()
        
        question = data.get('question', '')
        mode = data.get('mode', 'simple')
        config = data.get('config', {})
        
        if not question:
            return jsonify({
                'success': False,
                'error': '测试问题不能为空'
            }), 400
        
        # 构建提示词
        context = {
            'knowledge_content': config.get('knowledge_content', ''),
            'user_preferences': config.get('user_preferences', {})
        }
        
        prompt = prompt_system_manager.build_prompt(
            question=question,
            mode=mode,
            context=context
        )
        
        # 分析提示词特征
        analysis = {
            'length': len(prompt),
            'has_knowledge_content': 'knowledge_content' in context and bool(context['knowledge_content']),
            'estimated_tokens': len(prompt.split()) * 1.3,  # 粗略估算
            'complexity_score': _calculate_complexity_score(prompt)
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
        logger.error(f"测试提示词失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prompt_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    """提交用户反馈"""
    try:
        data = request.get_json()
        
        question_id = data.get('question_id', '')
        prompt_config = data.get('prompt_config', {})
        ai_response = data.get('ai_response', '')
        user_feedback = data.get('feedback', {})
        
        # 跟踪效果
        manager = prompt_system_manager.get_mode_manager('intelligent')
        manager.effectiveness_tracker.track_response(
            question_id, prompt_config, ai_response, user_feedback
        )
        
        return jsonify({
            'success': True,
            'message': '反馈提交成功'
        })
        
    except Exception as e:
        logger.error(f"提交反馈失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def _calculate_complexity_score(prompt: str) -> float:
    """计算提示词复杂度分数"""
    try:
        # 基于多个因素计算复杂度
        factors = {
            'length': len(prompt) / 1000,  # 长度因子
            'structure': prompt.count('\n') / 10,  # 结构因子
            'variables': prompt.count('{') + prompt.count('}'),  # 变量因子
            'keywords': len([word for word in ['重要', '优先', '基于', '请'] if word in prompt])  # 关键词因子
        }
        
        # 加权计算
        weights = {'length': 0.3, 'structure': 0.3, 'variables': 0.2, 'keywords': 0.2}
        score = sum(factors[key] * weights[key] for key in factors)
        
        return min(score, 5.0)  # 限制在5分以内
        
    except Exception:
        return 1.0  # 默认复杂度

# 错误处理
@prompt_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': '接口不存在'
    }), 404

@prompt_bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': '服务器内部错误'
    }), 500
