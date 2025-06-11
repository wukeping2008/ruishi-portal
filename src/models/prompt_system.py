"""
综合提示词优化系统
Comprehensive Prompt Optimization System
"""

import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from abc import ABC, abstractmethod
import re
import sqlite3
import os

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PromptSystemManager:
    """提示词系统管理器 - 统一入口"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or os.path.join(os.path.dirname(__file__), '../data/prompt_system.db')
        self.init_database()
        
        # 初始化各个模式管理器
        self.modes = {
            'simple': SimplePromptManager(self.db_path),
            'template': TemplatePromptManager(self.db_path),
            'json': JsonPromptManager(self.db_path),
            'intelligent': IntelligentPromptManager(self.db_path),
            'expert': ExpertPromptManager(self.db_path)
        }
        
        self.config_validator = ConfigValidator()
        self.backup_manager = BackupManager(self.db_path)
        self.version_manager = ConfigVersionManager(self.db_path)
        self.logger = PromptSystemLogger()
        
        # 用户权限配置
        self.permission_levels = {
            'basic': ['simple'],
            'intermediate': ['simple', 'template'],
            'advanced': ['simple', 'template', 'json'],
            'expert': ['simple', 'template', 'json', 'intelligent', 'expert']
        }
    
    def init_database(self):
        """初始化数据库表"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 提示词模板表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS prompt_templates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(100) NOT NULL,
                    category VARCHAR(50) NOT NULL,
                    template_content TEXT NOT NULL,
                    variables JSON,
                    priority INTEGER DEFAULT 1,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # JSON配置表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS json_configs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    config_name VARCHAR(100) NOT NULL,
                    config_data JSON NOT NULL,
                    version VARCHAR(20) DEFAULT '1.0',
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 分层提示词表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS layered_prompts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    layer_type VARCHAR(20) NOT NULL,
                    category VARCHAR(50) NOT NULL,
                    prompt_content TEXT NOT NULL,
                    priority INTEGER DEFAULT 1,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 智能优化记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS optimization_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_id VARCHAR(100),
                    original_prompt TEXT,
                    optimized_prompt TEXT,
                    performance_score FLOAT,
                    optimization_type VARCHAR(50),
                    confidence FLOAT,
                    applied BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 用户偏好表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id VARCHAR(100) NOT NULL,
                    preference_key VARCHAR(50) NOT NULL,
                    preference_value TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 配置版本表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS config_versions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    version_id VARCHAR(50) NOT NULL,
                    config_type VARCHAR(20) NOT NULL,
                    config_data JSON NOT NULL,
                    description TEXT,
                    author VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def get_mode_manager(self, mode: str, user_level: str = 'basic'):
        """获取指定模式的管理器"""
        if mode not in self.modes:
            raise ValueError(f"不支持的模式: {mode}")
        
        if mode not in self.permission_levels.get(user_level, []):
            raise PermissionError(f"用户级别 {user_level} 无权访问 {mode} 模式")
        
        return self.modes[mode]
    
    def build_prompt(self, question: str, mode: str = 'simple', 
                    user_level: str = 'basic', context: Dict = None) -> str:
        """构建提示词"""
        context = context or {}
        
        try:
            manager = self.get_mode_manager(mode, user_level)
            prompt = manager.build_prompt(question, context)
            
            # 记录操作日志
            self.logger.log_operation(
                operation='build_prompt',
                user=context.get('user_id', 'anonymous'),
                details={'mode': mode, 'question_length': len(question)}
            )
            
            return prompt
            
        except Exception as e:
            self.logger.handle_error('prompt_build_error', e, {
                'mode': mode, 'user_level': user_level, 'question': question[:100]
            })
            raise

class BasePromptManager(ABC):
    """提示词管理器基类"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    @abstractmethod
    def build_prompt(self, question: str, context: Dict) -> str:
        """构建提示词"""
        pass
    
    @abstractmethod
    def save_config(self, config: Dict) -> bool:
        """保存配置"""
        pass
    
    @abstractmethod
    def load_config(self) -> Dict:
        """加载配置"""
        pass

class SimplePromptManager(BasePromptManager):
    """简单模式管理器"""
    
    def __init__(self, db_path: str):
        super().__init__(db_path)
        self.default_config = {
            'company_name': '简仪科技',
            'main_product': '锐视测控平台',
            'response_style': 'professional',
            'focus_areas': ['PXI系统', '数据采集']
        }
    
    def build_prompt(self, question: str, context: Dict) -> str:
        """构建简单模式提示词"""
        config = self.load_config()
        
        # 基础提示词模板
        base_template = f"""你是{config['company_name']}的专业AI助手。

