/**
 * 产品中心页面JavaScript
 */

// 全局变量
let currentProducts = [];
let allProducts = [];
let currentCategories = [];
let currentView = 'grid';
let currentPage = 1;
let itemsPerPage = 12;
let currentFilters = {
    category: '',
    keyword: '',
    priceRanges: [],
    stockStatus: [],
    sortBy: 'name'
};

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializePage();
});

/**
 * 初始化页面
 */
async function initializePage() {
    try {
        showLoading();
        await loadCategories();
        await loadProducts();
        setupEventListeners();
        hideLoading();
    } catch (error) {
        console.error('页面初始化失败:', error);
        showError('页面加载失败，请刷新重试');
    }
}

/**
 * 设置事件监听器
 */
function setupEventListeners() {
    // 搜索输入框回车事件
    document.getElementById('search-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchProducts();
        }
    });

    // 价格筛选器变化事件
    document.querySelectorAll('.price-filter').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updatePriceFilters();
        });
    });

    // 库存筛选器变化事件
    document.querySelectorAll('.stock-filter').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateStockFilters();
        });
    });

    // 排序选择器变化事件
    document.getElementById('sort-select').addEventListener('change', function() {
        currentFilters.sortBy = this.value;
        sortProducts();
    });
}

/**
 * 加载产品分类
 */
async function loadCategories() {
    try {
        const response = await fetch('/api/products/categories');
        const data = await response.json();
        
        if (data.success) {
            currentCategories = data.categories;
            renderCategoryFilters();
        }
    } catch (error) {
        console.error('加载分类失败:', error);
    }
}

/**
 * 渲染分类筛选器
 */
function renderCategoryFilters() {
    const container = document.getElementById('category-filters');
    const allButton = container.querySelector('.category-filter');
    
    currentCategories.forEach(category => {
        const button = document.createElement('button');
        button.className = 'category-filter w-full text-left px-3 py-2 rounded-lg text-sm hover:bg-gray-100';
        button.textContent = `${category.name_cn} (${category.count})`;
        button.onclick = () => filterByCategory(category.name_en);
        container.appendChild(button);
    });
}

/**
 * 加载产品列表
 */
async function loadProducts(page = 1) {
    try {
        const params = new URLSearchParams({
            page: page,
            per_page: itemsPerPage,
            keyword: currentFilters.keyword,
            category: currentFilters.category
        });

        const response = await fetch(`/api/products?${params}`);
        const data = await response.json();
        
        if (data.success) {
            currentProducts = data.products;
            allProducts = data.products; // 保存所有产品用于客户端筛选
            renderProducts();
            renderPagination(data.pagination);
        }
    } catch (error) {
        console.error('加载产品失败:', error);
        showError('加载产品失败');
    }
}

/**
 * 渲染产品列表
 */
function renderProducts() {
    const gridContainer = document.getElementById('products-grid');
    const listContainer = document.getElementById('products-list');
    
    // 清空容器
    gridContainer.innerHTML = '';
    listContainer.innerHTML = '';
    
    if (currentProducts.length === 0) {
        showEmptyState();
        return;
    }
    
    hideEmptyState();
    
    if (currentView === 'grid') {
        renderGridView();
        showGridView();
    } else {
        renderListView();
        showListView();
    }
}

/**
 * 渲染网格视图
 */
function renderGridView() {
    const container = document.getElementById('products-grid');
    
    currentProducts.forEach(product => {
        const card = createProductCard(product);
        container.appendChild(card);
    });
}

/**
 * 渲染列表视图
 */
function renderListView() {
    const container = document.getElementById('products-list');
    
    currentProducts.forEach(product => {
        const item = createProductListItem(product);
        container.appendChild(item);
    });
}

/**
 * 创建产品卡片
 */
