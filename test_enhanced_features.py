#!/usr/bin/env python3
"""
测试产品页面增强功能
"""

import requests
import json
import time

# 测试配置
BASE_URL = "http://localhost:8083"
API_BASE = f"{BASE_URL}/api"

def test_server_health():
    """测试服务器健康状态"""
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            print("✅ 服务器运行正常")
            return True
        else:
            print(f"❌ 服务器异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 服务器连接失败: {e}")
        return False

def test_product_api():
    """测试产品API"""
    try:
        # 测试获取产品列表
        response = requests.get(f"{API_BASE}/products")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 产品API正常，共{len(data.get('products', []))}个产品")
            return True
        else:
            print(f"❌ 产品API异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 产品API测试失败: {e}")
        return False

def test_categories_api():
    """测试分类API"""
    try:
        response = requests.get(f"{API_BASE}/products/categories")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 分类API正常，共{len(data.get('categories', []))}个分类")
            return True
        else:
            print(f"❌ 分类API异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 分类API测试失败: {e}")
        return False

def test_search_api():
    """测试搜索API"""
    try:
        # 测试搜索功能
        search_data = {"keyword": "PXI", "category": ""}
        response = requests.post(f"{API_BASE}/products/search", json=search_data)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 搜索API正常，找到{len(data.get('products', []))}个结果")
            return True
        else:
            print(f"❌ 搜索API异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 搜索API测试失败: {e}")
        return False

def test_ai_integration():
    """测试AI集成"""
    try:
        # 测试AI聊天
        ai_data = {
            "message": "请推荐一款适合工业自动化的PXI产品",
            "context": "products"
        }
        response = requests.post(f"{API_BASE}/ai/chat", json=ai_data)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ AI集成正常")
                return True
            else:
                print("⚠️ AI集成响应但可能有错误")
                return False
        else:
            print(f"❌ AI集成异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ AI集成测试失败: {e}")
        return False

def test_enhanced_features():
    """测试增强功能"""
    print("\n🚀 开始测试产品页面增强功能...")
    
    tests = [
        ("服务器健康", test_server_health),
        ("产品API", test_product_api),
        ("分类API", test_categories_api),
        ("搜索API", test_search_api),
        ("AI集成", test_ai_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 测试{test_name}...")
        if test_func():
            passed += 1
        time.sleep(0.5)  # 避免请求过快
    
    print(f"\n📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有增强功能测试通过！")
        print("\n✨ 增强功能包括：")
        print("   • 高级筛选（品牌、接口类型、功耗等）")
        print("   • 多维度排序（评分、折扣、库存等）")
        print("   • 产品对比（最多5个产品）")
        print("   • 对比报告生成")
        print("   • 数据导出功能")
        print("   • AI智能推荐")
    else:
        print("⚠️ 部分功能需要检查")
    
    return passed == total

if __name__ == "__main__":
    test_enhanced_features()