我们的主要产品是{config['main_product']}，专注于{', '.join(config['focus_areas'])}等领域。

用户问题：{question}

请提供专业、准确的回答，重点介绍我们的技术优势和产品特色。"""
        
        # 根据知识库内容调整
        if context.get('knowledge_content'):
            knowledge_prompt = f"""
## 重要：请优先基于以下知识库内容回答用户问题

{context['knowledge_content']}

{base_template}

请基于知识库内容提供详细、准确的回答。"""
            return knowledge_prompt
        
        return base_template
    
    def save_config(self, config: Dict) -> bool:
        """保存简单模式配置"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO prompt_templates 
                    (name, category, template_content, variables, is_active)
                    VALUES (?, ?, ?, ?, ?)
                ''', ('simple_config', 'simple', json.dumps(config), '{}', 1))
                conn.commit()
            return True
        except Exception as e:
            logger.error(f"保存简单模式配置失败: {e}")
            return False
    
    def load_config(self) -> Dict:
        """加载简单模式配置"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT template_content FROM prompt_templates 
                    WHERE name = ? AND category = ? AND is_active = 1
                ''', ('simple_config', 'simple'))
                
                result = cursor.fetchone()
                if result:
                    return json.loads(result[0])
                else:
                    return self.default_config
        except Exception as e:
            logger.error(f"加载简单模式配置失败: {e}")
            return self.default_config

class TemplatePromptManager(BasePromptManager):
    """模板模式管理器"""
    
    def __init__(self, db_path: str):
        super().__init__(db_path)
        self.template_categories = {
            'company': '公司介绍',
            'product': '产品推荐', 
            'support': '技术支持',
            'education': '教育培训'
        }
    
    def build_prompt(self, question: str, context: Dict) -> str:
        """构建模板模式提示词"""
        # 分析问题类型
        question_type = self._analyze_question_type(question)
        
        # 获取对应模板
        template = self._get_template(question_type)
        
        # 替换变量
        variables = {
            'question': question,
            'knowledge_content': context.get('knowledge_content', ''),
            'user_context': context.get('user_context', ''),
            'company_name': '简仪科技',
            'product_name': '锐视测控平台'
        }
        
        prompt = self._replace_variables(template, variables)
        return prompt
    
    def _analyze_question_type(self, question: str) -> str:
        """分析问题类型"""
        patterns = {
            'product': ['产品', '价格', '规格', '型号', '购买', '推荐'],
            'support': ['故障', '错误', '问题', '调试', '修复', '帮助'],
            'education': ['教学', '学习', '培训', '课程', '实验', '教程'],
            'company': ['公司', '简仪科技', 'JYTEK', '介绍', '关于']
        }
        
        for category, keywords in patterns.items():
            if any(keyword in question for keyword in keywords):
                return category
        
        return 'company'  # 默认类型
    
    def _get_template(self, question_type: str) -> str:
        """获取模板内容"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT template_content FROM prompt_templates 
                    WHERE category = ? AND is_active = 1 
                    ORDER BY priority DESC LIMIT 1
                ''', (question_type,))
                
                result = cursor.fetchone()
                if result:
                    return result[0]
                else:
                    return self._get_default_template(question_type)
        except Exception as e:
            logger.error(f"获取模板失败: {e}")
            return self._get_default_template(question_type)
    
    def _get_default_template(self, question_type: str) -> str:
        """获取默认模板"""
        templates = {
            'company': '''你是{company_name}的专业AI助手。

{knowledge_content}

用户问题：{question}

请介绍我们公司的基本情况、技术优势和产品特色。''',
            
            'product': '''你是{company_name}产品专家。

{knowledge_content}

用户问题：{question}

请根据用户需求推荐最适合的产品，包括技术规格、应用场景和优势特点。''',
            
            'support': '''你是{company_name}技术支持工程师。

{knowledge_content}

用户问题：{question}

请提供详细的技术支持和解决方案，包括问题分析、解决步骤和预防措施。''',
            
            'education': '''你是{company_name}教育培训专家。

{knowledge_content}

用户问题：{question}

请提供完整的学习指导，包括理论基础、实践操作和项目案例。'''
        }
        
        return templates.get(question_type, templates['company'])
    
    def _replace_variables(self, template: str, variables: Dict) -> str:
        """替换模板变量"""
        for key, value in variables.items():
            template = template.replace(f'{{{key}}}', str(value))
        return template
    
    def save_template(self, category: str, template_content: str, 
                     variables: List[str] = None) -> bool:
        """保存模板"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO prompt_templates 
                    (name, category, template_content, variables, is_active)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    f'template_{category}_{int(time.time())}',
                    category,
                    template_content,
                    json.dumps(variables or []),
                    1
                ))
                conn.commit()
            return True
        except Exception as e:
            logger.error(f"保存模板失败: {e}")
            return False
    
    def save_config(self, config: Dict) -> bool:
        """保存模板配置"""
        return True  # 模板模式通过save_template保存
    
    def load_config(self) -> Dict:
        """加载模板配置"""
        return {'templates': self.template_categories}

