/**
 * 产品中心页面JavaScript - 重构版
 * 基于模块化架构，支持高级筛选、搜索、AI助手等功能
 */

// 全局配置
const CONFIG = {
    API_BASE: '/api',
    ITEMS_PER_PAGE: 12,
    SEARCH_DEBOUNCE: 300,
    MAX_COMPARE_ITEMS: 3,
    CACHE_DURATION: 5 * 60 * 1000, // 5分钟
};

// 工具函数
const Utils = {
    // 防抖函数
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // 节流函数
    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    },

    // 格式化价格
    formatPrice(price) {
        if (!price || price === 0) return '询价';
        return `¥${price.toLocaleString()}`;
    },

    // 提取数字
    extractNumber(str) {
        const match = str.match(/(\d+)/);
        return match ? parseInt(match[1]) : 0;
    },

    // 高亮搜索关键词
    highlightKeywords(text, keywords) {
        if (!keywords || !text) return text;
        const regex = new RegExp(`(${keywords.split(' ').join('|')})`, 'gi');
        return text.replace(regex, '<span class="search-suggestion-highlight">$1</span>');
    },

    // 显示消息
    showMessage(message, type = 'info', duration = 3000) {
        const messageEl = document.createElement('div');
        messageEl.className = `fixed top-4 right-4 z-50 px-6 py-3 rounded-lg shadow-lg transition-all duration-300 ${
            type === 'error' ? 'bg-red-600 text-white' : 
            type === 'success' ? 'bg-green-600 text-white' : 
            type === 'warning' ? 'bg-yellow-600 text-white' :
            'bg-blue-600 text-white'
        }`;
        messageEl.textContent = message;
        
        document.body.appendChild(messageEl);
        
        // 动画显示
        setTimeout(() => messageEl.classList.add('translate-x-0'), 10);
        
        // 自动移除
        setTimeout(() => {
            messageEl.classList.add('translate-x-full', 'opacity-0');
            setTimeout(() => {
                if (messageEl.parentNode) {
                    messageEl.parentNode.removeChild(messageEl);
                }
            }, 300);
        }, duration);
    },

    // 本地存储
    storage: {
        set(key, value, expiry = null) {
            const item = {
                value: value,
                expiry: expiry ? Date.now() + expiry : null
            };
            localStorage.setItem(key, JSON.stringify(item));
        },

        get(key) {
            const itemStr = localStorage.getItem(key);
            if (!itemStr) return null;

            const item = JSON.parse(itemStr);
            if (item.expiry && Date.now() > item.expiry) {
                localStorage.removeItem(key);
                return null;
            }
            return item.value;
        },

        remove(key) {
            localStorage.removeItem(key);
        }
    }
};

// 数据管理器
class DataManager {
    constructor() {
        this.cache = new Map();
        this.products = [];
        this.categories = [];
        this.filters = {
            keyword: '',
            category: '',
            priceRanges: [],
            stockStatus: [],
            channels: '',
            resolution: ''
        };
    }

    async fetchProducts(params = {}) {
        const cacheKey = `products_${JSON.stringify(params)}`;
        const cached = this.cache.get(cacheKey);
        
        if (cached && Date.now() - cached.timestamp < CONFIG.CACHE_DURATION) {
            return cached.data;
        }

        try {
            const queryParams = new URLSearchParams(params);
            const response = await fetch(`${CONFIG.API_BASE}/products?${queryParams}`);
            const data = await response.json();
            
            if (data.success) {
                this.cache.set(cacheKey, {
                    data: data,
                    timestamp: Date.now()
                });
                this.products = data.products;
                return data;
            } else {
                throw new Error(data.error || '获取产品数据失败');
            }
        } catch (error) {
            console.error('获取产品数据失败:', error);
            Utils.showMessage('获取产品数据失败，请稍后重试', 'error');
            return { success: false, products: [], pagination: {} };
        }
    }

    async fetchCategories() {
        const cached = this.cache.get('categories');
        if (cached && Date.now() - cached.timestamp < CONFIG.CACHE_DURATION) {
            return cached.data;
        }

        try {
            const response = await fetch(`${CONFIG.API_BASE}/products/categories`);
            const data = await response.json();
            
            if (data.success) {
                this.cache.set('categories', {
                    data: data,
                    timestamp: Date.now()
                });
                this.categories = data.categories;
                return data;
            } else {
                throw new Error(data.error || '获取分类数据失败');
            }
        } catch (error) {
            console.error('获取分类数据失败:', error);
            Utils.showMessage('获取分类数据失败', 'error');
            return { success: false, categories: [] };
        }
    }

    async fetchProductDetail(productId) {
        const cacheKey = `product_${productId}`;
        const cached = this.cache.get(cacheKey);
        
        if (cached && Date.now() - cached.timestamp < CONFIG.CACHE_DURATION) {
            return cached.data;
        }

        try {
            const response = await fetch(`${CONFIG.API_BASE}/products/${productId}`);
            const data = await response.json();
            
            if (data.success) {
                this.cache.set(cacheKey, {
                    data: data,
                    timestamp: Date.now()
                });
                return data;
            } else {
                throw new Error(data.error || '获取产品详情失败');
            }
        } catch (error) {
            console.error('获取产品详情失败:', error);
            Utils.showMessage('获取产品详情失败', 'error');
            return { success: false, product: null };
        }
    }

