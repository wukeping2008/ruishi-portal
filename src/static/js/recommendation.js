/**
 * AI智能推荐系统前端模块
 * 简仪科技锐视测控平台专用
 */

class RecommendationSystem {
    constructor() {
        this.apiBase = '/api/recommendation';
        this.currentRecommendations = [];
        this.currentSolution = null;
        this.isLoading = false;
        
        this.init();
    }
    
    init() {
        console.log('AI智能推荐系统初始化中...');
        this.setupEventListeners();
        this.loadProductCategories();
    }
    
    setupEventListeners() {
        // 监听AI搜索事件
        document.addEventListener('aiSearchCompleted', (event) => {
            this.handleAISearchResult(event.detail);
        });
        
        // 监听推荐反馈事件
        document.addEventListener('click', (event) => {
            if (event.target.matches('.recommendation-feedback-btn')) {
                this.handleRecommendationFeedback(event);
            }
            
            if (event.target.matches('.product-detail-btn')) {
                this.showProductDetail(event);
            }
            
            if (event.target.matches('.solution-config-btn')) {
                this.showSolutionConfig(event);
            }
        });
    }
    
    async loadProductCategories() {
        try {
            const response = await fetch(`${this.apiBase}/categories`);
            const data = await response.json();
            
            if (data.success) {
                this.productCategories = data.data.categories;
                this.applicationScenarios = data.data.application_scenarios;
                console.log('产品类别加载成功:', Object.keys(this.productCategories).length);
            }
        } catch (error) {
            console.error('加载产品类别失败:', error);
        }
    }
    
    async handleAISearchResult(searchData) {
        const { question, answer } = searchData;
        
        if (!question) return;
        
        try {
            // 调用完整推荐服务
            const recommendations = await this.getCompleteRecommendation(question);
            
            if (recommendations && recommendations.product_recommendations.length > 0) {
                // 在答案页面显示推荐
                this.displayRecommendationsInAnswer(recommendations);
            }
        } catch (error) {
            console.error('获取推荐失败:', error);
        }
    }
    
    async getCompleteRecommendation(question, context = {}) {
        this.isLoading = true;
        
        try {
            const response = await fetch(`${this.apiBase}/complete`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question: question,
                    context: context,
                    product_limit: 5
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.currentRecommendations = data.data.product_recommendations;
                this.currentSolution = data.data.solution_config;
                return data.data;
            } else {
                throw new Error(data.message || '推荐服务失败');
            }
        } catch (error) {
            console.error('完整推荐服务失败:', error);
            return null;
        } finally {
            this.isLoading = false;
        }
    }
    
    displayRecommendationsInAnswer(recommendations) {
        // 查找答案页面的推荐容器
        let container = document.getElementById('smart-product-recommendations');
        
        if (!container) {
            // 如果容器不存在，创建一个
            container = this.createRecommendationContainer();
        }
        
        if (!container) return;
        
        const { intent_analysis, product_recommendations, solution_config } = recommendations;
        
        // 生成推荐内容
        const recommendationHTML = this.generateRecommendationHTML(
            intent_analysis, 
            product_recommendations, 
            solution_config
        );
        
        container.innerHTML = recommendationHTML;
        
        // 添加交互事件
        this.setupRecommendationInteractions(container);
    }
    
    createRecommendationContainer() {
        // 尝试在答案页面创建推荐容器
        const answerContainer = document.querySelector('.answer-content') || 
                               document.querySelector('.ai-answer') ||
                               document.querySelector('#answer-container');
        
        if (!answerContainer) return null;
        
        const container = document.createElement('div');
        container.id = 'smart-product-recommendations';
        container.className = 'recommendation-container mt-6';
        
        // 插入到答案内容后面
        answerContainer.appendChild(container);
        
        return container;
    }
    
