/**
 * 锐视测控平台主要JavaScript文件
 * 简仪科技JYTEK专业PXI测控解决方案
 */

// 全局变量
let currentQuestion = '';
let currentAnswer = null;
let productCategories = {};

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    loadProductCategories();
    setupEventListeners();
    
    // 监听语言切换事件
    document.addEventListener('languageChanged', function(event) {
        updateDynamicContent();
    });
});

// 初始化应用
function initializeApp() {
    console.log('锐视测控平台初始化中...');
    
    // 检查API连接
    checkAPIConnection();
    
    // 初始化搜索框
    initializeSearchBox();
    
    // 初始化移动端菜单
    initializeMobileMenu();
}

// 检查API连接
async function checkAPIConnection() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        console.log('API连接正常:', data.message);
    } catch (error) {
        console.error('API连接失败:', error);
        showNotification('系统连接异常，部分功能可能不可用', 'warning');
    }
}

// 初始化搜索框
function initializeSearchBox() {
    const searchInput = document.getElementById('ai-search-input');
    const searchBtn = document.getElementById('ai-search-btn');
    
    if (searchInput && searchBtn) {
        // 回车键搜索
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                handleAISearch();
            }
        });
        
        // 点击搜索按钮
        searchBtn.addEventListener('click', handleAISearch);
        
        // 输入时的动态提示
        searchInput.addEventListener('input', function() {
            const value = this.value.trim();
            const tipElement = document.querySelector('.typing-animation');
            
            if (value.length > 0) {
                tipElement.textContent = `正在分析您的问题："${value.substring(0, 20)}${value.length > 20 ? '...' : ''}"`;
            } else {
                tipElement.textContent = 'AI正在等待您的问题...';
            }
        });
    }
}

// 初始化移动端菜单
function initializeMobileMenu() {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
}

// 设置事件监听器
function setupEventListeners() {
    // 平滑滚动
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// 处理AI搜索
async function handleAISearch() {
    const searchInput = document.getElementById('ai-search-input');
    const searchBtn = document.getElementById('ai-search-btn');
    const question = searchInput.value.trim();
    
    if (!question) {
        showNotification('请输入您的问题', 'warning');
        return;
    }
    
    // 更新UI状态
    searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>AI思考中...';
    searchBtn.disabled = true;
    
    try {
        // 调用AI问答API
        const response = await fetch('/api/llm/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: question,
                provider: null,
                model: null,
                options: {}
            })
        });
        
        const data = await response.json();
        
        console.log('Main page received data:', data);
        
        if (data.content) {
            // 存储问题和答案到localStorage
            localStorage.setItem('currentQuestion', question);
            localStorage.setItem('currentAnswer', JSON.stringify(data));
            
            // 跳转到答案页面
            window.open('answer.html', '_blank');
            
            // 清空搜索框
            searchInput.value = '';
            document.querySelector('.typing-animation').textContent = 'AI正在等待您的问题...';
        } else {
            console.error('No content in response:', data);
            throw new Error(data.error || '获取回答失败');
        }
        
    } catch (error) {
        console.error('AI搜索失败:', error);
        showNotification('AI搜索失败，请稍后重试', 'error');
    } finally {
        // 恢复UI状态
        searchBtn.innerHTML = '<i class="fas fa-search mr-2"></i>提问';
        searchBtn.disabled = false;
    }
}

// 加载产品分类
async function loadProductCategories() {
    try {
        const response = await fetch('/api/products/categories');
        const data = await response.json();
        
        if (data.success) {
            productCategories = data.categories;
            displayProductCategories();
        } else {
            throw new Error(data.error || '加载产品分类失败');
        }
    } catch (error) {
        console.error('加载产品分类失败:', error);
        displayProductCategoriesError();
    }
}

