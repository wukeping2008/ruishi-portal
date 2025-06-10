"""
Product Routes for Ruishi Control Platform
产品展示和管理路由
"""

from flask import Blueprint, request, jsonify, send_from_directory
import os
import json
from datetime import datetime

product_bp = Blueprint('products', __name__, url_prefix='/api/products')

# 简仪科技产品分类数据
JYTEK_CATEGORIES = {
    "ruishi_platform": {
        "name": "锐视测控平台",
        "description": "基于C#/.NET的开源测控解决方案",
        "products": [
            {
                "id": "seesharp-platform",
                "name": "锐视测控平台",
                "category": "软件平台",
                "description": "集成AI技术的开源测控软件平台，基于Microsoft .NET框架",
                "specifications": {
                    "framework": ".NET Framework",
                    "language": "C#",
                    "ai_integration": "AI Agent内置",
                    "misd_support": "MISD方法支持",
                    "cross_platform": "Windows/Linux"
                },
                "applications": ["自动化测试", "数据采集", "信号处理", "教学科研"],
                "features": [
                    "减少70%编程量",
                    "调试时间缩短至2分钟",
                    "AI智能优化",
                    "开源可定制"
                ]
            },
            {
                "id": "signalpanel",
                "name": "SignalPanel",
                "category": "图形化工具",
                "description": "图形化用户界面工具，简化仪器操作",
                "specifications": {
                    "interface": "图形化界面",
                    "real_time": "实时波形显示",
                    "signal_processing": "内置DSP功能",
                    "export_formats": "多种数据格式"
                },
                "applications": ["信号分析", "波形显示", "数据可视化"]
            },
            {
                "id": "jydm",
                "name": "JYDM设备管理工具",
                "category": "设备管理",
                "description": "设备管理工具，快速识别和管理连接的设备",
                "specifications": {
                    "auto_detection": "自动设备识别",
                    "driver_management": "驱动程序管理",
                    "device_config": "设备配置管理",
                    "diagnostics": "设备诊断功能"
                },
                "applications": ["设备管理", "故障诊断", "系统配置"]
            },
            {
                "id": "seesharptools",
                "name": "SeeSharpTools",
                "category": "开发工具包",
                "description": "丰富的开发工具包，用于快速开发测试应用程序",
                "specifications": {
                    "dsp_functions": "数字信号处理",
                    "plotting": "ScottPlot集成",
                    "fft_support": "傅里叶变换",
                    "filter_design": "滤波器设计"
                },
                "applications": ["应用开发", "信号处理", "数据分析"]
            },
            {
                "id": "ai-agent",
                "name": "AI Agent智能助手",
                "category": "AI工具",
                "description": "智能编程助手，支持代码生成、参数优化和故障诊断",
                "specifications": {
                    "code_generation": "自动代码生成",
                    "parameter_optimization": "智能参数优化",
                    "error_detection": "自动错误检测",
                    "performance_analysis": "性能分析"
                },
                "applications": ["智能编程", "系统优化", "故障诊断", "教学辅助"]
            }
        ]
    },
    "data_acquisition": {
        "name": "数据采集设备",
        "description": "高精度数据采集模块和便携式设备",
        "products": [
            {
                "id": "usb-1601",
                "name": "USB-1601",
                "category": "便携式数据采集",
                "description": "便携式数据采集设备，支持多种传感器，可直接集成到锐视平台",
                "specifications": {
                    "resolution": "16位",
                    "sample_rate": "250 kS/s",
                    "analog_inputs": 16,
                    "digital_io": 8,
                    "interface": "USB 2.0",
                    "power": "USB供电"
                },
                "applications": ["现场测试", "教学实验", "便携式测量", "传感器接口"],
                "features": [
                    "即插即用",
                    "无需外部电源",
                    "锐视平台无缝集成",
                    "教学友好"
                ]
            },
            {
                "id": "pxi-6251",
                "name": "PXI-6251",
                "category": "多功能数据采集",
                "description": "16位分辨率，1.25 MS/s采样率，16路模拟输入",
                "specifications": {
                    "resolution": "16位",
                    "sample_rate": "1.25 MS/s",
                    "analog_inputs": 16,
                    "analog_outputs": 2,
                    "digital_io": 24,
                    "timing_accuracy": "50 ppm"
                },
                "applications": ["自动化测试", "数据记录", "控制系统", "质量检测"]
            },
            {
                "id": "pxi-6289",
                "name": "PXI-6289",
                "category": "高精度数据采集",
                "description": "18位分辨率，625 kS/s采样率，32路模拟输入",
                "specifications": {
                    "resolution": "18位",
                    "sample_rate": "625 kS/s",
                    "analog_inputs": 32,
                    "analog_outputs": 4,
                    "digital_io": 48,
                    "accuracy": "±0.05%"
                },
                "applications": ["精密测量", "传感器测试", "质量控制", "科研应用"]
            }
        ]
    },
    "signal_generation": {
        "name": "信号发生",
        "description": "任意波形和函数信号发生器",
        "products": [
            {
                "id": "pxi-5421",
                "name": "PXI-5421",
                "category": "任意波形发生器",
                "description": "16位分辨率，100 MS/s更新率，任意波形生成",
                "specifications": {
                    "resolution": "16位",
                    "update_rate": "100 MS/s",
                    "memory": "32 MB",
                    "frequency_range": "DC to 43 MHz",
                    "amplitude": "±5 V"
                },
                "applications": ["信号仿真", "器件测试", "系统验证"]
            },
            {
                "id": "pxi-5422",
                "name": "PXI-5422",
                "category": "高速任意波形发生器",
                "description": "16位分辨率，200 MS/s更新率，高速波形生成",
                "specifications": {
                    "resolution": "16位",
                    "update_rate": "200 MS/s",
                    "memory": "64 MB",
                    "frequency_range": "DC to 80 MHz",
                    "amplitude": "±5 V"
                },
                "applications": ["高速信号测试", "雷达仿真", "通信测试"]
            }
        ]
    },
    "digital_io": {
        "name": "数字I/O",
        "description": "高速数字输入输出模块",
        "products": [
            {
                "id": "pxi-6552",
                "name": "PXI-6552",
                "category": "高速数字I/O",
                "description": "100 MHz时钟，32通道数字I/O",
                "specifications": {
                    "channels": 32,
                    "clock_rate": "100 MHz",
                    "voltage_levels": "1.8V, 2.5V, 3.3V, 5.0V",
                    "pattern_memory": "512 MB",
                    "timing_resolution": "10 ns"
                },
                "applications": ["数字电路测试", "协议测试", "FPGA验证"]
            },
            {
                "id": "pxi-6570",
                "name": "PXI-6570",
                "category": "数字波形仪器",
                "description": "1 GHz时钟，32通道数字波形发生器/分析仪",
                "specifications": {
                    "channels": 32,
                    "clock_rate": "1 GHz",
                    "voltage_levels": "可编程",
                    "pattern_memory": "2 GB",
                    "timing_resolution": "1 ns"
                },
                "applications": ["高速数字测试", "时序分析", "协议验证"]
            }
        ]
    },
    "digital_multimeter": {
        "name": "数字万用表",
        "description": "高精度数字万用表模块",
        "products": [
            {
                "id": "pxi-4071",
                "name": "PXI-4071",
                "category": "7.5位数字万用表",
                "description": "7.5位分辨率，高精度数字万用表",
                "specifications": {
                    "resolution": "7.5位",
                    "dc_voltage_accuracy": "±0.0035%",
                    "ac_voltage_accuracy": "±0.05%",
                    "resistance_range": "100 Ω to 100 MΩ",
                    "current_range": "1 μA to 3 A"
                },
                "applications": ["精密测量", "校准", "质量控制"]
            },
            {
                "id": "pxi-4072",
                "name": "PXI-4072",
                "category": "6.5位数字万用表",
                "description": "6.5位分辨率，高速数字万用表",
                "specifications": {
                    "resolution": "6.5位",
                    "dc_voltage_accuracy": "±0.0055%",
                    "ac_voltage_accuracy": "±0.06%",
                    "resistance_range": "100 Ω to 100 MΩ",
                    "measurement_rate": "3000 读数/秒"
                },
                "applications": ["生产测试", "功能测试", "参数测量"]
            }
        ]
    },
    "oscilloscope": {
        "name": "示波器",
        "description": "高性能数字示波器模块",
        "products": [
            {
                "id": "pxi-5122",
                "name": "PXI-5122",
                "category": "高速数字化仪",
                "description": "14位分辨率，100 MS/s采样率，双通道示波器",
                "specifications": {
                    "resolution": "14位",
                    "sample_rate": "100 MS/s",
                    "channels": 2,
                    "bandwidth": "100 MHz",
                    "memory": "32 MS/通道"
                },
                "applications": ["波形分析", "信号捕获", "瞬态测量"]
            },
            {
                "id": "pxi-5124",
                "name": "PXI-5124",
                "category": "高分辨率数字化仪",
                "description": "12位分辨率，200 MS/s采样率，双通道示波器",
                "specifications": {
                    "resolution": "12位",
                    "sample_rate": "200 MS/s",
                    "channels": 2,
                    "bandwidth": "200 MHz",
                    "memory": "64 MS/通道"
                },
                "applications": ["高速信号分析", "频域分析", "协议解码"]
            }
        ]
    },
    "education_kits": {
        "name": "教育套件",
        "description": "专为教学和科研设计的实验套件",
        "products": [
            {
                "id": "seesharplab-sensor",
                "name": "SeeSharpLab-Sensor",
                "category": "传感器实验套件",
                "description": "传感器实验套件，与锐视平台配合使用，支持AI故障诊断",
                "specifications": {
                    "sensors": "温度、湿度、压力、光照等",
                    "interface": "USB连接",
                    "software": "锐视测控平台教育版",
                    "ai_features": "AI故障诊断"
                },
                "applications": ["传感器教学", "数据采集实验", "AI应用学习", "工程实践"]
            },
            {
                "id": "usb-1601-edu",
                "name": "USB-1601教学版",
                "category": "教学数据采集",
                "description": "专门为教学优化的便携式数据采集设备",
                "specifications": {
                    "resolution": "16位",
                    "sample_rate": "250 kS/s",
                    "analog_inputs": 16,
                    "educational_software": "教学专用软件",
                    "tutorials": "完整教程资源"
                },
                "applications": ["工程教育", "实验教学", "项目实践", "技能培训"]
            },
            {
                "id": "pxi-edu-system",
                "name": "PXI教学系统",
                "category": "完整教学平台",
                "description": "完整的PXI教学平台，包含机箱、控制器和多种功能模块",
                "specifications": {
                    "chassis": "8槽PXI机箱",
                    "controller": "嵌入式控制器",
                    "modules": "数据采集、信号发生、数字I/O",
                    "curriculum": "完整课程体系"
                },
                "applications": ["高等教育", "职业培训", "科研项目", "系统集成教学"]
            }
        ]
    },
    "distributed_acquisition": {
        "name": "分布式采集",
        "description": "分布式数据采集系统",
        "products": [
            {
                "id": "cdaq-9178",
                "name": "cDAQ-9178",
                "category": "CompactDAQ机箱",
                "description": "8槽CompactDAQ机箱，USB接口",
                "specifications": {
                    "slots": 8,
                    "interface": "USB 2.0",
                    "power_supply": "外部电源",
                    "operating_temp": "-40°C to 70°C",
                    "dimensions": "212 x 106 x 86 mm"
                },
                "applications": ["分布式测量", "便携式测试", "现场数据采集"]
            },
            {
                "id": "cdaq-9188",
                "name": "cDAQ-9188",
                "category": "以太网CompactDAQ",
                "description": "8槽CompactDAQ机箱，以太网接口",
                "specifications": {
                    "slots": 8,
                    "interface": "以太网",
                    "power_supply": "PoE+或外部电源",
                    "operating_temp": "-40°C to 70°C",
                    "sync_accuracy": "±500 ns"
                },
                "applications": ["远程监测", "网络化测量", "多点同步采集"]
            },
            {
                "id": "ni-9205",
                "name": "NI-9205",
                "category": "模拟输入模块",
                "description": "32通道，±200 mV到±10 V，16位分辨率",
                "specifications": {
                    "channels": 32,
                    "resolution": "16位",
                    "input_range": "±200 mV to ±10 V",
                    "sample_rate": "250 kS/s",
                    "isolation": "2300 Vrms"
                },
                "applications": ["多通道数据采集", "传感器接口", "工业监测"]
            }
        ]
    }
}

