/**
 * 产品页面增强功能模块
 * 添加高级筛选、排序、对比功能
 */

// 增强的筛选配置
const ENHANCED_FILTERS = {
    // 新增筛选类型
    advancedFilters: {
        brand: [], // 品牌筛选
        series: [], // 产品系列
        interface: [], // 接口类型
        power: [], // 功耗范围
        temperature: [], // 工作温度范围
        certification: [] // 认证标准
    },

    // 数值范围筛选
    numericRanges: {
        frequency: { min: 0, max: 1000000, unit: 'Hz' }, // 频率范围
        voltage: { min: 0, max: 1000, unit: 'V' }, // 电压范围
        current: { min: 0, max: 100, unit: 'A' }, // 电流范围
        accuracy: { min: 0, max: 100, unit: '%' } // 精度范围
    },

    // 多选筛选
    multiSelectFilters: {
        features: [], // 功能特性
        applications: [], // 应用场景
        compatibility: [] // 兼容性
    }
};

// 增强的排序选项
const ENHANCED_SORTING = {
    options: [
        { value: 'name', label: '产品名称' },
        { value: 'price-asc', label: '价格从低到高' },
        { value: 'price-desc', label: '价格从高到低' },
        { value: 'popularity', label: '热门程度' },
        { value: 'rating', label: '用户评分' },
        { value: 'newest', label: '最新上架' },
        { value: 'stock', label: '库存状态' },
        { value: 'discount', label: '折扣力度' }
    ]
};

// 增强的对比功能
class EnhancedCompareManager {
    constructor() {
        this.compareData = new Map();
        this.maxCompareItems = 5;
        this.compareTemplates = {
            basic: ['name', 'price', 'category', 'stock_status'],
            technical: ['channels', 'resolution', 'sampling_rate', 'bandwidth'],
            detailed: ['dimensions', 'weight', 'power_consumption', 'operating_temp']
        };
    }

    // 添加产品到对比
    addToCompare(product, template = 'basic') {
        if (this.compareData.size >= this.maxCompareItems) {
            return { success: false, message: `最多只能对比${this.maxCompareItems}个产品` };
        }

        this.compareData.set(product.id, {
            ...product,
            template: template,
            addedAt: Date.now()
        });

        return { success: true, message: '已添加到对比列表' };
    }

    // 生成对比报告
    generateCompareReport(products, template = 'basic') {
        const specs = this.compareTemplates[template];
        const report = {
            summary: this.generateSummary(products),
            comparison: this.generateComparisonTable(products, specs),
            recommendations: this.generateRecommendations(products)
        };

        return report;
    }

    // 生成对比摘要
    generateSummary(products) {
        const priceRange = {
            min: Math.min(...products.map(p => p.price || 0)),
            max: Math.max(...products.map(p => p.price || 0))
        };

        const stockSummary = {
            available: products.filter(p => p.stock_status === '现货').length,
            limited: products.filter(p => p.stock_status === '预订').length,
            unavailable: products.filter(p => !['现货', '预订'].includes(p.stock_status)).length
        };

        return {
            totalProducts: products.length,
            priceRange,
            stockSummary,
            bestValue: this.findBestValue(products),
            mostPopular: this.findMostPopular(products)
        };
    }

    // 生成对比表格
    generateComparisonTable(products, specs) {
        const table = {
            headers: products.map(p => p.name || p.part_number),
            rows: []
        };

        specs.forEach(spec => {
            const row = {
                name: this.getSpecLabel(spec),
                values: products.map(p => this.getSpecValue(p, spec))
            };
            table.rows.push(row);
        });

        return table;
    }

    // 生成推荐
    generateRecommendations(products) {
        const recommendations = [];

        // 性价比推荐
        const valueProduct = products.find(p => p.price && p.rating > 4);
        if (valueProduct) {
            recommendations.push({
                type: 'value',
                product: valueProduct,
                reason: '高性价比选择'
            });
        }

        // 性能推荐
        const performanceProduct = products.reduce((best, current) => {
            return (current.specifications?.performance || 0) > (best.specifications?.performance || 0) ? current : best;
        });
        if (performanceProduct) {
            recommendations.push({
                type: 'performance',
                product: performanceProduct,
                reason: '最佳性能选择'
            });
        }

        return recommendations;
    }