// 显示产品分类
function displayProductCategories() {
    const container = document.getElementById('product-categories');
    if (!container) return;
    
    const categoryIcons = {
        'data_acquisition': 'fas fa-chart-line',
        'signal_generation': 'fas fa-wave-square',
        'digital_io': 'fas fa-microchip',
        'rf_microwave': 'fas fa-broadcast-tower'
    };
    
    const categoryColors = {
        'data_acquisition': 'blue',
        'signal_generation': 'green',
        'digital_io': 'purple',
        'rf_microwave': 'red'
    };
    
    // 国际化的产品分类名称和描述
    const categoryTranslations = {
        'data_acquisition': {
            name: getCurrentLanguage() === 'zh' ? '数据采集设备' : 'Data Acquisition',
            description: getCurrentLanguage() === 'zh' ? '高精度数据采集模块和设备' : 'High-precision data acquisition modules and devices'
        },
        'signal_generation': {
            name: getCurrentLanguage() === 'zh' ? '信号发生' : 'Signal Generation',
            description: getCurrentLanguage() === 'zh' ? '任意波形和信号发生器模块' : 'Arbitrary waveform and signal generator modules'
        },
        'digital_io': {
            name: getCurrentLanguage() === 'zh' ? '数字I/O' : 'Digital I/O',
            description: getCurrentLanguage() === 'zh' ? '高速数字I/O和控制模块' : 'High-speed digital I/O and control modules'
        },
        'rf_microwave': {
            name: getCurrentLanguage() === 'zh' ? '射频微波' : 'RF & Microwave',
            description: getCurrentLanguage() === 'zh' ? '射频微波测试和分析设备' : 'RF microwave test and analysis equipment'
        },
        'digital_multimeter': {
            name: getCurrentLanguage() === 'zh' ? '数字万用表' : 'Digital Multimeter',
            description: getCurrentLanguage() === 'zh' ? '高精度数字万用表模块' : 'High-precision digital multimeter modules'
        },
        'distributed_acquisition': {
            name: getCurrentLanguage() === 'zh' ? '分布式采集' : 'Distributed Acquisition',
            description: getCurrentLanguage() === 'zh' ? '分布式数据采集系统' : 'Distributed data acquisition systems'
        },
        'educational_kit': {
            name: getCurrentLanguage() === 'zh' ? '教育套件' : 'Educational Kit',
            description: getCurrentLanguage() === 'zh' ? '专为教学和科研设计的实验套件' : 'Experimental kits designed for education and research'
        },
        'educational_kits': {
            name: getCurrentLanguage() === 'zh' ? '教育套件' : 'Educational Kit',
            description: getCurrentLanguage() === 'zh' ? '专为教学和科研设计的实验套件' : 'Experimental kits designed for education and research'
        },
        'oscilloscope': {
            name: getCurrentLanguage() === 'zh' ? '示波器' : 'Oscilloscope',
            description: getCurrentLanguage() === 'zh' ? '高性能数字示波器模块' : 'High-performance digital oscilloscope modules'
        },
        'measurement_platform': {
            name: getCurrentLanguage() === 'zh' ? '锐视测控平台' : 'SeeSharp Platform',
            description: getCurrentLanguage() === 'zh' ? '基于C#/.NET的测控解决方案' : 'C#/.NET based test & measurement solution'
        },
        'seesharp_platform': {
            name: getCurrentLanguage() === 'zh' ? '锐视测控平台' : 'SeeSharp Platform',
            description: getCurrentLanguage() === 'zh' ? '基于C#/.NET的测控解决方案' : 'C#/.NET based test & measurement solution'
        },
        // 添加更多可能的分类映射
        '数字万用表': {
            name: getCurrentLanguage() === 'zh' ? '数字万用表' : 'Digital Multimeter',
            description: getCurrentLanguage() === 'zh' ? '高精度数字万用表模块' : 'High-precision digital multimeter modules'
        },
        '分布式采集': {
            name: getCurrentLanguage() === 'zh' ? '分布式采集' : 'Distributed Acquisition',
            description: getCurrentLanguage() === 'zh' ? '分布式数据采集系统' : 'Distributed data acquisition systems'
        },
        '教育套件': {
            name: getCurrentLanguage() === 'zh' ? '教育套件' : 'Educational Kit',
            description: getCurrentLanguage() === 'zh' ? '专为教学和科研设计的实验套件' : 'Experimental kits designed for education and research'
        },
        '示波器': {
            name: getCurrentLanguage() === 'zh' ? '示波器' : 'Oscilloscope',
            description: getCurrentLanguage() === 'zh' ? '高性能数字示波器模块' : 'High-performance digital oscilloscope modules'
        },
        '锐视测控平台': {
            name: getCurrentLanguage() === 'zh' ? '锐视测控平台' : 'SeeSharp Platform',
            description: getCurrentLanguage() === 'zh' ? '基于C#/.NET的测控解决方案' : 'C#/.NET based test & measurement solution'
        }
    };
    
    container.innerHTML = '';
    
    Object.entries(productCategories).forEach(([categoryId, category]) => {
        const icon = categoryIcons[categoryId] || 'fas fa-cog';
        const color = categoryColors[categoryId] || 'gray';
        const productCount = category.products ? category.products.length : 0;
        
        // 使用国际化的名称和描述
        const translation = categoryTranslations[categoryId];
        const displayName = translation ? translation.name : category.name;
        const displayDescription = translation ? translation.description : category.description;
        const countText = getCurrentLanguage() === 'zh' ? `${productCount} 个产品` : `${productCount} ${t('home.products.count')}`;
        
        const categoryCard = document.createElement('div');
        categoryCard.className = 'bg-white rounded-lg shadow-lg card-hover cursor-pointer overflow-hidden';
        categoryCard.onclick = () => showCategoryProducts(categoryId, category);
        
        categoryCard.innerHTML = `
            <div class="bg-${color}-100 p-8 text-center">
                <div class="bg-${color}-500 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                    <i class="${icon} text-white text-2xl"></i>
                </div>
                <h3 class="text-xl font-bold text-gray-800 mb-2">${displayName}</h3>
                <p class="text-gray-600 text-sm">${displayDescription}</p>
            </div>
            <div class="p-6">
                <div class="flex justify-between items-center">
                    <span class="text-sm text-gray-500">${countText}</span>
                    <i class="fas fa-arrow-right text-${color}-500"></i>
                </div>
            </div>
        `;
        
        container.appendChild(categoryCard);
    });
}

// 显示产品分类错误
function displayProductCategoriesError() {
    const container = document.getElementById('product-categories');
    if (!container) return;
    
    container.innerHTML = `
        <div class="col-span-full text-center py-12">
            <i class="fas fa-exclamation-triangle text-gray-400 text-4xl mb-4"></i>
            <h3 class="text-xl font-semibold text-gray-600 mb-2">${t('home.products.error')}</h3>
            <p class="text-gray-500 mb-4">${t('home.products.retry')}</p>
            <a href="https://www.jytek.com" target="_blank" class="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg">
                ${t('home.products.visitWebsite')}
            </a>
        </div>
    `;
}