@product_bp.route('/categories')
def get_categories():
    """获取产品分类"""
    return jsonify({
        "success": True,
        "categories": JYTEK_CATEGORIES
    })

@product_bp.route('/category/<category_id>')
def get_category_products(category_id):
    """获取指定分类的产品"""
    if category_id not in JYTEK_CATEGORIES:
        return jsonify({
            "success": False,
            "error": "分类不存在"
        }), 404
    
    category = JYTEK_CATEGORIES[category_id]
    return jsonify({
        "success": True,
        "category": category
    })

@product_bp.route('/product/<product_id>')
def get_product_detail(product_id):
    """获取产品详细信息"""
    # 在所有分类中查找产品
    for category_id, category in JYTEK_CATEGORIES.items():
        for product in category["products"]:
            if product["id"] == product_id:
                return jsonify({
                    "success": True,
                    "product": product,
                    "category": {
                        "id": category_id,
                        "name": category["name"]
                    }
                })
    
    return jsonify({
        "success": False,
        "error": "产品不存在"
    }), 404

@product_bp.route('/search')
def search_products():
    """搜索产品"""
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({
            "success": False,
            "error": "搜索关键词不能为空"
        })
    
    results = []
    for category_id, category in JYTEK_CATEGORIES.items():
        for product in category["products"]:
            # 在产品名称、描述、应用中搜索
            searchable_text = (
                product["name"] + " " + 
                product["description"] + " " + 
                " ".join(product["applications"])
            ).lower()
            
            if query in searchable_text:
                product_result = product.copy()
                product_result["category"] = {
                    "id": category_id,
                    "name": category["name"]
                }
                results.append(product_result)
    
    return jsonify({
        "success": True,
        "query": query,
        "results": results,
        "count": len(results)
    })