    async searchProducts(keyword, filters = {}) {
        try {
            const response = await fetch(`${CONFIG.API_BASE}/products/search`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    keyword: keyword,
                    ...filters
                })
            });
            const data = await response.json();
            
            if (data.success) {
                return data;
            } else {
                throw new Error(data.error || '搜索失败');
            }
        } catch (error) {
            console.error('搜索失败:', error);
            Utils.showMessage('搜索失败，请稍后重试', 'error');
            return { success: false, products: [] };
        }
    }

    getFilters() {
        return { ...this.filters };
    }

    setFilters(newFilters) {
        this.filters = { ...this.filters, ...newFilters };
    }

    clearFilters() {
        this.filters = {
            keyword: '',
            category: '',
            priceRanges: [],
            stockStatus: [],
            channels: '',
            resolution: ''
        };
    }
}

// 搜索管理器
class SearchManager {
    constructor(dataManager) {
        this.dataManager = dataManager;
        this.searchHistory = Utils.storage.get('search_history') || [];
        this.suggestions = [];
        this.initializeElements();
        this.bindEvents();
    }

    initializeElements() {
        this.searchInput = document.getElementById('search-input');
        this.suggestionsContainer = document.getElementById('search-suggestions');
    }

    bindEvents() {
        if (this.searchInput) {
            // 搜索输入事件
            this.searchInput.addEventListener('input', Utils.debounce((e) => {
                this.handleSearchInput(e.target.value);
            }, CONFIG.SEARCH_DEBOUNCE));

            // 回车搜索
            this.searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.performSearch(e.target.value);
                }
            });

            // 焦点事件
            this.searchInput.addEventListener('focus', () => {
                this.showSuggestions();
            });

            this.searchInput.addEventListener('blur', () => {
                // 延迟隐藏，允许点击建议
                setTimeout(() => this.hideSuggestions(), 200);
            });
        }
    }

    async handleSearchInput(value) {
        if (value.length < 2) {
            this.hideSuggestions();
            return;
        }

        // 生成搜索建议
        await this.generateSuggestions(value);
        this.showSuggestions();
    }

    async generateSuggestions(keyword) {
        // 从历史记录中筛选
        const historyMatches = this.searchHistory
            .filter(item => item.toLowerCase().includes(keyword.toLowerCase()))
            .slice(0, 3);

        // 从产品数据中生成建议
        const productMatches = this.dataManager.products
            .filter(product => 
                product.name.toLowerCase().includes(keyword.toLowerCase()) ||
                product.part_number.toLowerCase().includes(keyword.toLowerCase())
            )
            .map(product => product.name)
            .slice(0, 5);

        // 合并并去重
        this.suggestions = [...new Set([...historyMatches, ...productMatches])];
    }

    showSuggestions() {
        if (this.suggestions.length === 0) {
            this.hideSuggestions();
            return;
        }

        const keyword = this.searchInput.value;
        const suggestionsHTML = this.suggestions.map(suggestion => `
            <div class="search-suggestion-item" data-suggestion="${suggestion}">
                <i class="fas fa-search text-gray-400 mr-2"></i>
                ${Utils.highlightKeywords(suggestion, keyword)}
            </div>
        `).join('');

        this.suggestionsContainer.innerHTML = suggestionsHTML;
        this.suggestionsContainer.classList.remove('hidden');

        // 绑定点击事件
        this.suggestionsContainer.querySelectorAll('.search-suggestion-item').forEach(item => {
            item.addEventListener('click', () => {
                const suggestion = item.dataset.suggestion;
                this.searchInput.value = suggestion;
                this.performSearch(suggestion);
                this.hideSuggestions();
            });
        });
    }

    hideSuggestions() {
        this.suggestionsContainer.classList.add('hidden');
    }

    performSearch(keyword) {
        if (!keyword.trim()) return;

        // 添加到搜索历史
        this.addToHistory(keyword);

        // 更新筛选条件
        this.dataManager.setFilters({ keyword: keyword.trim() });

        // 触发搜索事件
        document.dispatchEvent(new CustomEvent('search-performed', {
            detail: { keyword: keyword.trim() }
        }));

        this.hideSuggestions();
    }

    addToHistory(keyword) {
        // 移除重复项
        this.searchHistory = this.searchHistory.filter(item => item !== keyword);
        // 添加到开头
        this.searchHistory.unshift(keyword);
        // 限制历史记录数量
        this.searchHistory = this.searchHistory.slice(0, 10);
        // 保存到本地存储
        Utils.storage.set('search_history', this.searchHistory);
    }

    clearHistory() {
        this.searchHistory = [];
        Utils.storage.remove('search_history');
    }
}

// 筛选管理器
class FilterManager {
    constructor(dataManager) {
        this.dataManager = dataManager;
        this.activeFilters = new Map();
        this.initializeElements();
        this.bindEvents();
    }

    initializeElements() {
        this.categoryFilters = document.getElementById('category-filters');
        this.priceFilters = document.querySelectorAll('.price-filter');
        this.stockFilters = document.querySelectorAll('.stock-filter');
        this.channelsFilter = document.getElementById('channels-filter');
        this.resolutionFilter = document.getElementById('resolution-filter');
        this.clearFiltersBtn = document.getElementById('clear-filters');
        this.applyFiltersBtn = document.getElementById('apply-filters');
        this.activeFiltersContainer = document.getElementById('active-filters');
    }

    bindEvents() {
        // 分类筛选
        if (this.categoryFilters) {
            this.categoryFilters.addEventListener('click', (e) => {
                if (e.target.classList.contains('category-filter')) {
                    this.handleCategoryFilter(e.target);
                }
            });
        }

        // 价格筛选
        this.priceFilters.forEach(filter => {
            filter.addEventListener('change', () => this.updateActiveFilters());
        });

        // 库存筛选
        this.stockFilters.forEach(filter => {
            filter.addEventListener('change', () => this.updateActiveFilters());
        });

        // 技术规格筛选
        if (this.channelsFilter) {
            this.channelsFilter.addEventListener('change', () => this.updateActiveFilters());
        }

        if (this.resolutionFilter) {
            this.resolutionFilter.addEventListener('change', () => this.updateActiveFilters());
        }

        // 清除筛选
        if (this.clearFiltersBtn) {
            this.clearFiltersBtn.addEventListener('click', () => this.clearAllFilters());
        }

        // 应用筛选
        if (this.applyFiltersBtn) {
            this.applyFiltersBtn.addEventListener('click', () => this.applyFilters());
        }
    }