// 显示分类产品
function showCategoryProducts(categoryId, category) {
    // 创建产品展示模态框
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 flex items-center justify-center z-50 p-4';
    modal.innerHTML = `
        <div class="fixed inset-0 bg-black opacity-50"></div>
        <div class="bg-white rounded-lg shadow-xl z-10 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            <div class="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6">
                <div class="flex justify-between items-center">
                    <div>
                        <h2 class="text-3xl font-bold mb-2">${category.name}</h2>
                        <p class="text-blue-100">${category.description}</p>
                    </div>
                    <button class="text-white hover:text-gray-200" onclick="closeModal(this)">
                        <i class="fas fa-times text-2xl"></i>
                    </button>
                </div>
            </div>
            
            <div class="p-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6" id="category-products">
                    ${generateProductCards(category.products || [])}
                </div>
                
                <div class="mt-8 text-center">
                    <p class="text-gray-600 mb-4">需要更多产品信息或技术支持？</p>
                    <a href="https://www.jytek.com" target="_blank" class="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg">
                        <i class="fas fa-external-link-alt mr-2"></i>访问简仪科技官网
                    </a>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // 点击背景关闭模态框
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            document.body.removeChild(modal);
        }
    });
    
    // 加载智能产品推荐
    loadSmartProductRecommendations(question, data.content);
}

// 加载智能产品推荐
async function loadSmartProductRecommendations(question, answer) {
    try {
        const response = await fetch('/api/llm/product-recommendation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: question,
                answer: answer,
                context: 'smart_recommendation'
            })
        });
        
        const data = await response.json();
        
        const container = document.getElementById('smart-product-recommendations');
        if (data.success && data.recommendations && data.recommendations.length > 0) {
            container.innerHTML = data.recommendations.map(product => `
                <div class="bg-white rounded-lg p-4 border border-gray-200 hover:border-blue-300 transition-colors">
                    <div class="flex items-start space-x-4">
                        <div class="bg-blue-100 w-12 h-12 rounded-lg flex items-center justify-center flex-shrink-0">
                            <i class="fas fa-microchip text-blue-600 text-lg"></i>
                        </div>
                        <div class="flex-1">
                            <h4 class="font-semibold text-gray-800 mb-2">${product.name}</h4>
                            <p class="text-sm text-gray-600 mb-3">${product.description}</p>
                            
                            <!-- 产品特点 -->
                            <div class="flex flex-wrap gap-2 mb-3">
                                ${(product.features || []).map(feature => 
                                    `<span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">${feature}</span>`
                                ).join('')}
                            </div>
                            
                            <!-- 推荐理由 -->
                            <div class="bg-green-50 p-3 rounded-lg mb-3">
                                <p class="text-sm text-green-800">
                                    <i class="fas fa-lightbulb mr-1"></i>
                                    <strong>推荐理由：</strong>${product.recommendation_reason}
                                </p>
                            </div>
                            
                            <!-- 操作按钮 -->
                            <div class="flex space-x-2">
                                <button onclick="askProductQuestion('${product.name}')" class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm">
                                    <i class="fas fa-question-circle mr-1"></i>了解详情
                                </button>
                                <button onclick="requestQuote('${product.name}')" class="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-sm">
                                    <i class="fas fa-calculator mr-1"></i>获取报价
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `).join('');
        } else {
            // 如果没有推荐结果，显示通用产品分类
            container.innerHTML = `
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="bg-white rounded-lg p-4 border border-gray-200 text-center">
                        <div class="bg-blue-100 w-12 h-12 rounded-lg flex items-center justify-center mx-auto mb-3">
                            <i class="fas fa-chart-line text-blue-600 text-lg"></i>
                        </div>
                        <h4 class="font-semibold text-gray-800 mb-2">数据采集模块</h4>
                        <p class="text-sm text-gray-600 mb-3">高精度多通道数据采集解决方案</p>
                        <button onclick="showCategoryProducts('data_acquisition', {name: '数据采集', description: '高精度数据采集模块'})" class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm">
                            查看产品
                        </button>
                    </div>
                    
                    <div class="bg-white rounded-lg p-4 border border-gray-200 text-center">
                        <div class="bg-green-100 w-12 h-12 rounded-lg flex items-center justify-center mx-auto mb-3">
                            <i class="fas fa-wave-square text-green-600 text-lg"></i>
                        </div>
                        <h4 class="font-semibold text-gray-800 mb-2">信号发生器</h4>
                        <p class="text-sm text-gray-600 mb-3">多功能信号发生与控制模块</p>
                        <button onclick="showCategoryProducts('signal_generation', {name: '信号发生', description: '信号发生器模块'})" class="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-sm">
                            查看产品
                        </button>
                    </div>
                    
                    <div class="bg-white rounded-lg p-4 border border-gray-200 text-center">
                        <div class="bg-purple-100 w-12 h-12 rounded-lg flex items-center justify-center mx-auto mb-3">
                            <i class="fas fa-microchip text-purple-600 text-lg"></i>
                        </div>
                        <h4 class="font-semibold text-gray-800 mb-2">锐视测控平台</h4>
                        <p class="text-sm text-gray-600 mb-3">AI增强的开源测控软件平台</p>
                        <a href="ruishi-platform.html" class="bg-purple-600 hover:bg-purple-700 text-white px-3 py-1 rounded text-sm inline-block">
                            了解详情
                        </a>
                    </div>
                    
                    <div class="bg-white rounded-lg p-4 border border-gray-200 text-center">
                        <div class="bg-red-100 w-12 h-12 rounded-lg flex items-center justify-center mx-auto mb-3">
                            <i class="fas fa-cogs text-red-600 text-lg"></i>
                        </div>
                        <h4 class="font-semibold text-gray-800 mb-2">定制方案</h4>
                        <p class="text-sm text-gray-600 mb-3">根据需求定制PXI测控方案</p>
                        <button onclick="showSolutionBuilder()" class="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded text-sm">
                            方案配置
                        </button>
                    </div>
                </div>
            `;
        }
    } catch (error) {
        console.error('加载产品推荐失败:', error);
        const container = document.getElementById('smart-product-recommendations');
        container.innerHTML = `
            <div class="text-center py-4">
                <i class="fas fa-exclamation-triangle text-gray-400 text-2xl mb-2"></i>
                <p class="text-gray-500">产品推荐加载失败，请稍后重试</p>
                <button onclick="loadSmartProductRecommendations('${question}', '${answer}')" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg mt-2">
                    重新加载
                </button>
            </div>
        `;
    }
}

// 请求报价
function requestQuote(productName) {
    const question = `我想了解${productName}的详细报价和采购信息，包括技术规格、价格和交付周期`;
    
    // 关闭当前模态框
    const modal = document.querySelector('.fixed.inset-0');
    if (modal) {
        document.body.removeChild(modal);
    }
    
    // 设置搜索框内容并触发搜索
    const searchInput = document.getElementById('ai-search-input');
    if (searchInput) {
        searchInput.value = question;
        handleAISearch();
    }
}

// 生成产品卡片
function generateProductCards(products) {
    if (!products || products.length === 0) {
        return `
            <div class="col-span-full text-center py-8">
                <i class="fas fa-box-open text-gray-400 text-4xl mb-4"></i>
                <p class="text-gray-500">该分类暂无产品信息</p>
            </div>
        `;
    }
    
    return products.map(product => `
        <div class="bg-gray-50 rounded-lg p-6 card-hover">
            <h3 class="text-xl font-bold text-gray-800 mb-2">${product.name}</h3>
            <p class="text-sm text-blue-600 mb-3">${product.category}</p>
            <p class="text-gray-600 mb-4">${product.description}</p>
            
            <div class="space-y-2 mb-4">
                ${Object.entries(product.specifications || {}).map(([key, value]) => 
                    `<div class="flex justify-between text-sm">
                        <span class="text-gray-500">${key}:</span>
                        <span class="font-medium">${value}</span>
                    </div>`
                ).join('')}
            </div>
            
            <div class="flex flex-wrap gap-2 mb-4">
                ${(product.applications || []).map(app => 
                    `<span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">${app}</span>`
                ).join('')}
            </div>
            
            <div class="flex space-x-2">
                <button onclick="askProductQuestion('${product.name}')" class="flex-1 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded text-sm">
                    <i class="fas fa-question-circle mr-1"></i>咨询
                </button>
                <button onclick="compareProduct('${product.id}')" class="flex-1 bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded text-sm">
                    <i class="fas fa-balance-scale mr-1"></i>对比
                </button>
            </div>
        </div>
    `).join('');
}

// 关闭模态框
function closeModal(button) {
    const modal = button.closest('.fixed');
    if (modal) {
        document.body.removeChild(modal);
    }
}

// 询问产品问题
function askProductQuestion(productName) {
    const question = `请详细介绍${productName}的技术特点、应用场景和选型建议`;
    const answerUrl = `/static/answer.html?q=${encodeURIComponent(question)}`;
    window.open(answerUrl, '_blank');
}

// 产品对比
function compareProduct(productId) {
    // 这里可以实现产品对比功能
    showNotification('产品对比功能开发中，请访问官网获取详细对比信息', 'info');
}

// 快速提问
function askQuestion(question) {
    const answerUrl = `/static/answer.html?q=${encodeURIComponent(question)}`;
    window.open(answerUrl, '_blank');
}

// 显示产品中心
function showProductCenter() {
    document.getElementById('products').scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

// 显示方案构建器
function showSolutionBuilder() {
    // 创建方案构建器模态框
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 flex items-center justify-center z-50 p-4';
    modal.innerHTML = `
        <div class="fixed inset-0 bg-black opacity-50"></div>
        <div class="bg-white rounded-lg shadow-xl z-10 w-full max-w-2xl">
            <div class="bg-gradient-to-r from-green-600 to-blue-600 text-white p-6">
                <div class="flex justify-between items-center">
                    <div>
                        <h2 class="text-2xl font-bold mb-2">${t('solutionBuilder.title')}</h2>
                        <p class="text-green-100">${t('solutionBuilder.subtitle')}</p>
                    </div>
                    <button class="text-white hover:text-gray-200" onclick="closeModal(this)">
                        <i class="fas fa-times text-xl"></i>
                    </button>
                </div>
            </div>
            
            <div class="p-6">
                <form id="solution-form" class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">${t('solutionBuilder.measurementType')}</label>
                        <select name="measurement_type" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                            <option value="">${t('solutionBuilder.options.measurementTypes.placeholder')}</option>
                            <option value="数据采集">${t('solutionBuilder.options.measurementTypes.dataAcquisition')}</option>
                            <option value="信号发生">${t('solutionBuilder.options.measurementTypes.signalGeneration')}</option>
                            <option value="射频测试">${t('solutionBuilder.options.measurementTypes.rfTest')}</option>
                            <option value="数字I/O">${t('solutionBuilder.options.measurementTypes.digitalIO')}</option>
                            <option value="混合信号">${t('solutionBuilder.options.measurementTypes.mixedSignal')}</option>
                        </select>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">${t('solutionBuilder.channelCount')}</label>
                        <select name="channel_count" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                            <option value="">${t('solutionBuilder.options.channels.placeholder')}</option>
                            <option value="1-8">${t('solutionBuilder.options.channels.1-8')}</option>
                            <option value="9-16">${t('solutionBuilder.options.channels.9-16')}</option>
                            <option value="17-32">${t('solutionBuilder.options.channels.17-32')}</option>
                            <option value="32+">${t('solutionBuilder.options.channels.32+')}</option>
                        </select>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">${t('solutionBuilder.frequencyRange')}</label>
                        <select name="frequency_range" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                            <option value="">${t('solutionBuilder.options.frequency.placeholder')}</option>
                            <option value="DC-1MHz">${t('solutionBuilder.options.frequency.DC-1MHz')}</option>
                            <option value="1MHz-100MHz">${t('solutionBuilder.options.frequency.1MHz-100MHz')}</option>
                            <option value="100MHz-1GHz">${t('solutionBuilder.options.frequency.100MHz-1GHz')}</option>
                            <option value="1GHz+">${t('solutionBuilder.options.frequency.1GHz+')}</option>
                        </select>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">${t('solutionBuilder.accuracy')}</label>
                        <select name="accuracy_requirement" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                            <option value="">${t('solutionBuilder.options.accuracyLevels.placeholder')}</option>
                            <option value="标准">${t('solutionBuilder.options.accuracyLevels.standard')}</option>
                            <option value="高精度">${t('solutionBuilder.options.accuracyLevels.high')}</option>
                            <option value="超高精度">${t('solutionBuilder.options.accuracyLevels.ultraHigh')}</option>
                        </select>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">${t('solutionBuilder.budget')}</label>
                        <select name="budget_range" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                            <option value="">${t('solutionBuilder.options.budgetRanges.placeholder')}</option>
                            <option value="10万以下">${t('solutionBuilder.options.budgetRanges.under100k')}</option>
                            <option value="10-50万">${t('solutionBuilder.options.budgetRanges.100k-500k')}</option>
                            <option value="50-100万">${t('solutionBuilder.options.budgetRanges.500k-1m')}</option>
                            <option value="100万以上">${t('solutionBuilder.options.budgetRanges.over1m')}</option>
                        </select>
                    </div>
                    
                    <div class="flex space-x-4 pt-4">
                        <button type="button" onclick="generateSolution()" class="flex-1 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium">
                            <i class="fas fa-cogs mr-2"></i>${t('solutionBuilder.generate')}
                        </button>
                        <button type="button" onclick="closeModal(this)" class="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50">
                            ${t('solutionBuilder.cancel')}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
}

