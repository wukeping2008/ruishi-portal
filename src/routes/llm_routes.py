"""
API routes for LLM integration in Ruishi Control Platform
锐视测控平台LLM集成路由
"""

from flask import Blueprint, request, jsonify
import json
import os
import time
from models.llm_models import model_selector
from models.enhanced_knowledge import enhanced_knowledge_base
from models.ai_conversation import ai_conversation_manager
from config.jytek_prompts import build_enhanced_prompt, get_prompt_template

# Create blueprint
llm_bp = Blueprint('llm', __name__, url_prefix='/api/llm')

@llm_bp.route('/ask', methods=['POST'])
def ask_question():
    """
    Endpoint to ask a question to the selected LLM
    支持知识库增强的AI问答
    
    Request body:
    {
        "question": "Your question here",
        "provider": "claude", // optional, defaults to auto-selection
        "model": "claude-3-sonnet-20240229",    // optional, defaults to provider default
        "options": {          // optional
            "temperature": 0.7,
            "max_tokens": 1000
        }
    }
    """
    try:
        data = request.json
        
        if not data or 'question' not in data:
            return jsonify({
                'error': 'Missing required parameter: question'
            }), 400
        
        question = data['question']
        provider = data.get('provider')
        model = data.get('model')
        options = data.get('options', {})
        context_type = data.get('context_type', 'company')  # 新增：上下文类型
        
        # 获取知识库相关内容
        relevant_content = enhanced_knowledge_base.get_relevant_content(question, max_docs=3)
        print(f"DEBUG: 知识库搜索结果长度: {len(relevant_content) if relevant_content else 0}")
        if relevant_content:
            print(f"DEBUG: 知识库内容预览: {relevant_content[:200]}...")
        
        # 智能判断问题类型并选择合适的提示词模板
        question_lower = question.lower()
        if any(keyword in question_lower for keyword in ['misd', '模块仪器软件词典', '语法树', 'api']):
            context_type = 'misd'
        elif any(keyword in question_lower for keyword in ['推荐', '选择', '产品', '方案', '配置']):
            context_type = 'product_recommendation'
        elif any(keyword in question_lower for keyword in ['代码', '编程', 'c#', 'python', '开发']):
            context_type = 'code_generation'
        elif any(keyword in question_lower for keyword in ['教学', '教育', '科研', '实验', '学习']):
            context_type = 'education'
        elif any(keyword in question_lower for keyword in ['故障', '错误', '问题', '调试', '排除']):
            context_type = 'troubleshooting'
        
        # 使用增强的提示词系统
        enhanced_question = build_enhanced_prompt(
            question=question,
            context_type=context_type,
            additional_context=f"相关知识库内容：\n{relevant_content}" if relevant_content else ""
        )
        
        # 记录开始时间
        start_time = time.time()
        
        # Generate response from LLM
        response = model_selector.ask_question(
            question=enhanced_question,
            provider=provider,
            model=model,
            options=options
        )
        
        # 计算响应时间
        response_time = time.time() - start_time
        
        # 添加知识库信息到响应
        response['has_knowledge_base_content'] = bool(relevant_content)
        if relevant_content:
            response['knowledge_base_sources'] = len(enhanced_knowledge_base.search_documents(question, limit=3))
        
        # 记录AI对话到数据库
        try:
            # 获取用户信息
            user_ip = request.environ.get('REMOTE_ADDR', 'unknown')
            user_agent = request.headers.get('User-Agent', 'unknown')
            session_id = request.headers.get('X-Session-ID') or request.cookies.get('session_id', f"guest_{user_ip}_{int(time.time())}")
            
            # 检查是否为注册用户
            user_id = None
            user_type = 'guest'
            auth_token = request.headers.get('Authorization') or request.cookies.get('admin_session')
            if auth_token:
                from models.database import user_manager
                user = user_manager.verify_session(auth_token)
                if user:
                    user_id = user['id']
                    user_type = 'registered'
            
            # 获取相关文档列表
            related_docs = []
            if relevant_content:
                docs = enhanced_knowledge_base.search_documents(question, limit=3)
                related_docs = [
                    {
                        'id': doc.get('id'),
                        'filename': doc.get('original_filename', ''),
                        'title': doc.get('title', ''),
                        'category': doc.get('category', ''),
                        'file_type': doc.get('file_type', ''),
                        'relevance_score': doc.get('relevance_score', 0)
                    }
                    for doc in docs if doc.get('id')  # 确保有有效的文档ID
                ]
            
            # 记录对话
            conversation_id = ai_conversation_manager.record_conversation(
                question=question,
                answer=response.get('content', ''),
                ai_provider=response.get('provider', 'unknown'),
                ai_model=response.get('model', 'unknown'),
                user_id=user_id,
                session_id=session_id,
                user_type=user_type,
                user_ip=user_ip,
                user_agent=user_agent,
                trigger_type='question',
                related_documents=related_docs if related_docs else None,
                response_time=response_time
            )
            
            # 添加对话ID到响应
            if conversation_id:
                response['conversation_id'] = conversation_id
                
        except Exception as e:
            # 记录失败不影响主要功能
            print(f"记录AI对话失败: {e}")
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'An error occurred while processing your request'
        }), 500