class JsonPromptManager(BasePromptManager):
    """JSON配置模式管理器"""
    
    def __init__(self, db_path: str):
        super().__init__(db_path)
        self.config_schema = {
            'prompt_system': {
                'version': '2.0',
                'default_language': 'zh-CN',
                'fallback_strategy': 'layered'
            },
            'templates': {},
            'optimization': {
                'auto_learning': True,
                'feedback_threshold': 4.0,
                'update_frequency': 'daily'
            }
        }
    
    def build_prompt(self, question: str, context: Dict) -> str:
        """基于JSON配置构建提示词"""
        config = self.load_config()
        
        # 分析问题匹配模板
        matched_template = self._match_template(question, config.get('templates', {}))
        
        if matched_template:
            return self._build_from_template(question, matched_template, context)
        else:
            # 使用默认模板
            return self._build_default_prompt(question, context)
    
    def _match_template(self, question: str, templates: Dict) -> Optional[Dict]:
        """匹配最适合的模板"""
        best_match = None
        best_score = 0
        
        for template_name, template_config in templates.items():
            conditions = template_config.get('conditions', [])
            score = sum(1 for condition in conditions if condition in question)
            
            if score > best_score:
                best_score = score
                best_match = template_config
        
        return best_match
    
    def _build_from_template(self, question: str, template: Dict, context: Dict) -> str:
        """基于模板构建提示词"""
        content = template.get('content', '')
        variables = template.get('variables', [])
        
        # 替换变量
        replacements = {
            'question': question,
            'knowledge_content': context.get('knowledge_content', ''),
            'company_info': '简仪科技（JYTEK）锐视测控平台',
            'product_list': 'PXI系统、数据采集设备、信号处理软件'
        }
        
        for var in variables:
            if var in replacements:
                content = content.replace(f'{{{var}}}', replacements[var])
        
        return content
    
    def _build_default_prompt(self, question: str, context: Dict) -> str:
        """构建默认提示词"""
        return f"""你是简仪科技（JYTEK）锐视测控平台的专业AI助手。

{context.get('knowledge_content', '')}

用户问题：{question}

请提供专业、准确的回答。"""
    
    def save_config(self, config: Dict) -> bool:
        """保存JSON配置"""
        try:
            # 验证配置格式
            if not self._validate_config(config):
                return False
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO json_configs 
                    (config_name, config_data, version, is_active)
                    VALUES (?, ?, ?, ?)
                ''', (
                    f'json_config_{int(time.time())}',
                    json.dumps(config),
                    config.get('prompt_system', {}).get('version', '1.0'),
                    1
                ))
                conn.commit()
            return True
        except Exception as e:
            logger.error(f"保存JSON配置失败: {e}")
            return False
    
    def load_config(self) -> Dict:
        """加载JSON配置"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT config_data FROM json_configs 
                    WHERE is_active = 1 
                    ORDER BY created_at DESC LIMIT 1
                ''')
                
                result = cursor.fetchone()
                if result:
                    return json.loads(result[0])
                else:
                    return self.config_schema
        except Exception as e:
            logger.error(f"加载JSON配置失败: {e}")
            return self.config_schema
    
    def _validate_config(self, config: Dict) -> bool:
        """验证配置格式"""
        required_keys = ['prompt_system', 'templates']
        return all(key in config for key in required_keys)

