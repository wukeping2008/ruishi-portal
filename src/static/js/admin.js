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
        case 'prompts':
            loadPromptManagement();
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
        // 加载基础统计
        const response = await fetch('/admin/statistics');
        const data = await response.json();
        
        if (data.success) {
            const stats = data.statistics;
            
            // 更新概览数据
            document.getElementById('stats-total-conversations').textContent = stats.total_conversations || 0;
            
            // 显示文档类型统计
            displayTypeStats(stats.documents_by_type || {});
            
            // 显示AI提供商统计
            displayProviderStats(stats.conversations_by_provider || {});
        }
        
        // 加载详细统计
        await loadDetailedStatistics();
        
    } catch (error) {
        console.error('加载统计信息失败:', error);
    }
}

// 加载详细统计信息
async function loadDetailedStatistics() {
    try {
        // 并行加载各种统计数据
        const [
            keywordResponse,
            userResponse,
            documentUsageResponse,
            triggerResponse,
            conversationsResponse
        ] = await Promise.all([
            fetch('/admin/keyword-statistics'),
            fetch('/admin/user-statistics'),
            fetch('/admin/document-usage-statistics'),
            fetch('/admin/trigger-statistics'),
            fetch('/admin/detailed-conversations?per_page=10')
        ]);

        // 处理关键词统计
        if (keywordResponse.ok) {
            const keywordData = await keywordResponse.json();
            if (keywordData.success) {
                displayKeywordStats(keywordData.keyword_statistics);
            }
        }

        // 处理用户统计
        if (userResponse.ok) {
            const userData = await userResponse.json();
            if (userData.success) {
                displayUserStats(userData.user_statistics);
            }
        }

        // 处理文档使用统计
        if (documentUsageResponse.ok) {
            const docUsageData = await documentUsageResponse.json();
            if (docUsageData.success) {
                displayDocumentUsageStats(docUsageData.document_statistics);
            }
        }

        // 处理触发类型统计
        if (triggerResponse.ok) {
            const triggerData = await triggerResponse.json();
            if (triggerData.success) {
                displayTriggerStats(triggerData.trigger_statistics);
            }
        }

        // 处理详细对话记录
        if (conversationsResponse.ok) {
            const conversationsData = await conversationsResponse.json();
            if (conversationsData.success) {
                displayDetailedConversations(conversationsData.conversations);
            }
        }

    } catch (error) {
        console.error('加载详细统计失败:', error);
    }
}

// 显示关键词统计
function displayKeywordStats(keywordStats) {
    const container = document.getElementById('keyword-stats');
    const totalKeywords = document.getElementById('stats-total-keywords');
    
    if (!keywordStats.hot_keywords || keywordStats.hot_keywords.length === 0) {
        container.innerHTML = '<p class="text-gray-500 text-center py-4 col-span-full">暂无关键词数据</p>';
        totalKeywords.textContent = '0';
        return;
    }
    
    totalKeywords.textContent = keywordStats.hot_keywords.length;
    
    container.innerHTML = keywordStats.hot_keywords.slice(0, 12).map(item => `
        <div class="bg-gray-50 p-3 rounded-lg text-center">
            <div class="text-sm font-medium text-gray-900">${item.keyword}</div>
            <div class="text-xs text-gray-500">${item.frequency}次</div>
        </div>
    `).join('');
}

