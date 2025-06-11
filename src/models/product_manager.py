"""
简仪科技产品管理模块
处理产品信息、规格、价格等数据
"""

import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime

class ProductManager:
    def __init__(self):
        self.products_data = {}
        self.categories = {
            'GPS': 'GPS同步模块',
            'Controller Accessory': '控制器配件',
            'PXI/PXIe bus expansion': 'PXI/PXIe总线扩展',
            'Digitizer Accessory': '数字化仪配件',
            'PXIe Transceiver': 'PXIe收发器',
            'PXIe AWG': 'PXIe任意波形发生器',
            'PXIe Digitizers': 'PXIe数字化仪',
            'PCIe Digitizers': 'PCIe数字化仪',
            'Software': '软件',
            'USB DAQ': 'USB数据采集',
            'PXIe Disk Array': 'PXIe磁盘阵列',
            'TXI Chassis': 'TXI机箱',
            'PXIe DAQ': 'PXIe数据采集',
            'DAQ Accessories': '数据采集配件',
            'PXIe Controllers': 'PXIe控制器',
            'PCIe DAQ': 'PCIe数据采集',
            'PXIe Chassis': 'PXIe机箱',
            'PXIe DIO': 'PXIe数字输入输出',
            'PCIe DIO': 'PCIe数字输入输出',
            'PCIe AWG': 'PCIe任意波形发生器',
            'USB AWG': 'USB任意波形发生器',
            'Serial': '串口通信',
            'PXIe Accessory': 'PXIe配件',
            'PXI Accessory': 'PXI配件',
            'DDA': '分布式数据采集',
            'PXIe DSA': 'PXIe动态信号分析',
            'PCIe DSA': 'PCIe动态信号分析',
            'PXIe Switch': 'PXIe开关',
            'SW Accessories': '软件配件',
            'PXIe DMM': 'PXIe数字万用表',
            'DMM Accessories': '数字万用表配件',
            'Chassis Accessory': '机箱配件'
        }
        self.load_product_data()
    
    def load_product_data(self):
        """加载产品数据"""
        # 尝试加载示例数据
        sample_data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_products.json')
        if os.path.exists(sample_data_path):
            try:
                with open(sample_data_path, 'r', encoding='utf-8') as f:
                    self.products_data = json.load(f)
                print(f"成功加载示例产品数据: {len(self.products_data.get('products', []))} 个产品")
                return
            except Exception as e:
                print(f"加载示例数据失败: {e}")
        
        # 如果示例数据加载失败，创建基础结构
        self.products_data = {
            'products': [],
            'specifications': {},
            'controllers': {},
            'chassis': {},
            'categories': self.categories
        }
    
    def add_product_from_excel_data(self, product_data: Dict):
        """从Excel数据添加产品"""
        try:
            product = {
                'id': self.generate_product_id(product_data.get('PN', '')),
                'name': product_data.get('Product,\nSpecs,\nManual', ''),
                'part_number': product_data.get('PN', ''),
                'price': float(product_data.get('Unit Price (Pre-Tax)', 0)),
                'description': product_data.get('Description', ''),
                'category': product_data.get('Category', ''),
                'category_cn': self.categories.get(product_data.get('Category', ''), ''),
                'cable': product_data.get('Cable', ''),
                'terminal_block': product_data.get('Terminal Block', ''),
                'update_date': product_data.get('Update Date', ''),
                'notes': product_data.get('Notes', ''),
                'stock_status': product_data.get('截止昨日库存情况', ''),
                'delivery_period': product_data.get('供货周期\n(月)', ''),
                'specifications': {},
                'manual_url': '',
                'video_url': '',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            # 提取产品链接
            if '[object Object]' in product.get('name', ''):
                # 这里需要解析实际的产品链接
                product['manual_url'] = self.extract_product_url(product['name'])
            
            self.products_data['products'].append(product)
            return product
        except Exception as e:
            print(f"添加产品数据时出错: {e}")
            return None
    
    def generate_product_id(self, part_number: str) -> str:
        """生成产品ID"""
        if part_number:
            return part_number.replace('-', '_').replace(' ', '_')
        return f"product_{len(self.products_data.get('products', []))}"
    
    def extract_product_url(self, product_name: str) -> str:
        """提取产品URL"""
        # 这里需要解析Excel中的链接格式
        # 暂时返回空字符串，实际使用时需要解析
        return ""
    
    def get_products_by_category(self, category: str) -> List[Dict]:
        """根据分类获取产品"""
        return [p for p in self.products_data.get('products', []) 
                if p.get('category') == category]
    
    def search_products(self, keyword: str, category: str = None) -> List[Dict]:
        """搜索产品"""
        products = self.products_data.get('products', [])
        
        if category:
            products = [p for p in products if p.get('category') == category]
        
        if keyword:
            keyword = keyword.lower()
            products = [p for p in products if 
                       keyword in p.get('name', '').lower() or
                       keyword in p.get('description', '').lower() or
                       keyword in p.get('part_number', '').lower()]
        
        return products
    
    def get_product_by_id(self, product_id: str) -> Optional[Dict]:
        """根据ID获取产品"""
        for product in self.products_data.get('products', []):
            if product.get('id') == product_id:
                return product
        return None
    
    def get_categories_stats(self) -> Dict:
        """获取分类统计"""
        stats = {}
        for product in self.products_data.get('products', []):
            category = product.get('category', 'unknown')
            category_cn = self.categories.get(category, category)
            if category_cn not in stats:
                stats[category_cn] = {
                    'count': 0,
                    'category_en': category,
                    'products': []
                }
            stats[category_cn]['count'] += 1
            stats[category_cn]['products'].append(product['id'])
        
        return stats
    
    def get_price_range_stats(self) -> Dict:
        """获取价格区间统计"""
        ranges = {
            '0-1000': {'min': 0, 'max': 1000, 'count': 0},
            '1000-5000': {'min': 1000, 'max': 5000, 'count': 0},
            '5000-10000': {'min': 5000, 'max': 10000, 'count': 0},
            '10000-50000': {'min': 10000, 'max': 50000, 'count': 0},
            '50000+': {'min': 50000, 'max': float('inf'), 'count': 0}
        }
        
        for product in self.products_data.get('products', []):
            price = product.get('price', 0)
            for range_name, range_info in ranges.items():
                if range_info['min'] <= price < range_info['max']:
                    range_info['count'] += 1
                    break
        
        return ranges
    
    def add_product_specification(self, product_id: str, spec_data: Dict):
        """添加产品规格"""
        if product_id not in self.products_data['specifications']:
            self.products_data['specifications'][product_id] = {}
        
        self.products_data['specifications'][product_id].update(spec_data)
    
    def get_product_specification(self, product_id: str) -> Dict:
        """获取产品规格"""
        return self.products_data['specifications'].get(product_id, {})
    
    def generate_ai_knowledge_base(self) -> Dict:
        """生成AI知识库"""
        knowledge_base = {
            'company_info': {
                'name': '简仪科技',
                'name_en': 'JYTEK',
                'description': '专业的测试测量解决方案提供商',
                'main_products': ['PXI系统', '数据采集卡', '任意波形发生器', '数字化仪', '控制器'],
                'technical_fields': ['PXI/PXIe', '数据采集', '信号生成', '自动化测试']
            },
            'product_categories': self.get_categories_stats(),
            'products_summary': {
                'total_count': len(self.products_data.get('products', [])),
                'categories_count': len(self.categories),
                'price_ranges': self.get_price_range_stats()
            },
            'common_questions': [
                {
                    'question': 'PXI和PXIe有什么区别？',
                    'answer': 'PXI是基于CompactPCI的模块化仪器标准，PXIe是PXI的增强版本，采用PCIe技术，提供更高的带宽和性能。',
                    'related_products': ['PXIe Controllers', 'PXIe Chassis', 'PXIe DAQ']
                },
                {
                    'question': '数据采集卡的采样率如何选择？',
                    'answer': '采样率应至少是信号最高频率的2倍（奈奎斯特定理）。对于高精度测量，建议选择更高的采样率。',
                    'related_products': ['PXIe DAQ', 'PCIe DAQ', 'USB DAQ']
                },
                {
                    'question': '如何选择合适的机箱？',
                    'answer': '根据模块数量选择槽位数，根据带宽需求选择Gen2或Gen3，根据功耗选择电源规格。',
                    'related_products': ['PXIe Chassis']
                }
            ],
            'technical_specs': self.products_data['specifications'],
            'last_updated': datetime.now().isoformat()
        }
        
        return knowledge_base
    
    def save_data(self, filepath: str = None):
        """保存产品数据"""
        if not filepath:
            filepath = 'data/products.json'
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.products_data, f, ensure_ascii=False, indent=2)
    
    def load_data(self, filepath: str = None):
        """加载产品数据"""
        if not filepath:
            filepath = 'data/products.json'
        
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                self.products_data = json.load(f)

# 全局产品管理器实例
product_manager = ProductManager()
