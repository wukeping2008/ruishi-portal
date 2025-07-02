"""
AI智能推荐系统
基于用户问题和行为的智能产品推荐引擎
简仪科技锐视测控平台专用
"""

import re
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import sqlite3
import os
from .database import db_manager

logger = logging.getLogger(__name__)

class IntelligentRecommendation:
    """智能推荐系统核心类"""
    
    def __init__(self):
        self.db = db_manager
        self.init_recommendation_tables()
        
        # PXI产品特征模式
        self.product_patterns = {
            'data_acquisition': {
                'keywords': ['数据采集', '采集卡', 'DAQ', '模拟输入', '数字化', '采样', '测量', '传感器', '信号调理'],
                'features': ['高精度', '多通道', '同步采集', '实时处理'],
                'applications': ['测试测量', '监控系统', '科研实验', '工业自动化']
            },
            'signal_generation': {
                'keywords': ['信号发生', '波形发生器', '任意波形', 'AWG', '函数发生器', '信号源', '激励信号'],
                'features': ['高频率', '低失真', '多波形', '可编程'],
                'applications': ['信号测试', '设备校准', '系统激励', '仿真测试']
            },
            'digital_io': {
                'keywords': ['数字IO', '数字输入输出', 'DIO', '开关量', '逻辑控制', '继电器', '数字信号'],
                'features': ['高速响应', '大电流驱动', '光电隔离', '可配置'],
                'applications': ['设备控制', '状态监测', '逻辑处理', '接口转换']
            },
            'rf_microwave': {
                'keywords': ['射频', '微波', 'RF', '频谱', '网络分析', '信号分析', '天线测试'],
                'features': ['宽频带', '高动态范围', '低噪声', '高精度'],
                'applications': ['通信测试', '雷达系统', '卫星通信', '无线设备']
            },
            'oscilloscope': {
                'keywords': ['示波器', '波形显示', '时域分析', '触发', '存储深度', '带宽'],
                'features': ['高带宽', '高采样率', '深存储', '多触发'],
                'applications': ['信号调试', '波形分析', '时序测试', '故障诊断']
            },
            'multimeter': {
                'keywords': ['万用表', '电压测量', '电流测量', '电阻测量', 'DMM', '精密测量'],
                'features': ['高精度', '多量程', '自动量程', '数据记录'],
                'applications': ['电路测试', '元件测量', '校准验证', '质量检测']
            }
        }
        
        # 应用场景映射
        self.application_scenarios = {
            '汽车电子测试': ['data_acquisition', 'signal_generation', 'oscilloscope'],
            '航空航天': ['rf_microwave', 'data_acquisition', 'signal_generation'],
            '通信设备测试': ['rf_microwave', 'signal_generation', 'oscilloscope'],
            '工业自动化': ['digital_io', 'data_acquisition', 'multimeter'],
            '科研教学': ['data_acquisition', 'signal_generation', 'oscilloscope', 'multimeter'],
            '电力系统': ['data_acquisition', 'multimeter', 'oscilloscope'],
            '医疗设备': ['data_acquisition', 'signal_generation', 'digital_io'],
            '半导体测试': ['rf_microwave', 'data_acquisition', 'signal_generation']
        }
        
        # 产品兼容性矩阵
        self.compatibility_matrix = {
            'pxi_chassis': {
                'compatible_with': ['all_modules'],
                'required_for': ['system_integration']
            },
            'pxi_controller': {
                'compatible_with': ['all_modules'],
                'required_for': ['system_control']
            }
        }
    
    def init_recommendation_tables(self):
        """初始化推荐系统相关数据表"""
        conn = self.db.get_connection()
        try:
            # 推荐缓存表
            conn.execute('''
                CREATE TABLE IF NOT EXISTS recommendation_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_hash TEXT UNIQUE,
                    user_intent JSON,
                    recommended_products JSON,
                    recommendation_score REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    hit_count INTEGER DEFAULT 0,
                    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 用户偏好表
            conn.execute('''
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    session_id TEXT,
                    preference_type TEXT,
                    preference_data JSON,
                    weight REAL DEFAULT 1.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 产品评分表
            conn.execute('''
                CREATE TABLE IF NOT EXISTS product_ratings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_category TEXT,
                    product_name TEXT,
                    user_rating REAL,
                    recommendation_context TEXT,
                    feedback_data JSON,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            logger.info("推荐系统数据表初始化完成")
            
        except Exception as e:
            logger.error(f"推荐系统数据表初始化失败: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def analyze_user_intent(self, question: str, context: Dict = None) -> Dict[str, Any]:
        """
        分析用户意图和需求
        
        Args:
            question: 用户问题
            context: 上下文信息（可选）
            
        Returns:
            用户意图分析结果
        """
        try:
            # 生成问题哈希用于缓存
            import hashlib
            question_hash = hashlib.md5(question.encode('utf-8')).hexdigest()
            
            # 检查缓存
            cached_result = self._get_cached_recommendation(question_hash)
            if cached_result:
                return cached_result
            
            # 文本预处理
            question_lower = question.lower()
            
            # 意图分析结果
            intent_result = {
                'question': question,
                'question_hash': question_hash,
                'detected_categories': [],
                'technical_requirements': {},
                'application_scenario': None,
                'urgency_level': 'normal',
                'budget_indication': None,
                'specific_products': [],
                'confidence_score': 0.0
            }
            
            # 1. 产品类别检测
            category_scores = {}
            for category, patterns in self.product_patterns.items():
                score = 0
                matched_keywords = []
                
                # 关键词匹配
                for keyword in patterns['keywords']:
                    if keyword.lower() in question_lower:
                        score += 2
                        matched_keywords.append(keyword)
                
                # 特征匹配
                for feature in patterns['features']:
                    if feature.lower() in question_lower:
                        score += 1
                
                # 应用场景匹配
                for app in patterns['applications']:
                    if app.lower() in question_lower:
                        score += 1.5
                
                if score > 0:
                    category_scores[category] = {
                        'score': score,
                        'matched_keywords': matched_keywords
                    }
            
            # 排序并选择最相关的类别
            sorted_categories = sorted(category_scores.items(), key=lambda x: x[1]['score'], reverse=True)
            intent_result['detected_categories'] = [
                {
                    'category': cat,
                    'score': data['score'],
                    'matched_keywords': data['matched_keywords']
                }
                for cat, data in sorted_categories[:3]  # 取前3个最相关的类别
            ]
            
            # 2. 技术需求提取
            intent_result['technical_requirements'] = self._extract_technical_requirements(question)
            
            # 3. 应用场景识别
            intent_result['application_scenario'] = self._identify_application_scenario(question)
            
            # 4. 紧急程度判断
            intent_result['urgency_level'] = self._assess_urgency(question)
            
            # 5. 预算指示提取
            intent_result['budget_indication'] = self._extract_budget_info(question)
            
            # 6. 具体产品提及
            intent_result['specific_products'] = self._identify_specific_products(question)
            
            # 7. 计算整体置信度
            intent_result['confidence_score'] = self._calculate_confidence_score(intent_result)
            
            # 缓存结果
            self._cache_recommendation(question_hash, intent_result)
            
            logger.info(f"用户意图分析完成，置信度: {intent_result['confidence_score']:.2f}")
            return intent_result
            
        except Exception as e:
            logger.error(f"用户意图分析失败: {e}")
            return {
                'question': question,
                'error': str(e),
                'detected_categories': [],
                'confidence_score': 0.0
            }
    
    def _extract_technical_requirements(self, question: str) -> Dict[str, Any]:
        """提取技术需求"""
        requirements = {}
        
        # 通道数需求
        channel_patterns = [
            r'(\d+)\s*通道', r'(\d+)\s*路', r'(\d+)\s*channel',
            r'(\d+)\s*ch', r'(\d+)\s*个通道'
        ]
        for pattern in channel_patterns:
            match = re.search(pattern, question, re.IGNORECASE)
            if match:
                requirements['channels'] = int(match.group(1))
                break
        
        # 频率需求
        freq_patterns = [
            r'(\d+(?:\.\d+)?)\s*(khz|mhz|ghz|hz)', 
            r'频率.*?(\d+(?:\.\d+)?)\s*(khz|mhz|ghz|hz)',
            r'带宽.*?(\d+(?:\.\d+)?)\s*(khz|mhz|ghz|hz)'
        ]
        for pattern in freq_patterns:
            match = re.search(pattern, question, re.IGNORECASE)
            if match:
                freq_value = float(match.group(1))
                freq_unit = match.group(2).lower()
                requirements['frequency'] = {
                    'value': freq_value,
                    'unit': freq_unit
                }
                break
        
        # 精度需求
        accuracy_patterns = [
            r'精度.*?(\d+(?:\.\d+)?)\s*%',
            r'准确度.*?(\d+(?:\.\d+)?)\s*%',
            r'误差.*?(\d+(?:\.\d+)?)\s*%'
        ]
        for pattern in accuracy_patterns:
            match = re.search(pattern, question, re.IGNORECASE)
            if match:
                requirements['accuracy'] = float(match.group(1))
                break
        
        # 采样率需求
        sample_patterns = [
            r'采样率.*?(\d+(?:\.\d+)?)\s*(ksps|msps|gsps|sps)',
            r'采样.*?(\d+(?:\.\d+)?)\s*(ksps|msps|gsps|sps)'
        ]
        for pattern in sample_patterns:
            match = re.search(pattern, question, re.IGNORECASE)
            if match:
                requirements['sample_rate'] = {
                    'value': float(match.group(1)),
                    'unit': match.group(2).lower()
                }
                break
        
        return requirements
    
    def _identify_application_scenario(self, question: str) -> Optional[str]:
        """识别应用场景"""
        question_lower = question.lower()
        
        for scenario, _ in self.application_scenarios.items():
            scenario_keywords = scenario.lower().split()
            if any(keyword in question_lower for keyword in scenario_keywords):
                return scenario
        
        # 通用场景关键词匹配
        scenario_keywords = {
            '汽车电子测试': ['汽车', '车载', '电子', 'ecu', '汽车电子'],
            '航空航天': ['航空', '航天', '飞机', '卫星', '雷达'],
            '通信设备测试': ['通信', '5g', '4g', '基站', '天线', '射频'],
            '工业自动化': ['工业', '自动化', '控制', '生产线', '制造'],
            '科研教学': ['科研', '教学', '实验', '研究', '学校', '大学'],
            '电力系统': ['电力', '电网', '变电', '配电', '电能'],
            '医疗设备': ['医疗', '医用', '生物', '心电', '血压'],
            '半导体测试': ['半导体', '芯片', '集成电路', 'ic', '晶圆']
        }
        
        for scenario, keywords in scenario_keywords.items():
            if any(keyword in question_lower for keyword in keywords):
                return scenario
        
        return None
    
    def _assess_urgency(self, question: str) -> str:
        """评估紧急程度"""
        urgent_keywords = ['紧急', '急需', '马上', '立即', '尽快', 'urgent', 'asap']
        normal_keywords = ['计划', '准备', '考虑', '了解', 'plan', 'consider']
        
        question_lower = question.lower()
        
        if any(keyword in question_lower for keyword in urgent_keywords):
            return 'urgent'
        elif any(keyword in question_lower for keyword in normal_keywords):
            return 'planned'
        else:
            return 'normal'
    
    def _extract_budget_info(self, question: str) -> Optional[Dict[str, Any]]:
        """提取预算信息"""
        budget_patterns = [
            r'预算.*?(\d+(?:\.\d+)?)\s*(万|千|元)',
            r'价格.*?(\d+(?:\.\d+)?)\s*(万|千|元)',
            r'成本.*?(\d+(?:\.\d+)?)\s*(万|千|元)',
            r'(\d+(?:\.\d+)?)\s*(万|千|元).*?预算'
        ]
        
        for pattern in budget_patterns:
            match = re.search(pattern, question, re.IGNORECASE)
            if match:
                amount = float(match.group(1))
                unit = match.group(2)
                
                # 转换为标准单位（元）
                if unit == '万':
                    amount *= 10000
                elif unit == '千':
                    amount *= 1000
                
                return {
                    'amount': amount,
                    'currency': 'CNY',
                    'type': 'approximate'
                }
        
        return None
    
    def _identify_specific_products(self, question: str) -> List[str]:
        """识别具体产品提及"""
        # 简仪科技产品名称模式
        product_patterns = [
            r'JY\d+[A-Z]*',  # JY开头的产品型号
            r'SeeSharp',      # SeeSharp平台
            r'锐视',          # 锐视系列
        ]
        
        identified_products = []
        for pattern in product_patterns:
            matches = re.findall(pattern, question, re.IGNORECASE)
            identified_products.extend(matches)
        
        return list(set(identified_products))  # 去重
    
    def _calculate_confidence_score(self, intent_result: Dict[str, Any]) -> float:
        """计算置信度分数"""
        score = 0.0
        
        # 类别检测得分
        if intent_result['detected_categories']:
            max_category_score = max(cat['score'] for cat in intent_result['detected_categories'])
            score += min(max_category_score / 10, 0.4)  # 最多0.4分
        
        # 技术需求得分
        tech_req_count = len(intent_result['technical_requirements'])
        score += min(tech_req_count * 0.1, 0.3)  # 最多0.3分
        
        # 应用场景得分
        if intent_result['application_scenario']:
            score += 0.2
        
        # 具体产品得分
        if intent_result['specific_products']:
            score += 0.1
        
        return min(score, 1.0)  # 最大1.0分
    
    def recommend_products(self, intent_data: Dict[str, Any], limit: int = 5) -> List[Dict[str, Any]]:
        """
        基于意图数据推荐产品
        
        Args:
            intent_data: 用户意图分析结果
            limit: 推荐产品数量限制
            
        Returns:
            推荐产品列表
        """
        try:
            recommendations = []
            
            # 获取检测到的产品类别
            detected_categories = intent_data.get('detected_categories', [])
            if not detected_categories:
                return self._get_default_recommendations(limit)
            
            # 为每个类别生成推荐
            for category_info in detected_categories:
                category = category_info['category']
                category_score = category_info['score']
                
                # 获取该类别的产品推荐
                category_products = self._get_category_products(category, intent_data)
                
                for product in category_products:
                    # 计算推荐分数
                    recommendation_score = self._calculate_recommendation_score(
                        product, intent_data, category_score
                    )
                    
                    recommendation = {
                        'product_id': product.get('id', f"{category}_{len(recommendations)}"),
                        'name': product['name'],
                        'category': category,
                        'description': product['description'],
                        'features': product.get('features', []),
                        'specifications': product.get('specifications', {}),
                        'applications': product.get('applications', []),
                        'recommendation_score': recommendation_score,
                        'recommendation_reason': self._generate_recommendation_reason(
                            product, intent_data, category_info
                        ),
                        'price_range': product.get('price_range', '请咨询'),
                        'availability': product.get('availability', '现货'),
                        'technical_support': True,
                        'documentation_url': f"https://www.jytek.com/products/{category}",
                        'contact_info': {
                            'website': 'https://www.jytek.com',
                            'phone': '021-50475899',
                            'email': 'info@jytek.com'
                        }
                    }
                    
                    recommendations.append(recommendation)
            
            # 按推荐分数排序
            recommendations.sort(key=lambda x: x['recommendation_score'], reverse=True)
            
            # 限制返回数量
            final_recommendations = recommendations[:limit]
            
            # 记录推荐结果
            self._log_recommendation(intent_data, final_recommendations)
            
            logger.info(f"生成了 {len(final_recommendations)} 个产品推荐")
            return final_recommendations
            
        except Exception as e:
            logger.error(f"产品推荐生成失败: {e}")
            return self._get_default_recommendations(limit)
    
    def _get_category_products(self, category: str, intent_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """获取指定类别的产品信息"""
        # 这里应该从产品数据库或API获取真实产品数据
        # 现在使用模拟数据
        
        product_database = {
            'data_acquisition': [
                {
                    'id': 'JY5001',
                    'name': 'JY5001 高精度数据采集卡',
                    'description': '16位分辨率，8通道同步采集，最高1MS/s采样率',
                    'features': ['16位ADC', '8通道', '1MS/s采样率', '软件校准', 'LabVIEW驱动'],
                    'specifications': {
                        '分辨率': '16位',
                        '通道数': '8路差分',
                        '采样率': '1MS/s',
                        '输入范围': '±10V',
                        '精度': '0.1%'
                    },
                    'applications': ['测试测量', '数据记录', '信号监测', '科研实验'],
                    'price_range': '8000-12000元',
                    'availability': '现货'
                },
                {
                    'id': 'JY5002',
                    'name': 'JY5002 多功能数据采集模块',
                    'description': '24位高精度，多种信号类型支持，适合精密测量',
                    'features': ['24位ADC', '多信号类型', '隔离输入', '高精度', '易于集成'],
                    'specifications': {
                        '分辨率': '24位',
                        '通道数': '4路',
                        '采样率': '100kS/s',
                        '输入类型': '电压/电流/热电偶',
                        '精度': '0.01%'
                    },
                    'applications': ['精密测量', '温度监测', '工业控制', '质量检测'],
                    'price_range': '15000-20000元',
                    'availability': '现货'
                }
            ],
            'signal_generation': [
                {
                    'id': 'JY6001',
                    'name': 'JY6001 任意波形发生器',
                    'description': '双通道任意波形输出，14位分辨率，100MS/s采样率',
                    'features': ['双通道输出', '14位DAC', '100MS/s', '任意波形', '函数发生'],
                    'specifications': {
                        '通道数': '2路',
                        '分辨率': '14位',
                        '采样率': '100MS/s',
                        '频率范围': 'DC-50MHz',
                        '输出幅度': '±10V'
                    },
                    'applications': ['信号测试', '设备校准', '系统激励', '波形仿真'],
                    'price_range': '12000-18000元',
                    'availability': '现货'
                }
            ],
            'digital_io': [
                {
                    'id': 'JY7001',
                    'name': 'JY7001 数字I/O模块',
                    'description': '32路数字I/O，5V TTL兼容，高速响应',
                    'features': ['32路I/O', 'TTL兼容', '高速响应', '可配置方向', '光电隔离'],
                    'specifications': {
                        '通道数': '32路',
                        '电平标准': '5V TTL',
                        '响应时间': '<1μs',
                        '驱动能力': '24mA',
                        '隔离电压': '2500V'
                    },
                    'applications': ['设备控制', '状态监测', '逻辑处理', '接口转换'],
                    'price_range': '6000-9000元',
                    'availability': '现货'
                }
            ],
            'rf_microwave': [
                {
                    'id': 'JY8001',
                    'name': 'JY8001 射频信号分析仪',
                    'description': '9kHz-6GHz频率范围，高动态范围，实时频谱分析',
                    'features': ['宽频带', '实时分析', '高动态范围', '多种测量', '便携设计'],
                    'specifications': {
                        '频率范围': '9kHz-6GHz',
                        '动态范围': '120dB',
                        '分辨率带宽': '1Hz-10MHz',
                        '相位噪声': '-110dBc/Hz@10kHz',
                        '测量精度': '±0.5dB'
                    },
                    'applications': ['通信测试', '频谱分析', '信号质量', '干扰分析'],
                    'price_range': '80000-120000元',
                    'availability': '预订'
                }
            ],
            'oscilloscope': [
                {
                    'id': 'JY9001',
                    'name': 'JY9001 数字示波器模块',
                    'description': '4通道，200MHz带宽，1GS/s采样率，深存储',
                    'features': ['4通道', '200MHz带宽', '1GS/s采样', '深存储', '多种触发'],
                    'specifications': {
                        '通道数': '4路',
                        '带宽': '200MHz',
                        '采样率': '1GS/s',
                        '存储深度': '100Mpts',
                        '垂直分辨率': '8位'
                    },
                    'applications': ['信号调试', '波形分析', '时序测试', '故障诊断'],
                    'price_range': '25000-35000元',
                    'availability': '现货'
                }
            ],
            'multimeter': [
                {
                    'id': 'JY4001',
                    'name': 'JY4001 精密数字万用表',
                    'description': '6.5位分辨率，多种测量功能，高精度测量',
                    'features': ['6.5位分辨率', '多功能测量', '高精度', '数据记录', '远程控制'],
                    'specifications': {
                        '分辨率': '6.5位',
                        '直流电压精度': '0.0035%',
                        '交流电压精度': '0.06%',
                        '电阻精度': '0.01%',
                        '测量速度': '1000次/秒'
                    },
                    'applications': ['精密测量', '校准验证', '质量检测', '研发测试'],
                    'price_range': '18000-25000元',
                    'availability': '现货'
                }
            ]
        }
        
        return product_database.get(category, [])
    
    def _calculate_recommendation_score(self, product: Dict[str, Any], 
                                      intent_data: Dict[str, Any], 
                                      category_score: float) -> float:
        """计算产品推荐分数"""
        score = category_score * 0.3  # 基础类别匹配分数
        
        # 技术需求匹配
        tech_requirements = intent_data.get('technical_requirements', {})
        product_specs = product.get('specifications', {})
        
        # 通道数匹配
        if 'channels' in tech_requirements and '通道数' in product_specs:
            required_channels = tech_requirements['channels']
            product_channels = self._extract_number_from_spec(product_specs['通道数'])
            if product_channels and product_channels >= required_channels:
                score += 2.0
            elif product_channels:
                score += 1.0
        
        # 频率需求匹配
        if 'frequency' in tech_requirements:
            freq_specs = ['带宽', '频率范围', '采样率']
            for spec in freq_specs:
                if spec in product_specs:
                    score += 1.5
                    break
        
        # 精度需求匹配
        if 'accuracy' in tech_requirements:
            accuracy_specs = ['精度', '分辨率']
            for spec in accuracy_specs:
                if spec in product_specs:
                    score += 1.0
                    break
        
        # 应用场景匹配
        application_scenario = intent_data.get('application_scenario')
        if application_scenario and application_scenario in self.application_scenarios:
            recommended_categories = self.application_scenarios[application_scenario]
            product_category = product.get('category', '')
            if product_category in recommended_categories:
                score += 2.0
        
        # 产品应用匹配
        product_applications = product.get('applications', [])
        if application_scenario:
            scenario_keywords = application_scenario.lower().split()
            for app in product_applications:
                if any(keyword in app.lower() for keyword in scenario_keywords):
                    score += 1.0
                    break
        
        return min(score, 10.0)  # 最大10分
    
    def _extract_number_from_spec(self, spec_text: str) -> Optional[int]:
        """从规格文本中提取数字"""
        if not spec_text:
            return None
        
        match = re.search(r'(\d+)', str(spec_text))
        return int(match.group(1)) if match else None
    
    def _generate_recommendation_reason(self, product: Dict[str, Any], 
                                      intent_data: Dict[str, Any], 
                                      category_info: Dict[str, Any]) -> str:
        """生成推荐理由"""
        reasons = []
        
        # 类别匹配理由
        matched_keywords = category_info.get('matched_keywords', [])
        if matched_keywords:
            reasons.append(f"匹配您提到的关键词：{', '.join(matched_keywords[:3])}")
        
        # 技术需求匹配理由
        tech_requirements = intent_data.get('technical_requirements', {})
        product_specs = product.get('specifications', {})
        
        if 'channels' in tech_requirements and '通道数' in product_specs:
            required_channels = tech_requirements['channels']
            product_channels = self._extract_number_from_spec(product_specs['通道数'])
            if product_channels and product_channels >= required_channels:
                reasons.append(f"满足您的{required_channels}通道需求")
        
        if 'frequency' in tech_requirements:
            freq_req = tech_requirements['frequency']
            if any(spec in product_specs for spec in ['带宽', '频率范围', '采样率']):
                reasons.append(f"支持您需要的{freq_req['value']}{freq_req['unit']}频率要求")
        
        # 应用场景匹配理由
        application_scenario = intent_data.get('application_scenario')
        if application_scenario:
            product_applications = product.get('applications', [])
            scenario_keywords = application_scenario.lower().split()
            for app in product_applications:
                if any(keyword in app.lower() for keyword in scenario_keywords):
                    reasons.append(f"适用于{application_scenario}场景")
                    break
        
        # 产品特色理由
        features = product.get('features', [])
        if features:
            key_features = features[:2]  # 取前2个特色
            reasons.append(f"具备{', '.join(key_features)}等优势")
        
        if not reasons:
            reasons.append("简仪科技专业PXI产品，质量可靠")
        
        return "；".join(reasons)
    
    def _get_default_recommendations(self, limit: int = 5) -> List[Dict[str, Any]]:
        """获取默认推荐产品"""
        default_products = [
            {
                'product_id': 'JY5001',
                'name': 'JY5001 高精度数据采集卡',
                'category': 'data_acquisition',
                'description': '16位分辨率，8通道同步采集，最高1MS/s采样率',
                'features': ['16位ADC', '8通道', '1MS/s采样率', '软件校准'],
                'specifications': {
                    '分辨率': '16位',
                    '通道数': '8路差分',
                    '采样率': '1MS/s',
                    '输入范围': '±10V'
                },
                'applications': ['测试测量', '数据记录', '信号监测'],
                'recommendation_score': 8.0,
                'recommendation_reason': '简仪科技热门产品，适用于多种测控应用',
                'price_range': '8000-12000元',
                'availability': '现货',
                'technical_support': True,
                'documentation_url': 'https://www.jytek.com/products/data_acquisition',
                'contact_info': {
                    'website': 'https://www.jytek.com',
                    'phone': '021-50475899',
                    'email': 'info@jytek.com'
                }
            },
            {
                'product_id': 'JY6001',
                'name': 'JY6001 任意波形发生器',
                'category': 'signal_generation',
                'description': '双通道任意波形输出，14位分辨率，100MS/s采样率',
                'features': ['双通道输出', '14位DAC', '100MS/s', '任意波形'],
                'specifications': {
                    '通道数': '2路',
                    '分辨率': '14位',
                    '采样率': '100MS/s',
                    '频率范围': 'DC-50MHz'
                },
                'applications': ['信号测试', '设备校准', '系统激励'],
                'recommendation_score': 7.5,
                'recommendation_reason': '高性能信号发生器，支持多种波形输出',
                'price_range': '12000-18000元',
                'availability': '现货',
                'technical_support': True,
                'documentation_url': 'https://www.jytek.com/products/signal_generation',
                'contact_info': {
                    'website': 'https://www.jytek.com',
                    'phone': '021-50475899',
                    'email': 'info@jytek.com'
                }
            },
            {
                'product_id': 'JY9001',
                'name': 'JY9001 数字示波器模块',
                'category': 'oscilloscope',
                'description': '4通道，200MHz带宽，1GS/s采样率，深存储',
                'features': ['4通道', '200MHz带宽', '1GS/s采样', '深存储'],
                'specifications': {
                    '通道数': '4路',
                    '带宽': '200MHz',
                    '采样率': '1GS/s',
                    '存储深度': '100Mpts'
                },
                'applications': ['信号调试', '波形分析', '时序测试'],
                'recommendation_score': 7.0,
                'recommendation_reason': '高性能示波器模块，适合信号分析应用',
                'price_range': '25000-35000元',
                'availability': '现货',
                'technical_support': True,
                'documentation_url': 'https://www.jytek.com/products/oscilloscope',
                'contact_info': {
                    'website': 'https://www.jytek.com',
                    'phone': '021-50475899',
                    'email': 'info@jytek.com'
                }
            }
        ]
        
        return default_products[:limit]
    
    def _get_cached_recommendation(self, question_hash: str) -> Optional[Dict[str, Any]]:
        """获取缓存的推荐结果"""
        conn = self.db.get_connection()
        try:
            cursor = conn.execute('''
                SELECT user_intent, hit_count FROM recommendation_cache 
                WHERE question_hash = ?
            ''', (question_hash,))
            
            result = cursor.fetchone()
            if result:
                # 更新命中次数和访问时间
                conn.execute('''
                    UPDATE recommendation_cache 
                    SET hit_count = hit_count + 1, last_accessed = CURRENT_TIMESTAMP
                    WHERE question_hash = ?
                ''', (question_hash,))
                conn.commit()
                
                return json.loads(result['user_intent'])
            
            return None
            
        except Exception as e:
            logger.error(f"获取缓存推荐失败: {e}")
            return None
        finally:
            conn.close()
    
    def _cache_recommendation(self, question_hash: str, intent_result: Dict[str, Any]):
        """缓存推荐结果"""
        conn = self.db.get_connection()
        try:
            conn.execute('''
                INSERT OR REPLACE INTO recommendation_cache 
                (question_hash, user_intent, recommendation_score, created_at, hit_count)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP, 1)
            ''', (
                question_hash,
                json.dumps(intent_result, ensure_ascii=False),
                intent_result.get('confidence_score', 0.0)
            ))
            conn.commit()
            
        except Exception as e:
            logger.error(f"缓存推荐结果失败: {e}")
        finally:
            conn.close()
    
    def _log_recommendation(self, intent_data: Dict[str, Any], recommendations: List[Dict[str, Any]]):
        """记录推荐结果用于分析"""
        try:
            # 这里可以记录推荐日志，用于后续分析和优化
            logger.info(f"推荐记录 - 意图置信度: {intent_data.get('confidence_score', 0):.2f}, "
                       f"推荐数量: {len(recommendations)}")
            
            # 可以将推荐结果保存到数据库用于分析
            # 暂时只记录日志
            
        except Exception as e:
            logger.error(f"记录推荐日志失败: {e}")
    
    def generate_solution_config(self, products: List[Dict[str, Any]], 
                               intent_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        基于推荐产品生成完整解决方案配置
        
        Args:
            products: 推荐产品列表
            intent_data: 用户意图数据
            
        Returns:
            完整的解决方案配置
        """
        try:
            # 分析产品类别
            categories = set(product['category'] for product in products)
            
            # 生成系统配置
            solution_config = {
                'solution_id': f"solution_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'name': self._generate_solution_name(intent_data, categories),
                'description': self._generate_solution_description(intent_data, products),
                'components': {
                    'chassis': self._recommend_chassis(products, intent_data),
                    'controller': self._recommend_controller(products, intent_data),
                    'modules': products,
                    'software': self._recommend_software(categories),
                    'accessories': self._recommend_accessories(products)
                },
                'estimated_cost': self._estimate_total_cost(products),
                'technical_specs': self._generate_system_specs(products),
                'applications': self._merge_applications(products),
                'advantages': self._generate_solution_advantages(products, intent_data),
                'implementation_guide': self._generate_implementation_guide(products),
                'support_info': {
                    'technical_support': True,
                    'training_available': True,
                    'warranty': '2年质保',
                    'documentation': 'https://www.jytek.com/support',
                    'contact': {
                        'website': 'https://www.jytek.com',
                        'phone': '021-50475899',
                        'email': 'support@jytek.com'
                    }
                }
            }
            
            return solution_config
            
        except Exception as e:
            logger.error(f"生成解决方案配置失败: {e}")
            return {
                'error': str(e),
                'message': '解决方案生成失败，请联系技术支持'
            }
    
    def _generate_solution_name(self, intent_data: Dict[str, Any], categories: set) -> str:
        """生成解决方案名称"""
        application_scenario = intent_data.get('application_scenario')
        if application_scenario:
            return f"{application_scenario}PXI测控解决方案"
        
        category_names = {
            'data_acquisition': '数据采集',
            'signal_generation': '信号发生',
            'digital_io': '数字控制',
            'rf_microwave': '射频测试',
            'oscilloscope': '信号分析',
            'multimeter': '精密测量'
        }
        
        main_categories = [category_names.get(cat, cat) for cat in list(categories)[:2]]
        return f"{'&'.join(main_categories)}PXI系统方案"
    
    def _generate_solution_description(self, intent_data: Dict[str, Any], 
                                     products: List[Dict[str, Any]]) -> str:
        """生成解决方案描述"""
        description_parts = []
        
        # 应用场景描述
        application_scenario = intent_data.get('application_scenario')
        if application_scenario:
            description_parts.append(f"专为{application_scenario}设计的PXI测控解决方案")
        
        # 技术特点描述
        tech_requirements = intent_data.get('technical_requirements', {})
        if 'channels' in tech_requirements:
            description_parts.append(f"支持{tech_requirements['channels']}通道测量")
        
        if 'frequency' in tech_requirements:
            freq = tech_requirements['frequency']
            description_parts.append(f"频率范围覆盖{freq['value']}{freq['unit']}")
        
        # 产品特色描述
        all_features = []
        for product in products:
            all_features.extend(product.get('features', []))
        
        unique_features = list(set(all_features))[:3]
        if unique_features:
            description_parts.append(f"具备{', '.join(unique_features)}等特色")
        
        if not description_parts:
            description_parts.append("基于简仪科技PXI平台的专业测控解决方案")
        
        return "，".join(description_parts) + "。"
    
    def _recommend_chassis(self, products: List[Dict[str, Any]], 
                          intent_data: Dict[str, Any]) -> Dict[str, Any]:
        """推荐PXI机箱"""
        # 根据模块数量推荐机箱
        module_count = len(products)
        
        if module_count <= 4:
            chassis_type = "4槽紧凑型"
            chassis_model = "JY-PXI-4"
        elif module_count <= 8:
            chassis_type = "8槽标准型"
            chassis_model = "JY-PXI-8"
        else:
            chassis_type = "18槽扩展型"
            chassis_model = "JY-PXI-18"
        
        return {
            'name': f'{chassis_model} PXI机箱',
            'type': chassis_type,
            'slots': module_count,
            'description': f'{chassis_type}PXI机箱，适合{module_count}个模块的系统配置',
            'features': ['标准PXI总线', '高速背板', '散热设计', '电源管理'],
            'price_range': '8000-15000元'
        }
    
    def _recommend_controller(self, products: List[Dict[str, Any]], 
                            intent_data: Dict[str, Any]) -> Dict[str, Any]:
        """推荐PXI控制器"""
        # 根据应用复杂度推荐控制器
        application_scenario = intent_data.get('application_scenario')
        
        if application_scenario in ['航空航天', '通信设备测试', '半导体测试']:
            controller_type = "高性能"
            controller_model = "JY-PXI-8840"
        else:
            controller_type = "标准"
            controller_model = "JY-PXI-8820"
        
        return {
            'name': f'{controller_model} PXI控制器',
            'type': controller_type,
            'description': f'{controller_type}PXI控制器，提供系统控制和数据处理',
            'features': ['Intel处理器', 'Windows系统', '千兆网络', 'USB接口'],
            'specifications': {
                '处理器': 'Intel Core i7',
                '内存': '8GB DDR4',
                '存储': '256GB SSD',
                '网络': '千兆以太网'
            },
            'price_range': '15000-25000元'
        }
    
    def _recommend_software(self, categories: set) -> Dict[str, Any]:
        """推荐软件平台"""
        return {
            'name': 'SeeSharp锐视测控平台',
            'description': '基于.NET的专业测控软件平台',
            'features': ['图形化编程', '实时数据处理', '报表生成', 'API接口'],
            'supported_categories': list(categories),
            'license_type': '商业授权',
            'price_range': '5000-10000元/年'
        }
    
    def _recommend_accessories(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """推荐配件"""
        accessories = []
        
        # 根据产品类型推荐配件
        categories = set(product['category'] for product in products)
        
        if 'data_acquisition' in categories:
            accessories.append({
                'name': '信号调理模块',
                'description': '提供信号放大、滤波和隔离功能',
                'price_range': '2000-5000元'
            })
        
        if 'signal_generation' in categories:
            accessories.append({
                'name': '射频连接器套件',
                'description': '高质量射频连接器和电缆',
                'price_range': '500-1500元'
            })
        
        accessories.append({
            'name': '机架安装套件',
            'description': '标准19英寸机架安装配件',
            'price_range': '800-1200元'
        })
        
        return accessories
    
    def _estimate_total_cost(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """估算总成本"""
        total_min = 0
        total_max = 0
        
        # 计算产品成本
        for product in products:
            price_range = product.get('price_range', '0-0元')
            min_price, max_price = self._parse_price_range(price_range)
            total_min += min_price
            total_max += max_price
        
        # 添加机箱和控制器成本
        total_min += 23000  # 机箱+控制器最低价
        total_max += 40000  # 机箱+控制器最高价
        
        # 添加软件和配件成本
        total_min += 8000   # 软件+配件最低价
        total_max += 16500  # 软件+配件最高价
        
        return {
            'range': f'{total_min}-{total_max}元',
            'currency': 'CNY',
            'includes': ['硬件模块', 'PXI机箱', '控制器', '软件平台', '基础配件'],
            'excludes': ['定制开发', '现场安装', '培训服务'],
            'note': '具体价格请联系销售获取正式报价'
        }
    
    def _parse_price_range(self, price_range: str) -> Tuple[int, int]:
        """解析价格范围"""
        try:
            # 移除"元"字符
            price_str = price_range.replace('元', '')
            
            if '-' in price_str:
                min_str, max_str = price_str.split('-')
                return int(min_str), int(max_str)
            else:
                # 单一价格
                price = int(price_str)
                return price, price
        except:
            return 0, 0
    
    def _generate_system_specs(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """生成系统技术规格"""
        specs = {
            'module_count': len(products),
            'categories': list(set(product['category'] for product in products)),
            'total_channels': 0,
            'max_sample_rate': '未指定',
            'frequency_range': '未指定',
            'accuracy': '未指定'
        }
        
        # 统计总通道数
        for product in products:
            product_specs = product.get('specifications', {})
            if '通道数' in product_specs:
                channels = self._extract_number_from_spec(product_specs['通道数'])
                if channels:
                    specs['total_channels'] += channels
        
        return specs
    
    def _merge_applications(self, products: List[Dict[str, Any]]) -> List[str]:
        """合并产品应用场景"""
        all_applications = []
        for product in products:
            all_applications.extend(product.get('applications', []))
        
        return list(set(all_applications))
    
    def _generate_solution_advantages(self, products: List[Dict[str, Any]], 
                                    intent_data: Dict[str, Any]) -> List[str]:
        """生成解决方案优势"""
        advantages = [
            "简仪科技自主研发，技术先进可靠",
            "模块化设计，灵活配置扩展",
            "完整的软硬件生态支持",
            "专业技术支持和售后服务"
        ]
        
        # 根据产品特色添加优势
        all_features = []
        for product in products:
            all_features.extend(product.get('features', []))
        
        unique_features = set(all_features)
        if '高精度' in unique_features:
            advantages.append("高精度测量，满足严格技术要求")
        
        if '高速' in unique_features or '高速响应' in unique_features:
            advantages.append("高速数据处理，实时性能优异")
        
        return advantages
    
    def _generate_implementation_guide(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """生成实施指南"""
        return {
            'phases': [
                {
                    'phase': '需求确认',
                    'duration': '1-2天',
                    'activities': ['技术需求评审', '系统配置确认', '接口规格确定']
                },
                {
                    'phase': '系统集成',
                    'duration': '3-5天',
                    'activities': ['硬件安装配置', '软件部署调试', '系统联调测试']
                },
                {
                    'phase': '验收培训',
                    'duration': '2-3天',
                    'activities': ['功能验收测试', '操作培训', '文档交付']
                }
            ],
            'total_duration': '1-2周',
            'support_included': ['现场安装', '技术培训', '文档资料', '质保服务']
        }


# 创建全局推荐系统实例
intelligent_recommendation = IntelligentRecommendation()