// 显示用户统计
function displayUserStats(userStats) {
    const container = document.getElementById('user-type-stats');
    const activeUsers = document.getElementById('stats-active-users');
    
    activeUsers.textContent = userStats.today_active_users || 0;
    
    if (!userStats.user_type_distribution || Object.keys(userStats.user_type_distribution).length === 0) {
        container.innerHTML = '<p class="text-gray-500 text-center py-4">暂无用户数据</p>';
        return;
    }
    
    const total = Object.values(userStats.user_type_distribution).reduce((sum, count) => sum + count, 0);
    
    container.innerHTML = Object.entries(userStats.user_type_distribution).map(([type, count]) => {
        const percentage = total > 0 ? Math.round((count / total) * 100) : 0;
        const typeName = type === 'guest' ? '游客' : '注册用户';
        return `
            <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">${typeName}</span>
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

// 显示文档使用统计
function displayDocumentUsageStats(docStats) {
    const container = document.getElementById('document-usage-stats');
    const docAssociation = document.getElementById('stats-doc-association');
    
    docAssociation.textContent = `${docStats.document_association_rate || 0}%`;
    
    if (!docStats.popular_documents || docStats.popular_documents.length === 0) {
        container.innerHTML = '<p class="text-gray-500 text-center py-4">暂无文档使用数据</p>';
        return;
    }
    
    container.innerHTML = docStats.popular_documents.slice(0, 10).map(doc => `
        <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div class="flex items-center space-x-3">
                <i class="fas fa-file-alt text-gray-400"></i>
                <span class="text-sm font-medium text-gray-900">${doc.document_name}</span>
            </div>
            <span class="text-sm text-gray-500">${doc.usage_count}次</span>
        </div>
    `).join('');
}

// 显示触发类型统计
function displayTriggerStats(triggerStats) {
    const container = document.getElementById('trigger-type-stats');
    
    if (!triggerStats.trigger_distribution || Object.keys(triggerStats.trigger_distribution).length === 0) {
        container.innerHTML = '<p class="text-gray-500 text-center py-4">暂无触发数据</p>';
        return;
    }
    
    const total = Object.values(triggerStats.trigger_distribution).reduce((sum, count) => sum + count, 0);
    
    container.innerHTML = Object.entries(triggerStats.trigger_distribution).map(([type, count]) => {
        const percentage = total > 0 ? Math.round((count / total) * 100) : 0;
        const typeName = type === 'question' ? '问答触发' : '模块触发';
        return `
            <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">${typeName}</span>
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

// 显示详细对话记录
function displayDetailedConversations(conversations) {
    const container = document.getElementById('detailed-conversations');
    
    if (!conversations || conversations.length === 0) {
        container.innerHTML = '<p class="text-gray-500 text-center py-4">暂无对话记录</p>';
        return;
    }
    
    container.innerHTML = conversations.map(conv => `
        <div class="border border-gray-200 rounded-lg p-4">
            <div class="flex justify-between items-start mb-2">
                <div class="flex items-center space-x-2">
                    <span class="px-2 py-1 text-xs rounded-full ${conv.user_type === 'guest' ? 'bg-gray-100 text-gray-800' : 'bg-blue-100 text-blue-800'}">
                        ${conv.user_type === 'guest' ? '游客' : '注册用户'}
                    </span>
                    <span class="px-2 py-1 text-xs rounded-full bg-purple-100 text-purple-800">
                        ${conv.ai_provider}
                    </span>
                    <span class="px-2 py-1 text-xs rounded-full bg-green-100 text-green-800">
                        ${conv.trigger_type === 'question' ? '问答' : '模块'}
                    </span>
                </div>
                <span class="text-xs text-gray-500">${formatDate(conv.created_at)}</span>
            </div>
            <div class="text-sm text-gray-900 mb-2">${conv.question}</div>
            <div class="flex justify-between items-center text-xs text-gray-500">
                <div class="flex items-center space-x-4">
                    <span>IP: ${conv.user_ip}</span>
                    ${conv.response_time ? `<span>响应: ${conv.response_time.toFixed(2)}s</span>` : ''}
                    ${conv.keywords && conv.keywords.length > 0 ? `<span>关键词: ${conv.keywords.length}个</span>` : ''}
                    ${conv.related_files && conv.related_files.length > 0 ? `<span>关联文档: ${conv.related_files.length}个</span>` : ''}
                </div>
                ${conv.rating ? `<span class="text-yellow-600">评分: ${conv.rating}/5</span>` : ''}
            </div>
            ${conv.keywords && conv.keywords.length > 0 ? `
                <div class="mt-2 flex flex-wrap gap-1">
                    ${conv.keywords.slice(0, 8).map(keyword => `
                        <span class="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded">${keyword}</span>
                    `).join('')}
                    ${conv.keywords.length > 8 ? `<span class="text-xs text-gray-500">+${conv.keywords.length - 8}个</span>` : ''}
                </div>
            ` : ''}
            ${conv.related_files && conv.related_files.length > 0 ? `
                <div class="mt-2">
                    <div class="text-xs text-gray-600 mb-1">关联文档:</div>
                    <div class="flex flex-wrap gap-1">
                        ${conv.related_files.slice(0, 5).map(filename => `
                            <span class="px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded flex items-center">
                                <i class="fas fa-file-alt mr-1"></i>${filename}
                            </span>
                        `).join('')}
                        ${conv.related_files.length > 5 ? `<span class="text-xs text-gray-500">+${conv.related_files.length - 5}个文档</span>` : ''}
                    </div>
                </div>
            ` : ''}
        </div>
    `).join('');
}

// 刷新关键词统计
async function refreshKeywordStats() {
    try {
        const response = await fetch('/admin/keyword-statistics');
        const data = await response.json();
        
        if (data.success) {
            displayKeywordStats(data.keyword_statistics);
            showNotification('关键词统计已刷新', 'success');
        }
    } catch (error) {
        console.error('刷新关键词统计失败:', error);
        showNotification('刷新失败', 'error');
    }
}

// 刷新对话记录
async function refreshConversations() {
    try {
        const userType = document.getElementById('filter-user-type').value;
        const aiProvider = document.getElementById('filter-ai-provider').value;
        
        const params = new URLSearchParams();
        if (userType) params.append('user_type', userType);
        if (aiProvider) params.append('ai_provider', aiProvider);
        params.append('per_page', '10');
        
        const response = await fetch(`/admin/detailed-conversations?${params}`);
        const data = await response.json();
        
        if (data.success) {
            displayDetailedConversations(data.conversations);
            showNotification('对话记录已刷新', 'success');
        }
    } catch (error) {
        console.error('刷新对话记录失败:', error);
        showNotification('刷新失败', 'error');
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

// ==================== 提示词管理功能 ====================

// 加载提示词管理
async function loadPromptManagement() {
    try {
        // 加载管理模式
        await loadPromptModes();
        
        // 设置学习阈值滑块事件
        const thresholdSlider = document.getElementById('learning-threshold');
        if (thresholdSlider) {
            thresholdSlider.addEventListener('input', function() {
                document.getElementById('threshold-value').textContent = this.value;
            });
        }
        
    } catch (error) {
        console.error('加载提示词管理失败:', error);
        showNotification('加载提示词管理失败', 'error');
    }
}

// 加载提示词模式
async function loadPromptModes() {
    try {
        // 管理员后台默认使用expert权限级别
        const response = await fetch('/api/prompt/modes?user_level=expert');
        const data = await response.json();
        
        if (data.success) {
            displayPromptModes(data.modes);
        } else {
            throw new Error(data.error || '加载模式失败');
        }
    } catch (error) {
        console.error('加载提示词模式失败:', error);
        const container = document.getElementById('prompt-modes');
        container.innerHTML = '<p class="text-red-500 text-center py-4">加载模式失败，请刷新重试</p>';
    }
}

// 显示提示词模式
function displayPromptModes(modes) {
    const container = document.getElementById('prompt-modes');
    
    container.innerHTML = modes.map(mode => `
        <div class="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow cursor-pointer" onclick="selectPromptMode('${mode.id}')">
            <div class="text-center mb-4">
                <div class="text-4xl mb-2">${mode.icon}</div>
                <h4 class="text-lg font-semibold text-gray-900">${mode.name}</h4>
                <p class="text-sm text-gray-600 mt-1">${mode.description}</p>
            </div>
            <div class="mb-4">
                <div class="flex items-center justify-between text-sm">
                    <span class="text-gray-600">难度</span>
                    <div class="flex">
                        ${Array.from({length: 5}, (_, i) => 
                            `<i class="fas fa-star ${i < mode.difficulty ? 'text-yellow-400' : 'text-gray-300'}"></i>`
                        ).join('')}
                    </div>
                </div>
            </div>
            <div class="space-y-2">
                ${mode.features.map(feature => `
                    <div class="flex items-center text-sm text-gray-600">
                        <i class="fas fa-check text-green-500 mr-2"></i>
                        <span>${feature}</span>
                    </div>
                `).join('')}
            </div>
        </div>
    `).join('');
}

// 选择提示词模式
function selectPromptMode(modeId) {
    // 隐藏所有配置区域
    document.querySelectorAll('[id$="-mode-config"]').forEach(el => {
        el.classList.add('hidden');
    });
    
    // 显示选中的配置区域
    const configElement = document.getElementById(`${modeId}-mode-config`);
    if (configElement) {
        configElement.classList.remove('hidden');
        
        // 滚动到配置区域
        configElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        // 加载对应模式的配置
        loadModeConfig(modeId);
    }
    
    showNotification(`已选择${getModeDisplayName(modeId)}`, 'info');
}

// 获取模式显示名称
function getModeDisplayName(modeId) {
    const names = {
        'simple': '简单模式',
        'template': '模板模式',
        'json': 'JSON模式',
        'intelligent': '智能模式',
        'expert': '专家模式'
    };
    return names[modeId] || modeId;
}

// 加载模式配置
async function loadModeConfig(modeId) {
    try {
        // 管理员后台使用expert权限级别
        const response = await fetch(`/api/prompt/${modeId}/config?user_level=expert`);
        if (response.ok) {
            const data = await response.json();
            if (data.success) {
                populateModeConfig(modeId, data.config);
            }
        }
    } catch (error) {
        console.log(`加载${modeId}模式配置失败:`, error);
        // 不显示错误，因为可能是新配置
    }
}

// 填充模式配置
function populateModeConfig(modeId, config) {
    switch (modeId) {
        case 'simple':
            if (config.company_name) document.getElementById('simple-company-name').value = config.company_name;
            if (config.main_product) document.getElementById('simple-main-product').value = config.main_product;
            if (config.tech_field) document.getElementById('simple-tech-field').value = config.tech_field;
            if (config.style) document.getElementById('simple-style').value = config.style;
            break;
        case 'template':
            if (config.template_type) document.getElementById('template-type').value = config.template_type;
            if (config.content) document.getElementById('template-content').value = config.content;
            break;
        case 'json':
            if (config.json_config) document.getElementById('json-config').value = JSON.stringify(config.json_config, null, 2);
            break;
        case 'expert':
            if (config.foundation_layer) document.getElementById('foundation-layer').value = config.foundation_layer;
            if (config.business_product) document.getElementById('business-product').value = config.business_product;
            if (config.business_technical) document.getElementById('business-technical').value = config.business_technical;
            if (config.business_training) document.getElementById('business-training').value = config.business_training;
            if (config.personal_preference) document.getElementById('personal-preference').value = config.personal_preference;
            if (config.personal_industry) document.getElementById('personal-industry').value = config.personal_industry;
            if (config.personal_custom) document.getElementById('personal-custom').value = config.personal_custom;
            if (config.priority_strategy) document.getElementById('priority-strategy').value = config.priority_strategy;
            if (config.conflict_resolution) document.getElementById('conflict-resolution').value = config.conflict_resolution;
            break;
    }
}

// 保存简单模式配置
async function saveSimpleConfig() {
    const config = {
        company_name: document.getElementById('simple-company-name').value,
        main_product: document.getElementById('simple-main-product').value,
        tech_field: document.getElementById('simple-tech-field').value,
        style: document.getElementById('simple-style').value
    };
    
    await savePromptConfig('simple', config);
}

// 保存模板模式配置
async function saveTemplateConfig() {
    const config = {
        template_type: document.getElementById('template-type').value,
        content: document.getElementById('template-content').value
    };
    
    await savePromptConfig('template', config);
}

// 验证JSON配置
function validateJsonConfig() {
    const jsonText = document.getElementById('json-config').value;
    
    try {
        JSON.parse(jsonText);
        showNotification('JSON格式验证通过', 'success');
        return true;
    } catch (error) {
        showNotification(`JSON格式错误: ${error.message}`, 'error');
        return false;
    }
}

// 保存JSON模式配置
async function saveJsonConfig() {
    if (!validateJsonConfig()) {
        return;
    }
    
    const jsonText = document.getElementById('json-config').value;
    const config = {
        json_config: JSON.parse(jsonText)
    };
    
    await savePromptConfig('json', config);
}

// 保存智能模式配置
async function saveIntelligentConfig() {
    const config = {
        intent_product: document.getElementById('intent-product').checked,
        intent_technical: document.getElementById('intent-technical').checked,
        intent_sales: document.getElementById('intent-sales').checked,
        intent_general: document.getElementById('intent-general').checked,
        optimization_frequency: document.getElementById('optimization-frequency').value,
        learning_threshold: parseFloat(document.getElementById('learning-threshold').value)
    };
    
    await savePromptConfig('intelligent', config);
}

// 保存专家模式配置
async function saveExpertConfig() {
    const config = {
        foundation_layer: document.getElementById('foundation-layer').value,
        business_product: document.getElementById('business-product').value,
        business_technical: document.getElementById('business-technical').value,
        business_training: document.getElementById('business-training').value,
        personal_preference: document.getElementById('personal-preference').value,
        personal_industry: document.getElementById('personal-industry').value,
        personal_custom: document.getElementById('personal-custom').value,
        priority_strategy: document.getElementById('priority-strategy').value,
        conflict_resolution: document.getElementById('conflict-resolution').value
    };
    
    await savePromptConfig('expert', config);
}

// 通用保存配置函数
async function savePromptConfig(mode, config) {
    try {
        // 管理员后台使用expert权限级别
        const response = await fetch(`/api/prompt/${mode}/config?user_level=expert`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(config)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(`${getModeDisplayName(mode)}配置保存成功`, 'success');
        } else {
            throw new Error(data.error || '保存失败');
        }
    } catch (error) {
        console.error(`保存${mode}配置失败:`, error);
        showNotification(`保存配置失败: ${error.message}`, 'error');
    }
}

// 预览模板效果
async function previewTemplate() {
    const templateType = document.getElementById('template-type').value;
    const content = document.getElementById('template-content').value;
    
    if (!content.trim()) {
        showNotification('请先输入模板内容', 'warning');
        return;
    }
    
    try {
        const response = await fetch('/api/prompt/template/preview', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                template_type: templateType,
                content: content,
                variables: {
                    company_name: '简仪科技',
                    product_name: '锐视测控平台',
                    question: '示例问题',
                    knowledge_content: '示例知识库内容'
                }
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // 显示预览模态框
            showPreviewModal('模板预览', data.preview);
        } else {
            throw new Error(data.error || '预览失败');
        }
    } catch (error) {
        console.error('预览模板失败:', error);
        showNotification('预览失败', 'error');
    }
}

// 预览专家模式提示词
async function previewExpertPrompt() {
    const config = {
        foundation_layer: document.getElementById('foundation-layer').value,
        business_product: document.getElementById('business-product').value,
        business_technical: document.getElementById('business-technical').value,
        business_training: document.getElementById('business-training').value,
        personal_preference: document.getElementById('personal-preference').value,
        personal_industry: document.getElementById('personal-industry').value,
        personal_custom: document.getElementById('personal-custom').value,
        priority_strategy: document.getElementById('priority-strategy').value,
        conflict_resolution: document.getElementById('conflict-resolution').value
    };
    
    try {
        const response = await fetch('/api/prompt/expert/preview', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(config)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showPreviewModal('专家模式合成预览', data.preview);
        } else {
            throw new Error(data.error || '预览失败');
        }
    } catch (error) {
        console.error('预览专家模式失败:', error);
        showNotification('预览失败', 'error');
    }
}

// 运行智能分析
async function runIntelligentAnalysis() {
    try {
        showNotification('正在运行智能分析...', 'info');
        
        const response = await fetch('/api/prompt/intelligent/analysis', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                analyze_conversations: true,
                optimize_prompts: true
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('智能分析完成', 'success');
            
            // 显示分析结果
            if (data.analysis) {
                showPreviewModal('智能分析结果', JSON.stringify(data.analysis, null, 2));
            }
        } else {
            throw new Error(data.error || '分析失败');
        }
    } catch (error) {
        console.error('智能分析失败:', error);
        showNotification('智能分析失败', 'error');
    }
}

// 测试提示词
async function testPrompt() {
    const question = document.getElementById('test-question').value.trim();
    const modeElement = document.getElementById('test-mode');
    const mode = modeElement ? modeElement.value : 'simple';
    
    if (!question) {
        showNotification('请输入测试问题', 'warning');
        return;
    }
    
    try {
        const response = await fetch('/api/prompt/test', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: question,
                mode: mode,
                user_level: 'expert'  // 管理后台使用expert权限
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayTestResults(data);
        } else {
            throw new Error(data.error || '测试失败');
        }
    } catch (error) {
        console.error('测试提示词失败:', error);
        showNotification(`测试失败: ${error.message}`, 'error');
    }
}

// 显示测试结果
function displayTestResults(data) {
    const resultsContainer = document.getElementById('test-results');
    const analysisContainer = document.getElementById('test-analysis');
    
    // 显示生成的提示词
    resultsContainer.innerHTML = `
        <div class="space-y-2">
            <div class="text-sm font-medium text-gray-700">生成的提示词:</div>
            <div class="text-sm text-gray-900 whitespace-pre-wrap">${data.generated_prompt || '未生成提示词'}</div>
        </div>
    `;
    
    // 显示分析结果
    analysisContainer.innerHTML = `
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div>
                <div class="text-lg font-semibold text-blue-600">${data.mode || '未知'}</div>
                <div class="text-xs text-gray-500">模式</div>
            </div>
            <div>
                <div class="text-lg font-semibold text-green-600">${data.prompt_length || 0}</div>
                <div class="text-xs text-gray-500">字符数</div>
            </div>
            <div>
                <div class="text-lg font-semibold text-purple-600">${data.estimated_tokens || 0}</div>
                <div class="text-xs text-gray-500">预估Token</div>
            </div>
            <div>
                <div class="text-lg font-semibold text-orange-600">${(data.complexity_score || 0).toFixed(1)}/5.0</div>
                <div class="text-xs text-gray-500">复杂度</div>
            </div>
        </div>
        ${data.has_knowledge ? '<div class="mt-2 text-sm text-green-600"><i class="fas fa-check mr-1"></i>包含知识库内容</div>' : '<div class="mt-2 text-sm text-gray-500"><i class="fas fa-times mr-1"></i>未包含知识库内容</div>'}
    `;
}

// 显示预览模态框
function showPreviewModal(title, content) {
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4';
    modal.innerHTML = `
        <div class="bg-white rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] overflow-hidden">
            <div class="flex justify-between items-center p-6 border-b">
                <h3 class="text-lg font-semibold text-gray-900">${title}</h3>
                <button onclick="this.closest('.fixed').remove()" class="text-gray-400 hover:text-gray-600">
                    <i class="fas fa-times text-xl"></i>
                </button>
            </div>
            <div class="p-6 overflow-y-auto max-h-[70vh]">
                <pre class="whitespace-pre-wrap text-sm text-gray-700 bg-gray-50 p-4 rounded-lg">${content}</pre>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
}
