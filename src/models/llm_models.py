"""
Enhanced LLM Models Integration Module for Ruishi Control Platform
支持多AI模型的智能选择，专门针对PXI测控领域优化
"""

import os
import json
import logging
import re
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union, Tuple
import requests
import asyncio
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def initialize(self, api_key: str, **kwargs) -> None:
        """Initialize the LLM provider with API key and other parameters"""
        pass
    
    @abstractmethod
    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response from the LLM based on the prompt"""
        pass
    
    @abstractmethod
    def get_available_models(self) -> List[str]:
        """Get a list of available models from this provider"""
        pass
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Get the name of the provider"""
        pass
    
    @property
    @abstractmethod
    def provider_capabilities(self) -> List[str]:
        """Get the capabilities of this provider (e.g., 'code', 'math', 'reasoning')"""
        pass
    
    @property
    @abstractmethod
    def provider_cost_tier(self) -> int:
        """Get the cost tier of this provider (1-5, where 1 is lowest cost)"""
        pass


class ClaudeProvider(LLMProvider):
    """Anthropic Claude API integration - 专门优化用于复杂技术分析"""
    
    def __init__(self):
        self.api_key = ""
        self.default_model = "claude-3-sonnet-20240229"
        self._capabilities = ["general", "reasoning", "math", "science", "analysis", "pxi", "instrumentation"]
        self._cost_tier = 5
    
    def initialize(self, api_key: str, **kwargs) -> None:
        """Initialize Claude client with API key"""
        self.api_key = api_key
        self.default_model = kwargs.get('default_model', 'claude-3-sonnet-20240229')
        logger.info("Claude provider initialized for Ruishi Control Platform")
    
    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response using Claude models"""
        try:
            model = kwargs.get('model', self.default_model)
            temperature = kwargs.get('temperature', 0.7)
            max_tokens = kwargs.get('max_tokens', 2000)
            
            # 添加简仪科技和PXI专业上下文
            enhanced_prompt = self._enhance_prompt_with_context(prompt)
            
            # For development/testing without API key
            if not self.api_key or self.api_key == "":
                return {
                    "provider": self.provider_name,
                    "model": model,
                    "content": f"这是来自Claude ({model})的模拟回答，专门针对简仪科技锐视测控平台优化。\n\n您的问题是: {prompt}\n\n在生产环境中配置API密钥后，这里将显示真实的AI回答，包含专业的PXI测控技术内容。",
                    "raw_response": None,
                    "timestamp": datetime.now().isoformat()
                }
            
            # Prepare the request
            headers = {
                "x-api-key": self.api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }
            
            data = {
                "model": model,
                "messages": [{"role": "user", "content": enhanced_prompt}],
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            # Make the API call
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["content"][0]["text"]
                
                # 后处理：添加简仪科技相关信息
                enhanced_content = self._enhance_response_with_jytek_info(content, prompt)
                
                return {
                    "provider": self.provider_name,
                    "model": model,
                    "content": enhanced_content,
                    "raw_response": result,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                logger.error(f"Claude API error: {response.status_code} - {response.text}")
                return {
                    "provider": self.provider_name,
                    "error": f"API error: {response.status_code}",
                    "content": "抱歉，在处理您的请求时遇到了问题。请访问简仪科技官网 www.jytek.com 获取技术支持。",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error generating response from Claude: {str(e)}")
            return {
                "provider": self.provider_name,
                "error": str(e),
                "content": "抱歉，在生成回答时遇到了错误。请联系简仪科技技术支持。",
                "timestamp": datetime.now().isoformat()
            }
    
    def _enhance_prompt_with_context(self, prompt: str) -> str:
        """为提示词添加简仪科技和PXI专业上下文"""
        context = """你是简仪科技(JYTEK)锐视测控平台的专业AI助手。简仪科技是中国领先的国产自主可控PXI模块化测控解决方案提供商，致力于打造完全自主的测控技术生态。