// 生成解决方案
async function generateSolution() {
    const form = document.getElementById('solution-form');
    const formData = new FormData(form);
    const params = new URLSearchParams();
    
    for (let [key, value] of formData.entries()) {
        if (value) {
            params.append(key, value);
        }
    }
    
    try {
        const response = await fetch(`/api/products/solution-builder?${params}`);
        const data = await response.json();
        
        if (data.success) {
            displaySolutionResult(data.solution);
        } else {
            throw new Error(data.error || '生成方案失败');
        }
    } catch (error) {
        console.error('生成方案失败:', error);
        showNotification('生成方案失败，请稍后重试', 'error');
    }
}

// 显示方案结果
function displaySolutionResult(solution) {
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 flex items-center justify-center z-50 p-4';
    modal.innerHTML = `
        <div class="fixed inset-0 bg-black opacity-50"></div>
        <div class="bg-white rounded-lg shadow-xl z-10 w-full max-w-3xl max-h-[90vh] overflow-y-auto">
            <div class="bg-gradient-to-r from-purple-600 to-blue-600 text-white p-6">
                <div class="flex justify-between items-center">
                    <div>
                        <h2 class="text-2xl font-bold mb-2">推荐方案</h2>
                        <p class="text-purple-100">基于您的需求生成的PXI系统配置</p>
                    </div>
                    <button class="text-white hover:text-gray-200" onclick="closeModal(this)">
                        <i class="fas fa-times text-xl"></i>
                    </button>
                </div>
            </div>
            
            <div class="p-6">
                <div class="space-y-6">
                    <!-- 机箱配置 -->
                    <div class="bg-gray-50 rounded-lg p-4">
                        <h3 class="text-lg font-bold text-gray-800 mb-3">
                            <i class="fas fa-server text-blue-600 mr-2"></i>机箱配置
                        </h3>
                        <div class="bg-white rounded p-4">
                            <h4 class="font-semibold">${solution.chassis.name}</h4>
                            <p class="text-gray-600 text-sm">${solution.chassis.description}</p>
                            <p class="text-blue-600 text-sm mt-2">推荐理由: ${solution.chassis.reason}</p>
                        </div>
                    </div>
                    
                    <!-- 控制器配置 -->
                    <div class="bg-gray-50 rounded-lg p-4">
                        <h3 class="text-lg font-bold text-gray-800 mb-3">
                            <i class="fas fa-microchip text-green-600 mr-2"></i>控制器配置
                        </h3>
                        <div class="bg-white rounded p-4">
                            <h4 class="font-semibold">${solution.controller.name}</h4>
                            <p class="text-gray-600 text-sm">${solution.controller.description}</p>
                            <p class="text-green-600 text-sm mt-2">推荐理由: ${solution.controller.reason}</p>
                        </div>
                    </div>
                    
                    <!-- 模块配置 -->
                    <div class="bg-gray-50 rounded-lg p-4">
                        <h3 class="text-lg font-bold text-gray-800 mb-3">
                            <i class="fas fa-puzzle-piece text-purple-600 mr-2"></i>功能模块
                        </h3>
                        <div class="space-y-3">
                            ${solution.modules.map(module => `
                                <div class="bg-white rounded p-4">
                                    <h4 class="font-semibold">${module.name}</h4>
                                    <p class="text-sm text-gray-500">${module.type}</p>
                                    <p class="text-purple-600 text-sm mt-2">推荐理由: ${module.reason}</p>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                    
                    <!-- 成本估算 -->
                    <div class="bg-yellow-50 rounded-lg p-4">
                        <h3 class="text-lg font-bold text-gray-800 mb-3">
                            <i class="fas fa-calculator text-yellow-600 mr-2"></i>成本估算
                        </h3>
                        <p class="text-gray-700">${solution.estimated_cost}</p>
                        <p class="text-yellow-600 text-sm mt-2">${solution.contact_info.message}</p>
                    </div>
                </div>
                
                <div class="mt-8 text-center">
                    <a href="${solution.contact_info.website}" target="_blank" class="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg mr-4">
                        <i class="fas fa-external-link-alt mr-2"></i>获取详细报价
                    </a>
                    <button onclick="askSolutionQuestion()" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg">
                        <i class="fas fa-question-circle mr-2"></i>咨询方案
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
}

