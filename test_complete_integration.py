#!/usr/bin/env python3
"""
完整的知识库集成测试
Complete knowledge base integration test
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from models.enhanced_knowledge import enhanced_knowledge_base
from config.jytek_prompts import build_enhanced_prompt
from models.llm_models import model_selector
import json

def test_complete_integration():
    """测试完整的知识库集成流程"""
    print("=" * 80)
    print("🔧 锐视测控平台完整知识库集成测试")
    print("=" * 80)
    
    # 测试问题
    test_question = "PXI数据采集系统如何配置和使用？"
    print(f"\n📝 测试问题: {test_question}")
    
    # 1. 测试知识库搜索
    print("\n🔍 步骤1: 知识库搜索")
    relevant_content = enhanced_knowledge_base.get_relevant_content(test_question, max_docs=3)
    print(f"   知识库内容长度: {len(relevant_content)}")
    if relevant_content:
        print(f"   内容预览: {relevant_content[:200]}...")
    else:
        print("   ❌ 没有找到相关内容")
        return False
    
    # 2. 测试提示词构建
    print("\n🛠️ 步骤2: 提示词构建")
    enhanced_prompt = build_enhanced_prompt(
        question=test_question,
        context_type='company',
        additional_context=f'相关知识库内容：\n{relevant_content}' if relevant_content else ''
    )
    print(f"   提示词长度: {len(enhanced_prompt)}")
    print(f"   提示词包含知识库内容: {'相关知识库内容' in enhanced_prompt}")
    
    # 3. 测试AI问答
    print("\n🤖 步骤3: AI问答测试")
    try:
        response = model_selector.ask_question(
            question=enhanced_prompt,
            options={'temperature': 0.7}
        )
        
        print(f"   AI提供商: {response.get('provider', 'unknown')}")
        print(f"   回答长度: {len(response.get('content', ''))}")
        
        # 检查回答是否包含知识库内容
        answer_content = response.get('content', '')
        knowledge_indicators = [
            'AI+锐视测控平台',
            'MISD',
            '简仪科技',
            'JYTEK',
            '数据采集',
            'PXI'
        ]
        
        found_indicators = [indicator for indicator in knowledge_indicators if indicator in answer_content]
        print(f"   回答包含知识库关键词: {found_indicators}")
        
        if found_indicators:
            print("   ✅ AI回答成功结合了知识库内容")
        else:
            print("   ⚠️ AI回答可能没有很好地结合知识库内容")
        
        print(f"\n📄 AI回答预览:")
        print(f"   {answer_content[:300]}...")
        
    except Exception as e:
        print(f"   ❌ AI问答失败: {e}")
        return False
    
    # 4. 测试文档关联
    print("\n📚 步骤4: 文档关联测试")
    docs = enhanced_knowledge_base.search_documents(test_question, limit=3)
    related_docs = [
        {
            'id': doc.get('id'),
            'filename': doc.get('original_filename', ''),
            'title': doc.get('title', ''),
            'relevance_score': doc.get('relevance_score', 0)
        }
        for doc in docs if doc.get('id')
    ]
    
    print(f"   关联文档数量: {len(related_docs)}")
    for i, doc in enumerate(related_docs):
        print(f"   {i+1}. {doc['filename']} (相关度: {doc['relevance_score']:.3f})")
    
    # 5. 测试完整流程
    print("\n🔄 步骤5: 完整流程验证")
    
    # 检查各个组件是否正常工作
    checks = {
        "知识库内容提取": len(relevant_content) > 0,
        "提示词构建": "重要：请优先基于以下知识库内容" in enhanced_prompt,
        "AI模型响应": 'content' in response and len(response['content']) > 0,
        "文档关联": len(related_docs) > 0,
        "内容结合": len(found_indicators) > 0
    }
    
    print("\n✅ 系统检查结果:")
    all_passed = True
    for check_name, passed in checks.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"   {check_name}: {status}")
        if not passed:
            all_passed = False
    
    # 6. 问题诊断
    if not all_passed:
        print("\n🔧 问题诊断:")
        
        if not checks["知识库内容提取"]:
            print("   - 知识库内容提取失败，检查文档索引和搜索功能")
        
        if not checks["提示词构建"]:
            print("   - 提示词构建有问题，检查jytek_prompts.py")
        
        if not checks["AI模型响应"]:
            print("   - AI模型响应失败，检查模型配置和API密钥")
        
        if not checks["文档关联"]:
            print("   - 文档关联失败，检查搜索算法")
        
        if not checks["内容结合"]:
            print("   - AI没有很好地结合知识库内容，检查提示词设计")
    
    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 所有测试通过！知识库集成工作正常。")
        print("💡 建议：现在可以在前台测试实际的用户问答体验。")
    else:
        print("⚠️ 部分测试失败，需要进一步调试。")
        print("🔍 请根据上述诊断信息进行修复。")
    print("=" * 80)
    
    return all_passed

def test_specific_scenarios():
    """测试特定场景"""
    print("\n🎯 特定场景测试:")
    
    scenarios = [
        {
            "name": "PXI硬件配置",
            "question": "如何选择合适的PXI机箱和控制器？",
            "expected_keywords": ["PXI", "机箱", "控制器"]
        },
        {
            "name": "数据采集编程",
            "question": "用C#编写PXI数据采集程序的步骤是什么？",
            "expected_keywords": ["C#", "数据采集", "编程"]
        },
        {
            "name": "简仪科技产品",
            "question": "简仪科技有哪些主要产品？",
            "expected_keywords": ["简仪科技", "产品", "JYTEK"]
        }
    ]
    
    for scenario in scenarios:
        print(f"\n   📋 场景: {scenario['name']}")
        print(f"   问题: {scenario['question']}")
        
        # 获取知识库内容
        relevant_content = enhanced_knowledge_base.get_relevant_content(scenario['question'], max_docs=2)
        
        if relevant_content:
            # 构建提示词
            enhanced_prompt = build_enhanced_prompt(
                question=scenario['question'],
                context_type='company',
                additional_context=f'相关知识库内容：\n{relevant_content}'
            )
            
            # 测试AI回答
            try:
                response = model_selector.ask_question(enhanced_prompt)
                answer = response.get('content', '')
                
                # 检查关键词
                found_keywords = [kw for kw in scenario['expected_keywords'] if kw in answer]
                
                print(f"   结果: 找到关键词 {found_keywords}")
                print(f"   状态: {'✅ 通过' if found_keywords else '⚠️ 部分通过'}")
                
            except Exception as e:
                print(f"   状态: ❌ 失败 - {e}")
        else:
            print(f"   状态: ❌ 没有找到相关知识库内容")

if __name__ == "__main__":
    success = test_complete_integration()
    
    if success:
        test_specific_scenarios()
    
    print(f"\n🏁 测试完成。")