@llm_bp.route('/providers', methods=['GET'])
def get_providers():
    """Get all available LLM providers"""
    try:
        providers = model_selector.get_available_providers()
        return jsonify({
            'providers': providers,
            'default_provider': model_selector.default_provider
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'An error occurred while fetching providers'
        }), 500

@llm_bp.route('/models/<provider>', methods=['GET'])
def get_provider_models(provider):
    """Get available models for a specific provider"""
    try:
        if provider in model_selector.providers:
            provider_info = model_selector.providers[provider]
            models = provider_info.get('models', [])
            return jsonify({
                'provider': provider,
                'models': models
            })
        else:
            return jsonify({
                'error': f'Provider {provider} not found'
            }), 404
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': f'An error occurred while fetching models for {provider}'
        }), 500

@llm_bp.route('/generate-related-content', methods=['POST'])
def generate_related_content():
    """
    Generate related knowledge points and experiments based on question and answer
    基于问题和回答生成相关知识点和实验
    
    Request body:
    {
        "question": "用户的问题",
        "answer": "AI的回答内容"
    }
    """
    try:
        data = request.json
        
        if not data or 'question' not in data or 'answer' not in data:
            return jsonify({
                'error': 'Missing required parameters: question and answer'
            }), 400
        
        question = data['question']
        answer = data['answer']
        
        # 生成相关技术的提示词
        technology_prompt = f"""
基于以下问题和回答，请生成4个最相关的PXI技术领域。每个技术应该是具体的、实用的技术概念。

问题：{question}
回答：{answer}

请以JSON格式返回，格式如下：
{{
    "knowledge_points": [
        {{"title": "PXI总线技术", "description": "PXI总线的技术原理和应用"}},
        {{"title": "高速数据采集", "description": "高速数据采集技术和实现方法"}},
        {{"title": "实时信号处理", "description": "实时信号处理算法和硬件实现"}},
        {{"title": "同步测量技术", "description": "多通道同步测量的技术要点"}}
    ]
}}
"""

        # 生成推荐配置的提示词
        configuration_prompt = f"""
基于以下问题和回答，请生成4个最相关的PXI系统配置方案。每个配置应该是实际可行的硬件配置。

问题：{question}
回答：{answer}

请以JSON格式返回，格式如下：
{{
    "experiments": [
        {{"title": "基础数据采集配置", "type": "basic_daq", "description": "适合入门级数据采集应用的PXI配置"}},
        {{"title": "高精度测量配置", "type": "precision", "description": "高精度测量应用的专业PXI配置"}},
        {{"title": "多通道同步配置", "type": "multichannel", "description": "多通道同步采集的PXI系统配置"}},
        {{"title": "自动化测试配置", "type": "automation", "description": "自动化测试系统的完整PXI配置"}}
    ]
}}
"""

        # 生成产品展示的提示词
        product_prompt = f"""
基于以下问题和回答，请生成简仪科技相关产品的展示内容。产品展示应该包含图片、规格和特点。

问题：{question}
回答：{answer}

请以JSON格式返回产品展示设计，格式如下：
{{
    "simulation": {{
        "title": "简仪科技产品展示",
        "type": "product-gallery",
        "description": "根据您的问题推荐的简仪科技产品",
        "products": [
            {{
                "id": "pxi-daq-001",
                "name": "PXI数据采集模块",
                "icon": "fa-microchip",
                "description": "高精度多通道数据采集模块",
                "specs": ["16位分辨率", "1MS/s采样率", "32通道同步"],
                "features": {{"分辨率": "16位", "采样率": "1MS/s", "通道数": "32", "带宽": "100kHz", "价格": "联系销售"}}
            }},
            {{
                "id": "pxi-awg-001", 
                "name": "PXI任意波形发生器",
                "icon": "fa-wave-square",
                "description": "高性能任意波形发生器",
                "specs": ["100MHz带宽", "任意波形", "双通道输出"],
                "features": {{"分辨率": "14位", "采样率": "500MS/s", "通道数": "2", "带宽": "100MHz", "价格": "联系销售"}}
            }}
        ]
    }}
}}
"""

        # 生成三种内容
        try:
            knowledge_result = model_selector.ask_question(
                question=technology_prompt,
                provider=None,
                model=None,
                options={'temperature': 0.7}
            )
            
            experiment_result = model_selector.ask_question(
                question=configuration_prompt,
                provider=None,
                model=None,
                options={'temperature': 0.7}
            )
            
            simulation_result = model_selector.ask_question(
                question=product_prompt,
                provider=None,
                model=None,
                options={'temperature': 0.7}
            )
            
            # 解析JSON响应
            try:
                knowledge_data = json.loads(knowledge_result['content'])
                experiment_data = json.loads(experiment_result['content'])
                simulation_data = json.loads(simulation_result['content'])
            except json.JSONDecodeError:
                # 如果JSON解析失败，返回默认内容
                knowledge_data = {
                    "knowledge_points": [
                        {"title": "PXI系统架构", "description": "了解PXI系统的基本架构和组件"},
                        {"title": "数据采集技术", "description": "掌握PXI数据采集的原理和应用"},
                        {"title": "信号处理", "description": "学习PXI信号处理和分析技术"},
                        {"title": "系统集成", "description": "了解PXI系统集成和配置方法"}
                    ]
                }
                experiment_data = {
                    "experiments": [
                        {"title": "基础数据采集", "type": "basic", "description": "PXI数据采集基础实验"},
                        {"title": "信号发生", "type": "generation", "description": "PXI信号发生实验"},
                        {"title": "自动化测试", "type": "automation", "description": "PXI自动化测试实验"},
                        {"title": "系统配置", "type": "configuration", "description": "PXI系统配置实验"}
                    ]
                }
                simulation_data = {
                    "simulation": {
                        "title": "PXI仿真实验",
                        "type": "pxi-basic",
                        "description": "基础PXI系统仿真",
                        "parameters": [
                            {"name": "参数1", "type": "slider", "min": 0, "max": 100, "default": 50, "unit": ""}
                        ],
                        "outputs": [
                            {"name": "输出", "type": "chart", "description": "仿真结果"}
                        ]
                    }
                }
            
            return jsonify({
                'knowledge_points': knowledge_data.get('knowledge_points', []),
                'experiments': experiment_data.get('experiments', []),
                'simulation': simulation_data.get('simulation', {}),
                'success': True
            })
            
        except Exception as e:
            # 如果AI生成失败，返回默认内容
            return jsonify({
                'knowledge_points': [
                    {"title": "PXI系统架构", "description": "了解PXI系统的基本架构和组件"},
                    {"title": "数据采集技术", "description": "掌握PXI数据采集的原理和应用"},
                    {"title": "信号处理", "description": "学习PXI信号处理和分析技术"},
                    {"title": "系统集成", "description": "了解PXI系统集成和配置方法"}
                ],
                'experiments': [
                    {"title": "基础数据采集", "type": "basic", "description": "PXI数据采集基础实验"},
                    {"title": "信号发生", "type": "generation", "description": "PXI信号发生实验"},
                    {"title": "自动化测试", "type": "automation", "description": "PXI自动化测试实验"},
                    {"title": "系统配置", "type": "configuration", "description": "PXI系统配置实验"}
                ],
                'simulation': {
                    "title": "PXI仿真实验",
                    "type": "pxi-basic",
                    "description": "基础PXI系统仿真",
                    "parameters": [
                        {"name": "参数1", "type": "slider", "min": 0, "max": 100, "default": 50, "unit": ""}
                    ],
                    "outputs": [
                        {"name": "输出", "type": "chart", "description": "仿真结果"}
                    ]
                },
                'success': True
            })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'An error occurred while generating related content'
        }), 500