// 咨询方案问题
function askSolutionQuestion() {
    const question = '我想了解更多关于PXI系统方案配置的信息，包括产品选型、系统集成和技术支持';
    const answerUrl = `/static/answer.html?q=${encodeURIComponent(question)}`;
    window.open(answerUrl, '_blank');
}

// 显示知识库
function showKnowledgeBase() {
    // 创建知识库模态框
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 flex items-center justify-center z-50 p-4';
    modal.innerHTML = `
        <div class="fixed inset-0 bg-black opacity-50"></div>
        <div class="bg-white rounded-lg shadow-xl z-10 w-full max-w-5xl max-h-[90vh] overflow-y-auto">
            <div class="bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-6">
                <div class="flex justify-between items-center">
                    <div>
                        <h2 class="text-2xl font-bold mb-2">${t('knowledgeBase.title')}</h2>
                        <p class="text-indigo-100">${t('knowledgeBase.subtitle')}</p>
                    </div>
                    <button class="text-white hover:text-gray-200" onclick="closeModal(this)">
                        <i class="fas fa-times text-xl"></i>
                    </button>
                </div>
            </div>
            
            <div class="p-6">
                <!-- 功能选项卡 -->
                <div class="flex border-b border-gray-200 mb-6">
                    <button class="px-4 py-2 border-b-2 border-indigo-600 text-indigo-600 font-medium" onclick="switchKnowledgeTab('search', this)">
                        <i class="fas fa-search mr-2"></i>搜索文档
                    </button>
                    <button class="px-4 py-2 text-gray-500 hover:text-gray-700" onclick="switchKnowledgeTab('upload', this)">
                        <i class="fas fa-upload mr-2"></i>上传文档
                    </button>
                    <button class="px-4 py-2 text-gray-500 hover:text-gray-700" onclick="switchKnowledgeTab('manage', this)">
                        <i class="fas fa-folder mr-2"></i>文档管理
                    </button>
                </div>
                
                <!-- 搜索文档选项卡 -->
                <div id="knowledge-search-tab" class="knowledge-tab">
                    <!-- 搜索框 -->
                    <div class="mb-6">
                        <div class="flex">
                            <input type="text" id="knowledge-search" placeholder="搜索技术文档、产品手册、应用笔记..." 
                                   class="flex-1 px-4 py-3 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-indigo-500">
                            <button onclick="searchKnowledge()" class="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-r-lg">
                                <i class="fas fa-search"></i>
                            </button>
                        </div>
                    </div>
                    
                    <!-- 文档分类 -->
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                        <div class="bg-blue-50 p-4 rounded-lg text-center cursor-pointer hover:bg-blue-100" onclick="searchKnowledgeByCategory('system_architecture')">
                            <i class="fas fa-sitemap text-blue-600 text-2xl mb-2"></i>
                            <p class="text-sm font-medium">系统架构</p>
                        </div>
                        <div class="bg-green-50 p-4 rounded-lg text-center cursor-pointer hover:bg-green-100" onclick="searchKnowledgeByCategory('product_specs')">
                            <i class="fas fa-file-alt text-green-600 text-2xl mb-2"></i>
                            <p class="text-sm font-medium">产品规格</p>
                        </div>
                        <div class="bg-purple-50 p-4 rounded-lg text-center cursor-pointer hover:bg-purple-100" onclick="searchKnowledgeByCategory('software_development')">
                            <i class="fas fa-code text-purple-600 text-2xl mb-2"></i>
                            <p class="text-sm font-medium">软件开发</p>
                        </div>
                        <div class="bg-red-50 p-4 rounded-lg text-center cursor-pointer hover:bg-red-100" onclick="searchKnowledgeByCategory('application_notes')">
                            <i class="fas fa-lightbulb text-red-600 text-2xl mb-2"></i>
                            <p class="text-sm font-medium">应用笔记</p>
                        </div>
                    </div>
                    
                    <!-- 搜索结果 -->
                    <div id="knowledge-search-results" class="hidden">
                        <h3 class="text-lg font-bold text-gray-800 mb-4">搜索结果</h3>
                        <div id="search-results-list"></div>
                    </div>
                    
                    <!-- 热门文档 -->
                    <div class="mb-6">
                        <h3 class="text-lg font-bold text-gray-800 mb-4">热门文档</h3>
                        <div id="popular-documents" class="space-y-3">
                            <div class="text-center py-4">
                                <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-600 mx-auto mb-2"></div>
                                <span class="text-gray-600">加载文档列表...</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- 上传文档选项卡 -->
                <div id="knowledge-upload-tab" class="knowledge-tab hidden">
                    <div class="max-w-2xl mx-auto">
                        <h3 class="text-lg font-bold text-gray-800 mb-4">上传技术文档</h3>
                        <form id="document-upload-form" class="space-y-4">
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">选择文件</label>
                                <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-indigo-500 transition-colors">
                                    <input type="file" id="document-file" name="file" accept=".pdf,.doc,.docx,.txt,.md" class="hidden" onchange="handleFileSelect(this)">
                                    <div id="file-drop-area" onclick="document.getElementById('document-file').click()">
                                        <i class="fas fa-cloud-upload-alt text-4xl text-gray-400 mb-4"></i>
                                        <p class="text-gray-600 mb-2">点击选择文件或拖拽文件到此处</p>
                                        <p class="text-sm text-gray-500">支持 PDF, Word, TXT, Markdown 格式</p>
                                    </div>
                                    <div id="file-info" class="hidden">
                                        <i class="fas fa-file text-2xl text-indigo-600 mb-2"></i>
                                        <p id="file-name" class="font-medium"></p>
                                        <p id="file-size" class="text-sm text-gray-500"></p>
                                    </div>
                                </div>
                            </div>
                            
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">文档分类</label>
                                <select name="category" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500">
                                    <option value="general">通用文档</option>
                                    <option value="system_architecture">系统架构</option>
                                    <option value="product_specs">产品规格</option>
                                    <option value="software_development">软件开发</option>
                                    <option value="application_notes">应用笔记</option>
                                    <option value="troubleshooting">故障排除</option>
                                </select>
                            </div>
                            
                            <div class="flex space-x-4">
                                <button type="submit" class="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-lg font-medium">
                                    <i class="fas fa-upload mr-2"></i>上传文档
                                </button>
                                <button type="button" onclick="resetUploadForm()" class="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50">
                                    重置
                                </button>
                            </div>
                        </form>
                        
                        <div id="upload-progress" class="hidden mt-4">
                            <div class="bg-gray-200 rounded-full h-2">
                                <div id="upload-progress-bar" class="bg-indigo-600 h-2 rounded-full transition-all duration-300" style="width: 0%"></div>
                            </div>
                            <p id="upload-status" class="text-sm text-gray-600 mt-2">上传中...</p>
                        </div>
                    </div>
                </div>
                
                <!-- 文档管理选项卡 -->
                <div id="knowledge-manage-tab" class="knowledge-tab hidden">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="text-lg font-bold text-gray-800">文档管理</h3>
                        <button onclick="refreshDocumentList()" class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg">
                            <i class="fas fa-sync-alt mr-2"></i>刷新
                        </button>
                    </div>
                    
                    <div id="document-list" class="space-y-3">
                        <div class="text-center py-8">
                            <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-600 mx-auto mb-2"></div>
                            <span class="text-gray-600">加载文档列表...</span>
                        </div>
                    </div>
                </div>
                
                <div class="text-center mt-6">
                    <p class="text-gray-600 mb-4">需要技术支持或更多资料？</p>
                    <a href="https://www.jytek.com" target="_blank" class="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg mr-4">
                        <i class="fas fa-external-link-alt mr-2"></i>访问简仪科技官网
                    </a>
                    <button onclick="askKnowledgeQuestion()" class="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-lg">
                        <i class="fas fa-question-circle mr-2"></i>AI技术咨询
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // 初始化知识库功能
    initializeKnowledgeBase();
}

// 搜索知识库
function searchKnowledge() {
    const searchInput = document.getElementById('knowledge-search');
    const query = searchInput.value.trim();
    
    if (!query) {
        showNotification('请输入搜索关键词', 'warning');
        return;
    }
    
    const question = `请在简仪科技的技术文档中搜索关于"${query}"的相关信息`;
    const answerUrl = `/static/answer.html?q=${encodeURIComponent(question)}`;
    window.open(answerUrl, '_blank');
}

// 按分类搜索知识库
function searchKnowledgeByCategory(category) {
    const question = `请介绍简仪科技PXI产品在"${category}"方面的技术资料和相关文档`;
    const answerUrl = `/static/answer.html?q=${encodeURIComponent(question)}`;
    window.open(answerUrl, '_blank');
}

// 询问文档问题
function askDocumentQuestion(documentTitle) {
    const question = `请详细介绍"${documentTitle}"这份技术文档的主要内容和关键技术点`;
    const answerUrl = `/static/answer.html?q=${encodeURIComponent(question)}`;
    window.open(answerUrl, '_blank');
}

// 询问知识库问题
function askKnowledgeQuestion() {
    const question = '我需要了解PXI技术相关的文档资料，请推荐一些重要的技术文档和学习资源';
    const answerUrl = `/static/answer.html?q=${encodeURIComponent(question)}`;
    window.open(answerUrl, '_blank');
}

// 知识库相关函数

// 初始化知识库
function initializeKnowledgeBase() {
    loadPopularDocuments();
    loadDocumentList();
    setupDocumentUpload();
}

// 切换知识库选项卡
function switchKnowledgeTab(tabName, button) {
    // 隐藏所有选项卡
    document.querySelectorAll('.knowledge-tab').forEach(tab => {
        tab.classList.add('hidden');
    });
    
    // 重置所有按钮样式
    button.parentElement.querySelectorAll('button').forEach(btn => {
        btn.className = 'px-4 py-2 text-gray-500 hover:text-gray-700';
    });
    
    // 激活当前按钮
    button.className = 'px-4 py-2 border-b-2 border-indigo-600 text-indigo-600 font-medium';
    
    // 显示对应选项卡
    document.getElementById(`knowledge-${tabName}-tab`).classList.remove('hidden');
}

// 加载热门文档
async function loadPopularDocuments() {
    try {
        const response = await fetch('/api/knowledge/documents?per_page=5');
        const data = await response.json();
        
        const container = document.getElementById('popular-documents');
        if (data.success && data.documents.length > 0) {
            container.innerHTML = data.documents.map(doc => `
                <div class="bg-gray-50 p-4 rounded-lg cursor-pointer hover:bg-gray-100" onclick="askDocumentQuestionById('${doc.doc_id}', '${doc.filename}')">
                    <h4 class="font-semibold text-gray-800">${doc.filename}</h4>
                    <p class="text-sm text-gray-600">${doc.content_summary}</p>
                    <div class="flex justify-between items-center mt-2">
                        <span class="text-xs text-blue-600">${doc.doc_type}</span>
                        <span class="text-xs text-gray-500">${doc.file_size}</span>
                    </div>
                </div>
            `).join('');
        } else {
            container.innerHTML = `
                <div class="text-center py-8">
                    <i class="fas fa-folder-open text-gray-400 text-4xl mb-4"></i>
                    <p class="text-gray-500">暂无文档，请先上传一些技术资料</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('加载热门文档失败:', error);
        document.getElementById('popular-documents').innerHTML = `
            <div class="text-center py-4">
                <p class="text-red-500">加载失败，请稍后重试</p>
            </div>
        `;
    }
}

