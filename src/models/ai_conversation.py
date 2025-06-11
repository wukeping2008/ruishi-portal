"""
AI对话记录和统计模块
AI Conversation Recording and Statistics Module
"""

import json
import time
from datetime import datetime
from typing import Dict, Any, Optional, List
from models.database import db_manager
import logging

logger = logging.getLogger(__name__)

class AIConversationManager:
    """AI对话管理器"""
    
    def __init__(self):
        self.db = db_manager
    
    def record_conversation(self, 
                          question: str,
                          answer: str,
                          ai_provider: str,
                          ai_model: str,
                          user_id: Optional[int] = None,
                          session_id: Optional[str] = None,
                          user_type: str = 'guest',
                          user_ip: Optional[str] = None,
                          user_agent: Optional[str] = None,
                          trigger_type: str = 'question',
                          keywords: Optional[List[str]] = None,
                          related_documents: Optional[List[Dict]] = None,
                          response_time: Optional[float] = None) -> Optional[int]:
        """记录AI对话"""
        try:
            conn = self.db.get_connection()
            
            # 提取和处理关键词
            extracted_keywords = self._extract_keywords(question)
            if keywords:
                extracted_keywords.extend(keywords)
            extracted_keywords = list(set(extracted_keywords))  # 去重
            
            # 准备文档信息
            related_docs_json = None
            document_names = []
            if related_documents:
                related_docs_json = json.dumps(related_documents)
                document_names = [doc.get('filename', doc.get('title', '')) for doc in related_documents]
            
            # 记录对话
            cursor = conn.execute('''
                INSERT INTO ai_conversations (
                    user_id, session_id, user_type, user_ip, user_agent,
                    question, answer, ai_provider, ai_model, trigger_type,
                    keywords, related_documents, document_names,
                    response_time, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, session_id, user_type, user_ip, user_agent,
                question, answer, ai_provider, ai_model, trigger_type,
                json.dumps(extracted_keywords) if extracted_keywords else None,
                related_docs_json,
                json.dumps(document_names) if document_names else None,
                response_time, datetime.now().isoformat()
            ))
            
            conversation_id = cursor.lastrowid
            conn.commit()
            
            # 更新关键词统计
            self._update_keyword_statistics(extracted_keywords, 'question')
            
            # 更新用户会话统计
            self._update_session_statistics(session_id, user_type, user_ip, trigger_type)
            
            logger.info(f"AI对话记录成功: ID={conversation_id}, Provider={ai_provider}, Keywords={len(extracted_keywords)}")
            return conversation_id
            
        except Exception as e:
            logger.error(f"记录AI对话失败: {e}")
            return None
        finally:
            conn.close()
    
    def _extract_keywords(self, text: str) -> List[str]:
        """从文本中提取关键词"""
        import re
        
        # 定义PXI和测控相关的关键词模式
        keyword_patterns = [
            r'PXI[E]?[-\s]*\d*',  # PXI, PXIE, PXI-1234等
            r'数据采集|data\s*acquisition|DAQ',
            r'信号发生|signal\s*generation|AWG',
            r'示波器|oscilloscope',
            r'频谱分析|spectrum\s*analyzer',
            r'数字万用表|digital\s*multimeter|DMM',
            r'逻辑分析|logic\s*analyzer',
            r'MISD|模块仪器软件词典',
            r'LabVIEW|TestStand|VISA|IVI',
            r'简仪科技|JYTEK|SeeSharp',
            r'测控|测试|测量|控制|仪器|仪表',
            r'自动化|automation',
            r'同步|synchronization|trigger',
            r'采样率|sample\s*rate',
            r'分辨率|resolution',
            r'带宽|bandwidth',
            r'精度|accuracy|precision',
            r'校准|calibration',
            r'驱动|driver|API',
            r'编程|programming|开发|development'
        ]
        
        keywords = []
        text_lower = text.lower()
        
        # 提取模式匹配的关键词
        for pattern in keyword_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            keywords.extend(matches)
        
        # 提取中文关键词（2-6个字符的词组）
        chinese_words = re.findall(r'[\u4e00-\u9fa5]{2,6}', text)
        keywords.extend(chinese_words)
        
        # 提取英文关键词（3-15个字符的单词）
        english_words = re.findall(r'\b[a-zA-Z]{3,15}\b', text)
        keywords.extend([word.lower() for word in english_words])
        
        # 去重并过滤
        keywords = list(set(keywords))
        
        # 过滤掉常见的停用词
        stop_words = {'的', '是', '在', '有', '和', '与', '或', '但', '如果', '因为', '所以', '这', '那', '什么', '怎么', '为什么',
                     'the', 'is', 'are', 'and', 'or', 'but', 'if', 'because', 'so', 'this', 'that', 'what', 'how', 'why',
                     'can', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'shall'}
        
        filtered_keywords = [kw for kw in keywords if kw not in stop_words and len(kw) > 1]
        
        return filtered_keywords[:20]  # 最多返回20个关键词
    
    def _update_keyword_statistics(self, keywords: List[str], source_type: str):
        """更新关键词统计"""
        if not keywords:
            return
            
        try:
            conn = self.db.get_connection()
            
            for keyword in keywords:
                # 尝试更新现有记录
                cursor = conn.execute('''
                    UPDATE keyword_statistics 
                    SET frequency = frequency + 1, last_used = CURRENT_TIMESTAMP
                    WHERE keyword = ? AND source_type = ?
                ''', (keyword, source_type))
                
                # 如果没有更新任何记录，则插入新记录
                if cursor.rowcount == 0:
                    conn.execute('''
                        INSERT INTO keyword_statistics (keyword, frequency, source_type)
                        VALUES (?, 1, ?)
                    ''', (keyword, source_type))
            
            conn.commit()
            
        except Exception as e:
            logger.error(f"更新关键词统计失败: {e}")
        finally:
            conn.close()
    
    def _update_session_statistics(self, session_id: str, user_type: str, user_ip: str, trigger_type: str):
        """更新用户会话统计"""
        if not session_id:
            return
            
        try:
            conn = self.db.get_connection()
            
            # 尝试更新现有会话记录
            cursor = conn.execute('''
                UPDATE user_session_stats 
                SET last_activity = CURRENT_TIMESTAMP,
                    total_questions = total_questions + CASE WHEN ? = 'question' THEN 1 ELSE 0 END,
                    total_ai_calls = total_ai_calls + 1
                WHERE session_id = ?
            ''', (trigger_type, session_id))
            
            # 如果没有更新任何记录，则插入新记录
            if cursor.rowcount == 0:
                conn.execute('''
                    INSERT INTO user_session_stats (
                        session_id, user_type, user_ip, 
                        total_questions, total_ai_calls
                    ) VALUES (?, ?, ?, ?, 1)
                ''', (
                    session_id, user_type, user_ip,
                    1 if trigger_type == 'question' else 0
                ))
            
            conn.commit()
            
        except Exception as e:
            logger.error(f"更新会话统计失败: {e}")
        finally:
            conn.close()
    
    def get_conversation_statistics(self) -> Dict[str, Any]:
        """获取对话统计信息"""
        try:
            conn = self.db.get_connection()
            stats = {}
            
            # 总对话数
            cursor = conn.execute('SELECT COUNT(*) as total FROM ai_conversations')
            stats['total_conversations'] = cursor.fetchone()['total']
            
            # 按提供商统计
            cursor = conn.execute('''
                SELECT ai_provider, COUNT(*) as count 
                FROM ai_conversations 
                GROUP BY ai_provider
            ''')
            stats['conversations_by_provider'] = {
                row['ai_provider']: row['count'] 
                for row in cursor.fetchall()
            }
            
            # 按模型统计
            cursor = conn.execute('''
                SELECT ai_model, COUNT(*) as count 
                FROM ai_conversations 
                GROUP BY ai_model
            ''')
            stats['conversations_by_model'] = {
                row['ai_model']: row['count'] 
                for row in cursor.fetchall()
            }
            
            # 今日对话数
            cursor = conn.execute('''
                SELECT COUNT(*) as today_count 
                FROM ai_conversations 
                WHERE DATE(created_at) = DATE('now')
            ''')
            stats['today_conversations'] = cursor.fetchone()['today_count']
            
            # 平均响应时间
            cursor = conn.execute('''
                SELECT AVG(response_time) as avg_time 
                FROM ai_conversations 
                WHERE response_time IS NOT NULL
            ''')
            avg_time = cursor.fetchone()['avg_time']
            stats['average_response_time'] = round(avg_time, 2) if avg_time else 0
            
            # 最近7天的对话趋势
            cursor = conn.execute('''
                SELECT DATE(created_at) as date, COUNT(*) as count
                FROM ai_conversations 
                WHERE created_at >= DATE('now', '-7 days')
                GROUP BY DATE(created_at)
                ORDER BY date
            ''')
            stats['weekly_trend'] = [
                {'date': row['date'], 'count': row['count']}
                for row in cursor.fetchall()
            ]
            
            # 使用知识库的对话比例
            cursor = conn.execute('''
                SELECT 
                    COUNT(CASE WHEN related_documents IS NOT NULL THEN 1 END) as with_docs,
                    COUNT(*) as total
                FROM ai_conversations
            ''')
            result = cursor.fetchone()
            if result['total'] > 0:
                stats['knowledge_base_usage_rate'] = round(
                    (result['with_docs'] / result['total']) * 100, 1
                )
            else:
                stats['knowledge_base_usage_rate'] = 0
            
            return stats
            
        except Exception as e:
            logger.error(f"获取对话统计失败: {e}")
            return {}
        finally:
            conn.close()
    
    def get_recent_conversations(self, limit: int = 10) -> List[Dict]:
        """获取最近的对话记录"""
        try:
            conn = self.db.get_connection()
            
            cursor = conn.execute('''
                SELECT 
                    id, question, ai_provider, ai_model, 
                    created_at, response_time, rating
                FROM ai_conversations 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (limit,))
            
            conversations = []
            for row in cursor.fetchall():
                conversations.append({
                    'id': row['id'],
                    'question': row['question'][:100] + '...' if len(row['question']) > 100 else row['question'],
                    'ai_provider': row['ai_provider'],
                    'ai_model': row['ai_model'],
                    'created_at': row['created_at'],
                    'response_time': row['response_time'],
                    'rating': row['rating']
                })
            
            return conversations
            
        except Exception as e:
            logger.error(f"获取最近对话失败: {e}")
            return []
        finally:
            conn.close()
    
    def rate_conversation(self, conversation_id: int, rating: int) -> bool:
        """为对话评分"""
        try:
            if rating not in [1, 2, 3, 4, 5]:
                return False
            
            conn = self.db.get_connection()
            
            cursor = conn.execute('''
                UPDATE ai_conversations 
                SET rating = ? 
                WHERE id = ?
            ''', (rating, conversation_id))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            logger.error(f"对话评分失败: {e}")
            return False
        finally:
            conn.close()
    
    def get_provider_performance(self) -> Dict[str, Any]:
        """获取AI提供商性能统计"""
        try:
            conn = self.db.get_connection()
            
            cursor = conn.execute('''
                SELECT 
                    ai_provider,
                    COUNT(*) as total_conversations,
                    AVG(response_time) as avg_response_time,
                    AVG(rating) as avg_rating,
                    COUNT(CASE WHEN rating >= 4 THEN 1 END) as positive_ratings
                FROM ai_conversations 
                WHERE ai_provider IS NOT NULL
                GROUP BY ai_provider
            ''')
            
            performance = {}
            for row in cursor.fetchall():
                provider = row['ai_provider']
                total = row['total_conversations']
                
                performance[provider] = {
                    'total_conversations': total,
                    'avg_response_time': round(row['avg_response_time'], 2) if row['avg_response_time'] else 0,
                    'avg_rating': round(row['avg_rating'], 2) if row['avg_rating'] else 0,
                    'satisfaction_rate': round((row['positive_ratings'] / total) * 100, 1) if total > 0 else 0
                }
            
            return performance
            
        except Exception as e:
            logger.error(f"获取提供商性能统计失败: {e}")
            return {}
        finally:
            conn.close()
    
    def get_keyword_statistics(self, limit: int = 20) -> Dict[str, Any]:
        """获取关键词统计"""
        try:
            conn = self.db.get_connection()
            
            # 获取热门关键词
            cursor = conn.execute('''
                SELECT keyword, frequency, last_used
                FROM keyword_statistics 
                WHERE source_type = 'question'
                ORDER BY frequency DESC 
                LIMIT ?
            ''', (limit,))
            
            hot_keywords = [
                {
                    'keyword': row['keyword'],
                    'frequency': row['frequency'],
                    'last_used': row['last_used']
                }
                for row in cursor.fetchall()
            ]
            
            # 获取今日新增关键词
            cursor = conn.execute('''
                SELECT COUNT(*) as today_new_keywords
                FROM keyword_statistics 
                WHERE DATE(created_at) = DATE('now')
            ''')
            today_new_keywords = cursor.fetchone()['today_new_keywords']
            
            # 获取关键词趋势（最近7天）
            cursor = conn.execute('''
                SELECT DATE(last_used) as date, COUNT(DISTINCT keyword) as unique_keywords
                FROM keyword_statistics 
                WHERE last_used >= DATE('now', '-7 days')
                GROUP BY DATE(last_used)
                ORDER BY date
            ''')
            keyword_trend = [
                {'date': row['date'], 'count': row['unique_keywords']}
                for row in cursor.fetchall()
            ]
            
            return {
                'hot_keywords': hot_keywords,
                'today_new_keywords': today_new_keywords,
                'keyword_trend': keyword_trend,
                'total_keywords': len(hot_keywords)
            }
            
        except Exception as e:
            logger.error(f"获取关键词统计失败: {e}")
            return {}
        finally:
            conn.close()
    
    def get_user_statistics(self) -> Dict[str, Any]:
        """获取用户统计"""
        try:
            conn = self.db.get_connection()
            
            # 用户类型分布
            cursor = conn.execute('''
                SELECT user_type, COUNT(DISTINCT session_id) as count
                FROM user_session_stats
                GROUP BY user_type
            ''')
            user_type_distribution = {
                row['user_type']: row['count']
                for row in cursor.fetchall()
            }
            
            # 今日活跃用户
            cursor = conn.execute('''
                SELECT COUNT(DISTINCT session_id) as today_active_users
                FROM user_session_stats
                WHERE DATE(last_activity) = DATE('now')
            ''')
            today_active_users = cursor.fetchone()['today_active_users']
            
            # 用户活跃度分析
            cursor = conn.execute('''
                SELECT 
                    AVG(total_questions) as avg_questions_per_user,
                    AVG(total_ai_calls) as avg_ai_calls_per_user,
                    MAX(total_questions) as max_questions_per_user
                FROM user_session_stats
            ''')
            activity_stats = cursor.fetchone()
            
            # 最近7天用户活跃趋势
            cursor = conn.execute('''
                SELECT DATE(last_activity) as date, COUNT(DISTINCT session_id) as active_users
                FROM user_session_stats
                WHERE last_activity >= DATE('now', '-7 days')
                GROUP BY DATE(last_activity)
                ORDER BY date
            ''')
            user_trend = [
                {'date': row['date'], 'count': row['active_users']}
                for row in cursor.fetchall()
            ]
            
            return {
                'user_type_distribution': user_type_distribution,
                'today_active_users': today_active_users,
                'avg_questions_per_user': round(activity_stats['avg_questions_per_user'], 1) if activity_stats['avg_questions_per_user'] else 0,
                'avg_ai_calls_per_user': round(activity_stats['avg_ai_calls_per_user'], 1) if activity_stats['avg_ai_calls_per_user'] else 0,
                'max_questions_per_user': activity_stats['max_questions_per_user'] or 0,
                'user_trend': user_trend
            }
            
        except Exception as e:
            logger.error(f"获取用户统计失败: {e}")
            return {}
        finally:
            conn.close()
    
    def get_document_usage_statistics(self) -> Dict[str, Any]:
        """获取文档使用统计"""
        try:
            conn = self.db.get_connection()
            
            # 通过related_documents获取文档使用统计，并显示原始文件名
            cursor = conn.execute('''
                SELECT 
                    related_documents,
                    COUNT(*) as usage_count
                FROM ai_conversations 
                WHERE related_documents IS NOT NULL 
                AND related_documents != 'null'
                AND related_documents != '[]'
                GROUP BY related_documents
                ORDER BY usage_count DESC
                LIMIT 20
            ''')
            
            document_usage_dict = {}
            for row in cursor.fetchall():
                try:
                    related_docs = json.loads(row['related_documents'])
                    if related_docs:
                        for doc in related_docs:
                            doc_id = doc.get('id')
                            if doc_id:
                                # 获取文档的原始文件名
                                doc_cursor = conn.execute('''
                                    SELECT original_filename 
                                    FROM documents 
                                    WHERE id = ? AND is_active = 1
                                ''', (doc_id,))
                                doc_result = doc_cursor.fetchone()
                                if doc_result:
                                    filename = doc_result['original_filename']
                                    document_usage_dict[filename] = document_usage_dict.get(filename, 0) + row['usage_count']
                except (json.JSONDecodeError, TypeError):
                    continue
            
            # 按使用次数排序
            popular_documents = [
                {'document_name': filename, 'usage_count': count}
                for filename, count in sorted(document_usage_dict.items(), key=lambda x: x[1], reverse=True)[:10]
            ]
            
            # 按文档类型统计使用情况
            cursor = conn.execute('''
                SELECT 
                    related_documents,
                    COUNT(*) as usage_count
                FROM ai_conversations 
                WHERE related_documents IS NOT NULL AND related_documents != 'null'
                GROUP BY related_documents
            ''')
            
            document_type_usage = {}
            for row in cursor.fetchall():
                try:
                    docs = json.loads(row['related_documents'])
                    for doc in docs:
                        file_type = doc.get('file_type', 'unknown')
                        document_type_usage[file_type] = document_type_usage.get(file_type, 0) + row['usage_count']
                except (json.JSONDecodeError, TypeError):
                    continue
            
            # 文档关联率
            cursor = conn.execute('''
                SELECT 
                    COUNT(CASE WHEN related_documents IS NOT NULL AND related_documents != 'null' THEN 1 END) as with_docs,
                    COUNT(*) as total
                FROM ai_conversations
            ''')
            result = cursor.fetchone()
            document_association_rate = round((result['with_docs'] / result['total']) * 100, 1) if result['total'] > 0 else 0
            
            return {
                'popular_documents': popular_documents[:10],
                'document_type_usage': document_type_usage,
                'document_association_rate': document_association_rate,
                'total_document_references': result['with_docs']
            }
            
        except Exception as e:
            logger.error(f"获取文档使用统计失败: {e}")
            return {}
        finally:
            conn.close()
    
    def get_trigger_type_statistics(self) -> Dict[str, Any]:
        """获取触发类型统计"""
        try:
            conn = self.db.get_connection()
            
            # 按触发类型统计
            cursor = conn.execute('''
                SELECT trigger_type, COUNT(*) as count
                FROM ai_conversations
                GROUP BY trigger_type
            ''')
            trigger_distribution = {
                row['trigger_type']: row['count']
                for row in cursor.fetchall()
            }
            
            # 最近7天的触发类型趋势
            cursor = conn.execute('''
                SELECT DATE(created_at) as date, trigger_type, COUNT(*) as count
                FROM ai_conversations
                WHERE created_at >= DATE('now', '-7 days')
                GROUP BY DATE(created_at), trigger_type
                ORDER BY date, trigger_type
            ''')
            
            trigger_trend = {}
            for row in cursor.fetchall():
                date = row['date']
                if date not in trigger_trend:
                    trigger_trend[date] = {}
                trigger_trend[date][row['trigger_type']] = row['count']
            
            return {
                'trigger_distribution': trigger_distribution,
                'trigger_trend': trigger_trend
            }
            
        except Exception as e:
            logger.error(f"获取触发类型统计失败: {e}")
            return {}
        finally:
            conn.close()
    
    def get_comprehensive_statistics(self) -> Dict[str, Any]:
        """获取综合统计信息"""
        try:
            # 获取所有统计数据
            conversation_stats = self.get_conversation_statistics()
            provider_performance = self.get_provider_performance()
            keyword_stats = self.get_keyword_statistics()
            user_stats = self.get_user_statistics()
            document_stats = self.get_document_usage_statistics()
            trigger_stats = self.get_trigger_type_statistics()
            
            return {
                'conversation_statistics': conversation_stats,
                'provider_performance': provider_performance,
                'keyword_statistics': keyword_stats,
                'user_statistics': user_stats,
                'document_statistics': document_stats,
                'trigger_statistics': trigger_stats,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"获取综合统计失败: {e}")
            return {}

# 全局AI对话管理器实例
ai_conversation_manager = AIConversationManager()