@llm_bp.route('/misd-analysis', methods=['POST'])
def misd_analysis():
    """
    MISD方法分析和硬件配置建议
    
    Request body:
    {
        "hardware_config": {
            "modules": ["PXI-6251", "PXI-5421"],
            "application": "数据采集和信号发生",
            "requirements": "高精度测量"
        }
    }
    """
    try:
        data = request.json
        
        if not data or 'hardware_config' not in data:
            return jsonify({
                'error': 'Missing required parameter: hardware_config'
            }), 400
        
        hardware_config = data['hardware_config']
        modules = hardware_config.get('modules', [])
        application = hardware_config.get('application', '')
        requirements = hardware_config.get('requirements', '')
        
        # 构建MISD分析提示词
        misd_prompt = build_enhanced_prompt(
            question=f"""请基于MISD方法分析以下硬件配置：

硬件模块：{', '.join(modules)}
应用场景：{application}
技术要求：{requirements}

请提供：
1. MISD语法树分析
2. 硬件兼容性评估
3. 最优配置建议
4. AI优化参数
5. 示例代码生成""",
            context_type='misd'
        )
        
        # 生成MISD分析
        response = model_selector.ask_question(
            question=misd_prompt,
            provider=None,
            model=None,
            options={'temperature': 0.3}  # 较低温度确保技术准确性
        )
        
        if response.get('content'):
            return jsonify({
                'success': True,
                'misd_analysis': response['content'],
                'hardware_config': hardware_config,
                'optimization_suggestions': [
                    "使用AI Agent自动优化采样参数",
                    "启用FirmDrive®标准化驱动",
                    "应用MISD语法树简化编程",
                    "集成SeeSharpTools提升开发效率"
                ],
                'provider_used': response.get('provider', 'unknown')
            })
        else:
            return jsonify({
                'success': False,
                'error': 'MISD分析生成失败'
            }), 500
            
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'An error occurred during MISD analysis'
        }), 500