    async loadCategories() {
        const data = await this.dataManager.fetchCategories();
        if (data.success) {
            this.renderCategoryFilters(data.categories);
        }
    }

    renderCategoryFilters(categories) {
        const totalCount = categories.reduce((sum, cat) => sum + cat.count, 0);
        document.getElementById('total-count').textContent = totalCount;

        const categoryHTML = categories.map(category => `
            <button class="category-filter w-full text-left px-3 py-2 rounded-lg text-sm hover:bg-gray-100 transition-colors" 
                    data-category="${category.name_en}">
                ${category.name_cn} (${category.count})
            </button>
        `).join('');

        // 插入到"全部分类"按钮后面
        const allCategoryBtn = this.categoryFilters.querySelector('.category-filter');
        allCategoryBtn.insertAdjacentHTML('afterend', categoryHTML);
    }

    handleCategoryFilter(button) {
        // 移除其他按钮的active状态
        this.categoryFilters.querySelectorAll('.category-filter').forEach(btn => {
            btn.classList.remove('active', 'bg-jytek-blue', 'text-white');
            btn.classList.add('hover:bg-gray-100');
        });

        // 激活当前按钮
        button.classList.add('active', 'bg-jytek-blue', 'text-white');
        button.classList.remove('hover:bg-gray-100');

        const category = button.dataset.category;
        this.dataManager.setFilters({ category });
        this.updateActiveFilters();
        this.applyFilters();
    }

    updateActiveFilters() {
        this.activeFilters.clear();

        // 分类筛选
        const activeCategory = this.categoryFilters?.querySelector('.category-filter.active');
        if (activeCategory && activeCategory.dataset.category) {
            this.activeFilters.set('category', {
                label: activeCategory.textContent.trim(),
                value: activeCategory.dataset.category
            });
        }

        // 价格筛选
        const selectedPrices = Array.from(this.priceFilters)
            .filter(filter => filter.checked)
            .map(filter => filter.value);
        if (selectedPrices.length > 0) {
            this.activeFilters.set('price', {
                label: `价格: ${selectedPrices.length}个区间`,
                value: selectedPrices
            });
        }

        // 库存筛选
        const selectedStock = Array.from(this.stockFilters)
            .filter(filter => filter.checked)
            .map(filter => filter.value);
        if (selectedStock.length > 0) {
            this.activeFilters.set('stock', {
                label: `库存: ${selectedStock.join(', ')}`,
                value: selectedStock
            });
        }

        // 通道数筛选
        if (this.channelsFilter?.value) {
            this.activeFilters.set('channels', {
                label: `通道数: ${this.channelsFilter.value}`,
                value: this.channelsFilter.value
            });
        }

        // 分辨率筛选
        if (this.resolutionFilter?.value) {
            this.activeFilters.set('resolution', {
                label: `分辨率: ${this.resolutionFilter.value}位`,
                value: this.resolutionFilter.value
            });
        }

        this.renderActiveFilters();
    }

    renderActiveFilters() {
        if (this.activeFilters.size === 0) {
            this.activeFiltersContainer.innerHTML = '';
            return;
        }

        const filtersHTML = Array.from(this.activeFilters.entries()).map(([key, filter]) => `
            <span class="filter-tag">
                ${filter.label}
                <i class="fas fa-times remove-tag" data-filter="${key}"></i>
            </span>
        `).join('');

        this.activeFiltersContainer.innerHTML = filtersHTML;

        // 绑定移除事件
        this.activeFiltersContainer.querySelectorAll('.remove-tag').forEach(btn => {
            btn.addEventListener('click', () => {
                this.removeFilter(btn.dataset.filter);
            });
        });
    }

    removeFilter(filterKey) {
        this.activeFilters.delete(filterKey);

        // 重置对应的UI控件
        switch (filterKey) {
            case 'category':
                const allCategoryBtn = this.categoryFilters.querySelector('.category-filter[data-category=""]');
                if (allCategoryBtn) {
                    this.handleCategoryFilter(allCategoryBtn);
                }
                break;
            case 'price':
                this.priceFilters.forEach(filter => filter.checked = false);
                break;
            case 'stock':
                this.stockFilters.forEach(filter => filter.checked = false);
                break;
            case 'channels':
                if (this.channelsFilter) this.channelsFilter.value = '';
                break;
            case 'resolution':
                if (this.resolutionFilter) this.resolutionFilter.value = '';
                break;
        }

        this.updateActiveFilters();
        this.applyFilters();
    }

    clearAllFilters() {
        // 重置所有筛选控件
        const allCategoryBtn = this.categoryFilters?.querySelector('.category-filter[data-category=""]');
        if (allCategoryBtn) {
            this.handleCategoryFilter(allCategoryBtn);
        }

        this.priceFilters.forEach(filter => filter.checked = false);
        this.stockFilters.forEach(filter => filter.checked = false);
        
        if (this.channelsFilter) this.channelsFilter.value = '';
        if (this.resolutionFilter) this.resolutionFilter.value = '';

        // 清除搜索
        const searchInput = document.getElementById('search-input');
        if (searchInput) searchInput.value = '';

        this.activeFilters.clear();
        this.dataManager.clearFilters();
        this.renderActiveFilters();
        this.applyFilters();
    }