function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'product-card bg-white rounded-lg shadow-sm hover:shadow-md transition-all duration-300 cursor-pointer';
    card.onclick = () => showProductDetail(product.id);
    
    const stockClass = product.stock_status === '现货' ? 'stock-available' : 'stock-unavailable';
    const stockIcon = product.stock_status === '现货' ? 'fas fa-check-circle' : 'fas fa-times-circle';
    
    card.innerHTML = `
        <div class="p-6">
            <div class="flex justify-between items-start mb-4">
                <h3 class="text-lg font-semibold text-gray-900 line-clamp-2">${product.name || product.part_number}</h3>
                <span class="price-badge text-white px-3 py-1 rounded-full text-sm font-medium">
                    ¥${product.price ? product.price.toLocaleString() : '询价'}
                </span>
            </div>
            
            <div class="space-y-2 mb-4">
                <div class="flex items-center text-sm text-gray-600">
                    <i class="fas fa-tag mr-2"></i>
                    <span>${product.part_number}</span>
                </div>
                <div class="flex items-center text-sm text-gray-600">
                    <i class="fas fa-folder mr-2"></i>
                    <span>${product.category_cn || product.category}</span>
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
                <button onclick="event.stopPropagation(); showProductDetail('${product.id}')" 
                        class="flex-1 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm">
                    查看详情
                </button>
                <button onclick="event.stopPropagation(); contactSales('${product.id}')" 
                        class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 text-sm">
                    <i class="fas fa-envelope"></i>
                </button>
            </div>
        </div>
    `;
    
    return card;
}

/**
 * 创建产品列表项
 */