    // 工具方法
    getSpecLabel(spec) {
        const labels = {
            name: '产品名称',
            price: '价格',
            category: '分类',
            stock_status: '库存状态',
            channels: '通道数',
            resolution: '分辨率',
            sampling_rate: '采样率',
            bandwidth: '带宽',
            dimensions: '尺寸',
            weight: '重量',
            power_consumption: '功耗',
            operating_temp: '工作温度'
        };
        return labels[spec] || spec;
    }

    getSpecValue(product, spec) {
        if (spec === 'price') return product.price ? `¥${product.price.toLocaleString()}` : '询价';
        if (spec === 'stock_status') return product.stock_status || '未知';
        return product[spec] || product.specifications?.[spec] || '-';
    }

    findBestValue(products) {
        return products.reduce((best, current) => {
            const bestValue = (best.rating || 0) / (best.price || 1);
            const currentValue = (current.rating || 0) / (current.price || 1);
            return currentValue > bestValue ? current : best;
        });
    }

    findMostPopular(products) {
        return products.reduce((popular, current) => {
            return (current.popularity || 0) > (popular.popularity || 0) ? current : popular;
        });
    }
}

// 增强的筛选管理器（独立实现）
class EnhancedFilterManager {
    constructor(dataManager) {
        this.dataManager = dataManager;
        this.advancedFilters = new Map();
        this.savedFilters = [];
        this.initializeAdvancedFilters();
    }

    initializeAdvancedFilters() {
        this.createAdvancedFilterUI();
        this.loadSavedFilters();
    }

    createAdvancedFilterUI() {
        const advancedFilterHTML = `
            <div class="advanced-filters-section">
                <h3 class="text-sm font-medium text-gray-900 mb-3">高级筛选</h3>
                
                <!-- 品牌筛选 -->
                <div class="mb-4">
                    <label class="block text-xs text-gray-600 mb-1">品牌</label>
                    <select id="brand-filter" class="w-full text-sm border border-gray-300 rounded-lg px-3 py-2">
                        <option value="">所有品牌</option>
                    </select>
                </div>

                <!-- 接口类型 -->
                <div class="mb-4">
                    <label class="block text-xs text-gray-600 mb-1">接口类型</label>
                    <div class="space-y-1">
                        <label class="flex items-center">
                            <input type="checkbox" class="interface-filter" value="USB">
                            <span class="ml-2 text-xs text-gray-700">USB</span>
                        </label>
                        <label class="flex items-center">
                            <input type="checkbox" class="interface-filter" value="Ethernet">
                            <span class="ml-2 text-xs text-gray-700">以太网</span>
                        </label>
                        <label class="flex items-center">
                            <input type="checkbox" class="interface-filter" value="PCIe">
                            <span class="ml-2 text-xs text-gray-700">PCIe</span>
                        </label>
                    </div>
                </div>

                <!-- 功耗范围 -->
                <div class="mb-4">
                    <label class="block text-xs text-gray-600 mb-1">功耗范围 (W)</label>
                    <div class="range-slider">
                        <input type="range" id="power-min" min="0" max="100" value="0" class="w-full">
                        <input type="range" id="power-max" min="0" max="100" value="100" class="w-full">
                        <div class="flex justify-between text-xs text-gray-500 mt-1">
                            <span id="power-min-value">0W</span>
                            <span id="power-max-value">100W</span>
                        </div>
                    </div>
                </div>

                <!-- 保存筛选 -->
                <div class="mb-4">
                    <button id="save-filter-btn" class="w-full text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 py-2 px-3 rounded-lg">
                        <i class="fas fa-save mr-1"></i>保存当前筛选
                    </button>
                </div>

                <!-- 已保存的筛选 -->
                <div id="saved-filters" class="mb-4">
                    <h4 class="text-xs font-medium text-gray-600 mb-2">已保存的筛选</h4>
                    <div id="saved-filters-list" class="space-y-1"></div>
                </div>
            </div>
        `;

        // 插入到现有筛选面板中
        const filterPanel = document.querySelector('.bg-white.rounded-lg.shadow-sm.p-6');
        if (filterPanel) {
            const advancedSection = document.createElement('div');
            advancedSection.innerHTML = advancedFilterHTML;
            filterPanel.appendChild(advancedSection);
        }
    }

