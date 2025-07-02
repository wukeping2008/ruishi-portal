#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from models.recommendation import intelligent_recommendation
    print("推荐系统模块导入成功")
except Exception as e:
    print(f"导入失败: {e}")
    import traceback
    traceback.print_exc()

try:
    from routes.recommendation_routes import recommendation_bp
    print("推荐系统路由导入成功")
except Exception as e:
    print(f"路由导入失败: {e}")
    import traceback
    traceback.print_exc()
