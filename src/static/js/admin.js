/**
 * 锐视测控平台管理员后台JavaScript
 * Admin backend JavaScript for Ruishi Control Platform
 */

// 全局变量
let currentUser = null;
let currentPage = 1;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
    setupEventListeners();
});

// 检查认证状态
async function checkAuth() {
    try {
        const response = await fetch('/admin/profile');
        const data = await response.json();
        
        if (data.success) {
            currentUser = data.user;
            document.getElementById('admin-username').textContent = `欢迎，${currentUser.username}`;
            document.getElementById('login-modal').style.display = 'none';
            loadDashboard();
        } else {
            showLoginModal();
        }
    } catch (error) {
        console.error('认证检查失败:', error);
        showLoginModal();
    }
}

// 显示登录模态框
function showLoginModal() {
    document.getElementById('login-modal').style.display = 'flex';
}

// 设置事件监听器
function setupEventListeners() {
    // 登录表单
    document.getElementById('login-form').addEventListener('submit', handleLogin);
    
    // 上传表单
    document.getElementById('upload-form').addEventListener('submit', handleUpload);
    
    // 文件选择
    const fileInput = document.getElementById('file-input');
    const uploadArea = document.getElementById('upload-area');
    
    uploadArea.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelect);
    
    // 拖拽上传
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // 搜索功能
    document.getElementById('search-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchDocuments();
        }
    });
}

// 处理登录
async function handleLogin(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const loginData = {
        username: formData.get('username'),
        password: formData.get('password')
    };
    
    try {
        const response = await fetch('/admin/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(loginData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentUser = data.user;
            document.getElementById('admin-username').textContent = `欢迎，${currentUser.username}`;
            document.getElementById('login-modal').style.display = 'none';
            showNotification('登录成功', 'success');
            loadDashboard();
        } else {
            showNotification(data.error || '登录失败', 'error');
        }
    } catch (error) {
        console.error('登录失败:', error);
        showNotification('登录失败，请稍后重试', 'error');
    }
}

// 登出
async function logout() {
    try {
        await fetch('/admin/logout', { method: 'POST' });
        currentUser = null;
        showLoginModal();
        showNotification('已登出', 'info');
    } catch (error) {
        console.error('登出失败:', error);
    }
}

// 显示指定区域
function showSection(sectionName) {
    // 隐藏所有区域
    document.querySelectorAll('.section').forEach(section => {
        section.classList.add('hidden');
    });
    
    // 移除所有侧边栏活跃状态
    document.querySelectorAll('.sidebar-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // 显示指定区域
    document.getElementById(`${sectionName}-section`).classList.remove('hidden');
    
    // 激活对应侧边栏项
    event.target.classList.add('active');
    
    // 加载对应数据
    switch(sectionName) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'documents':
            loadDocuments();
            break;
        case 'statistics':
            loadStatistics();
            break;
    }
}

// 加载仪表板
async function loadDashboard() {
    try {
        const response = await fetch('/admin/statistics');
        const data = await response.json();
        
        if (data.success) {
            const stats = data.statistics;
            
            // 更新统计数字
            document.getElementById('total-documents').textContent = stats.total_documents || 0;
            document.getElementById('total-users').textContent = stats.total_users || 0;
            document.getElementById('total-conversations').textContent = stats.total_conversations || 0;
            
            // 显示最近文档
            displayRecentDocuments(stats.recent_documents || []);
            
            // 显示分类统计
            displayCategoryStats(stats.documents_by_category || {});
        }
    } catch (error) {
        console.error('加载仪表板失败:', error);
    }
}

// 显示最近文档
function displayRecentDocuments(documents) {
    const container = document.getElementById('recent-documents');
    
    if (documents.length === 0) {
        container.innerHTML = '<p class="text-gray-500 text-center py-4">暂无文档</p>';
        return;
    }
    
    container.innerHTML = documents.map(doc => `
        <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div class="flex-1">
                <p class="font-medium text-gray-900">${doc.filename}</p>
                <p class="text-sm text-gray-500">${doc.category} • ${formatDate(doc.upload_time)}</p>
            </div>
            <i class="fas fa-file-alt text-gray-400"></i>
        </div>
    `).join('');
}