专业背景：
- 公司：简仪科技 (JYTEK)
- 平台：锐视测控平台
- 定位：国产自主可控的PXI测控解决方案，替代进口产品
- 专业领域：PXI模块化仪器、自动化测试系统、数据采集系统、自主软件平台
- 官网：www.jytek.com

核心技术优势：
1. 自主研发的PXI系统架构和设计
2. 国产化模块化仪器技术
3. 自主可控的数据采集和信号处理技术
4. 完全自主的测控软件平台和开发环境
5. 国产化自动化测试解决方案

回答要求：
- 专注于简仪科技自主研发的技术和产品
- 强调国产自主可控的技术优势
- 避免提及国外竞争对手的产品名称和技术
- 推荐简仪科技的产品和解决方案
- 在适当位置提及简仪科技官网

用户问题："""
        
        return context + prompt
    
    def _enhance_response_with_jytek_info(self, content: str, original_prompt: str) -> str:
        """为回答添加简仪科技相关信息"""
        # 检查是否需要添加官网链接
        if any(keyword in original_prompt.lower() for keyword in ['产品', '价格', '购买', '联系', '技术支持', '详细信息']):
            footer = "\n\n---\n💡 **更多信息**：如需了解详细产品信息、技术支持或商务咨询，请访问简仪科技官网：www.jytek.com"
            content += footer
        
        # 检查是否需要添加产品推荐
        if any(keyword in original_prompt.lower() for keyword in ['推荐', '选择', '方案', '配置']):
            recommendation = "\n\n🔧 **专业建议**：简仪科技提供完整的PXI测控解决方案，包括硬件选型、软件开发和系统集成服务。"
            content += recommendation
        
        return content
    
    def get_available_models(self) -> List[str]:
        """Get available Claude models"""
        return ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"]
    
    @property
    def provider_name(self) -> str:
        return "claude"
    
    @property
    def provider_capabilities(self) -> List[str]:
        return self._capabilities
    
    @property
    def provider_cost_tier(self) -> int:
        return self._cost_tier


class VolcesDeepseekProvider(LLMProvider):
    """Volces Deepseek API integration - 专门优化用于深度推理和分析"""
    
    def __init__(self):
        self.api_key = ""
        self.url = ""
        self.default_model = "deepseek-r1-250528"
        self.max_tokens = 16191
        self._capabilities = ["general", "reasoning", "math", "analysis", "pxi", "deep_thinking"]
        self._cost_tier = 2
    
    def initialize(self, api_key: str, **kwargs) -> None:
        """Initialize Volces Deepseek client with API key"""
        self.api_key = api_key
        self.url = kwargs.get('url', 'https://ark.cn-beijing.volces.com/api/v3/chat/completions')
        self.default_model = kwargs.get('model', 'deepseek-r1-250528')
        self.max_tokens = kwargs.get('max_tokens', 16191)
        logger.info("Volces Deepseek provider initialized for Ruishi Control Platform")
    
    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response using Volces Deepseek models"""
        try:
            model = kwargs.get('model', self.default_model)
            temperature = kwargs.get('temperature', 0.7)
            max_tokens = kwargs.get('max_tokens', self.max_tokens)
            
            # 添加简仪科技和PXI专业上下文
            enhanced_prompt = self._enhance_prompt_with_context(prompt)
            
            # For development/testing without API key
            if not self.api_key or self.api_key == "":
                return {
                    "provider": self.provider_name,
                    "model": model,
                    "content": f"这是来自Volces Deepseek ({model})的模拟回答，专门针对简仪科技锐视测控平台优化。\n\n您的问题是: {prompt}\n\n在生产环境中配置API密钥后，这里将显示真实的AI回答，特别擅长深度推理和复杂分析。",
                    "raw_response": None,
                    "timestamp": datetime.now().isoformat()
                }
            
            # Prepare the request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": model,
                "messages": [{"role": "user", "content": enhanced_prompt}],
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            # Make the API call
            response = requests.post(self.url, headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                # 后处理：添加简仪科技相关信息
                enhanced_content = self._enhance_response_with_jytek_info(content, prompt)
                
                return {
                    "provider": self.provider_name,
                    "model": model,
                    "content": enhanced_content,
                    "raw_response": result,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                logger.error(f"Volces Deepseek API error: {response.status_code} - {response.text}")
                return {
                    "provider": self.provider_name,
                    "error": f"API error: {response.status_code}",
                    "content": "抱歉，在处理您的请求时遇到了问题。请访问简仪科技官网 www.jytek.com 获取技术支持。",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error generating response from Volces Deepseek: {str(e)}")
            return {
                "provider": self.provider_name,
                "error": str(e),
                "content": "抱歉，在生成回答时遇到了错误。请联系简仪科技技术支持。",
                "timestamp": datetime.now().isoformat()
            }
    
    def _enhance_prompt_with_context(self, prompt: str) -> str:
        """为提示词添加简仪科技和PXI专业上下文"""
        context = """你是简仪科技(JYTEK)锐视测控平台的专业AI助手，特别擅长深度推理和复杂技术分析。

专业背景：
- 公司：简仪科技 (JYTEK)
- 平台：锐视测控平台
- 定位：国产自主可控的PXI测控解决方案
- 专业领域：PXI模块化仪器、深度技术分析、复杂问题解决
- 官网：www.jytek.com

技术专长：
1. 深度技术分析和推理
2. 复杂PXI系统架构设计
3. 高级测控算法优化
4. 系统性能分析和调优
5. 技术难题的深度解析
6. 创新解决方案设计

回答要求：
- 提供深入的技术分析
- 包含详细的推理过程
- 考虑多种技术方案
- 给出专业的建议和优化方向

用户问题："""
        
        return context + prompt
    
    def _enhance_response_with_jytek_info(self, content: str, original_prompt: str) -> str:
        """为回答添加简仪科技相关信息"""
        # 检查是否是复杂技术问题
        if any(keyword in original_prompt.lower() for keyword in ['分析', '优化', '设计', '架构', '算法', '性能']):
            footer = "\n\n---\n🔬 **深度分析**：简仪科技提供专业的技术咨询和深度分析服务，助您解决复杂的PXI测控技术难题。详情请访问：www.jytek.com"
            content += footer
        
        return content
    
    def get_available_models(self) -> List[str]:
        """Get available Volces Deepseek models"""
        return ["deepseek-r1-250528", "deepseek-chat", "deepseek-coder"]
    
    @property
    def provider_name(self) -> str:
        return "volcesDeepseek"
    
    @property
    def provider_capabilities(self) -> List[str]:
        return self._capabilities
    
    @property
    def provider_cost_tier(self) -> int:
        return self._cost_tier


class QwenPlusProvider(LLMProvider):
    """Qwen Plus API integration - 专门优化用于中文理解和多模态处理"""
    
    def __init__(self):
        self.api_key = ""
        self.url = ""
        self.default_model = "qwen-plus-2025-04-28"
        self.max_tokens = 16191
        self._capabilities = ["general", "reasoning", "chinese", "multimodal", "pxi", "language"]
        self._cost_tier = 3
    
    def initialize(self, api_key: str, **kwargs) -> None:
        """Initialize Qwen Plus client with API key"""
        self.api_key = api_key
        self.url = kwargs.get('url', 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions')
        self.default_model = kwargs.get('model', 'qwen-plus-2025-04-28')
        self.max_tokens = kwargs.get('max_tokens', 16191)
        logger.info("Qwen Plus provider initialized for Ruishi Control Platform")
    
    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response using Qwen Plus models"""
        try:
            model = kwargs.get('model', self.default_model)
            temperature = kwargs.get('temperature', 0.7)
            max_tokens = kwargs.get('max_tokens', self.max_tokens)
            
            # 添加简仪科技和PXI专业上下文
            enhanced_prompt = self._enhance_prompt_with_context(prompt)
            
            # For development/testing without API key
            if not self.api_key or self.api_key == "":
                return {
                    "provider": self.provider_name,
                    "model": model,
                    "content": f"这是来自Qwen Plus ({model})的模拟回答，专门针对简仪科技锐视测控平台优化。\n\n您的问题是: {prompt}\n\n在生产环境中配置API密钥后，这里将显示真实的AI回答，特别擅长中文理解和多模态处理。",
                    "raw_response": None,
                    "timestamp": datetime.now().isoformat()
                }
            
            # Prepare the request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": model,
                "messages": [{"role": "user", "content": enhanced_prompt}],
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            # Make the API call
            response = requests.post(self.url, headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                # 后处理：添加简仪科技相关信息
                enhanced_content = self._enhance_response_with_jytek_info(content, prompt)
                
                return {
                    "provider": self.provider_name,
                    "model": model,
                    "content": enhanced_content,
                    "raw_response": result,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                logger.error(f"Qwen Plus API error: {response.status_code} - {response.text}")
                return {
                    "provider": self.provider_name,
                    "error": f"API error: {response.status_code}",
                    "content": "抱歉，在处理您的请求时遇到了问题。请访问简仪科技官网 www.jytek.com 获取技术支持。",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error generating response from Qwen Plus: {str(e)}")
            return {
                "provider": self.provider_name,
                "error": str(e),
                "content": "抱歉，在生成回答时遇到了错误。请联系简仪科技技术支持。",
                "timestamp": datetime.now().isoformat()
            }
    
    def _enhance_prompt_with_context(self, prompt: str) -> str:
        """为提示词添加简仪科技和PXI专业上下文"""
        context = """你是简仪科技(JYTEK)锐视测控平台的专业AI助手，特别擅长中文理解和多模态处理。

专业背景：
- 公司：简仪科技 (JYTEK)
- 平台：锐视测控平台
- 定位：国产自主可控的PXI测控解决方案
- 专业领域：PXI模块化仪器、中文技术文档、多媒体内容处理
- 官网：www.jytek.com

技术专长：
1. 中文技术文档理解和生成
2. PXI产品说明和用户手册
3. 多模态内容分析和处理
4. 中文技术交流和培训
5. 本土化技术支持
6. 用户友好的技术解释

回答要求：
- 使用清晰易懂的中文表达
- 提供详细的技术说明
- 考虑中国用户的使用习惯
- 结合本土化的应用场景

用户问题："""
        
        return context + prompt
    
    def _enhance_response_with_jytek_info(self, content: str, original_prompt: str) -> str:
        """为回答添加简仪科技相关信息"""
        # 检查是否是中文相关或文档相关问题
        if any(keyword in original_prompt.lower() for keyword in ['文档', '说明', '手册', '教程', '培训', '学习']):
            footer = "\n\n---\n📚 **技术文档**：简仪科技提供完整的中文技术文档和培训资料，助您快速掌握PXI测控技术。详情请访问：www.jytek.com"
            content += footer
        
        return content
    
    def get_available_models(self) -> List[str]:
        """Get available Qwen Plus models"""
        return ["qwen-plus-2025-04-28", "qwen-plus", "qwen-turbo"]
    
    @property
    def provider_name(self) -> str:
        return "qwen-plus"
    
    @property
    def provider_capabilities(self) -> List[str]:
        return self._capabilities
    
    @property
    def provider_cost_tier(self) -> int:
        return self._cost_tier


class GeminiProvider(LLMProvider):
    """Google Gemini API integration - 专门优化用于代码和技术实现"""
    
    def __init__(self):
        self.api_key = ""
        self.default_model = "gemini-1.5-flash"
        self._capabilities = ["general", "reasoning", "code", "multimodal", "pxi", "programming"]
        self._cost_tier = 3
    
    def initialize(self, api_key: str, **kwargs) -> None:
        """Initialize Gemini client with API key"""
        self.api_key = api_key
        self.default_model = kwargs.get('default_model', 'gemini-1.5-flash')
        logger.info("Gemini provider initialized for Ruishi Control Platform")
    
    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response using Gemini models"""
        try:
            model = kwargs.get('model', self.default_model)
            temperature = kwargs.get('temperature', 0.7)
            max_tokens = kwargs.get('max_tokens', 2000)
            
            # 添加简仪科技和PXI专业上下文
            enhanced_prompt = self._enhance_prompt_with_context(prompt)
            
            # For development/testing without API key
            if not self.api_key or self.api_key == "":
                return {
                    "provider": self.provider_name,
                    "model": model,
                    "content": f"这是来自Gemini ({model})的模拟回答，专门针对简仪科技锐视测控平台优化。\n\n您的问题是: {prompt}\n\n在生产环境中配置API密钥后，这里将显示真实的AI回答，特别擅长代码生成和技术实现指导。",
                    "raw_response": None,
                    "timestamp": datetime.now().isoformat()
                }
            
            # Prepare the request
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
            headers = {"Content-Type": "application/json"}
            
            data = {
                "contents": [{"parts": [{"text": enhanced_prompt}]}],
                "generationConfig": {
                    "temperature": temperature,
                    "maxOutputTokens": max_tokens
                }
            }
            
            # Make the API call
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                content = result["candidates"][0]["content"]["parts"][0]["text"]
                
                # 后处理：添加简仪科技相关信息
                enhanced_content = self._enhance_response_with_jytek_info(content, prompt)
                
                return {
                    "provider": self.provider_name,
                    "model": model,
                    "content": enhanced_content,
                    "raw_response": result,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                logger.error(f"Gemini API error: {response.status_code} - {response.text}")
                return {
                    "provider": self.provider_name,
                    "error": f"API error: {response.status_code}",
                    "content": "抱歉，在处理您的请求时遇到了问题。请访问简仪科技官网 www.jytek.com 获取技术支持。",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error generating response from Gemini: {str(e)}")
            return {
                "provider": self.provider_name,
                "error": str(e),
                "content": "抱歉，在生成回答时遇到了错误。请联系简仪科技技术支持。",
                "timestamp": datetime.now().isoformat()
            }
    
    def _enhance_prompt_with_context(self, prompt: str) -> str:
        """为提示词添加简仪科技和PXI专业上下文"""
        context = """你是简仪科技(JYTEK)锐视测控平台的专业AI助手，特别擅长代码生成和技术实现。

专业背景：
- 公司：简仪科技 (JYTEK)
- 平台：锐视测控平台  
- 专业领域：PXI模块化仪器、LabVIEW开发、驱动程序、API接口
- 官网：www.jytek.com

技术专长：
1. LabVIEW程序开发和优化
2. PXI驱动程序开发
3. TestStand测试序列设计
4. VISA和IVI接口编程
5. 数据采集算法实现
6. 自动化测试脚本

回答要求：
- 提供可执行的代码示例
- 包含详细的技术实现步骤
- 考虑PXI系统的特殊要求
- 推荐最佳编程实践

用户问题："""
        
        return context + prompt
    
    def _enhance_response_with_jytek_info(self, content: str, original_prompt: str) -> str:
        """为回答添加简仪科技相关信息"""
        # 检查是否是代码相关问题
        if any(keyword in original_prompt.lower() for keyword in ['代码', '编程', '开发', 'labview', '驱动', 'api']):
            footer = "\n\n---\n💻 **开发支持**：简仪科技提供完整的软件开发支持，包括驱动程序、示例代码和技术文档。详情请访问：www.jytek.com"
            content += footer
        
        return content
    
    def get_available_models(self) -> List[str]:
        """Get available Gemini models"""
        return ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
    
    @property
    def provider_name(self) -> str:
        return "gemini"
    
    @property
    def provider_capabilities(self) -> List[str]:
        return self._capabilities
    
    @property
    def provider_cost_tier(self) -> int:
        return self._cost_tier


class ModelSelector:
    """智能模型选择器，专门针对PXI测控领域优化"""
    
    def __init__(self, llm_manager):
        self.llm_manager = llm_manager
        # PXI专业领域的特征模式
        self.patterns = {
            "math": r"(数学|方程|计算|积分|微分|导数|矩阵|向量|概率|统计|几何|代数|三角|函数|算法)",
            "code": r"(代码|编程|函数|算法|程序|开发|软件|编写|实现|调试|API|接口|类|对象|变量|循环|条件|语法|LabVIEW|TestStand|VISA|IVI)",
            "pxi": r"(PXI|CompactPCI|模块化仪器|机箱|控制器|背板|插槽|同步|触发|时钟|总线)",
            "instrumentation": r"(仪器|测量|测试|校准|精度|分辨率|采样率|带宽|示波器|信号发生器|数字万用表|频谱分析仪|逻辑分析仪|数据采集)",
            "automation": r"(自动化|测控|数据采集|实时|同步|触发|序列|流程|批处理|调度)",
            "electronics": r"(电路|电子|电工|电压|电流|电阻|电容|电感|晶体管|二极管|逻辑门|数字电路|模拟电路|信号|频率|波形|滤波)",
            "physics": r"(物理|力学|动力学|热力学|电磁学|光学|量子|相对论|能量|功率|速度|加速度|质量|动量|波动|振动)",
            "chinese": r"[\u4e00-\u9fa5]{10,}",  # At least 10 Chinese characters
            "general": r"(什么|如何|为什么|怎么|介绍|说明|解释|帮助|问题|咨询)"
        }
    
    def select_model(self, query: str, user_preference: Optional[str] = None) -> Tuple[str, str]:
        """
        选择最佳模型，专门针对PXI测控领域优化
        
        Args:
            query: 用户问题
            user_preference: 可选的用户偏好提供商
            
        Returns:
            Tuple of (provider_name, model_name)
        """
        # 如果用户有偏好且可用，使用用户偏好
        if user_preference and user_preference in self.llm_manager.get_all_providers():
            provider = self.llm_manager.providers[user_preference]
            return user_preference, provider.default_model
        
        # 检测查询特征
        characteristics = self._detect_characteristics(query)
        logger.info(f"Detected characteristics: {characteristics}")
        
        # 优先使用有真实API密钥的提供商（包括新增的提供商）
        real_api_providers = ['claude', 'gemini', 'volcesDeepseek', 'qwen-plus']
        available_real_providers = [p for p in real_api_providers if p in self.llm_manager.get_all_providers()]
        
        if available_real_providers:
            # 只对真实API提供商评分
            providers = {name: self.llm_manager.providers[name] for name in available_real_providers}
            scores = {}
            for name, provider in providers.items():
                score = self._calculate_provider_score(provider, characteristics)
                scores[name] = score
            
            logger.info(f"Real API provider scores: {scores}")
            
            # 选择最佳真实API提供商
            best_provider_name = max(scores.items(), key=lambda x: x[1])[0]
            best_provider = self.llm_manager.providers[best_provider_name]
            
            return best_provider_name, best_provider.default_model
        
        # 回退到所有提供商
        providers = {name: self.llm_manager.providers[name] for name in self.llm_manager.get_all_providers()}
        scores = {}
        for name, provider in providers.items():
            score = self._calculate_provider_score(provider, characteristics)
            scores[name] = score
        
        logger.info(f"Fallback provider scores: {scores}")
        
        # 选择得分最高的提供商
        if not scores:
            # 最终回退到默认提供商
            return self.llm_manager.default_provider, self.llm_manager.providers[self.llm_manager.default_provider].default_model
        
        best_provider_name = max(scores.items(), key=lambda x: x[1])[0]
        best_provider = self.llm_manager.providers[best_provider_name]
        
        return best_provider_name, best_provider.default_model
    
    def _detect_characteristics(self, query: str) -> List[str]:
        """检测查询的特征，专门针对PXI领域优化"""
        characteristics = []
        
        # 检查每个模式
        for category, pattern in self.patterns.items():
            if re.search(pattern, query, re.IGNORECASE):
                characteristics.append(category)
        
        # 默认添加general
        if not characteristics or len(characteristics) == 1 and characteristics[0] == "chinese":
            characteristics.append("general")
        
        # 检查查询长度判断复杂性
        if len(query) > 200:
            characteristics.append("complex")
        
        # PXI专业领域特殊检测
        if any(keyword in characteristics for keyword in ["pxi", "instrumentation", "automation"]):
            characteristics.append("professional")
        
        return characteristics
    
    def _calculate_provider_score(self, provider: LLMProvider, characteristics: List[str]) -> float:
        """计算提供商得分，针对PXI领域优化"""
        score = 0.0
        
        # 基础能力匹配得分
        for characteristic in characteristics:
            if characteristic in provider.provider_capabilities:
                if characteristic in ["pxi", "instrumentation", "automation"]:
                    # PXI专业特征给更高权重
                    score += 2.0
                elif characteristic in ["code", "math"]:
                    # 技术特征给中等权重
                    score += 1.5
                else:
                    # 一般特征给基础权重
                    score += 1.0
        
        # 根据成本层级调整得分
        if "complex" in characteristics or "professional" in characteristics:
            # 复杂或专业问题偏好高层级模型
            score += provider.provider_cost_tier * 0.2
        else:
            # 简单问题偏好低成本模型
            score += (6 - provider.provider_cost_tier) * 0.1
        
        # 特殊优化：Claude擅长复杂分析，Gemini擅长代码
        if provider.provider_name == "claude" and any(char in characteristics for char in ["math", "physics", "complex", "professional"]):
            score += 0.5
        elif provider.provider_name == "gemini" and any(char in characteristics for char in ["code", "automation"]):
            score += 0.5
        
        return score


class LLMManager:
    """LLM管理器，专门针对锐视测控平台优化"""
    
    def __init__(self):
        """Initialize LLM manager"""
        self.providers = {}
        self.default_provider = None
        self.model_selector = None
    
    def register_provider(self, name: str, provider: LLMProvider) -> None:
        """Register a new LLM provider"""
        self.providers[name] = provider
        if self.default_provider is None:
            self.default_provider = name
        logger.info(f"Registered provider for Ruishi Platform: {name}")
    
    def set_default_provider(self, name: str) -> None:
        """Set the default LLM provider"""
        if name in self.providers:
            self.default_provider = name
            logger.info(f"Default provider set to: {name}")
        else:
            raise ValueError(f"Provider '{name}' not registered")
    
    def initialize_model_selector(self) -> None:
        """Initialize the model selector"""
        self.model_selector = ModelSelector(self)
        logger.info("Model selector initialized for Ruishi Control Platform")
    
    async def generate_response(self, prompt: str, provider: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Generate a response using the specified or auto-selected provider"""
        # 使用模型选择器（如果可用且未指定特定提供商）
        if self.model_selector and not provider:
            selected_provider, selected_model = self.model_selector.select_model(prompt, None)
            provider = selected_provider
            kwargs['model'] = selected_model
            logger.info(f"Auto-selected provider: {selected_provider}, model: {selected_model}")
        else:
            provider_name = provider or self.default_provider
            
        if provider not in self.providers:
            logger.error(f"Provider '{provider}' not found")
            return {
                "error": f"Provider '{provider}' not found",
                "content": "抱歉，请求的AI模型不可用。请访问简仪科技官网 www.jytek.com 获取技术支持。",
                "timestamp": datetime.now().isoformat()
            }
        
        return await self.providers[provider].generate_response(prompt, **kwargs)
    
    def get_all_providers(self) -> List[str]:
        """Get a list of all registered providers"""
        return list(self.providers.keys())
    
    def get_provider_models(self, provider: str) -> List[str]:
        """Get available models for a specific provider"""
        if provider not in self.providers:
            logger.error(f"Provider '{provider}' not found")
            return []
        
        return self.providers[provider].get_available_models()
    
    def get_provider_capabilities(self, provider: str) -> List[str]:
        """Get capabilities for a specific provider"""
        if provider not in self.providers:
            logger.error(f"Provider '{provider}' not found")
            return []
        
        return self.providers[provider].provider_capabilities


# 创建LLMManager单例实例
llm_manager = LLMManager()

# 创建一个简化的模型选择器接口
class SimpleModelSelector:
    """简化的模型选择器接口"""
    
    def __init__(self):
        self.providers = {}
        self.default_provider = 'claude'
    
    def ask_question(self, question: str, provider: str = None, model: str = None, options: dict = None) -> dict:
        """同步问答接口"""
        import asyncio
        import threading
        
        # 使用新线程来运行异步函数，避免事件循环冲突
        try:
            result = None
            error = None
            
            def run_async():
                nonlocal result, error
                try:
                    # 在新线程中创建新的事件循环
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    result = loop.run_until_complete(self._async_ask_question(question, provider, model, options))
                    loop.close()
                except Exception as e:
                    error = e
            
            # 在新线程中运行异步函数
            thread = threading.Thread(target=run_async)
            thread.start()
            thread.join(timeout=30)  # 30秒超时
            
            if error:
                raise error
            
            if result is None:
                raise TimeoutError("请求超时")
            
            return result
            
        except Exception as e:
            return {
                'error': str(e),
                'content': f'抱歉，在处理您的问题时遇到了错误。请访问简仪科技官网 www.jytek.com 获取技术支持。',
                'provider': provider or self.default_provider
            }
    
    async def _async_ask_question(self, question: str, provider: str = None, model: str = None, options: dict = None) -> dict:
        """异步问答实现"""
        options = options or {}
        if model:
            options['model'] = model
        
        return await llm_manager.generate_response(question, provider, **options)
    
    def get_available_providers(self) -> list:
        """获取可用的提供商列表"""
        return llm_manager.get_all_providers()

# 创建全局模型选择器实例
model_selector = SimpleModelSelector()

def initialize_llm_providers(config: Dict[str, Any]) -> None:
    """初始化所有LLM提供商，专门针对锐视测控平台配置"""
    
    # 初始化Claude（专门用于复杂技术分析）
    claude_provider = ClaudeProvider()
    claude_provider.initialize(
        api_key=config.get('claude', {}).get('api_key', ''),
        default_model=config.get('claude', {}).get('default_model', 'claude-3-sonnet-20240229')
    )
    llm_manager.register_provider('claude', claude_provider)
    
    # 初始化Gemini（专门用于代码生成和技术实现）
    gemini_provider = GeminiProvider()
    gemini_provider.initialize(
        api_key=config.get('gemini', {}).get('api_key', ''),
        default_model=config.get('gemini', {}).get('default_model', 'gemini-1.5-flash')
    )
    llm_manager.register_provider('gemini', gemini_provider)
    
    # 初始化Volces Deepseek（专门用于深度推理和分析）
    if 'volcesDeepseek' in config:
        volces_provider = VolcesDeepseekProvider()
        volces_provider.initialize(
            api_key=config.get('volcesDeepseek', {}).get('api_key', ''),
            url=config.get('volcesDeepseek', {}).get('url', 'https://ark.cn-beijing.volces.com/api/v3/chat/completions'),
            model=config.get('volcesDeepseek', {}).get('model', 'deepseek-r1-250528'),
            max_tokens=config.get('volcesDeepseek', {}).get('max_tokens', 16191)
        )
        llm_manager.register_provider('volcesDeepseek', volces_provider)
    
    # 初始化Qwen Plus（专门用于中文理解和多模态处理）
    if 'qwen-plus' in config:
        qwen_provider = QwenPlusProvider()
        qwen_provider.initialize(
            api_key=config.get('qwen-plus', {}).get('api_key', ''),
            url=config.get('qwen-plus', {}).get('url', 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions'),
            model=config.get('qwen-plus', {}).get('model', 'qwen-plus-2025-04-28'),
            max_tokens=config.get('qwen-plus', {}).get('max_tokens', 16191)
        )
        llm_manager.register_provider('qwen-plus', qwen_provider)
    
    # 设置默认提供商
    default_provider = config.get('default_provider', 'claude')
    if default_provider in llm_manager.get_all_providers():
        llm_manager.set_default_provider(default_provider)
    
    # 初始化模型选择器
    llm_manager.initialize_model_selector()
    
    logger.info(f"Initialized LLM providers for Ruishi Control Platform: {llm_manager.get_all_providers()}")
