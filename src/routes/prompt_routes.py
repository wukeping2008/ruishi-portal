"""
提示词优化系统路由
Prompt Optimization System Routes
"""

from flask import Blueprint, request, jsonify, render_template
import json
import logging
from typing import Dict, Any
import traceback
from datetime import datetime

from models.prompt_system import prompt_system_manager

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
        
        # 转换为前端期望的数组格式
        modes_array = []
        for mode_id, mode_info in available_modes.items():
            mode_data = mode_info.copy()
            mode_data['id'] = mode_id
            mode_data['icon'] = {
                'simple': '🚀',
                'template': '📄', 
                'json': '📝',
                'intelligent': '🧠',
                'expert': '🏗️'
            }.get(mode_id, '⚙️')
            modes_array.append(mode_data)
        
        return jsonify({
            'success': True,
            'modes': modes_array
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
        user_level = request.args.get('user_level', 'expert')
        manager = prompt_system_manager.get_mode_manager('template', user_level)
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

@prompt_bp.route('/template/config', methods=['GET', 'POST'])
def template_config():
    """模板配置管理"""
    try:
        user_level = request.args.get('user_level', 'expert')
        manager = prompt_system_manager.get_mode_manager('template', user_level)
        
        if request.method == 'GET':
            # 获取模板配置
            config = manager.load_config()
            return jsonify({
                'success': True,
                'config': config
            })
        
        elif request.method == 'POST':
            # 保存模板配置
            data = request.get_json()
            config = data.get('config', data)  # 兼容不同的数据格式
            
            success = manager.save_config(config)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': '模板配置保存成功'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': '模板配置保存失败'
                }), 500
                
    except Exception as e:
        logger.error(f"模板配置操作失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prompt_bp.route('/template/preview', methods=['POST'])
def preview_template():
    """预览模板效果"""
    try:
        data = request.get_json()
        
        template_type = data.get('template_type', 'general')
        content = data.get('content', '')
        variables = data.get('variables', {})
        
        if not content:
            return jsonify({
                'success': False,
                'error': '模板内容不能为空'
            }), 400
        
        # 替换变量生成预览
        preview_content = content
        for key, value in variables.items():
            preview_content = preview_content.replace(f'{{{key}}}', str(value))
        
        return jsonify({
            'success': True,
            'preview': preview_content,
            'template_type': template_type,
            'variables_used': list(variables.keys())
        })
        
    except Exception as e:
        logger.error(f"预览模板失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prompt_bp.route('/json/config', methods=['GET', 'POST'])
def json_config():
    """JSON配置模式"""
    try:
        # 获取用户权限级别，默认为expert（管理员后台）
        user_level = request.args.get('user_level', 'expert')
        manager = prompt_system_manager.get_mode_manager('json', user_level)
        
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
            if not data:
                return jsonify({
                    'success': False,
                    'error': '请求数据为空'
                }), 400
            
            # 从请求中获取配置数据，支持多种格式
            config = data.get('config', data)  # 如果没有config字段，使用整个data
            
            # 如果config是字符串，尝试解析为JSON
            if isinstance(config, str):
                try:
                    config = json.loads(config)
                except json.JSONDecodeError as e:
                    return jsonify({
                        'success': False,
                        'error': f'JSON格式错误: {str(e)}'
                    }), 400
            
            # 简化验证逻辑 - 只检查基本结构
            if not isinstance(config, dict):
                return jsonify({
                    'success': False,
                    'error': '配置必须是JSON对象格式'
                }), 400
            
            # 检查必要的字段
            if 'prompt_system' not in config:
                # 如果没有prompt_system字段，添加默认值
                config['prompt_system'] = {
                    'version': '2.0',
                    'default_language': 'zh-CN',
                    'fallback_strategy': 'layered'
                }
            
            if 'templates' not in config:
                # 如果没有templates字段，添加默认值
                config['templates'] = {}
            
            try:
                success = manager.save_config(config)
                
                if success:
                    # 尝试保存版本，如果失败也不影响主要功能
                    try:
                        version_id = prompt_system_manager.version_manager.save_version(
                            config, 'json', data.get('description', ''), data.get('author', 'system')
                        )
                    except Exception as ve:
                        logger.warning(f"保存版本失败: {ve}")
                        version_id = None
                    
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
                    
            except Exception as save_error:
                logger.error(f"保存配置时出错: {save_error}")
                return jsonify({
                    'success': False,
                    'error': f'保存配置失败: {str(save_error)}'
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
    """智能分析 - 分析问题意图和运行优化"""
    try:
        data = request.get_json()
        
        # 支持两种模式：问题意图分析 和 系统优化分析
        question = data.get('question', '')
        analyze_conversations = data.get('analyze_conversations', False)
        optimize_prompts = data.get('optimize_prompts', False)
        
        user_level = request.args.get('user_level', 'expert')
        manager = prompt_system_manager.get_mode_manager('intelligent', user_level)
        
        result = {}
        
        # 如果有问题，进行意图分析
        if question:
            intent_scores = manager.intent_analyzer.analyze_intent(question)
            result['question_analysis'] = {
                'question': question,
                'intent_scores': intent_scores,
                'primary_intent': max(intent_scores.items(), key=lambda x: x[1])[0] if intent_scores else 'unknown'
            }
        
        # 如果请求系统分析
        if analyze_conversations or optimize_prompts:
            analysis_result = {
                'timestamp': datetime.now().isoformat(),
                'analysis_type': 'system_optimization',
                'conversations_analyzed': 0,
                'optimizations_found': 0,
                'recommendations': []
            }
            
            # 模拟分析过程
            if analyze_conversations:
                analysis_result['conversations_analyzed'] = 50  # 模拟分析了50个对话
                analysis_result['recommendations'].append({
                    'type': 'conversation_pattern',
                    'description': '发现用户经常询问产品规格相关问题',
                    'suggestion': '建议增强产品介绍模板的详细程度'
                })
            
            if optimize_prompts:
                analysis_result['optimizations_found'] = 3  # 模拟找到3个优化点
                analysis_result['recommendations'].append({
                    'type': 'prompt_optimization',
                    'description': '检测到技术支持类问题的回答准确度可以提升',
                    'suggestion': '建议在技术支持模板中添加更多故障排除步骤'
                })
                analysis_result['recommendations'].append({
                    'type': 'knowledge_integration',
                    'description': '知识库内容利用率较低',
                    'suggestion': '建议优化知识库检索算法，提高相关内容匹配度'
                })
            
            result['system_analysis'] = analysis_result
        
        # 如果没有任何有效输入
        if not question and not analyze_conversations and not optimize_prompts:
            return jsonify({
                'success': False,
                'error': '请提供问题进行意图分析，或启用系统分析选项'
            }), 400
        
        return jsonify({
            'success': True,
            'analysis': result
        })
        
    except Exception as e:
        logger.error(f"智能分析失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prompt_bp.route('/intelligent/optimizations', methods=['GET'])
def get_optimization_suggestions():
    """获取优化建议"""
    try:
        user_level = request.args.get('user_level', 'expert')
        manager = prompt_system_manager.get_mode_manager('intelligent', user_level)
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
        user_level = request.args.get('user_level', 'expert')
        manager = prompt_system_manager.get_mode_manager('expert', user_level)
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

@prompt_bp.route('/expert/config', methods=['GET', 'POST'])
def expert_config():
    """专家模式配置管理"""
    try:
        user_level = request.args.get('user_level', 'expert')
        manager = prompt_system_manager.get_mode_manager('expert', user_level)
        
        if request.method == 'GET':
            # 获取专家模式配置
            config = manager.load_config()
            return jsonify({
                'success': True,
                'config': config
            })
        
        elif request.method == 'POST':
            # 保存专家模式配置
            data = request.get_json()
            config = data.get('config', data)  # 兼容不同的数据格式
            
            success = manager.save_config(config)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': '专家模式配置保存成功'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': '专家模式配置保存失败'
                }), 500
                
    except Exception as e:
        logger.error(f"专家模式配置操作失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prompt_bp.route('/expert/preview', methods=['POST'])
def preview_expert_prompt():
    """预览专家模式提示词"""
    try:
        data = request.get_json()
        
        # 构建示例提示词
        foundation_layer = data.get('foundation_layer', '你是简仪科技的专业AI助手。')
        business_product = data.get('business_product', '作为产品专家，请重点介绍相关产品特性。')
        business_technical = data.get('business_technical', '作为技术专家，请提供详细的技术支持。')
        business_training = data.get('business_training', '作为培训专家，请提供完整的学习指导。')
        personal_preference = data.get('personal_preference', '请根据用户偏好调整回答风格。')
        
        # 合成预览
        preview = f"""=== 基础层 ===
{foundation_layer}

=== 业务层 - 产品咨询 ===
{business_product}

=== 业务层 - 技术支持 ===
{business_technical}

=== 业务层 - 教育培训 ===
{business_training}

=== 个性化层 ===
{personal_preference}

=== 合成示例 ===
{foundation_layer}

根据问题类型，会自动选择相应的业务层提示词：
- 产品相关问题 → {business_product}
- 技术支持问题 → {business_technical}
- 学习培训问题 → {business_training}

最后应用个性化设置：
{personal_preference}

## 用户问题：[示例问题]

请基于以上分层指导原则，提供专业、准确、个性化的回答。"""
        
        return jsonify({
            'success': True,
            'preview': preview
        })
        
    except Exception as e:
        logger.error(f"预览专家模式失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prompt_bp.route('/intelligent/config', methods=['GET', 'POST'])
def intelligent_config():
    """智能模式配置管理"""
    try:
        user_level = request.args.get('user_level', 'expert')
        manager = prompt_system_manager.get_mode_manager('intelligent', user_level)
        
        if request.method == 'GET':
            # 获取智能模式配置
            config = manager.load_config()
            return jsonify({
                'success': True,
                'config': config
            })
        
        elif request.method == 'POST':
            # 保存智能模式配置
            data = request.get_json()
            config = data.get('config', data)  # 兼容不同的数据格式
            
            success = manager.save_config(config)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': '智能模式配置保存成功'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': '智能模式配置保存失败'
                }), 500
                
    except Exception as e:
        logger.error(f"智能模式配置操作失败: {e}")
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
        user_level = data.get('user_level', 'expert')  # 管理后台默认使用expert权限
        
        if not question:
            return jsonify({
                'success': False,
                'error': '测试问题不能为空'
            }), 400
        
        # 模拟知识库内容，用于测试
        sample_knowledge = """
## 简仪科技产品知识库

### 公司简介
简仪科技（JYTEK）成立于2016年，专注于测试测量技术创新。
核心产品：锐视测控平台（SeeSharp Platform）
技术特色：开源测控解决方案、国产自主可控、AI集成

### 主要产品
1. **PXI数据采集卡**
   - 高精度模拟输入
   - 多通道同步采集
   - 支持各种传感器接口

2. **PXI信号发生器**
   - 任意波形生成
   - 高频信号输出
   - 精确时序控制

3. **锐视测控软件**
   - 图形化编程界面
   - 实时数据处理
   - 自动化测试流程

### 技术优势
- 自主研发的核心算法
- 完整的产品生态链
- 专业的技术支持团队
        """
        
        # 构建提示词上下文，包含知识库内容
        context = {
            'knowledge_content': config.get('knowledge_content', sample_knowledge),
            'user_preferences': config.get('user_preferences', {}),
            'user_context': f'测试环境 - {mode}模式'
        }
        
        prompt = prompt_system_manager.build_prompt(
            question=question,
            mode=mode,
            user_level=user_level,
            context=context
        )
        
        # 分析提示词特征
        has_knowledge = bool(context.get('knowledge_content', '').strip())
        
        return jsonify({
            'success': True,
            'generated_prompt': prompt,
            'mode': mode,
            'prompt_length': len(prompt),
            'estimated_tokens': int(len(prompt.split()) * 1.3),
            'complexity_score': _calculate_complexity_score(prompt),
            'has_knowledge': has_knowledge
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