// 加载文档列表
async function loadDocumentList() {
    try {
        const response = await fetch('/api/knowledge/documents');
        const data = await response.json();
        
        const container = document.getElementById('document-list');
        if (data.success && data.documents.length > 0) {
            container.innerHTML = data.documents.map(doc => `
                <div class="bg-white border border-gray-200 rounded-lg p-4">
                    <div class="flex justify-between items-start">
                        <div class="flex-1">
                            <h4 class="font-semibold text-gray-800">${doc.filename}</h4>
                            <p class="text-sm text-gray-600 mt-1">${doc.content_summary}</p>
                            <div class="flex items-center space-x-4 mt-2">
                                <span class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">${doc.doc_type}</span>
                                <span class="text-xs text-gray-500">${doc.file_size}</span>
                                <span class="text-xs text-gray-500">${new Date(doc.upload_time).toLocaleDateString()}</span>
                            </div>
                        </div>
                        <div class="flex space-x-2 ml-4">
                            <button onclick="askDocumentQuestionById('${doc.doc_id}', '${doc.filename}')" class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm">
                                <i class="fas fa-question-circle mr-1"></i>问答
                            </button>
                            <button onclick="deleteDocument('${doc.doc_id}')" class="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded text-sm">
                                <i class="fas fa-trash mr-1"></i>删除
                            </button>
                        </div>
                    </div>
                </div>
            `).join('');
        } else {
            container.innerHTML = `
                <div class="text-center py-8">
                    <i class="fas fa-folder-open text-gray-400 text-4xl mb-4"></i>
                    <p class="text-gray-500">暂无文档，请先上传一些技术资料</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('加载文档列表失败:', error);
        document.getElementById('document-list').innerHTML = `
            <div class="text-center py-4">
                <p class="text-red-500">加载失败，请稍后重试</p>
            </div>
        `;
    }
}

// 设置文档上传
function setupDocumentUpload() {
    const form = document.getElementById('document-upload-form');
    if (form) {
        form.addEventListener('submit', handleDocumentUpload);
    }
}

// 处理文件选择
function handleFileSelect(input) {
    const file = input.files[0];
    if (file) {
        const fileInfo = document.getElementById('file-info');
        const fileName = document.getElementById('file-name');
        const fileSize = document.getElementById('file-size');
        const dropArea = document.getElementById('file-drop-area');
        
        fileName.textContent = file.name;
        fileSize.textContent = `${(file.size / 1024 / 1024).toFixed(2)} MB`;
        
        dropArea.classList.add('hidden');
        fileInfo.classList.remove('hidden');
    }
}

// 处理文档上传
async function handleDocumentUpload(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const file = formData.get('file');
    
    if (!file || file.size === 0) {
        showNotification('请选择要上传的文件', 'warning');
        return;
    }
    
    // 显示上传进度
    const progressContainer = document.getElementById('upload-progress');
    const progressBar = document.getElementById('upload-progress-bar');
    const statusText = document.getElementById('upload-status');
    
    progressContainer.classList.remove('hidden');
    progressBar.style.width = '0%';
    statusText.textContent = '正在上传...';
    
    try {
        // 模拟上传进度
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += Math.random() * 30;
            if (progress > 90) progress = 90;
            progressBar.style.width = `${progress}%`;
        }, 200);
        
        const response = await fetch('/api/knowledge/upload', {
            method: 'POST',
            body: formData
        });
        
        clearInterval(progressInterval);
        progressBar.style.width = '100%';
        
        const data = await response.json();
        
        if (data.success) {
            statusText.textContent = '上传成功！';
            showNotification(data.message, 'success');
            
            // 重置表单
            resetUploadForm();
            
            // 刷新文档列表
            loadPopularDocuments();
            loadDocumentList();
            
            setTimeout(() => {
                progressContainer.classList.add('hidden');
            }, 2000);
        } else {
            throw new Error(data.error || '上传失败');
        }
    } catch (error) {
        console.error('文档上传失败:', error);
        statusText.textContent = '上传失败';
        showNotification(error.message || '文档上传失败，请稍后重试', 'error');
        
        setTimeout(() => {
            progressContainer.classList.add('hidden');
        }, 3000);
    }
}

// 重置上传表单
function resetUploadForm() {
    const form = document.getElementById('document-upload-form');
    if (form) {
        form.reset();
        
        const fileInfo = document.getElementById('file-info');
        const dropArea = document.getElementById('file-drop-area');
        
        fileInfo.classList.add('hidden');
        dropArea.classList.remove('hidden');
    }
}

// 刷新文档列表
function refreshDocumentList() {
    loadDocumentList();
    showNotification('文档列表已刷新', 'info');
}

// 基于文档ID询问问题
function askDocumentQuestionById(docId, filename) {
    const question = `请基于文档"${filename}"回答我的问题：这个文档的主要内容是什么？有哪些关键技术点？`;
    
    // 使用知识库API
    fetch('/api/knowledge/ask-document', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            doc_id: docId,
            question: question
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // 创建临时回答页面URL
            const answerUrl = `/static/answer.html?q=${encodeURIComponent(question)}&doc_id=${docId}`;
            window.open(answerUrl, '_blank');
        } else {
            showNotification(data.error || '文档问答失败', 'error');
        }
    })
    .catch(error => {
        console.error('文档问答失败:', error);
        showNotification('文档问答失败，请稍后重试', 'error');
    });
}

// 删除文档
async function deleteDocument(docId) {
    if (!confirm('确定要删除这个文档吗？此操作不可撤销。')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/knowledge/delete/${docId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(data.message, 'success');
            loadDocumentList();
            loadPopularDocuments();
        } else {
            throw new Error(data.error || '删除失败');
        }
    } catch (error) {
        console.error('删除文档失败:', error);
        showNotification(error.message || '删除文档失败，请稍后重试', 'error');
    }
}

// 显示通知
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = 'fixed bottom-4 right-4 px-6 py-3 rounded-lg shadow-lg z-50 transition-all duration-300';
    
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

// 显示答案模态框
function showAnswerModal(question, data) {
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 flex items-center justify-center z-50 p-4';
    modal.innerHTML = `
        <div class="fixed inset-0 bg-black opacity-50"></div>
        <div class="bg-white rounded-lg shadow-xl z-10 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            <div class="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6">
                <div class="flex justify-between items-center">
                    <div>
                        <h2 class="text-2xl font-bold mb-2">AI智能问答</h2>
                        <p class="text-blue-100">简仪科技锐视测控平台专业技术咨询</p>
                    </div>
                    <button class="text-white hover:text-gray-200" onclick="closeModal(this)">
                        <i class="fas fa-times text-xl"></i>
                    </button>
                </div>
            </div>
            
            <div class="p-6">
                <!-- 问题显示 -->
                <div class="bg-gray-50 rounded-lg p-4 mb-6">
                    <h3 class="text-lg font-semibold text-gray-800 mb-2">
                        <i class="fas fa-question-circle text-blue-600 mr-2"></i>您的问题
                    </h3>
                    <p class="text-gray-700">${question}</p>
                </div>
                
                <!-- AI回答 -->
                <div class="bg-white border border-gray-200 rounded-lg p-6 mb-6">
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">
                        <i class="fas fa-robot text-green-600 mr-2"></i>AI专业回答
                    </h3>
                    <div class="prose max-w-none text-gray-700">
                        ${formatAnswerContent(data.content)}
                    </div>
                </div>
                
                <!-- 智能产品推荐模块 -->
                <div class="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6 mb-6">
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">
                        <i class="fas fa-microchip text-blue-600 mr-2"></i>相关简仪科技产品推荐
                    </h3>
                    <div id="smart-product-recommendations" class="space-y-4">
                        <div class="text-center py-4">
                            <div class="animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-blue-600 mx-auto mb-2"></div>
                            <span class="text-gray-600 text-sm">AI正在分析并推荐相关产品...</span>
                        </div>
                    </div>
                </div>
                
                <!-- 操作按钮 -->
                <div class="flex flex-wrap gap-3 justify-center">
                    <button onclick="copyAnswer('${question}', '${data.content.replace(/'/g, "\\'")}'" class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg">
                        <i class="fas fa-copy mr-2"></i>复制回答
                    </button>
                    <button onclick="askFollowUpQuestion()" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg">
                        <i class="fas fa-comment mr-2"></i>追问
                    </button>
                    <a href="https://www.jytek.com" target="_blank" class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg">
                        <i class="fas fa-external-link-alt mr-2"></i>访问官网
                    </a>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // 点击背景关闭模态框
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            document.body.removeChild(modal);
        }
    });
    
    // 加载智能产品推荐
    loadSmartProductRecommendations(question, data.content);
}