    // 保存当前筛选条件
    saveCurrentFilter(name) {
        const currentFilters = {
            name: name,
            filters: this.getCurrentFilters(),
            timestamp: Date.now()
        };
        
        this.savedFilters.push(currentFilters);
        if (window.Utils) {
            window.Utils.storage.set('saved_filters', this.savedFilters);
        }
        this.renderSavedFilters();
    }

    // 加载保存的筛选
    loadSavedFilters() {
        if (window.Utils) {
            this.savedFilters = window.Utils.storage.get('saved_filters') || [];
        }
        this.renderSavedFilters();
    }

    // 渲染保存的筛选
    renderSavedFilters() {
        const container = document.getElementById('saved-filters-list');
        if (!container) return;

        const html = this.savedFilters.map((filter, index) => `
            <div class="saved-filter-item flex items-center justify-between p-2 bg-gray-50 rounded">
                <span class="text-xs">${filter.name}</span>
                <div class="flex space-x-1">
                    <button onclick="applySavedFilter(${index})" class="text-xs text-jytek-blue hover:text-jytek-light-blue">
                        <i class="fas fa-play"></i>
                    </button>
                    <button onclick="deleteSavedFilter(${index})" class="text-xs text-red-500 hover:text-red-700">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `).join('');

        container.innerHTML = html;
    }

    // 获取当前所有筛选条件
    getCurrentFilters() {
        return {
            advanced: Object.fromEntries(this.advancedFilters)
        };
    }
}

// 增强的排序功能
class EnhancedSortingManager {
    constructor() {
        this.sortOptions = ENHANCED_SORTING.options;
        this.customSorts = [];
        this.initializeEnhancedSorting();
    }

    initializeEnhancedSorting() {
        this.createSortUI();
        this.bindSortEvents();
    }

    createSortUI() {
        const existingSort = document.getElementById('sort-select');
        if (!existingSort) return;

        // 添加额外的排序选项
        const enhancedOptions = this.sortOptions.map(option =>
            `<option value="${option.value}">${option.label}</option>`
        ).join('');
        
        existingSort.innerHTML = enhancedOptions;
    }

    bindSortEvents() {
        // 绑定自定义排序事件
        const customSortBtn = document.getElementById('custom-sort-btn');
        const customSortModal = document.getElementById('custom-sort-modal');
        
        if (customSortBtn) {
            customSortBtn.addEventListener('click', () => {
                customSortModal.classList.remove('hidden');
            });
        }
    }

    // 多维度排序
    sortProducts(products, sortConfig) {
        const { primary, secondary, direction } = sortConfig;
        
        return products.sort((a, b) => {
            let result = 0;
            
            // 主要排序
            result = this.compareValues(a[primary], b[primary], direction);
            
            // 次要排序
            if (result === 0 && secondary) {
                result = this.compareValues(a[secondary], b[secondary], direction);
            }
            
            return result;
        });
    }

    compareValues(a, b, direction = 'asc') {
        let aVal = a || 0;
        let bVal = b || 0;
        
        // 处理字符串
        if (typeof aVal === 'string') aVal = aVal.toLowerCase();
        if (typeof bVal === 'string') bVal = bVal.toLowerCase();
        
        let result = 0;
        if (aVal < bVal) result = -1;
        if (aVal > bVal) result = 1;
        
        return direction === 'desc' ? -result : result;
    }
}

// 增强的对比功能控制器
class EnhancedCompareController {
    constructor() {
        this.compareManager = new EnhancedCompareManager();
        this.initializeEnhancedCompare();
    }

    initializeEnhancedCompare() {
        this.createCompareUI();
        this.bindCompareEvents();
    }