    applyFilters() {
        // 收集所有筛选条件
        const filters = {
            category: this.activeFilters.get('category')?.value || '',
            priceRanges: this.activeFilters.get('price')?.value || [],
            stockStatus: this.activeFilters.get('stock')?.value || [],
            channels: this.activeFilters.get('channels')?.value || '',
            resolution: this.activeFilters.get('resolution')?.value || ''
        };

        this.dataManager.setFilters(filters);

        // 触发筛选事件
        document.dispatchEvent(new CustomEvent('filters-applied', {
            detail: { filters }
        }));
    }
}

// 产品展示管理器
class ProductDisplayManager {
    constructor(dataManager) {
        this.dataManager = dataManager;
        this.currentView = 'grid';
        this.currentPage = 1;
        this.sortBy = 'name';
        this.compareItems = new Set();
        this.initializeElements();
        this.bindEvents();
    }

    initializeElements() {
        this.productsGrid = document.getElementById('products-grid');
        this.productsList = document.getElementById('products-list');
        this.loadingState = document.getElementById('loading-state');
        this.emptyState = document.getElementById('empty-state');
        this.resultsCount = document.getElementById('results-count');
        this.pagination = document.getElementById('pagination');
        this.gridViewBtn = document.getElementById('grid-view-btn');
        this.listViewBtn = document.getElementById('list-view-btn');
        this.sortSelect = document.getElementById('sort-select');
        this.compareBar = document.getElementById('compare-bar');
        this.compareCount = document.getElementById('compare-count');
        this.compareItems = document.getElementById('compare-items');
    }