// 格式化答案内容
function formatAnswerContent(content) {
    // 将换行符转换为HTML换行
    let formatted = content.replace(/\n/g, '<br>');
    
    // 处理代码块
    formatted = formatted.replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre class="bg-gray-100 p-4 rounded-lg overflow-x-auto"><code>$2</code></pre>');
    
    // 处理行内代码
    formatted = formatted.replace(/`([^`]+)`/g, '<code class="bg-gray-100 px-2 py-1 rounded">$1</code>');
    
    // 处理粗体
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // 处理列表
    formatted = formatted.replace(/^\* (.+)$/gm, '<li>$1</li>');
    formatted = formatted.replace(/(<li>.*<\/li>)/s, '<ul class="list-disc list-inside space-y-1">$1</ul>');
    
    return formatted;
}

// 复制答案
function copyAnswer(question, answer) {
    const text = `问题：${question}\n\n回答：${answer}`;
    navigator.clipboard.writeText(text).then(() => {
        showNotification('回答已复制到剪贴板', 'success');
    }).catch(() => {
        showNotification('复制失败，请手动复制', 'error');
    });
}

// 追问功能
function askFollowUpQuestion() {
    const input = prompt(t('aiModal.followUpPrompt'));
    if (input && input.trim()) {
        // 关闭当前模态框
        const modal = document.querySelector('.fixed.inset-0');
        if (modal) {
            document.body.removeChild(modal);
        }
        
        // 设置搜索框内容并触发搜索
        const searchInput = document.getElementById('ai-search-input');
        if (searchInput) {
            searchInput.value = input.trim();
            handleAISearch();
        }
    }
}

// 更新动态内容（语言切换时调用）
function updateDynamicContent() {
    // 更新搜索框提示
    const searchInput = document.getElementById('ai-search-input');
    if (searchInput) {
        searchInput.placeholder = t('home.aiSearch.placeholder');
    }
    
    // 更新搜索按钮
    const searchBtn = document.getElementById('ai-search-btn');
    if (searchBtn && !searchBtn.disabled) {
        searchBtn.innerHTML = `<i class="fas fa-search mr-2"></i>${t('home.aiSearch.button')}`;
    }
    
    // 更新动态提示文字
    const tipElement = document.querySelector('.typing-animation');
    if (tipElement && tipElement.textContent.includes('AI正在等待') || tipElement.textContent.includes('AI is waiting')) {
        tipElement.textContent = t('home.aiSearch.waiting');
    }
    
    // 重新加载产品分类（使用新语言）
    displayProductCategories();
    
    // 更新通知消息
    updateNotificationMessages();
}

// 更新通知消息
function updateNotificationMessages() {
    // 这个函数用于更新已显示的通知消息的语言
    // 由于通知是临时的，主要用于未来的通知
}

// 语言感知的通知函数
function showNotification(messageKey, type = 'info', params = {}) {
    // 如果messageKey是翻译键，使用t()函数翻译
    let message;
    if (messageKey.includes('.')) {
        message = t(messageKey, params);
    } else {
        // 向后兼容，直接使用消息文本
        message = messageKey;
    }
    
    const notification = document.createElement('div');
    notification.className = 'fixed bottom-4 right-4 px-6 py-3 rounded-lg shadow-lg z-50 transition-all duration-300';
    
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

// 追问功能的辅助函数
function askFollowUpQuestion() {
    const input = prompt('请输入您的追问：');
    if (input && input.trim()) {
        // 关闭当前模态框
        const modal = document.querySelector('.fixed.inset-0');
        if (modal) {
            document.body.removeChild(modal);
        }
        
        // 设置搜索框内容并触发搜索
        const searchInput = document.getElementById('ai-search-input');
        if (searchInput) {
            searchInput.value = input.trim();
            handleAISearch();
        }
    }
}

// 获取当前语言的辅助函数
function getCurrentLanguage() {
    return currentLanguage || 'zh';
}