function createProductListItem(product) {
    const item = document.createElement('div');
    item.className = 'bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-all duration-300';
    
    const stockClass = product.stock_status === '现货' ? 'stock-available' : 'stock-unavailable';
    const stockIcon = product.stock_status === '现货' ? 'fas fa-check-circle' : 'fas fa-times-circle';
    
    item.innerHTML = `
        <div class="flex flex-col md:flex-row md:items-center justify-between">
            <div class="flex-1">
                <div class="flex flex-col md:flex-row md:items-center md:space-x-6">
                    <div class="flex-1 mb-4 md:mb-0">
                        <h3 class="text-lg font-semibold text-gray-900 mb-2">${product.name || product.part_number}</h3>
                        <div class="flex flex-wrap items-center gap-4 text-sm text-gray-600">
                            <span><i class="fas fa-tag mr-1"></i>${product.part_number}</span>
                            <span><i class="fas fa-folder mr-1"></i>${product.category_cn || product.category}</span>
                            <span class="${stockClass}"><i class="${stockIcon} mr-1"></i>${product.stock_status || '未知'}</span>
                        </div>
                        <p class="text-gray-600 text-sm mt-2 line-clamp-2">${product.description || '暂无描述'}</p>
                    </div>
                    
                    <div class="flex flex-col md:items-end space-y-2">
                        <span class="price-badge text-white px-4 py-2 rounded-full font-medium">
                            ¥${product.price ? product.price.toLocaleString() : '询价'}
                        </span>
                        <div class="flex space-x-2">
                            <button onclick="showProductDetail('${product.id}')" 
                                    class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm">
                                查看详情
                            </button>
                            <button onclick="contactSales('${product.id}')" 
                                    class="border border-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-50 text-sm">
                                <i class="fas fa-envelope mr-1"></i>联系
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    return item;
}

/**
 * 搜索产品
 */
async function searchProducts() {
    const keyword = document.getElementById('search-input').value.trim();
    currentFilters.keyword = keyword;
    currentPage = 1;
    
    showLoading();
    await loadProducts(currentPage);
    hideLoading();
}

/**
 * 按分类筛选
 */
async function filterByCategory(category) {
    currentFilters.category = category;
    currentPage = 1;
    
    // 更新分类按钮状态
    document.querySelectorAll('.category-filter').forEach(btn => {
        btn.classList.remove('active');
    });
    
    if (category === '') {
        document.querySelector('.category-filter').classList.add('active');
    } else {
        event.target.classList.add('active');
    }
    
    showLoading();
    await loadProducts(currentPage);
    hideLoading();
}

/**
 * 更新价格筛选器
 */
function updatePriceFilters() {
    const checkedBoxes = document.querySelectorAll('.price-filter:checked');
    currentFilters.priceRanges = Array.from(checkedBoxes).map(cb => cb.value);
}

/**
 * 更新库存筛选器
 */
function updateStockFilters() {
    const checkedBoxes = document.querySelectorAll('.stock-filter:checked');
    currentFilters.stockStatus = Array.from(checkedBoxes).map(cb => cb.value);
}

/**
 * 应用筛选器
 */
function applyFilters() {
    updatePriceFilters();
    updateStockFilters();
    
    let filteredProducts = [...allProducts];
    
    // 价格筛选
    if (currentFilters.priceRanges.length > 0) {
        filteredProducts = filteredProducts.filter(product => {
            const price = product.price || 0;
            return currentFilters.priceRanges.some(range => {
                switch (range) {
                    case '0-1000': return price >= 0 && price < 1000;
                    case '1000-5000': return price >= 1000 && price < 5000;
                    case '5000-10000': return price >= 5000 && price < 10000;
                    case '10000-50000': return price >= 10000 && price < 50000;
                    case '50000+': return price >= 50000;
                    default: return false;
                }
            });
        });
    }
    
    // 库存状态筛选
    if (currentFilters.stockStatus.length > 0) {
        filteredProducts = filteredProducts.filter(product => 
            currentFilters.stockStatus.includes(product.stock_status)
        );
    }
    
    currentProducts = filteredProducts;
    renderProducts();
}

/**
 * 清除筛选器
 */
function clearFilters() {
    // 清除价格筛选
    document.querySelectorAll('.price-filter').forEach(cb => cb.checked = false);
    
    // 清除库存筛选
    document.querySelectorAll('.stock-filter').forEach(cb => cb.checked = false);
    
    // 重置筛选条件
    currentFilters.priceRanges = [];
    currentFilters.stockStatus = [];
    
    // 重新显示所有产品
    currentProducts = [...allProducts];
    renderProducts();
}

/**
 * 排序产品
 */
function sortProducts() {
    const sortBy = document.getElementById('sort-select').value;
    
    currentProducts.sort((a, b) => {
        switch (sortBy) {
            case 'name':
                return (a.name || a.part_number).localeCompare(b.name || b.part_number);
            case 'price-asc':
                return (a.price || 0) - (b.price || 0);
            case 'price-desc':
                return (b.price || 0) - (a.price || 0);
            case 'update-date':
                return new Date(b.updated_at || 0) - new Date(a.updated_at || 0);
            default:
                return 0;
        }
    });
    
    renderProducts();
}

/**
 * 设置视图模式
 */
function setView(view) {
    currentView = view;
    
    // 更新按钮状态
    document.getElementById('grid-view-btn').className = view === 'grid' 
        ? 'p-2 rounded-lg bg-blue-600 text-white' 
        : 'p-2 rounded-lg text-gray-600 hover:bg-gray-100';
    
    document.getElementById('list-view-btn').className = view === 'list' 
        ? 'p-2 rounded-lg bg-blue-600 text-white' 
        : 'p-2 rounded-lg text-gray-600 hover:bg-gray-100';
    
    renderProducts();
}

/**
 * 显示网格视图
 */
function showGridView() {
    document.getElementById('products-grid').classList.remove('hidden');
    document.getElementById('products-list').classList.add('hidden');
}

/**
 * 显示列表视图
 */
function showListView() {
    document.getElementById('products-list').classList.remove('hidden');
    document.getElementById('products-grid').classList.add('hidden');
}

/**
 * 显示产品详情
 */
async function showProductDetail(productId) {
    try {
        const response = await fetch(`/api/products/${productId}`);
        const data = await response.json();
        
        if (data.success) {
            const product = data.product;
            
            // 填充模态框内容
            document.getElementById('modal-product-name').textContent = product.name || product.part_number;
            document.getElementById('modal-part-number').textContent = product.part_number;
            document.getElementById('modal-category').textContent = product.category_cn || product.category;
            document.getElementById('modal-price').textContent = product.price ? `¥${product.price.toLocaleString()}` : '询价';
            document.getElementById('modal-stock-status').textContent = product.stock_status || '未知';
            document.getElementById('modal-delivery-period').textContent = product.delivery_period || '请咨询';
            document.getElementById('modal-description').textContent = product.description || '暂无描述';
            
            // 渲染规格表
            renderSpecifications(product.specifications || {});
            
            // 显示模态框
            document.getElementById('product-modal').classList.remove('hidden');
        }
    } catch (error) {
        console.error('获取产品详情失败:', error);
        showError('获取产品详情失败');
    }
}

/**
 * 渲染产品规格
 */
function renderSpecifications(specs) {
    const container = document.getElementById('modal-specifications');
    
    if (Object.keys(specs).length === 0) {
        container.innerHTML = '<p class="text-gray-500">暂无技术规格信息</p>';
        return;
    }
    
    let html = '<table class="w-full text-sm">';
    for (const [key, value] of Object.entries(specs)) {
        html += `
            <tr class="border-b border-gray-200">
                <td class="py-2 pr-4 font-medium text-gray-700">${key}:</td>
                <td class="py-2 text-gray-600">${value}</td>
            </tr>
        `;
    }
    html += '</table>';
    
    container.innerHTML = html;
}

/**
 * 关闭产品详情模态框
 */
function closeProductModal() {
    document.getElementById('product-modal').classList.add('hidden');
}

/**
 * 联系销售
 */
function contactSales(productId = null) {
    const subject = productId ? `产品咨询 - ${productId}` : '产品咨询';
    const body = productId ? `我对产品 ${productId} 感兴趣，请联系我。` : '我对贵公司的产品感兴趣，请联系我。';
    
    const mailtoLink = `mailto:sales@jytek.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    window.open(mailtoLink);
}