// 显示分类统计
function displayCategoryStats(categories) {
    const container = document.getElementById('category-stats');
    
    if (Object.keys(categories).length === 0) {
        container.innerHTML = '<p class="text-gray-500 text-center py-4">暂无数据</p>';
        return;
    }
    
    const total = Object.values(categories).reduce((sum, count) => sum + count, 0);
    
    container.innerHTML = Object.entries(categories).map(([category, count]) => {
        const percentage = total > 0 ? Math.round((count / total) * 100) : 0;
        return `
            <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">${getCategoryName(category)}</span>
                <div class="flex items-center space-x-2">
                    <div class="w-16 bg-gray-200 rounded-full h-2">
                        <div class="bg-blue-600 h-2 rounded-full" style="width: ${percentage}%"></div>
                    </div>
                    <span class="text-sm font-medium text-gray-900">${count}</span>
                </div>
            </div>
        `;
    }).join('');
}

// 获取分类中文名称
function getCategoryName(category) {
    const names = {
        'general': '通用文档',
        'product_specs': '产品规格',
        'user_manual': '用户手册',
        'technical_docs': '技术文档',
        'application_notes': '应用笔记',
        'software_docs': '软件文档',
        'training_materials': '培训资料'
    };
    return names[category] || category;
}

// 加载文档列表
async function loadDocuments(page = 1) {
    try {
        const response = await fetch(`/admin/documents?page=${page}&per_page=20`);
        const data = await response.json();
        
        if (data.success) {
            displayDocuments(data.data.documents);
            displayPagination(data.data);
            currentPage = page;
        }
    } catch (error) {
        console.error('加载文档列表失败:', error);
        showNotification('加载文档列表失败', 'error');
    }
}

// 显示文档列表
function displayDocuments(documents) {
    const container = document.getElementById('documents-table');
    
    if (documents.length === 0) {
        container.innerHTML = '<p class="text-gray-500 text-center py-8">暂无文档</p>';
        return;
    }
    
    container.innerHTML = `
        <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
                <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">文档名称</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">分类</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">类型</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">大小</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">上传时间</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
                </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
                ${documents.map(doc => `
                    <tr>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <div class="flex items-center">
                                <i class="fas fa-file-${getFileIcon(doc.file_type)} text-gray-400 mr-3"></i>
                                <div>
                                    <div class="text-sm font-medium text-gray-900">${doc.title || doc.original_filename}</div>
                                    <div class="text-sm text-gray-500">${doc.original_filename}</div>
                                </div>
                            </div>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                                ${getCategoryName(doc.category)}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${doc.file_type}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${formatFileSize(doc.file_size)}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${formatDate(doc.upload_time)}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                            <button onclick="viewDocument(${doc.id})" class="text-blue-600 hover:text-blue-900 mr-3">
                                <i class="fas fa-eye"></i>
                            </button>
                            <button onclick="deleteDocument(${doc.id})" class="text-red-600 hover:text-red-900">
                                <i class="fas fa-trash"></i>
                            </button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}

// 显示分页
function displayPagination(data) {
    const container = document.getElementById('documents-pagination');
    
    if (data.pages <= 1) {
        container.innerHTML = '';
        return;
    }
    
    let pagination = '<div class="flex space-x-2">';
    
    // 上一页
    if (data.page > 1) {
        pagination += `<button onclick="loadDocuments(${data.page - 1})" class="px-3 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">上一页</button>`;
    }
    
    // 页码
    for (let i = Math.max(1, data.page - 2); i <= Math.min(data.pages, data.page + 2); i++) {
        const active = i === data.page ? 'bg-blue-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-50';
        pagination += `<button onclick="loadDocuments(${i})" class="px-3 py-2 border border-gray-300 rounded-lg ${active}">${i}</button>`;
    }
    
    // 下一页
    if (data.page < data.pages) {
        pagination += `<button onclick="loadDocuments(${data.page + 1})" class="px-3 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">下一页</button>`;
    }
    
    pagination += '</div>';
    container.innerHTML = pagination;
}

// 获取文件图标
function getFileIcon(fileType) {
    const icons = {
        'pdf': 'pdf',
        'word': 'word',
        'powerpoint': 'powerpoint',
        'excel': 'excel',
        'text': 'alt',
        'image': 'image'
    };
    return icons[fileType] || 'alt';
}