class IntelligentPromptManager(BasePromptManager):
    """智能优化模式管理器"""
    
    def __init__(self, db_path: str):
        super().__init__(db_path)
        self.intent_analyzer = QuestionIntentAnalyzer()
        self.prompt_composer = DynamicPromptComposer()
        self.effectiveness_tracker = PromptEffectivenessTracker(db_path)
    
    def build_prompt(self, question: str, context: Dict) -> str:
        """智能构建提示词"""
        # 1. 分析问题意图
        intent_scores = self.intent_analyzer.analyze_intent(question)
        
        # 2. 动态组合提示词
        prompt = self.prompt_composer.compose_prompt(
            question=question,
            intent_scores=intent_scores,
            knowledge_content=context.get('knowledge_content', ''),
            user_preferences=context.get('user_preferences', {})
        )
        
        # 3. 应用智能优化
        optimized_prompt = self._apply_optimizations(prompt, intent_scores)
        
        return optimized_prompt
    
    def _apply_optimizations(self, prompt: str, intent_scores: Dict) -> str:
        """应用智能优化"""
        # 获取历史优化建议
        optimizations = self._get_applicable_optimizations(intent_scores)
        
        for optimization in optimizations:
            if optimization['confidence'] > 0.8 and optimization['applied']:
                prompt = self._apply_optimization_rule(prompt, optimization)
        
        return prompt
    
    def _get_applicable_optimizations(self, intent_scores: Dict) -> List[Dict]:
        """获取适用的优化建议"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM optimization_logs 
                    WHERE confidence > 0.7 AND applied = 1
                    ORDER BY performance_score DESC LIMIT 5
                ''')
                
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in results]
        except Exception as e:
            logger.error(f"获取优化建议失败: {e}")
            return []
    
    def _apply_optimization_rule(self, prompt: str, optimization: Dict) -> str:
        """应用优化规则"""
        # 这里可以实现具体的优化逻辑
        # 例如：添加特定的提示词片段、调整格式等
        return prompt
    
    def save_config(self, config: Dict) -> bool:
        """保存智能优化配置"""
        return True
    
    def load_config(self) -> Dict:
        """加载智能优化配置"""
        return {'auto_optimization': True}

class ExpertPromptManager(BasePromptManager):
    """专家模式管理器（分层架构）"""
    
    def __init__(self, db_path: str):
        super().__init__(db_path)
        self.layers = {
            'foundation': FoundationLayer(db_path),
            'business': BusinessLayer(db_path),
            'personalization': PersonalizationLayer(db_path)
        }
        self.inheritance_rules = InheritanceRuleEngine()
    
    def build_prompt(self, question: str, context: Dict) -> str:
        """构建分层提示词"""
        # 1. 基础层
        foundation_prompt = self.layers['foundation'].get_prompt(context)
        
        # 2. 业务层
        business_prompt = self.layers['business'].get_prompt(question, context)
        
        # 3. 个性化层
        personal_prompt = self.layers['personalization'].get_prompt(
            context.get('user_id'), context.get('preferences', {})
        )
        
        # 4. 合并层级
        final_prompt = self.inheritance_rules.merge_layers(
            foundation_prompt, business_prompt, personal_prompt, question
        )
        
        return final_prompt
    
    def save_config(self, config: Dict) -> bool:
        """保存专家模式配置"""
        return True
    
    def load_config(self) -> Dict:
        """加载专家模式配置"""
        return {'layers': ['foundation', 'business', 'personalization']}

# 辅助类定义
class QuestionIntentAnalyzer:
    """问题意图分析器"""
    
    def __init__(self):
        self.intent_patterns = {
            'product_inquiry': ['产品', '价格', '规格', '型号', '购买'],
            'technical_support': ['故障', '错误', '问题', '调试', '修复'],
            'code_generation': ['代码', '编程', '开发', 'C#', 'Python'],
            'education': ['教学', '学习', '培训', '课程', '实验'],
            'company_info': ['公司', '简仪科技', 'JYTEK', '介绍']
        }
    
    def analyze_intent(self, question: str) -> Dict[str, float]:
        """分析问题意图"""
        intent_scores = {}
        
        for intent, keywords in self.intent_patterns.items():
            score = sum(1 for keyword in keywords if keyword in question)
            intent_scores[intent] = score / len(keywords)
        
        return intent_scores

class DynamicPromptComposer:
    """动态提示词组合器"""
    
    def __init__(self):
        self.prompt_fragments = {
            'base': {
                'company_intro': "你是简仪科技（JYTEK）锐视测控平台的专业AI助手。",
                'response_format': "请提供专业、准确的回答。",
            },
            'context_specific': {
                'product_inquiry': "作为产品专家，请重点介绍相关产品特性和优势。",
                'technical_support': "作为技术支持专家，请提供详细的解决方案。",
                'code_generation': "作为编程专家，请生成高质量的代码示例。",
            },
            'enhancement': {
                'knowledge_base': "## 重要：请优先基于以下知识库内容回答用户问题\n{knowledge_content}",
                'examples': "请提供具体的应用示例和案例。",
                'references': "请在回答中包含相关的产品型号和技术参数。",
            }
        }
    
    def compose_prompt(self, question: str, intent_scores: Dict[str, float], 
                      knowledge_content: str = '', user_preferences: Dict = None) -> str:
        """组合提示词"""
        prompt_parts = [self.prompt_fragments['base']['company_intro']]
        
        # 知识库内容
        if knowledge_content:
            knowledge_prompt = self.prompt_fragments['enhancement']['knowledge_base'].format(
                knowledge_content=knowledge_content
            )
            prompt_parts.append(knowledge_prompt)
        
        # 根据意图添加特定上下文
        primary_intent = max(intent_scores.items(), key=lambda x: x[1])[0]
        if primary_intent in self.prompt_fragments['context_specific']:
            prompt_parts.append(self.prompt_fragments['context_specific'][primary_intent])
        
        # 添加问题和格式要求
        prompt_parts.extend([
            f"\n## 用户问题：{question}",
            self.prompt_fragments['base']['response_format']
        ])
        
        return "\n\n".join(prompt_parts)

class PromptEffectivenessTracker:
    """提示词效果跟踪器"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def track_response(self, question_id: str, prompt_config: Dict, 
                      ai_response: str, user_feedback: Dict = None):
        """跟踪回答效果"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO optimization_logs 
                    (question_id, original_prompt, performance_score, optimization_type)
                    VALUES (?, ?, ?, ?)
                ''', (
                    question_id,
                    json.dumps(prompt_config),
                    user_feedback.get('rating', 0) if user_feedback else 0,
                    'manual'
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"跟踪效果失败: {e}")

class FoundationLayer:
    """基础层"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def get_prompt(self, context: Dict) -> str:
        """获取基础层提示词"""
        return """你是简仪科技（JYTEK）锐视测控平台的专业AI助手。
简仪科技成立于2016年，专注于测试测量技术创新。
核心产品：锐视测控平台（SeeSharp Platform）
技术特色：开源测控解决方案、国产自主可控、AI集成
官网：www.jytek.com"""

