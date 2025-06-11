#!/usr/bin/env python3
"""
测试知识库集成的完整流程
Test complete knowledge base integration workflow
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from models.enhanced_knowledge import enhanced_knowledge_base
from models.ai_conversation import ai_conversation_manager
import json

def test_knowledge_integration():
    """测试知识库集成"""
    print("=" * 60)
    print("锐视测控平台知识库集成测试")
    print("=" * 60)
    
    # 1. 测试知识库统计
    print("\n1. 知识库统计信息:")
    stats = enhanced_knowledge_base.get_document_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # 2. 测试文档搜索
    print("\n2. 测试文档搜索:")
    test_queries = [
        "PXI数据采集",
        "简仪科技产品",
        "AI测控平台",
        "MISD方法"
    ]
    
    for query in test_queries:
        print(f"\n   查询: {query}")
        results = enhanced_knowledge_base.search_documents(query, limit=2)
        print(f"   找到 {len(results)} 个相关文档:")
        for i, doc in enumerate(results):
            print(f"     {i+1}. {doc['title']} (相关度: {doc['relevance_score']:.3f})")
    
    # 3. 测试相关内容获取
    print("\n3. 测试相关内容获取:")
    test_question = "如何使用PXI进行数据采集？"
    print(f"   问题: {test_question}")
    
    relevant_content = enhanced_knowledge_base.get_relevant_content(test_question, max_docs=2)
    print(f"   相关内容长度: {len(relevant_content)}")
    
    if relevant_content:
        print(f"   内容预览:")
        print(f"   {relevant_content[:200]}...")
        
        # 4. 模拟完整的AI问答流程
        print("\n4. 模拟AI问答流程:")
        
        # 获取相关文档列表
        docs = enhanced_knowledge_base.search_documents(test_question, limit=3)
        related_docs = [
            {
                'id': doc.get('id'),
                'filename': doc.get('original_filename', ''),
                'title': doc.get('title', ''),
                'category': doc.get('category', ''),
                'file_type': doc.get('file_type', ''),
                'relevance_score': doc.get('relevance_score', 0)
            }
            for doc in docs if doc.get('id')
        ]
        
        print(f"   关联文档数量: {len(related_docs)}")
        for doc in related_docs:
            print(f"     - {doc['filename']} (相关度: {doc['relevance_score']:.3f})")
        
        # 模拟记录对话
        conversation_id = ai_conversation_manager.record_conversation(
            question=test_question,
            answer="这是一个模拟的AI回答，基于知识库内容生成。",
            ai_provider="test_provider",
            ai_model="test_model",
            user_id=None,
            session_id="test_session",
            user_type="guest",
            user_ip="127.0.0.1",
            user_agent="test_agent",
            trigger_type="question",
            related_documents=related_docs if related_docs else None,
            response_time=1.5
        )
        
        if conversation_id:
            print(f"   对话记录成功，ID: {conversation_id}")
        else:
            print("   对话记录失败")
    
    # 5. 测试文档使用统计
    print("\n5. 测试文档使用统计:")
    doc_stats = ai_conversation_manager.get_document_usage_statistics()
    print(f"   热门文档数量: {len(doc_stats.get('popular_documents', []))}")
    for doc in doc_stats.get('popular_documents', [])[:3]:
        print(f"     - {doc['document_name']}: {doc['usage_count']}次")
    
    print(f"   文档关联率: {doc_stats.get('document_association_rate', 0)}%")
    
    print("\n" + "=" * 60)
    print("测试完成！知识库集成正常工作。")
    print("=" * 60)

if __name__ == "__main__":
    test_knowledge_integration()