    createCompareUI() {
        const compareHTML = `
            <div class="enhanced-compare">
                <div id="compare-sidebar" class="hidden fixed right-0 top-0 h-full w-80 bg-white shadow-lg z-50">
                    <div class="p-4 border-b">
                        <div class="flex items-center justify-between">
                            <h3 class="text-lg font-semibold">产品对比</h3>
                            <button onclick="closeCompareSidebar()" class="text-gray-400 hover:text-gray-600">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                    </div>
                    <div class="p-4">
                        <div id="compare-products-list" class="space-y-2 mb-4"></div>
                        <div class="space-y-2">
                            <button onclick="generateCompareReport()" class="w-full bg-jytek-blue text-white py-2 rounded-lg">
                                生成对比报告
                            </button>
                            <button onclick="exportCompareData()" class="w-full border border-gray-300 py-2 rounded-lg">
                                导出数据
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', compareHTML);
    }

    bindCompareEvents() {
        // 绑定对比事件
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('quick-compare-btn')) {
                this.quickCompare(e.target.dataset.productId);
            }
        });
    }

    // 快速对比
    quickCompare(productId) {
        const product = dataManager.products.find(p => p.id === productId);
        if (product) {
            this.compareManager.addToCompare(product);
            this.updateCompareSidebar();
        }
    }

    // 更新对比侧边栏
    updateCompareSidebar() {
        const sidebar = document.getElementById('compare-sidebar');
        const list = document.getElementById('compare-products-list');
        
        const products = Array.from(this.compareManager.compareData.values());
        const html = products.map(product => `
            <div class="flex items-center justify-between p-2 bg-gray-50 rounded">
                <div>
                    <div class="text-sm font-medium">${product.name}</div>
                    <div class="text-xs text-gray-500">${product.price ? '¥' + product.price.toLocaleString() : '询价'}</div>
                </div>
                <button onclick="removeFromCompare('${product.id}')" class="text-red-500">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `).join('');

        if (list) list.innerHTML = html;
    }

    // 生成对比报告
    generateCompareReport() {
        const products = Array.from(this.compareManager.compareData.values());
        if (products.length < 2) {
            Utils.showMessage('请至少选择2个产品进行对比', 'warning');
            return;
        }

        const report = this.compareManager.generateCompareReport(products, 'detailed');
        
        // 显示报告模态框
        this.showCompareReportModal(report);
    }

    showCompareReportModal(report) {
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center';
        modal.innerHTML = `
            <div class="bg-white rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] overflow-y-auto">
                <div class="p-6">
                    <h2 class="text-2xl font-bold mb-4">产品对比报告</h2>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <h3 class="text-lg font-semibold mb-2">对比摘要</h3>
                            <p>共对比 ${report.summary.totalProducts} 个产品</p>
                            <p>价格范围: ${report.summary.priceRange.min} - ${report.summary.priceRange.max}</p>
                        </div>
                        <div>
                            <h3 class="text-lg font-semibold mb-2">推荐</h3>
                            ${report.recommendations.map(rec => `
                                <div class="mb-2">
                                    <strong>${rec.type}:</strong> ${rec.product.name}
                                    <p class="text-sm text-gray-600">${rec.reason}</p>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        modal.addEventListener('click', (e) => {
            if (e.target === modal) modal.remove();
        });
    }
}

// 全局变量
let enhancedCompare, enhancedSorting, enhancedFilterManager;

// 初始化增强功能
document.addEventListener('DOMContentLoaded', function() {
    try {
        // 等待主页面初始化完成
        setTimeout(() => {
            if (typeof dataManager !== 'undefined') {
                enhancedCompare = new EnhancedCompareController();
                enhancedSorting = new EnhancedSortingManager();
                enhancedFilterManager = new EnhancedFilterManager(dataManager);
                console.log('产品页面增强功能已加载');
            } else {
                console.warn('数据管理器未初始化，增强功能延迟加载');
                // 重试初始化
                setTimeout(arguments.callee, 500);
            }
        }, 100);
    } catch (error) {
        console.error('增强功能初始化失败:', error);
    }
});

// 全局函数
window.closeCompareSidebar = function() {
    const sidebar = document.getElementById('compare-sidebar');
    if (sidebar) sidebar.classList.add('hidden');
};

window.generateCompareReport = function() {
    if (typeof enhancedCompare !== 'undefined') {
        enhancedCompare.generateCompareReport();
    }
};

window.exportCompareData = function() {
    if (typeof enhancedCompare !== 'undefined') {
        const products = Array.from(enhancedCompare.compareManager.compareData.values());
        const csv = convertToCSV(products);
        downloadCSV(csv, '产品对比数据.csv');
    }
};

window.removeFromCompare = function(productId) {
    if (typeof enhancedCompare !== 'undefined') {
        enhancedCompare.compareManager.compareData.delete(productId);
        enhancedCompare.updateCompareSidebar();
    }
};

// 工具函数
function convertToCSV(products) {
    const headers = ['产品名称', '价格', '分类', '库存状态'];
    const rows = products.map(p => [p.name, p.price, p.category, p.stock_status]);
    
    return [headers, ...rows].map(row => row.join(',')).join('\n');
}

function downloadCSV(csv, filename) {
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
}