    generateRecommendationHTML(intentAnalysis, productRecommendations, solutionConfig) {
        const confidenceScore = intentAnalysis.confidence_score || 0;
        const detectedCategories = intentAnalysis.detected_categories || [];
        
        let html = `
            <div class="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6 border border-blue-200">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-semibold text-gray-800 flex items-center">
                        <i class="fas fa-lightbulb text-blue-600 mr-2"></i>
                        AI智能产品推荐
                    </h3>
                    <div class="flex items-center text-sm text-gray-600">
                        <span class="mr-2">置信度:</span>
                        <div class="w-16 bg-gray-200 rounded-full h-2">
                            <div class="bg-blue-600 h-2 rounded-full" style="width: ${confidenceScore * 100}%"></div>
                        </div>
                        <span class="ml-2">${Math.round(confidenceScore * 100)}%</span>
                    </div>
                </div>
        `;
        
        // 显示检测到的类别
        if (detectedCategories.length > 0) {
            html += `
                <div class="mb-4">
                    <p class="text-sm text-gray-600 mb-2">检测到的产品类别:</p>
                    <div class="flex flex-wrap gap-2">
                        ${detectedCategories.map(cat => `
                            <span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
                                ${this.getCategoryDisplayName(cat.category)} (${cat.score}分)
                            </span>
                        `).join('')}
                    </div>
                </div>
            `;
        }
        
        // 显示产品推荐
        if (productRecommendations.length > 0) {
            html += `
                <div class="space-y-4">
                    ${productRecommendations.map((product, index) => this.generateProductCard(product, index)).join('')}
                </div>
            `;
            
            // 如果有解决方案配置，显示按钮
            if (solutionConfig) {
                html += `
                    <div class="mt-6 text-center">
                        <button class="solution-config-btn bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg font-medium transition-colors">
                            <i class="fas fa-cogs mr-2"></i>
                            查看完整解决方案配置
                        </button>
                    </div>
                `;
            }
        } else {
            html += `
                <div class="text-center py-8">
                    <i class="fas fa-search text-gray-400 text-3xl mb-3"></i>
                    <p class="text-gray-600">暂无相关产品推荐</p>
                    <p class="text-sm text-gray-500 mt-2">请尝试更具体的技术问题或产品需求</p>
                </div>
            `;
        }
        
        html += `
                <div class="mt-6 pt-4 border-t border-blue-200">
                    <div class="flex justify-between items-center">
                        <p class="text-sm text-gray-600">
                            <i class="fas fa-info-circle mr-1"></i>
                            推荐基于AI分析，如需详细咨询请联系技术支持
                        </p>
                        <a href="https://www.jytek.com" target="_blank" class="text-blue-600 hover:text-blue-800 text-sm font-medium">
                            访问官网 <i class="fas fa-external-link-alt ml-1"></i>
                        </a>
                    </div>
                </div>
            </div>
        `;
        
        return html;
    }
    
