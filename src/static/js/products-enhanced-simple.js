/**
 * 产品页面增强功能 - 简化版
 * 避免复杂的类继承和依赖关系
 */

// 增强的筛选功能
function initializeEnhancedFilters() {
    // 添加高级筛选选项
    const filterPanel = document.querySelector('.bg-white.rounded-lg.shadow-sm.p-6');
    if (!filterPanel) return;

    const advancedFilterHTML = `
        <div class="mt-6 pt-6 border-t">
            <h3 class="text-sm font-medium text-gray-900 mb-3">高级筛选</h3>
            
            <!-- 品牌筛选 -->
            <div class="mb-4">
                <label class="block text-xs text-gray-600 mb-1">品牌</label>
                <select id="brand-filter" class="w-full text-sm border border-gray-300 rounded-lg px-3 py-2">
                    <option value="">所有品牌</option>
                    <option value="简仪科技">简仪科技</option>
                    <option value="NI">NI</option>
                    <option value="Keysight">Keysight</option>
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
        </div>
    `;

    filterPanel.insertAdjacentHTML('beforeend', advancedFilterHTML);
}

// 增强的排序功能
function initializeEnhancedSorting() {
    const sortSelect = document.getElementById('sort-select');
    if (!sortSelect) return;

    const enhancedOptions = [
        { value: 'name', label: '产品名称' },
        { value: 'price-asc', label: '价格从低到高' },
        { value: 'price-desc', label: '价格从高到低' },
        { value: 'popularity', label: '热门程度' },
        { value: 'rating', label: '用户评分' },
        { value: 'newest', label: '最新上架' },
        { value: 'stock', label: '库存状态' }
    ];

    sortSelect.innerHTML = enhancedOptions.map(option => 
        `<option value="${option.value}">${option.label}</option>`
    ).join('');
}

// 增强的对比功能
function initializeEnhancedCompare() {
    // 扩展对比数量到5个
    if (window.CONFIG) {
        window.CONFIG.MAX_COMPARE_ITEMS = 5;
    }
}

// 初始化所有增强功能
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        try {
            initializeEnhancedFilters();
            initializeEnhancedSorting();
            initializeEnhancedCompare();
            console.log('产品页面增强功能已加载（简化版）');
        } catch (error) {
            console.error('增强功能初始化失败:', error);
        }
    }, 500);
});