    bindEvents() {
        // 视图切换
        if (this.gridViewBtn) {
            this.gridViewBtn.addEventListener('click', () => this.setView('grid'));
        }
        if (this.listViewBtn) {
            this.listViewBtn.addEventListener('click', () => this.setView('list'));
        }

        // 排序
        if (this.sortSelect) {
            this.sortSelect.addEventListener('change', (e) => {
                this.sortBy = e.target.value;
                this.loadProducts();
            });
        }

        // 对比功能
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('compare-checkbox')) {
                this.toggleCompare(e.target);
            }
        });

        // 重置搜索
        const resetSearchBtn = document.getElementById('reset-search');
        if (resetSearchBtn) {
            resetSearchBtn.addEventListener('click', () => {
                document.dispatchEvent(new CustomEvent('reset-search'));
            });
        }

        // 监听筛选和搜索事件
        document.addEventListener('filters-applied', () => this.loadProducts());
        document.addEventListener('search-performed', () => this.loadProducts());
        document.addEventListener('reset-search', () => {
            this.dataManager.clearFilters();
            const searchInput = document.getElementById('search-input');
            if (searchInput) searchInput.value = '';
            this.loadProducts();
        });
    }

    async loadProducts(page = 1) {
        this.currentPage = page;
        this.showLoading();

        const filters = this.dataManager.getFilters();
        const params = {
            page: page,
            per_page: CONFIG.ITEMS_PER_PAGE,
            sort: this.sortBy,
            ...filters
        };

        const data = await this.dataManager.fetchProducts(params);
        
        if (data.success) {
            this.renderProducts(data.products);
            this.renderPagination(data.pagination);
            this.updateResultsCount(data.pagination?.total || data.products.length);
        } else {
            this.showEmpty();
        }

        this.hideLoading();
    }

    renderProducts(products) {
        if (products.length === 0) {
            this.showEmpty();
            return;
        }

        this.hideEmpty();

        if (this.currentView === 'grid') {
            this.renderGridView(products);
        } else {
            this.renderListView(products);
        }
    }

    renderGridView(products) {
        const productsHTML = products.map(product => this.createProductCard(product)).join('');
        this.productsGrid.innerHTML = productsHTML;
        this.productsGrid.classList.remove('hidden');
        this.productsList.classList.add('hidden');
    }

    renderListView(products) {
        const productsHTML = products.map(product => this.createProductListItem(product)).join('');
        this.productsList.innerHTML = productsHTML;
        this.productsList.classList.remove('hidden');
        this.productsGrid.classList.add('hidden');
    }

    createProductCard(product) {
        const stockClass = this.getStockClass(product.stock_status);
        const stockIcon = this.getStockIcon(product.stock_status);
        const isInCompare = this.compareItems.has(product.id);

        return `
            <div class="product-card bg-white rounded-lg shadow-sm p-6 cursor-pointer" data-product-id="${product.id}">
                <div class="compare-checkbox">
                    <input type="checkbox" class="compare-checkbox rounded border-gray-300 text-jytek-blue focus:ring-jytek-blue" 
                           ${isInCompare ? 'checked' : ''} data-product-id="${product.id}">
                </div>
                
                <div class="product-image-placeholder mb-4" onclick="showProductDetail('${product.id}')">
                    <i class="fas fa-microchip"></i>
                </div>
                
                <div class="flex justify-between items-start mb-4">
                    <h3 class="text-lg font-semibold text-gray-900 line-clamp-2 flex-1 mr-2" onclick="showProductDetail('${product.id}')">
                        ${product.name || product.part_number}
                    </h3>
                    <span class="price-badge">
                        ${Utils.formatPrice(product.price)}
                    </span>
                </div>
                
                <div class="space-y-2 mb-4">
                    <div class="flex items-center text-sm text-gray-600">
                        <i class="fas fa-tag mr-2"></i>
                        <span>${product.part_number || product.id}</span>
                    </div>
                    <div class="flex items-center text-sm text-gray-600">
                        <i class="fas fa-folder mr-2"></i>
                        <span>${product.category_cn || product.category || '未分类'}</span>
                    </div>
                    <div class="flex items-center text-sm ${stockClass}">
                        <i class="${stockIcon} mr-2"></i>
                        <span>${product.stock_status || '未知'}</span>
                    </div>
                </div>
                
                <p class="text-gray-600 text-sm line-clamp-3 mb-4">
                    ${product.description || '暂无描述'}
                </p>
                
                <div class="flex space-x-2">
                    <button onclick="showProductDetail('${product.id}')" 
                            class="flex-1 bg-jytek-blue hover:bg-jytek-light-blue text-white px-4 py-2 rounded-lg text-sm transition-colors">
                        查看详情
                    </button>
                    <button onclick="contactSales('${product.id}')" 
                            class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 text-sm transition-colors"
                            title="联系销售">
                        <i class="fas fa-envelope"></i>
                    </button>
                    <button onclick="addToFavorites('${product.id}')" 
                            class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 text-sm transition-colors"
                            title="收藏产品">
                        <i class="fas fa-heart"></i>
                    </button>
                </div>
            </div>
        `;
    }

    createProductListItem(product) {
        const stockClass = this.getStockClass(product.stock_status);
        const stockIcon = this.getStockIcon(product.stock_status);
        const isInCompare = this.compareItems.has(product.id);

        return `
            <div class="product-list-item bg-white rounded-lg shadow-sm p-6" data-product-id="${product.id}">
                <div class="flex flex-col md:flex-row md:items-center justify-between">
                    <div class="flex-1">
                        <div class="flex flex-col md:flex-row md:items-center md:space-x-6">
                            <div class="flex items-center mb-4 md:mb-0">
                                <input type="checkbox" class="compare-checkbox rounded border-gray-300 text-jytek-blue focus:ring-jytek-blue mr-4" 
                                       ${isInCompare ? 'checked' : ''} data-product-id="${product.id}">
                                <div class="w-16 h-16 bg-gray-100 rounded-lg flex items-center justify-center mr-4">
                                    <i class="fas fa-microchip text-gray-400"></i>
                                </div>
                            </div>
                            
                            <div class="flex-1 mb-4 md:mb-0">
                                <h3 class="text-lg font-semibold text-gray-900 mb-2 cursor-pointer" onclick="showProductDetail('${product.id}')">
                                    ${product.name || product.part_number}
                                </h3>
                                <div class="flex flex-wrap gap-4 text-sm text-gray-600">
                                    <span><i class="fas fa-tag mr-1"></i>${product.part_number || product.id}</span>
                                    <span><i class="fas fa-folder mr-1"></i>${product.category_cn || product.category || '未分类'}</span>
                                    <span class="${stockClass}"><i class="${stockIcon} mr-1"></i>${product.stock_status || '未知'}</span>
                                </div>
                                <p class="text-gray-600 text-sm mt-2 line-clamp-2">
                                    ${product.description || '暂无描述'}
                                </p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="flex flex-col md:flex-row md:items-center md:space-x-4">
                        <div class="mb-4 md:mb-0">
                            <span class="price-badge text-lg">
                                ${Utils.formatPrice(product.price)}
                            </span>
                        </div>
                        
                        <div class="flex space-x-2">
                            <button onclick="showProductDetail('${product.id}')" 
                                    class="bg-jytek-blue hover:bg-jytek-light-blue text-white px-4 py-2 rounded-lg text-sm transition-colors">
                                查看详情
                            </button>
                            <button onclick="contactSales('${product.id}')" 
                                    class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 text-sm transition-colors"
                                    title="联系销售">
                                <i class="fas fa-envelope"></i>
                            </button>
                            <button onclick="addToFavorites('${product.id}')" 
                                    class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 text-sm transition-colors"
                                    title="收藏产品">
                                <i class="fas fa-heart"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    getStockClass(stockStatus) {
        switch (stockStatus) {
            case '现货':
                return 'stock-available';
            case '预订':
                return 'stock-limited';
            default:
                return 'stock-unavailable';
        }
    }

    getStockIcon(stockStatus) {
        switch (stockStatus) {
            case '现货':
                return 'fas fa-check-circle';
            case '预订':
                return 'fas fa-clock';
            default:
                return 'fas fa-times-circle';
        }
    }

    setView(view) {
        this.currentView = view;
        
        if (view === 'grid') {
            this.gridViewBtn.classList.add('bg-jytek-blue', 'text-white');
            this.gridViewBtn.classList.remove('text-gray-600');
            this.listViewBtn.classList.remove('bg-jytek-blue', 'text-white');
            this.listViewBtn.classList.add('text-gray-600');
        } else {
            this.listViewBtn.classList.add('bg-jytek-blue', 'text-white');
            this.listViewBtn.classList.remove('text-gray-600');
            this.gridViewBtn.classList.remove('bg-jytek-blue', 'text-white');
            this.gridViewBtn.classList.add('text-gray-600');
        }

        // 重新渲染当前产品
        if (this.dataManager.products.length > 0) {
            this.renderProducts(this.dataManager.products);
        }
    }

    toggleCompare(checkbox) {
        const productId = checkbox.dataset.productId;
        
        if (checkbox.checked) {
            if (this.compareItems.size >= CONFIG.MAX_COMPARE_ITEMS) {
                checkbox.checked = false;
                Utils.showMessage(`最多只能对比${CONFIG.MAX_COMPARE_ITEMS}个产品`, 'warning');
                return;
            }
            this.compareItems.add(productId);
        } else {
            this.compareItems.delete(productId);
        }

        this.updateCompareBar();
    }

    updateCompareBar() {
        const count = this.compareItems.size;
        
        if (count === 0) {
            this.compareBar.classList.add('hidden');
            return;
        }

        this.compareBar.classList.remove('hidden');
        this.compareCount.textContent = count;

        // 更新对比项目显示
        const compareItemsHTML = Array.from(this.compareItems).map(productId => {
            const product = this.dataManager.products.find(p => p.id === productId);
            return `
                <div class="compare-item">
                    <span>${product?.name || productId}</span>
                    <i class="fas fa-times remove-compare" data-product-id="${productId}"></i>
                </div>
            `;
        }).join('');

        this.compareItems.innerHTML = compareItemsHTML;

        // 绑定移除事件
        this.compareItems.querySelectorAll('.remove-compare').forEach(btn => {
            btn.addEventListener('click', () => {
                const productId = btn.dataset.productId;
                this.compareItems.delete(productId);
                
                // 更新复选框状态
                const checkbox = document.querySelector(`input[data-product-id="${productId}"]`);
                if (checkbox) checkbox.checked = false;
                
                this.updateCompareBar();
            });
        });
    }

    showLoading() {
        this.loadingState.classList.remove('hidden');
        this.productsGrid.classList.add('hidden');
        this.productsList.classList.add('hidden');
        this.emptyState.classList.add('hidden');
    }

    hideLoading() {
        this.loadingState.classList.add('hidden');
    }

    showEmpty() {
        this.emptyState.classList.remove('hidden');
        this.productsGrid.classList.add('hidden');
        this.productsList.classList.add('hidden');
    }

    hideEmpty() {
        this.emptyState.classList.add('hidden');
    }

    updateResultsCount(count) {
        this.resultsCount.textContent = `共 ${count} 个产品`;
    }

    renderPagination(pagination) {
        if (!pagination || pagination.total_pages <= 1) {
            this.pagination.classList.add('hidden');
            return;
        }

        this.pagination.classList.remove('hidden');
        
        const { current_page, total_pages } = pagination;
        let paginationHTML = '';

        // 上一页
        if (current_page > 1) {
            paginationHTML += `
                <button onclick="loadPage(${current_page - 1})" 
                        class="px-3 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors">
                    <i class="fas fa-chevron-left mr-1"></i>上一页
                </button>
            `;
        }

        // 页码
        const startPage = Math.max(1, current_page - 2);
        const endPage = Math.min(total_pages, current_page + 2);

        if (startPage > 1) {
            paginationHTML += `
                <button onclick="loadPage(1)" 
                        class="px-3 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors">
                    1
                </button>
            `;
            if (startPage > 2) {
                paginationHTML += '<span class="px-2 text-gray-400">...</span>';
            }
        }

        for (let i = startPage; i <= endPage; i++) {
            const isActive = i === current_page;
            paginationHTML += `
                <button onclick="loadPage(${i})" 
                        class="px-3 py-2 text-sm rounded-lg transition-colors ${
                            isActive 
                                ? 'bg-jytek-blue text-white' 
                                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                        }">
                    ${i}
                </button>
            `;
        }

        if (endPage < total_pages) {
            if (endPage < total_pages - 1) {
                paginationHTML += '<span class="px-2 text-gray-400">...</span>';
            }
            paginationHTML += `
                <button onclick="loadPage(${total_pages})" 
                        class="px-3 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors">
                    ${total_pages}
                </button>
            `;
        }

        // 下一页
        if (current_page < total_pages) {
            paginationHTML += `
                <button onclick="loadPage(${current_page + 1})" 
                        class="px-3 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors">
                    下一页<i class="fas fa-chevron-right ml-1"></i>
                </button>
            `;
        }

        this.pagination.innerHTML = `<div class="flex items-center space-x-2">${paginationHTML}</div>`;
    }
}

// AI助手管理器
class AIAssistantManager {
    constructor(dataManager) {
        this.dataManager = dataManager;
        this.isOpen = false;
        this.chatHistory = [];
        this.initializeElements();
        this.bindEvents();
    }

    initializeElements() {
        this.modal = document.getElementById('ai-assistant-modal');
        this.chatContainer = document.getElementById('ai-chat-container');
        this.input = document.getElementById('ai-input');
        this.sendBtn = document.getElementById('send-ai-message');
        this.openBtn = document.getElementById('ai-assistant-btn');
        this.closeBtn = document.getElementById('close-ai-assistant');
    }

    bindEvents() {
        if (this.openBtn) {
            this.openBtn.addEventListener('click', () => this.open());
        }

        if (this.closeBtn) {
            this.closeBtn.addEventListener('click', () => this.close());
        }

        if (this.sendBtn) {
            this.sendBtn.addEventListener('click', () => this.sendMessage());
        }

        if (this.input) {
            this.input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });
        }

        // 点击模态框外部关闭
        if (this.modal) {
            this.modal.addEventListener('click', (e) => {
                if (e.target === this.modal) {
                    this.close();
                }
            });
        }
    }

    open() {
        this.isOpen = true;
        this.modal.classList.remove('hidden');
        this.input.focus();
    }

    close() {
        this.isOpen = false;
        this.modal.classList.add('hidden');
    }

    async sendMessage() {
        const message = this.input.value.trim();
        if (!message) return;

        // 添加用户消息
        this.addMessage(message, 'user');
        this.input.value = '';

        // 显示加载状态
        this.showTyping();

        try {
            // 发送到AI接口
            const response = await fetch('/api/ai/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    context: 'products',
                    filters: this.dataManager.getFilters()
                })
            });

            const data = await response.json();
            
            this.hideTyping();

            if (data.success) {
                this.addMessage(data.response, 'assistant');
                
                // 如果有推荐产品，显示推荐
                if (data.recommendations && data.recommendations.length > 0) {
                    this.addRecommendations(data.recommendations);
                }
            } else {
                this.addMessage('抱歉，我现在无法回答您的问题。请稍后再试。', 'assistant');
            }
        } catch (error) {
            console.error('AI聊天失败:', error);
            this.hideTyping();
            this.addMessage('网络连接出现问题，请稍后再试。', 'assistant');
        }
    }

    addMessage(content, sender) {
        const messageEl = document.createElement('div');
        messageEl.className = `ai-message ${sender}`;
        
        messageEl.innerHTML = `
            <div class="flex items-start gap-3 ${sender === 'user' ? 'flex-row-reverse' : ''}">
                <div class="w-8 h-8 ${sender === 'user' ? 'bg-gray-600' : 'bg-jytek-blue'} rounded-full flex items-center justify-center">
                    <i class="fas ${sender === 'user' ? 'fa-user' : 'fa-robot'} text-white text-sm"></i>
                </div>
                <div class="message-content">
                    ${content}
                </div>
            </div>
        `;

        this.chatContainer.appendChild(messageEl);
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
        
        this.chatHistory.push({ content, sender, timestamp: Date.now() });
    }

    addRecommendations(recommendations) {
        const recommendationsEl = document.createElement('div');
        recommendationsEl.className = 'ai-message assistant';
        
        const recommendationsHTML = recommendations.map(product => `
            <div class="border border-gray-200 rounded-lg p-3 mb-2 hover:bg-gray-50 cursor-pointer" 
                 onclick="showProductDetail('${product.product_id}')">
                <div class="flex justify-between items-start mb-2">
                    <h4 class="font-medium text-gray-900">${product.name}</h4>
                    <span class="text-sm text-jytek-blue font-medium">${product.price_range}</span>
                </div>
                <p class="text-sm text-gray-600 mb-2">${product.description}</p>
                <div class="flex items-center justify-between">
                    <span class="text-xs text-gray-500">推荐度: ${Math.round(product.recommendation_score * 10)}%</span>
                    <button onclick="showProductDetail('${product.product_id}')" 
                            class="text-xs bg-jytek-blue text-white px-2 py-1 rounded">
                        查看详情
                    </button>
                </div>
            </div>
        `).join('');

        recommendationsEl.innerHTML = `
            <div class="flex items-start gap-3">
                <div class="w-8 h-8 bg-jytek-blue rounded-full flex items-center justify-center">
                    <i class="fas fa-robot text-white text-sm"></i>
                </div>
                <div class="message-content">
                    <p class="mb-3">基于您的需求，我推荐以下产品：</p>
                    ${recommendationsHTML}
                </div>
            </div>
        `;

        this.chatContainer.appendChild(recommendationsEl);
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
    }

    showTyping() {
        const typingEl = document.createElement('div');
        typingEl.id = 'typing-indicator';
        typingEl.className = 'ai-message assistant';
        typingEl.innerHTML = `
            <div class="flex items-start gap-3">
                <div class="w-8 h-8 bg-jytek-blue rounded-full flex items-center justify-center">
                    <i class="fas fa-robot text-white text-sm"></i>
                </div>
                <div class="message-content">
                    <div class="flex items-center space-x-1">
                        <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                        <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                    </div>
                </div>
            </div>
        `;

        this.chatContainer.appendChild(typingEl);
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
    }

    hideTyping() {
        const typingEl = document.getElementById('typing-indicator');
        if (typingEl) {
            typingEl.remove();
        }
    }
}

// 全局变量和函数
let dataManager, searchManager, filterManager, displayManager, aiAssistant;

// 全局函数 - 供HTML调用
window.showProductDetail = async function(productId) {
    const data = await dataManager.fetchProductDetail(productId);
    if (data.success) {
        const modal = document.getElementById('product-modal');
        const product = data.product;
        
        // 填充模态框内容
        document.getElementById('modal-product-name').textContent = product.name || product.part_number;
        document.getElementById('modal-part-number').textContent = product.part_number || product.id;
        document.getElementById('modal-category').textContent = product.category_cn || product.category || '未分类';
        document.getElementById('modal-price').textContent = Utils.formatPrice(product.price);
        document.getElementById('modal-stock-status').textContent = product.stock_status || '未知';
        document.getElementById('modal-delivery-period').textContent = product.delivery_period || '请咨询';
        document.getElementById('modal-description').textContent = product.description || '暂无描述';
        
        // 填充技术规格
        const specsContainer = document.getElementById('modal-specifications');
        if (product.specifications && Object.keys(product.specifications).length > 0) {
            const specsHTML = Object.entries(product.specifications).map(([key, value]) => `
                <div class="flex justify-between py-2 border-b border-gray-200">
                    <span class="text-gray-600">${key}:</span>
                    <span class="font-medium">${value}</span>
                </div>
            `).join('');
            specsContainer.innerHTML = specsHTML;
        } else {
            specsContainer.innerHTML = '<p class="text-gray-500">暂无技术规格信息</p>';
        }
        
        modal.classList.remove('hidden');
    }
};

window.contactSales = function(productId) {
    Utils.showMessage('正在为您转接销售顾问...', 'info');
    // 这里可以集成客服系统或打开联系表单
};

window.downloadDatasheet = function(productId) {
    Utils.showMessage('正在准备下载资料...', 'info');
    // 这里可以触发文件下载
};

window.askAI = function(productId) {
    if (aiAssistant) {
        aiAssistant.open();
        // 可以预填充关于该产品的问题
    }
};

window.addToFavorites = function(productId) {
    const favorites = Utils.storage.get('favorites') || [];
    if (!favorites.includes(productId)) {
        favorites.push(productId);
        Utils.storage.set('favorites', favorites);
        Utils.showMessage('已添加到收藏夹', 'success');
    } else {
        Utils.showMessage('该产品已在收藏夹中', 'info');
    }
};

window.loadPage = function(page) {
    if (displayManager) {
        displayManager.loadProducts(page);
    }
};

// 页面初始化
document.addEventListener('DOMContentLoaded', async function() {
    try {
        // 初始化管理器
        dataManager = new DataManager();
        searchManager = new SearchManager(dataManager);
        filterManager = new FilterManager(dataManager);
        displayManager = new ProductDisplayManager(dataManager);
        aiAssistant = new AIAssistantManager(dataManager);

        // 加载初始数据
        await filterManager.loadCategories();
        await displayManager.loadProducts();

        // 绑定模态框关闭事件
        const modals = ['product-modal', 'compare-modal', 'ai-assistant-modal'];
        modals.forEach(modalId => {
            const modal = document.getElementById(modalId);
            const closeBtn = document.getElementById(`close-${modalId.replace('-modal', '')}`);
            
            if (closeBtn) {
                closeBtn.addEventListener('click', () => {
                    modal.classList.add('hidden');
                });
            }
            
            if (modal) {
                modal.addEventListener('click', (e) => {
                    if (e.target === modal) {
                        modal.classList.add('hidden');
                    }
                });
            }
        });

        // 移动端筛选面板
        const toggleMobileFilters = document.getElementById('toggle-mobile-filters');
        const mobileFilters = document.getElementById('mobile-filters');
        const closeMobileFilters = document.getElementById('close-mobile-filters');

        if (toggleMobileFilters) {
            toggleMobileFilters.addEventListener('click', () => {
                mobileFilters.classList.remove('hidden');
            });
        }

        if (closeMobileFilters) {
            closeMobileFilters.addEventListener('click', () => {
                mobileFilters.classList.add('hidden');
            });
        }

        // 对比功能
        const clearCompare = document.getElementById('clear-compare');
        const startCompare = document.getElementById('start-compare');

        if (clearCompare) {
            clearCompare.addEventListener('click', () => {
                displayManager.compareItems.clear();
                displayManager.updateCompareBar();
                // 清除所有复选框
                document.querySelectorAll('.compare-checkbox').forEach(cb => cb.checked = false);
            });
        }

        if (startCompare) {
            startCompare.addEventListener('click', () => {
                if (displayManager.compareItems.size < 2) {
                    Utils.showMessage('请至少选择2个产品进行对比', 'warning');
                    return;
                }
                // 打开对比模态框
                showCompareModal();
            });
        }

        console.log('产品页面初始化完成');
        
    } catch (error) {
        console.error('页面初始化失败:', error);
        Utils.showMessage('页面初始化失败，请刷新重试', 'error');
    }
});

// 对比模态框
function showCompareModal() {
    const modal = document.getElementById('compare-modal');
    const content = document.getElementById('compare-content');
    
    // 获取对比产品数据
    const compareProducts = Array.from(displayManager.compareItems).map(productId => {
        return dataManager.products.find(p => p.id === productId);
    }).filter(Boolean);

    if (compareProducts.length === 0) {
        Utils.showMessage('没有可对比的产品', 'warning');
        return;
    }

    // 生成对比表格
    const compareHTML = generateCompareTable(compareProducts);
    content.innerHTML = compareHTML;
    modal.classList.remove('hidden');
}

function generateCompareTable(products) {
    const specs = ['name', 'part_number', 'category', 'price', 'stock_status', 'description'];
    const specLabels = {
        'name': '产品名称',
        'part_number': '产品型号',
        'category': '产品分类',
        'price': '价格',
        'stock_status': '库存状态',
        'description': '产品描述'
    };

    let tableHTML = `
        <table class="compare-table">
            <thead>
                <tr>
                    <th class="spec-name">规格项目</th>
                    ${products.map(product => `
                        <th>${product.name || product.part_number}</th>
                    `).join('')}
                </tr>
            </thead>
            <tbody>
    `;

    specs.forEach(spec => {
        tableHTML += `
            <tr>
                <td class="spec-name">${specLabels[spec]}</td>
                ${products.map(product => {
                    let value = product[spec] || '未知';
                    if (spec === 'price') {
                        value = Utils.formatPrice(product.price);
                    }
                    return `<td>${value}</td>`;
                }).join('')}
            </tr>
        `;
    });

    // 添加技术规格对比
    const allSpecs = new Set();
    products.forEach(product => {
        if (product.specifications) {
            Object.keys(product.specifications).forEach(spec => allSpecs.add(spec));
        }
    });

    if (allSpecs.size > 0) {
        tableHTML += `
            <tr>
                <td colspan="${products.length + 1}" class="text-center font-semibold bg-gray-100 py-3">
                    技术规格对比
                </td>
            </tr>
        `;

        allSpecs.forEach(spec => {
            tableHTML += `
                <tr>
                    <td class="spec-name">${spec}</td>
                    ${products.map(product => {
                        const value = product.specifications?.[spec] || '-';
                        return `<td>${value}</td>`;
                    }).join('')}
                </tr>
            `;
        });
    }

    tableHTML += `
            </tbody>
        </table>
        <div class="mt-6 flex justify-center space-x-4">
            ${products.map(product => `
                <button onclick="showProductDetail('${product.id}')" 
                        class="bg-jytek-blue hover:bg-jytek-light-blue text-white px-6 py-2 rounded-lg transition-colors">
                    查看${product.name || product.part_number}详情
                </button>
            `).join('')}
        </div>
    `;

    return tableHTML;
}