class BusinessLayer:
    """业务层"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def get_prompt(self, question: str, context: Dict) -> str:
        """获取业务层提示词"""
        return "请基于简仪科技的专业背景，提供准确的技术解答。"

class PersonalizationLayer:
    """个性化层"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def get_prompt(self, user_id: str, preferences: Dict) -> str:
        """获取个性化层提示词"""
        if preferences.get('detailed_explanations', False):
            return "请提供详细的技术解释和原理说明。"
        return ""

class InheritanceRuleEngine:
    """继承规则引擎"""
    
    def merge_layers(self, foundation: str, business: str, 
                    personal: str, question: str) -> str:
        """合并各层提示词"""
        merged_prompt = f"""
{foundation}

{business}

{personal}

## 用户问题：{question}

## 回答要求：
请基于以上分层指导原则，提供专业、准确、个性化的回答。
优先级：个性化设置 > 业务专业要求 > 基础公司信息
        """
        
        return merged_prompt.strip()

class ConfigValidator:
    """配置验证器"""
    
    def validate(self, config: Dict, config_type: str) -> Tuple[bool, List[str]]:
        """验证配置"""
        errors = []
        
        if config_type == 'json':
            if 'prompt_system' not in config:
                errors.append("缺少prompt_system配置")
            if 'templates' not in config:
                errors.append("缺少templates配置")
        
        return len(errors) == 0, errors