@llm_bp.route('/generate-code', methods=['POST'])
def generate_code():
    """
    AI代码生成功能
    
    Request body:
    {
        "requirements": {
            "language": "csharp",
            "modules": ["USB-1601"],
            "task": "数据采集",
            "parameters": {
                "sample_rate": 10000,
                "channels": 8
            }
        }
    }
    """
    try:
        data = request.json
        
        if not data or 'requirements' not in data:
            return jsonify({
                'error': 'Missing required parameter: requirements'
            }), 400
        
        requirements = data['requirements']
        language = requirements.get('language', 'csharp')
        modules = requirements.get('modules', [])
        task = requirements.get('task', '')
        parameters = requirements.get('parameters', {})
        
        # 构建代码生成提示词
        code_prompt = build_enhanced_prompt(
            question=f"""请生成{language}代码实现以下需求：

硬件模块：{', '.join(modules)}
任务描述：{task}
参数配置：{parameters}

要求：
1. 使用SeeSharpTools库
2. 集成AI优化功能
3. 应用MISD方法
4. 包含错误处理
5. 添加详细注释

请生成完整的可运行代码。""",
            context_type='code_generation'
        )
        
        # 生成代码
        response = model_selector.ask_question(
            question=code_prompt,
            provider=None,
            model=None,
            options={'temperature': 0.2}  # 低温度确保代码准确性
        )
        
        if response.get('content'):
            return jsonify({
                'success': True,
                'generated_code': response['content'],
                'requirements': requirements,
                'ai_optimizations': [
                    "自动参数优化",
                    "智能错误检测",
                    "性能监控",
                    "代码质量分析"
                ],
                'provider_used': response.get('provider', 'unknown')
            })
        else:
            return jsonify({
                'success': False,
                'error': '代码生成失败'
            }), 500
            
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'An error occurred during code generation'
        }), 500