@product_bp.route('/compare')
def compare_products():
    """产品对比"""
    product_ids = request.args.getlist('ids')
    if len(product_ids) < 2:
        return jsonify({
            "success": False,
            "error": "至少需要选择2个产品进行对比"
        })
    
    products = []
    for product_id in product_ids:
        # 查找产品
        for category_id, category in JYTEK_CATEGORIES.items():
            for product in category["products"]:
                if product["id"] == product_id:
                    product_with_category = product.copy()
                    product_with_category["category"] = {
                        "id": category_id,
                        "name": category["name"]
                    }
                    products.append(product_with_category)
                    break
    
    if len(products) != len(product_ids):
        return jsonify({
            "success": False,
            "error": "部分产品不存在"
        })
    
    return jsonify({
        "success": True,
        "products": products,
        "comparison_date": datetime.now().isoformat()
    })

@product_bp.route('/recommendations')
def get_recommendations():
    """获取产品推荐"""
    application = request.args.get('application', '')
    budget = request.args.get('budget', '')
    
    # 基于应用场景推荐产品
    recommendations = []
    
    if application:
        for category_id, category in JYTEK_CATEGORIES.items():
            for product in category["products"]:
                if any(app.lower() in application.lower() for app in product["applications"]):
                    recommendation = product.copy()
                    recommendation["category"] = {
                        "id": category_id,
                        "name": category["name"]
                    }
                    recommendation["match_reason"] = f"适用于{application}应用场景"
                    recommendations.append(recommendation)
    
    # 如果没有基于应用的推荐，返回热门产品
    if not recommendations:
        # 返回每个分类的第一个产品作为推荐
        for category_id, category in JYTEK_CATEGORIES.items():
            if category["products"]:
                product = category["products"][0].copy()
                product["category"] = {
                    "id": category_id,
                    "name": category["name"]
                }
                product["match_reason"] = "热门产品推荐"
                recommendations.append(product)
    
    return jsonify({
        "success": True,
        "recommendations": recommendations[:6],  # 最多返回6个推荐
        "criteria": {
            "application": application,
            "budget": budget
        }
    })

