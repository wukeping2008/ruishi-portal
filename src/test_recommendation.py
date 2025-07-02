#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_recommendation_system():
    """测试推荐系统功能"""
    base_url = "http://localhost:8083"
    
    print("=" * 50)
    print("测试AI智能推荐系统")
    print("=" * 50)
    
    # 测试1: 健康检查
    print("\n1. 测试健康检查...")
    try:
        response = requests.get(f"{base_url}/api/recommendation/health")
        if response.status_code == 200:
            print("✓ 健康检查通过")
            data = response.json()
            print(f"  - 数据库状态: {data['data']['database']}")
            print(f"  - 推荐引擎状态: {data['data']['recommendation_engine']}")
            print(f"  - 产品模式数量: {data['data']['product_patterns']}")
            print(f"  - 应用场景数量: {data['data']['application_scenarios']}")
        else:
            print(f"✗ 健康检查失败: {response.status_code}")
            return
    except Exception as e:
        print(f"✗ 健康检查异常: {e}")
        return
    
    # 测试2: 获取产品类别
    print("\n2. 测试获取产品类别...")
    try:
        response = requests.get(f"{base_url}/api/recommendation/categories")
        if response.status_code == 200:
            print("✓ 产品类别获取成功")
            data = response.json()
            print(f"  - 总类别数: {data['data']['total_categories']}")
            categories = list(data['data']['categories'].keys())
            print(f"  - 类别列表: {', '.join(categories)}")
        else:
            print(f"✗ 产品类别获取失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 产品类别获取异常: {e}")
    
    # 测试3: 用户意图分析
    print("\n3. 测试用户意图分析...")
    try:
        test_data = {
            "question": "我需要一个数据采集系统来监控温度和压力传感器",
            "context": {}
        }
        
        response = requests.post(
            f"{base_url}/api/recommendation/analyze",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print("✓ 用户意图分析成功")
            data = response.json()
            intent_data = data['data']
            print(f"  - 置信度: {intent_data.get('confidence_score', 0):.2f}")
            print(f"  - 检测到的类别: {intent_data.get('detected_categories', [])}")
            print(f"  - 关键词: {intent_data.get('extracted_keywords', [])}")
            
            # 保存意图数据用于下一步测试
            global saved_intent_data
            saved_intent_data = intent_data
        else:
            print(f"✗ 用户意图分析失败: {response.status_code}")
            print(f"  响应内容: {response.text}")
            return
    except Exception as e:
        print(f"✗ 用户意图分析异常: {e}")
        return
    
    # 测试4: 产品推荐
    print("\n4. 测试产品推荐...")
    try:
        test_data = {
            "intent_data": saved_intent_data,
            "limit": 3
        }
        
        response = requests.post(
            f"{base_url}/api/recommendation/products",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print("✓ 产品推荐成功")
            data = response.json()
            recommendations = data['data']['recommendations']
            print(f"  - 推荐产品数量: {len(recommendations)}")
            
            for i, product in enumerate(recommendations[:3], 1):
                print(f"  {i}. {product.get('name', 'Unknown')} (评分: {product.get('recommendation_score', 0):.2f})")
                print(f"     类别: {product.get('category', 'Unknown')}")
                print(f"     匹配原因: {product.get('match_reason', 'N/A')}")
            
            # 保存推荐数据用于下一步测试
            global saved_recommendations
            saved_recommendations = recommendations
        else:
            print(f"✗ 产品推荐失败: {response.status_code}")
            print(f"  响应内容: {response.text}")
            return
    except Exception as e:
        print(f"✗ 产品推荐异常: {e}")
        return
    
    # 测试5: 完整推荐流程
    print("\n5. 测试完整推荐流程...")
    try:
        test_data = {
            "question": "我需要测试射频信号的设备",
            "context": {},
            "product_limit": 2
        }
        
        response = requests.post(
            f"{base_url}/api/recommendation/complete",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print("✓ 完整推荐流程成功")
            data = response.json()
            summary = data['data']['summary']
            print(f"  - 置信度: {summary['confidence_score']:.2f}")
            print(f"  - 检测类别数: {summary['detected_categories']}")
            print(f"  - 推荐产品数: {summary['recommended_products']}")
            print(f"  - 有解决方案: {summary['has_solution']}")
        else:
            print(f"✗ 完整推荐流程失败: {response.status_code}")
            print(f"  响应内容: {response.text}")
    except Exception as e:
        print(f"✗ 完整推荐流程异常: {e}")
    
    # 测试6: 统计信息
    print("\n6. 测试统计信息...")
    try:
        response = requests.get(f"{base_url}/api/recommendation/stats")
        if response.status_code == 200:
            print("✓ 统计信息获取成功")
            data = response.json()
            stats = data['data']
            print(f"  - 缓存问题数: {stats['cache_performance']['total_cached_questions']}")
            print(f"  - 缓存命中数: {stats['cache_performance']['total_cache_hits']}")
            print(f"  - 用户会话数: {stats['user_engagement']['unique_sessions']}")
            print(f"  - 产品评分数: {stats['product_feedback']['total_ratings']}")
        else:
            print(f"✗ 统计信息获取失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 统计信息获取异常: {e}")
    
    print("\n" + "=" * 50)
    print("推荐系统测试完成")
    print("=" * 50)

if __name__ == '__main__':
    test_recommendation_system()