@llm_bp.route('/product-recommendation', methods=['POST'])
def product_recommendation():
    """
    智能产品推荐
    
    Request body:
    {
        "requirements": {
            "application": "自动化测试",
            "budget": "50万以下",
            "channels": "16-32",
            "accuracy": "高精度",
            "environment": "实验室"
        }
    }
    """
    try:
        data = request.json
        
        if not data or 'requirements' not in data:
            return jsonify({
                'error': 'Missing required parameter: requirements'
            }), 400
        
        requirements = data['requirements']
        
        # 构建产品推荐提示词
        recommendation_prompt = build_enhanced_prompt(
            question=f"""请根据以下需求推荐最适合的简仪科技产品组合：

应用场景：{requirements.get('application', '')}
预算范围：{requirements.get('budget', '')}
通道需求：{requirements.get('channels', '')}
精度要求：{requirements.get('accuracy', '')}
使用环境：{requirements.get('environment', '')}

请提供：
1. 推荐的产品组合
2. 技术规格匹配分析
3. 成本效益评估
4. 实施建议
5. 替代方案""",
            context_type='product_recommendation'
        )
        
        # 生成推荐
        response = model_selector.ask_question(
            question=recommendation_prompt,
            provider=None,
            model=None,
            options={'temperature': 0.4}
        )
        
        if response.get('content'):
            return jsonify({
                'success': True,
                'recommendation': response['content'],
                'requirements': requirements,
                'jytek_advantages': [
                    "国产自主可控",
                    "开源生态系统",
                    "AI增强功能",
                    "完整技术支持"
                ],
                'provider_used': response.get('provider', 'unknown')
            })
        else:
            return jsonify({
                'success': False,
                'error': '产品推荐生成失败'
            }), 500
            
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'An error occurred during product recommendation'
        }), 500

@llm_bp.route('/education-support', methods=['POST'])
def education_support():
    """
    教育科研支持
    
    Request body:
    {
        "context": {
            "level": "undergraduate",
            "subject": "电子工程",
            "topic": "数据采集系统设计",
            "duration": "一学期"
        }
    }
    """
    try:
        data = request.json
        
        if not data or 'context' not in data:
            return jsonify({
                'error': 'Missing required parameter: context'
            }), 400
        
        context = data['context']
        
        # 构建教育支持提示词
        education_prompt = build_enhanced_prompt(
            question=f"""请为以下教育场景设计完整的教学方案：

教学层次：{context.get('level', '')}
学科专业：{context.get('subject', '')}
课程主题：{context.get('topic', '')}
教学周期：{context.get('duration', '')}

请提供：
1. 课程大纲设计
2. 实验项目规划
3. 硬件设备配置
4. 软件平台使用
5. 评估方案
6. 进阶学习路径""",
            context_type='education'
        )
        
        # 生成教育方案
        response = model_selector.ask_question(
            question=education_prompt,
            provider=None,
            model=None,
            options={'temperature': 0.5}
        )
        
        if response.get('content'):
            return jsonify({
                'success': True,
                'education_plan': response['content'],
                'context': context,
                'resources': [
                    "SeeSharpLab-Sensor实验套件",
                    "锐视测控平台教育版",
                    "AI Agent教学助手",
                    "在线实验平台"
                ],
                'provider_used': response.get('provider', 'unknown')
            })
        else:
            return jsonify({
                'success': False,
                'error': '教育方案生成失败'
            }), 500
            
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'An error occurred during education support'
        }), 500

@llm_bp.route('/rate', methods=['POST'])
def rate_answer():
    """
    Rate an answer for feedback
    对回答进行评分反馈
    
    Request body:
    {
        "answer_id": "answer_identifier",
        "rating": "helpful" | "unhelpful"
    }
    """
    try:
        data = request.json
        
        if not data or 'rating' not in data:
            return jsonify({
                'error': 'Missing required parameter: rating'
            }), 400
        
        answer_id = data.get('answer_id', 'unknown')
        rating = data['rating']
        
        # 这里可以实现评分存储逻辑
        # 目前只是简单记录
        print(f"Answer {answer_id} rated as: {rating}")
        
        return jsonify({
            'success': True,
            'message': '感谢您的反馈！'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'An error occurred while rating the answer'
        }), 500