// 刷新文档列表
function refreshDocuments() {
    loadDocuments(currentPage);
    showNotification('文档列表已刷新', 'info');
}

// 处理文件选择
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        displayFileInfo(file);
    }
}

// 显示文件信息
function displayFileInfo(file) {
    document.getElementById('upload-placeholder').classList.add('hidden');
    document.getElementById('file-info').classList.remove('hidden');
    document.getElementById('file-name').textContent = file.name;
    document.getElementById('file-size').textContent = formatFileSize(file.size);
}

// 处理拖拽
function handleDragOver(event) {
    event.preventDefault();
    event.currentTarget.classList.add('dragover');
}

function handleDragLeave(event) {
    event.currentTarget.classList.remove('dragover');
}

function handleDrop(event) {
    event.preventDefault();
    event.currentTarget.classList.remove('dragover');
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        document.getElementById('file-input').files = files;
        displayFileInfo(files[0]);
    }
}

// 处理文件上传
async function handleUpload(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
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
        
        const response = await fetch('/admin/documents/upload', {
            method: 'POST',
            body: formData
        });
        
        clearInterval(progressInterval);
        progressBar.style.width = '100%';
        
        const data = await response.json();
        
        if (data.success) {
            statusText.textContent = '上传成功！';
            showNotification(data.message, 'success');
            resetUploadForm();
            
            // 如果当前在文档管理页面，刷新列表
            if (!document.getElementById('documents-section').classList.contains('hidden')) {
                loadDocuments(currentPage);
            }
            
            setTimeout(() => {
                progressContainer.classList.add('hidden');
            }, 2000);
        } else {
            throw new Error(data.error || '上传失败');
        }
    } catch (error) {
        console.error('文件上传失败:', error);
        statusText.textContent = '上传失败';
        showNotification(error.message || '文件上传失败，请稍后重试', 'error');
        
        setTimeout(() => {
            progressContainer.classList.add('hidden');
        }, 3000);
    }
}

// 重置上传表单
function resetUploadForm() {
    document.getElementById('upload-form').reset();
    document.getElementById('upload-placeholder').classList.remove('hidden');
    document.getElementById('file-info').classList.add('hidden');
}

// 搜索文档
async function searchDocuments() {
    const query = document.getElementById('search-input').value.trim();
    const category = document.getElementById('search-category').value;
    
    if (!query && !category) {
        showNotification('请输入搜索关键词或选择分类', 'warning');
        return;
    }
    
    try {
        const params = new URLSearchParams();
        if (query) params.append('q', query);
        if (category) params.append('category', category);
        params.append('limit', '20');
        
        const response = await fetch(`/admin/documents/search?${params}`);
        const data = await response.json();
        
        if (data.success) {
            displaySearchResults(data.documents);
        } else {
            throw new Error(data.error || '搜索失败');
        }
    } catch (error) {
        console.error('搜索文档失败:', error);
        showNotification('搜索失败，请稍后重试', 'error');
    }
}