/**
 * 下载产品资料
 */
function downloadDatasheet() {
    showMessage('产品资料下载功能正在开发中', 'info');
}

/**
 * 询问AI
 */
function askAI() {
    const productName = document.getElementById('modal-product-name').textContent;
    const query = `请介绍一下产品 ${productName} 的特点和应用场景`;
    
    // 跳转到AI聊天页面并传递查询
    window.open(`/chat?q=${encodeURIComponent(query)}`, '_blank');
}

/**
 * 渲染分页
 */
function renderPagination(pagination) {
    const container = document.getElementById('pagination');
    
    if (pagination.pages <= 1) {
        container.classList.add('hidden');
        return;
    }
    
    container.classList.remove('hidden');
    
    let html = '';
    
    // 上一页
    if (pagination.page > 1) {
        html += `<button onclick="loadProducts(${pagination.page - 1})" class="px-3 py-2 mx-1 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">上一页</button>`;
    }
    
    // 页码
    const startPage = Math.max(1, pagination.page - 2);
    const endPage = Math.min(pagination.pages, pagination.page + 2);
    
    for (let i = startPage; i <= endPage; i++) {
        const isActive = i === pagination.page;
        const className = isActive 
            ? 'px-3 py-2 mx-1 bg-blue-600 text-white rounded-lg' 
            : 'px-3 py-2 mx-1 bg-white border border-gray-300 rounded-lg hover:bg-gray-50';
        
        html += `<button onclick="loadProducts(${i})" class="${className}">${i}</button>`;
    }
    
    // 下一页
    if (pagination.page < pagination.pages) {
        html += `<button onclick="loadProducts(${pagination.page + 1})" class="px-3 py-2 mx-1 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">下一页</button>`;
    }
    
    container.innerHTML = html;
}

/**
 * 显示加载状态
 */
function showLoading() {
    document.getElementById('loading-state').classList.remove('hidden');
    document.getElementById('products-grid').classList.add('hidden');
    document.getElementById('products-list').classList.add('hidden');
    document.getElementById('empty-state').classList.add('hidden');
}

/**
 * 隐藏加载状态
 */
function hideLoading() {
    document.getElementById('loading-state').classList.add('hidden');
}

/**
 * 显示空状态
 */
function showEmptyState() {
    document.getElementById('empty-state').classList.remove('hidden');
    document.getElementById('products-grid').classList.add('hidden');
    document.getElementById('products-list').classList.add('hidden');
}

/**
 * 隐藏空状态
 */
function hideEmptyState() {
    document.getElementById('empty-state').classList.add('hidden');
}

/**
 * 显示错误消息
 */
function showError(message) {
    showMessage(message, 'error');
}

/**
 * 显示消息
 */
function showMessage(message, type = 'info') {
    // 创建消息元素
    const messageEl = document.createElement('div');
    messageEl.className = `fixed top-4 right-4 z-50 px-6 py-3 rounded-lg shadow-lg ${
        type === 'error' ? 'bg-red-600 text-white' : 
        type === 'success' ? 'bg-green-600 text-white' : 
        'bg-blue-600 text-white'
    }`;
    messageEl.textContent = message;
    
    document.body.appendChild(messageEl);
    
    // 3秒后自动移除
    setTimeout(() => {
        if (messageEl.parentNode) {
            messageEl.parentNode.removeChild(messageEl);
        }
    }, 3000);
}

// 工具函数：限制文本行数
const style = document.createElement('style');
style.textContent = `
    .line-clamp-2 {
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    .line-clamp-3 {
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
`;
document.head.appendChild(style);
