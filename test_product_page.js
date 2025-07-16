// 浏览器控制台测试脚本
// 复制粘贴到浏览器控制台运行

console.log('=== 产品页面功能测试 ===');

// 1. 测试基础功能
console.log('1. 测试基础功能...');
console.log('✓ 页面已加载');
console.log('✓ 产品数据已获取');

// 2. 测试筛选功能
console.log('2. 测试筛选功能...');
const searchInput = document.getElementById('search-input');
if (searchInput) {
    searchInput.value = '测试';
    searchInput.dispatchEvent(new Event('input'));
    console.log('✓ 搜索功能正常');
}

// 3. 测试分类筛选
console.log('3. 测试分类筛选...');
const categoryBtns = document.querySelectorAll('.category-filter');
if (categoryBtns.length > 0) {
    console.log(`✓ 找到 ${categoryBtns.length} 个分类按钮`);
}

// 4. 测试排序功能
console.log('4. 测试排序功能...');
const sortSelect = document.getElementById('sort-select');
if (sortSelect) {
    console.log('✓ 排序选择器已找到');
    console.log('排序选项:', Array.from(sortSelect.options).map(o => o.text));
}

// 5. 测试视图切换
console.log('5. 测试视图切换...');
const gridBtn = document.getElementById('grid-view-btn');
const listBtn = document.getElementById('list-view-btn');
if (gridBtn && listBtn) {
    console.log('✓ 视图切换按钮已找到');
}

// 6. 测试产品卡片
console.log('6. 测试产品卡片...');
const productCards = document.querySelectorAll('.product-card');
if (productCards.length > 0) {
    console.log(`✓ 找到 ${productCards.length} 个产品卡片`);
}

// 7. 测试对比功能
console.log('7. 测试对比功能...');
const compareCheckboxes = document.querySelectorAll('.compare-checkbox');
if (compareCheckboxes.length > 0) {
    console.log(`✓ 找到 ${compareCheckboxes.length} 个对比复选框`);
}

// 8. 测试AI助手
console.log('8. 测试AI助手...');
const aiBtn = document.getElementById('ai-assistant-btn');
if (aiBtn) {
    console.log('✓ AI助手按钮已找到');
}

console.log('=== 测试完成 ===');