    generateProductCard(product, index) {
        const { name, description, features, specifications, recommendation_reason, price_range, availability } = product;
        
        return `
            <div class="bg-white rounded-lg p-4 border border-gray-200 hover:border-blue-300 transition-colors">
                <div class="flex items-start justify-between">
                    <div class="flex-1">
                        <div class="flex items-center mb-2">
                            <h4 class="font-semibold text-gray-800 mr-3">${name}</h4>
                            <span class="text-xs px-2 py-1 rounded ${availability === '现货' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}">
                                ${availability}
                            </span>
                        </div>
                        
                        <p class="text-sm text-gray-600 mb-3">${description}</p>
                        
                        <!-- 产品特点 -->
                        ${features && features.length > 0 ? `
                            <div class="flex flex-wrap gap-1 mb-3">
                                ${features.slice(0, 4).map(feature => 
                                    `<span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">${feature}</span>`
                                ).join('')}
                            </div>
                        ` : ''}
                        
                        <!-- 推荐理由 -->
                        <div class="bg-green-50 p-3 rounded-lg mb-3">
                            <p class="text-sm text-green-800">
                                <i class="fas fa-check-circle mr-1"></i>
                                <strong>推荐理由：</strong>${recommendation_reason}
                            </p>
                        </div>
                        
                        <!-- 价格信息 -->
                        <div class="flex items-center justify-between">
                            <span class="text-sm font-medium text-gray-700">价格范围: ${price_range}</span>
                            <div class="flex space-x-2">
                                <button class="product-detail-btn bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm transition-colors" 
                                        data-product-index="${index}">
                                    <i class="fas fa-info-circle mr-1"></i>详情
                                </button>
                                <button class="recommendation-feedback-btn bg-gray-600 hover:bg-gray-700 text-white px-3 py-1 rounded text-sm transition-colors"
                                        data-product-index="${index}" data-rating="5">
                                    <i class="fas fa-thumbs-up mr-1"></i>有用
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    setupRecommendationInteractions(container) {
        // 产品详情按钮
        container.querySelectorAll('.product-detail-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const productIndex = parseInt(e.target.dataset.productIndex);
                this.showProductDetail(productIndex);
            });
        });
        
        // 反馈按钮
        container.querySelectorAll('.recommendation-feedback-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const productIndex = parseInt(e.target.dataset.productIndex);
                const rating = parseInt(e.target.dataset.rating);
                this.submitRecommendationFeedback(productIndex, rating);
            });
        });
        
        // 解决方案配置按钮
        container.querySelectorAll('.solution-config-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.showSolutionConfig();
            });
        });
    }
    
    showProductDetail(productIndex) {
        if (!this.currentRecommendations || !this.currentRecommendations[productIndex]) {
            return;
        }
        
        const product = this.currentRecommendations[productIndex];
        
        // 创建产品详情模态框
        const modal = this.createModal('产品详情', this.generateProductDetailHTML(product));
        document.body.appendChild(modal);
    }
    
    generateProductDetailHTML(product) {
        const { name, description, features, specifications, applications, contact_info } = product;
        
        return `
            <div class="max-w-2xl">
                <div class="mb-6">
                    <h3 class="text-xl font-bold text-gray-800 mb-2">${name}</h3>
                    <p class="text-gray-600">${description}</p>
                </div>
                
                <!-- 产品特色 -->
                ${features && features.length > 0 ? `
                    <div class="mb-6">
                        <h4 class="font-semibold text-gray-800 mb-3">产品特色</h4>
                        <div class="grid grid-cols-2 gap-2">
                            ${features.map(feature => 
                                `<div class="bg-blue-50 p-2 rounded text-sm text-blue-800">${feature}</div>`
                            ).join('')}
                        </div>
                    </div>
                ` : ''}
                
                <!-- 技术规格 -->
                ${specifications && Object.keys(specifications).length > 0 ? `
                    <div class="mb-6">
                        <h4 class="font-semibold text-gray-800 mb-3">技术规格</h4>
                        <div class="bg-gray-50 p-4 rounded">
                            ${Object.entries(specifications).map(([key, value]) => 
                                `<div class="flex justify-between py-1 border-b border-gray-200 last:border-b-0">
                                    <span class="text-gray-600">${key}:</span>
                                    <span class="font-medium">${value}</span>
                                </div>`
                            ).join('')}
                        </div>
                    </div>
                ` : ''}
                
                <!-- 应用场景 -->
                ${applications && applications.length > 0 ? `
                    <div class="mb-6">
                        <h4 class="font-semibold text-gray-800 mb-3">应用场景</h4>
                        <div class="flex flex-wrap gap-2">
                            ${applications.map(app => 
                                `<span class="bg-green-100 text-green-800 text-sm px-3 py-1 rounded-full">${app}</span>`
                            ).join('')}
                        </div>
                    </div>
                ` : ''}
                
                <!-- 联系信息 -->
                <div class="bg-blue-50 p-4 rounded-lg">
                    <h4 class="font-semibold text-blue-800 mb-2">获取更多信息</h4>
                    <div class="space-y-2 text-sm">
                        <p><i class="fas fa-globe mr-2"></i>官网: <a href="${contact_info.website}" target="_blank" class="text-blue-600 hover:underline">${contact_info.website}</a></p>
                        <p><i class="fas fa-phone mr-2"></i>电话: ${contact_info.phone}</p>
                        <p><i class="fas fa-envelope mr-2"></i>邮箱: ${contact_info.email}</p>
                    </div>
                </div>
            </div>
        `;
    }
    
    showSolutionConfig() {
        if (!this.currentSolution) {
            this.showNotification('暂无解决方案配置信息', 'warning');
            return;
        }
        
        const modal = this.createModal('完整解决方案配置', this.generateSolutionConfigHTML(this.currentSolution));
        document.body.appendChild(modal);
    }
    
    generateSolutionConfigHTML(solution) {
        const { name, description, components, estimated_cost, advantages, implementation_guide } = solution;
        
        return `
            <div class="max-w-4xl">
                <div class="mb-6">
                    <h3 class="text-xl font-bold text-gray-800 mb-2">${name}</h3>
                    <p class="text-gray-600">${description}</p>
                </div>
                
                <!-- 系统组件 -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <!-- 机箱配置 -->
                    <div class="bg-gray-50 p-4 rounded-lg">
                        <h4 class="font-semibold text-gray-800 mb-3">
                            <i class="fas fa-server text-blue-600 mr-2"></i>机箱配置
                        </h4>
                        <div class="space-y-2 text-sm">
                            <p><strong>${components.chassis.name}</strong></p>
                            <p class="text-gray-600">${components.chassis.description}</p>
                            <p class="text-blue-600">${components.chassis.price_range}</p>
                        </div>
                    </div>
                    
                    <!-- 控制器配置 -->
                    <div class="bg-gray-50 p-4 rounded-lg">
                        <h4 class="font-semibold text-gray-800 mb-3">
                            <i class="fas fa-microchip text-green-600 mr-2"></i>控制器配置
                        </h4>
                        <div class="space-y-2 text-sm">
                            <p><strong>${components.controller.name}</strong></p>
                            <p class="text-gray-600">${components.controller.description}</p>
                            <p class="text-green-600">${components.controller.price_range}</p>
                        </div>
                    </div>
                </div>
                
                <!-- 成本估算 -->
                <div class="bg-yellow-50 p-4 rounded-lg mb-6">
                    <h4 class="font-semibold text-gray-800 mb-3">
                        <i class="fas fa-calculator text-yellow-600 mr-2"></i>成本估算
                    </h4>
                    <div class="text-lg font-bold text-yellow-800 mb-2">${estimated_cost.range}</div>
                    <p class="text-sm text-gray-600">${estimated_cost.note}</p>
                </div>
                
                <!-- 方案优势 -->
                ${advantages && advantages.length > 0 ? `
                    <div class="mb-6">
                        <h4 class="font-semibold text-gray-800 mb-3">方案优势</h4>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
                            ${advantages.map(advantage => 
                                `<div class="flex items-center text-sm text-gray-700">
                                    <i class="fas fa-check text-green-600 mr-2"></i>
                                    ${advantage}
                                </div>`
                            ).join('')}
                        </div>
                    </div>
                ` : ''}
                
                <!-- 实施指南 -->
                ${implementation_guide ? `
                    <div class="mb-6">
                        <h4 class="font-semibold text-gray-800 mb-3">实施指南</h4>
                        <div class="space-y-3">
                            ${implementation_guide.phases.map((phase, index) => 
                                `<div class="flex items-start">
                                    <div class="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 mt-1">
                                        ${index + 1}
                                    </div>
                                    <div class="flex-1">
                                        <h5 class="font-medium text-gray-800">${phase.phase}</h5>
                                        <p class="text-sm text-gray-600">预计时间: ${phase.duration}</p>
                                        <ul class="text-sm text-gray-600 mt-1">
                                            ${phase.activities.map(activity => `<li>• ${activity}</li>`).join('')}
                                        </ul>
                                    </div>
                                </div>`
                            ).join('')}
                        </div>
                        <div class="mt-4 p-3 bg-blue-50 rounded">
                            <p class="text-sm text-blue-800">
                                <i class="fas fa-clock mr-1"></i>
                                总实施周期: ${implementation_guide.total_duration}
                            </p>
                        </div>
                    </div>
                ` : ''}
                
                <!-- 联系方式 -->
                <div class="bg-red-50 p-4 rounded-lg text-center">
                    <h4 class="font-semibold text-red-800 mb-2">获取详细方案和报价</h4>
                    <p class="text-sm text-gray-600 mb-3">我们的技术专家将为您提供定制化的解决方案</p>
                    <a href="https://www.jytek.com" target="_blank" class="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-lg inline-block transition-colors">
                        <i class="fas fa-external-link-alt mr-2"></i>联系简仪科技
                    </a>
                </div>
            </div>
        `;
    }
    
    async submitRecommendationFeedback(productIndex, rating) {
        if (!this.currentRecommendations || !this.currentRecommendations[productIndex]) {
            return;
        }
        
        const product = this.currentRecommendations[productIndex];
        
        try {
            const response = await fetch(`${this.apiBase}/feedback`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    product_id: product.product_id,
                    rating: rating,
                    feedback: '用户点击有用按钮',
                    context: {
                        product_name: product.name,
                        recommendation_score: product.recommendation_score
                    }
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showNotification('感谢您的反馈！', 'success');
            }
        } catch (error) {
            console.error('提交反馈失败:', error);
        }
    }
    
    createModal(title, content) {
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 flex items-center justify-center z-50 p-4 bg-black bg-opacity-50';
        
        modal.innerHTML = `
            <div class="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
                <div class="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4">
                    <div class="flex justify-between items-center">
                        <h3 class="text-lg font-semibold">${title}</h3>
                        <button class="text-white hover:text-gray-200 text-xl" onclick="this.closest('.fixed').remove()">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>
                <div class="p-6">
                    ${content}
                </div>
            </div>
        `;
        
        // 点击背景关闭
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
        
        return modal;
    }
    
    getCategoryDisplayName(category) {
        const categoryNames = {
            'data_acquisition': '数据采集',
            'signal_generation': '信号发生',
            'digital_io': '数字I/O',
            'rf_microwave': '射频微波',
            'oscilloscope': '示波器',
            'multimeter': '万用表'
        };
        
        return categoryNames[category] || category;
    }
    
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `fixed bottom-4 right-4 px-6 py-3 rounded-lg shadow-lg z-50 transition-all duration-300`;
        
        switch (type) {
            case 'success':
                notification.classList.add('bg-green-500', 'text-white');
                break;
            case 'error':
                notification.classList.add('bg-red-500', 'text-white');
                break;
            case 'warning':
                notification.classList.add('bg-yellow-500', 'text-white');
                break;
            default:
                notification.classList.add('bg-blue-500', 'text-white');
        }
        
        notification.innerHTML = `
            <div class="flex items-center">
                <i class="fas fa-info-circle mr-2"></i>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// 全局推荐系统实例
let recommendationSystem;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    recommendationSystem = new RecommendationSystem();
});

// 导出给其他模块使用
window.RecommendationSystem = RecommendationSystem;
window.recommendationSystem = recommendationSystem;