@product_bp.route('/solution-builder')
def solution_builder():
    """解决方案构建器"""
    requirements = {
        "measurement_type": request.args.get('measurement_type', ''),
        "channel_count": request.args.get('channel_count', ''),
        "frequency_range": request.args.get('frequency_range', ''),
        "accuracy_requirement": request.args.get('accuracy_requirement', ''),
        "budget_range": request.args.get('budget_range', '')
    }
    
    # 基于需求推荐产品组合
    solution = {
        "platform": {
            "name": "锐视测控平台",
            "description": "简仪科技自主开发的开源测控软件平台",
            "reason": "提供完整的软件开发环境和AI增强功能"
        },
        "chassis": {
            "name": "JYTEK-PXI-1042Q",
            "description": "简仪科技8槽PXI机箱，国产自主可控",
            "reason": "满足基本扩展需求，完全自主设计"
        },
        "controller": {
            "name": "JYTEK-PXI-8108",
            "description": "简仪科技嵌入式控制器，2.5 GHz双核处理器",
            "reason": "提供充足的计算能力，国产自主可控"
        },
        "modules": []
    }
    
    # 根据测量类型推荐模块
    measurement_type = requirements["measurement_type"].lower()
    
    if "数据采集" in measurement_type or "data" in measurement_type:
        if "便携" in measurement_type or "教学" in measurement_type:
            solution["modules"].append({
                "name": "USB-1601",
                "type": "便携式数据采集",
                "reason": "便携式设计，适合现场测试和教学"
            })
        else:
            solution["modules"].append({
                "name": "PXI-6251",
                "type": "数据采集",
                "reason": "高精度多功能数据采集"
            })
    
    if "信号发生" in measurement_type or "signal" in measurement_type:
        solution["modules"].append({
            "name": "PXI-5421",
            "type": "信号发生",
            "reason": "任意波形信号生成"
        })
    
    if "数字万用表" in measurement_type or "dmm" in measurement_type:
        solution["modules"].append({
            "name": "PXI-4071",
            "type": "数字万用表",
            "reason": "高精度电压电流测量"
        })
    
    if "示波器" in measurement_type or "scope" in measurement_type:
        solution["modules"].append({
            "name": "PXI-5122",
            "type": "示波器",
            "reason": "波形捕获和分析"
        })
    
    if "分布式" in measurement_type or "distributed" in measurement_type:
        solution["modules"].append({
            "name": "cDAQ-9178",
            "type": "分布式采集",
            "reason": "分布式数据采集系统"
        })
    
    if "教学" in measurement_type or "教育" in measurement_type:
        solution["modules"].append({
            "name": "SeeSharpLab-Sensor",
            "type": "教育套件",
            "reason": "专为教学设计的传感器实验套件"
        })
    
    # 如果没有指定测量类型，推荐基础配置
    if not solution["modules"]:
        solution["modules"].extend([
            {
                "name": "USB-1601",
                "type": "数据采集",
                "reason": "通用便携式数据采集模块"
            },
            {
                "name": "AI Agent",
                "type": "AI工具",
                "reason": "智能编程助手，提升开发效率"
            }
        ])
    
    return jsonify({
        "success": True,
        "solution": solution,
        "requirements": requirements,
        "estimated_cost": "请联系销售获取报价",
        "jytek_advantages": [
            "国产自主可控",
            "开源生态系统", 
            "AI增强功能",
            "完整技术支持",
            "MISD方法简化开发"
        ],
        "contact_info": {
            "website": "https://www.jytek.com",
            "message": "详细配置和报价请访问简仪科技官网"
        }
    })

@product_bp.route('/jytek-features')
def get_jytek_features():
    """获取简仪科技特色功能"""
    return jsonify({
        "success": True,
        "features": {
            "ai_integration": {
                "name": "AI技术集成",
                "description": "内置AI Agent，支持智能代码生成和参数优化",
                "benefits": ["减少70%编程量", "调试时间缩短至2分钟", "智能错误检测"]
            },
            "misd_method": {
                "name": "MISD方法",
                "description": "模块仪器软件词典方法，简化硬件集成",
                "benefits": ["统一API接口", "自动代码生成", "简化系统集成"]
            },
            "open_source": {
                "name": "开源生态",
                "description": "完全开源的测控解决方案",
                "benefits": ["源码透明", "自由定制", "社区支持"]
            },
            "autonomous_control": {
                "name": "自主可控",
                "description": "国产自主研发，完全可控的技术栈",
                "benefits": ["技术自主", "安全可靠", "本土支持"]
            },
            "cross_platform": {
                "name": "跨平台支持",
                "description": "支持Windows和Linux操作系统",
                "benefits": ["平台灵活", "部署便捷", "兼容性强"]
            }
        }
    })