class BackupManager:
    """备份管理器"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.backup_dir = os.path.join(os.path.dirname(db_path), 'backups')
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def create_backup(self, trigger: str = 'manual') -> str:
        """创建备份"""
        timestamp = int(time.time())
        backup_file = f"backup_{trigger}_{timestamp}.json"
        backup_path = os.path.join(self.backup_dir, backup_file)
        
        try:
            backup_data = {
                'timestamp': datetime.now().isoformat(),
                'trigger': trigger,
                'database_backup': self._backup_database()
            }
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, ensure_ascii=False, indent=2)
            
            return backup_file
        except Exception as e:
            logger.error(f"创建备份失败: {e}")
            return ""
    
    def _backup_database(self) -> Dict:
        """备份数据库内容"""
        backup_data = {}
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 备份各个表
                tables = ['prompt_templates', 'json_configs', 'layered_prompts', 
                         'optimization_logs', 'user_preferences', 'config_versions']
                
                for table in tables:
                    cursor.execute(f"SELECT * FROM {table}")
                    rows = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                    backup_data[table] = [dict(zip(columns, row)) for row in rows]
            
            return backup_data
        except Exception as e:
            logger.error(f"备份数据库失败: {e}")
            return {}

class ConfigVersionManager:
    """配置版本管理器"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def save_version(self, config: Dict, config_type: str, 
                    description: str = "", author: str = "system") -> str:
        """保存配置版本"""
        version_id = f"v{int(time.time())}"
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO config_versions 
                    (version_id, config_type, config_data, description, author)
                    VALUES (?, ?, ?, ?, ?)
                ''', (version_id, config_type, json.dumps(config), description, author))
                conn.commit()
            
            return version_id
        except Exception as e:
            logger.error(f"保存版本失败: {e}")
            return ""
    
    def get_versions(self, config_type: str = None) -> List[Dict]:
        """获取版本列表"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if config_type:
                    cursor.execute('''
                        SELECT * FROM config_versions 
                        WHERE config_type = ? 
                        ORDER BY created_at DESC
                    ''', (config_type,))
                else:
                    cursor.execute('''
                        SELECT * FROM config_versions 
                        ORDER BY created_at DESC
                    ''')
                
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in results]
        except Exception as e:
            logger.error(f"获取版本列表失败: {e}")
            return []

class PromptSystemLogger:
    """提示词系统日志器"""
    
    def __init__(self):
        self.logger = logging.getLogger('prompt_system')
        self.error_handlers = {
            'config_error': self._handle_config_error,
            'template_error': self._handle_template_error,
            'prompt_build_error': self._handle_prompt_build_error
        }
    
    def log_operation(self, operation: str, user: str, details: Dict):
        """记录操作日志"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'user': user,
            'details': details,
            'success': True
        }
        self.logger.info(json.dumps(log_entry, ensure_ascii=False))
    
    def handle_error(self, error_type: str, error: Exception, context: Dict):
        """处理错误"""
        if error_type in self.error_handlers:
            return self.error_handlers[error_type](error, context)
        else:
            return self._default_error_handler(error, context)
    
    def _handle_config_error(self, error: Exception, context: Dict):
        """处理配置错误"""
        self.logger.error(f"配置错误: {error}, 上下文: {context}")
    
    def _handle_template_error(self, error: Exception, context: Dict):
        """处理模板错误"""
        self.logger.error(f"模板错误: {error}, 上下文: {context}")
    
    def _handle_prompt_build_error(self, error: Exception, context: Dict):
        """处理提示词构建错误"""
        self.logger.error(f"提示词构建错误: {error}, 上下文: {context}")
    
    def _default_error_handler(self, error: Exception, context: Dict):
        """默认错误处理"""
        self.logger.error(f"未知错误: {error}, 上下文: {context}")

# 全局实例
prompt_system_manager = PromptSystemManager()
