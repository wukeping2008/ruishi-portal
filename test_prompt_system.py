#!/usr/bin/env python3
"""
提示词优化系统测试脚本
Test script for the Prompt Optimization System
"""

import sys
import os
import json
import asyncio
from datetime import datetime

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.prompt_system import prompt_system_manager

def test_prompt_system():
    """测试提示词系统的各个功能"""
    
    print("🧠 提示词优化系统测试")
    print("=" * 60)
    
    # 测试用例
    test_cases = [
        {
            'question': '请介绍简仪科技的主要产品',
            'mode': 'simple',
            'expected_keywords': ['简仪科技', '锐视测控平台', 'PXI']
        },
        {
            'question': '如何解决PXI数据采集中的故障问题？',
            'mode': 'template',
            'expected_keywords': ['技术支持', '故障', 'PXI']
        },
        {
            'question': '什么是MISD方法？',
            'mode': 'intelligent',
            'expected_keywords': ['MISD', '模块仪器软件词典']
        },
        {
            'question': '简仪科技的教育解决方案有哪些？',
            'mode': 'expert',
            'expected_keywords': ['教育', '培训', '解决方案']
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 测试用例 {i}: {test_case['mode']}模式")
        print(f"问题: {test_case['question']}")
        print("-" * 40)
        
        try:
            # 构建提示词
            context = {
                'knowledge_content': '这是测试知识库内容，包含JYTEK AI Agent、MISD方法等相关信息...',
                'user_preferences': {'detailed_explanations': True}
            }
            
            prompt = prompt_system_manager.build_prompt(
                question=test_case['question'],
                mode=test_case['mode'],
                user_level='expert',
                context=context
            )
            
            # 验证结果
            success = True
            missing_keywords = []
            
            for keyword in test_case['expected_keywords']:
                if keyword not in prompt:
                    success = False
                    missing_keywords.append(keyword)
            
            # 记录结果
            result = {
                'test_case': i,
                'mode': test_case['mode'],
                'question': test_case['question'],
                'success': success,
                'prompt_length': len(prompt),
                'missing_keywords': missing_keywords,
                'prompt_preview': prompt[:200] + '...' if len(prompt) > 200 else prompt
            }
            
            results.append(result)
            
            # 输出结果
            status = "✅ 通过" if success else "❌ 失败"
            print(f"状态: {status}")
            print(f"提示词长度: {len(prompt)} 字符")
            
            if missing_keywords:
                print(f"缺失关键词: {', '.join(missing_keywords)}")
            
            print(f"提示词预览: {result['prompt_preview']}")
            
        except Exception as e:
            print(f"❌ 错误: {str(e)}")
            results.append({
                'test_case': i,
                'mode': test_case['mode'],
                'question': test_case['question'],
                'success': False,
                'error': str(e)
            })
    
    return results

def test_mode_permissions():
    """测试模式权限控制"""
    
    print(f"\n🔐 权限控制测试")
    print("-" * 40)
    
    permission_tests = [
        {'user_level': 'basic', 'mode': 'simple', 'should_pass': True},
        {'user_level': 'basic', 'mode': 'expert', 'should_pass': False},
        {'user_level': 'intermediate', 'mode': 'template', 'should_pass': True},
        {'user_level': 'advanced', 'mode': 'json', 'should_pass': True},
        {'user_level': 'expert', 'mode': 'intelligent', 'should_pass': True},
    ]
    
    for test in permission_tests:
        try:
            manager = prompt_system_manager.get_mode_manager(
                test['mode'], 
                test['user_level']
            )
            
            actual_pass = True
            error_msg = None
            
        except PermissionError as e:
            actual_pass = False
            error_msg = str(e)
        except Exception as e:
            actual_pass = False
            error_msg = f"意外错误: {str(e)}"
        
        expected = test['should_pass']
        status = "✅" if actual_pass == expected else "❌"
        
        print(f"{status} {test['user_level']} -> {test['mode']}: "
              f"预期{'通过' if expected else '拒绝'}, "
              f"实际{'通过' if actual_pass else '拒绝'}")
        
        if error_msg and not expected:
            print(f"   错误信息: {error_msg}")

def test_database_operations():
    """测试数据库操作"""
    
    print(f"\n💾 数据库操作测试")
    print("-" * 40)
    
    try:
        # 测试简单模式配置保存
        simple_manager = prompt_system_manager.get_mode_manager('simple', 'expert')
        test_config = {
            'company_name': '测试公司',
            'main_product': '测试产品',
            'response_style': 'professional',
            'focus_areas': ['测试领域1', '测试领域2']
        }
        
        save_success = simple_manager.save_config(test_config)
        print(f"✅ 简单模式配置保存: {'成功' if save_success else '失败'}")
        
        # 测试配置加载
        loaded_config = simple_manager.load_config()
        print(f"✅ 简单模式配置加载: 成功 (公司名: {loaded_config.get('company_name', '未知')})")
        
        # 测试模板保存
        template_manager = prompt_system_manager.get_mode_manager('template', 'expert')
        template_success = template_manager.save_template(
            'test_category',
            '这是测试模板内容 {question} {knowledge_content}',
            ['question', 'knowledge_content']
        )
        print(f"✅ 模板保存: {'成功' if template_success else '失败'}")
        
        # 测试备份创建
        backup_file = prompt_system_manager.backup_manager.create_backup('test')
        print(f"✅ 备份创建: {'成功' if backup_file else '失败'} (文件: {backup_file})")
        
    except Exception as e:
        print(f"❌ 数据库操作错误: {str(e)}")

def test_intelligent_features():
    """测试智能功能"""
    
    print(f"\n🤖 智能功能测试")
    print("-" * 40)
    
    try:
        intelligent_manager = prompt_system_manager.get_mode_manager('intelligent', 'expert')
        
        # 测试意图分析
        test_questions = [
            '请介绍简仪科技的产品',
            '我的PXI设备出现故障怎么办？',
            '如何编写数据采集代码？',
            '有什么教学资源吗？'
        ]
        
        for question in test_questions:
            intent_scores = intelligent_manager.intent_analyzer.analyze_intent(question)
            primary_intent = max(intent_scores.items(), key=lambda x: x[1])[0]
            max_score = intent_scores[primary_intent]
            
            print(f"问题: {question}")
            print(f"   主要意图: {primary_intent} (置信度: {max_score:.2f})")
        
        print("✅ 意图分析功能正常")
        
    except Exception as e:
        print(f"❌ 智能功能错误: {str(e)}")

def generate_test_report(results):
    """生成测试报告"""
    
    print(f"\n📊 测试报告")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r.get('success', False))
    failed_tests = total_tests - passed_tests
    
    print(f"总测试数: {total_tests}")
    print(f"通过: {passed_tests}")
    print(f"失败: {failed_tests}")
    print(f"成功率: {(passed_tests/total_tests*100):.1f}%")
    
    if failed_tests > 0:
        print(f"\n❌ 失败的测试:")
        for result in results:
            if not result.get('success', False):
                print(f"  - 测试 {result['test_case']}: {result['mode']}模式")
                if 'error' in result:
                    print(f"    错误: {result['error']}")
                if 'missing_keywords' in result:
                    print(f"    缺失关键词: {', '.join(result['missing_keywords'])}")
    
    # 保存详细报告
    report_data = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total': total_tests,
            'passed': passed_tests,
            'failed': failed_tests,
            'success_rate': passed_tests/total_tests*100
        },
        'results': results
    }
    
    report_file = f"prompt_system_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        print(f"\n📄 详细报告已保存: {report_file}")
    except Exception as e:
        print(f"⚠️ 报告保存失败: {str(e)}")

def main():
    """主测试函数"""
    
    print("🚀 开始提示词优化系统测试")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 核心功能测试
        results = test_prompt_system()
        
        # 权限控制测试
        test_mode_permissions()
        
        # 数据库操作测试
        test_database_operations()
        
        # 智能功能测试
        test_intelligent_features()
        
        # 生成测试报告
        generate_test_report(results)
        
        print(f"\n🎉 测试完成！")
        
    except Exception as e:
        print(f"\n💥 测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