// 显示搜索结果
function displaySearchResults(documents) {
    const container = document.getElementById('search-results');
    
    if (documents.length === 0) {
        container.innerHTML = `
            <div class="p-6 text-center text-gray-500">
                <i class="fas fa-search text-4xl mb-4"></i>
                <p>未找到匹配的文档</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = `
        <div class="p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">搜索结果 (${documents.length})</h3>
            <div class="space-y-4">
                ${documents.map(doc => `
                    <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                        <div class="flex items-center space-x-4">
                            <i class="fas fa-file-${getFileIcon(doc.file_type)} text-gray-400 text-xl"></i>
                            <div>
                                <h4 class="font-medium text-gray-900">${doc.title || doc.original_filename}</h4>
                                <p class="text-sm text-gray-500">${doc.content_summary || '无描述'}</p>
                                <div class="flex items-center space-x-4 mt-1">
                                    <span class="text-xs text-gray-500">${getCategoryName(doc.category)}</span>
                                    <span class="text-xs text-gray-500">${formatFileSize(doc.file_size)}</span>
                                    <span class="text-xs text-gray-500">${formatDate(doc.upload_time)}</span>
                                </div>
                            </div>
                        </div>
                        <div class="flex space-x-2">
                            <button onclick="viewDocument(${doc.id})" class="text-blue-600 hover:text-blue-900">
                                <i class="fas fa-eye"></i>
                            </button>
                            <button onclick="deleteDocument(${doc.id})" class="text-red-600 hover:text-red-900">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

// 查看文档
async function viewDocument(documentId) {
    try {
        const response = await fetch(`/admin/documents/${documentId}/content`);
        const data = await response.json();
        
        if (data.success) {
            // 创建文档查看模态框
            const modal = document.createElement('div');
            modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4';
            modal.innerHTML = `
                <div class="bg-white rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] overflow-hidden">
                    <div class="flex justify-between items-center p-6 border-b">
                        <h3 class="text-lg font-semibold text-gray-900">文档内容</h3>
                        <button onclick="this.closest('.fixed').remove()" class="text-gray-400 hover:text-gray-600">
                            <i class="fas fa-times text-xl"></i>
                        </button>
                    </div>
                    <div class="p-6 overflow-y-auto max-h-[70vh]">
                        <pre class="whitespace-pre-wrap text-sm text-gray-700">${data.content}</pre>
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
        } else {
            throw new Error(data.error || '获取文档内容失败');
        }
    } catch (error) {
        console.error('查看文档失败:', error);
        showNotification('查看文档失败', 'error');
    }
}

// 删除文档
async function deleteDocument(documentId) {
    if (!confirm('确定要删除这个文档吗？此操作不可撤销。')) {
        return;
    }
    
    try {
        const response = await fetch(`/admin/documents/${documentId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(data.message, 'success');
            
            // 刷新当前页面
            if (!document.getElementById('documents-section').classList.contains('hidden')) {
                loadDocuments(currentPage);
            } else if (!document.getElementById('search-section').classList.contains('hidden')) {
                searchDocuments();
            }
        } else {
            throw new Error(data.error || '删除失败');
        }
    } catch (error) {
        console.error('删除文档失败:', error);
        showNotification('删除文档失败', 'error');
    }
}

// 加载统计信息
async function loadStatistics() {
    try {
        const response = await fetch('/admin/statistics');
        const data = await response.json();
        
        if (data.success) {
            const stats = data.statistics;
            
            // 显示文档类型统计
            displayTypeStats(stats.documents_by_type || {});
            
            // 显示AI提供商统计
            displayProviderStats(stats.conversations_by_provider || {});
        }
    } catch (error) {
        console.error('加载统计信息失败:', error);
    }
}

// 显示文档类型统计
function displayTypeStats(types) {
    const container = document.getElementById('type-stats');
    
    if (Object.keys(types).length === 0) {
        container.innerHTML = '<p class="text-gray-500 text-center py-4">暂无数据</p>';
        return;
    }
    
    const total = Object.values(types).reduce((sum, count) => sum + count, 0);
    
    container.innerHTML = Object.entries(types).map(([type, count]) => {
        const percentage = total > 0 ? Math.round((count / total) * 100) : 0;
        return `
            <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">${type}</span>
                <div class="flex items-center space-x-2">
                    <div class="w-16 bg-gray-200 rounded-full h-2">
                        <div class="bg-green-600 h-2 rounded-full" style="width: ${percentage}%"></div>
                    </div>
                    <span class="text-sm font-medium text-gray-900">${count}</span>
                </div>
            </div>
        `;
    }).join('');
}

// 显示AI提供商统计
function displayProviderStats(providers) {
    const container = document.getElementById('provider-stats');
    
    if (Object.keys(providers).length === 0) {
        container.innerHTML = '<p class="text-gray-500 text-center py-4">暂无数据</p>';
        return;
    }
    
    const total = Object.values(providers).reduce((sum, count) => sum + count, 0);
    
    container.innerHTML = Object.entries(providers).map(([provider, count]) => {
        const percentage = total > 0 ? Math.round((count / total) * 100) : 0;
        return `
            <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">${provider}</span>
                <div class="flex items-center space-x-2">
                    <div class="w-16 bg-gray-200 rounded-full h-2">
                        <div class="bg-purple-600 h-2 rounded-full" style="width: ${percentage}%"></div>
                    </div>
                    <span class="text-sm font-medium text-gray-900">${count}</span>
                </div>
            </div>
        `;
    }).join('');
}

// 工具函数
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN') + ' ' + date.toLocaleTimeString('zh-CN', {hour: '2-digit', minute: '2-digit'});
}

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
