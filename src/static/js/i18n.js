/**
 * 国际化配置文件
 * 简仪科技锐视测控平台多语言支持
 */

// 语言配置
const i18nConfig = {
    // 中文配置
    zh: {
        // 通用
        common: {
            company: "简仪科技",
            platform: "锐视测控平台",
            loading: "加载中...",
            error: "错误",
            success: "成功",
            warning: "警告",
            info: "信息",
            confirm: "确认",
            cancel: "取消",
            close: "关闭",
            save: "保存",
            delete: "删除",
            edit: "编辑",
            view: "查看",
            search: "搜索",
            reset: "重置",
            submit: "提交",
            back: "返回",
            next: "下一步",
            previous: "上一步",
            home: "首页",
            about: "关于我们",
            contact: "联系我们",
            more: "更多"
        },
        
        // 导航栏
        nav: {
            home: "首页",
            platform: "锐视测控平台",
            products: "产品中心",
            solutions: "方案配置",
            support: "知识库",
            about: "关于我们",
            contact: "官网",
            language: "语言",
            chinese: "中文",
            english: "English",
            brand: "锐视测控平台",
            tagline: "简仪科技专业测控解决方案"
        },
        
        // 首页
        home: {
            title: "锐视测控平台 - 简仪科技JYTEK专业PXI测控解决方案",
            subtitle: "AI增强的开源PXI测控解决方案",
            description: "基于C#/.NET的专业测控平台，集成AI技术，提供完整的硬件驱动、信号处理和数据分析解决方案",
            hero: {
                title: "锐视测控平台",
                subtitle: "开源测控生态圈",
                description: "集成先进AI技术，提供智能问答、产品推荐、方案配置等专业服务<br>让PXI测控技术咨询变得更加高效和便捷"
            },
            aiSearch: {
                title: "AI智能问答助手",
                placeholder: "请输入您的PXI技术问题，例如：如何选择合适的数据采集模块？",
                button: "提问",
                thinking: "AI思考中...",
                waiting: "AI正在等待您的问题...",
                analyzing: "正在分析您的问题："
            },
            features: {
                title: "平台特色",
                subtitle: "基于AI技术的智能化PXI测控解决方案平台",
                ai: {
                    title: "AI智能问答",
                    desc: "专业的PXI技术AI助手，提供24/7智能技术咨询和解决方案推荐"
                },
                recommendation: {
                    title: "产品智能推荐",
                    desc: "基于需求分析的智能产品推荐，快速找到最适合的PXI模块和解决方案"
                },
                solution: {
                    title: "方案自动配置",
                    desc: "智能的系统配置工具，根据应用需求自动生成最优的PXI系统方案"
                },
                knowledge: {
                    title: "知识库检索",
                    desc: "海量技术文档智能检索，快速获取产品手册、应用笔记和技术规格"
                }
            },
            quickActions: {
                title: "快速操作",
                productCenter: "产品中心",
                solutionBuilder: "方案配置",
                knowledgeBase: "知识库",
                aiConsult: "AI咨询"
            },
            products: {
                title: "产品分类",
                subtitle: "专业的PXI模块化仪器产品线，满足各种测控应用需求",
                loading: "加载产品分类...",
                error: "加载产品分类失败",
                retry: "请稍后重试或访问简仪科技官网获取产品信息",
                visitWebsite: "访问官网",
                count: "个产品"
            },
            hotQuestions: {
                title: "热门问题",
                subtitle: "用户最关心的PXI技术问题和解答",
                q1: {
                    title: "如何选择合适的PXI数据采集模块？",
                    desc: "了解数据采集模块的关键参数和选型要点"
                },
                q2: {
                    title: "PXI系统的同步和触发机制是什么？",
                    desc: "深入了解PXI系统的时钟同步和触发原理"
                },
                q3: {
                    title: "锐视测控平台如何与PXI模块通信？",
                    desc: "学习简仪科技自主软件平台的驱动程序开发和API使用"
                },
                q4: {
                    title: "PXI机箱如何选型和配置？",
                    desc: "了解PXI机箱的规格、插槽和扩展能力"
                },
                q5: {
                    title: "自动化测试系统如何设计？",
                    desc: "学习自动化测试系统的架构设计和实现"
                },
                q6: {
                    title: "PXI系统的成本如何估算？",
                    desc: "了解PXI系统的成本构成和预算规划"
                }
            }
        },
        
        // 锐视测控平台页面
        platform: {
            title: "锐视测控平台 - 简仪科技AI增强的开源测控解决方案",
            subtitle: "AI增强的开源PXI测控解决方案",
            nav: {
                backHome: "返回首页",
                features: "核心特性",
                misd: "MISD方法",
                aiAgent: "AI Agent",
                tryNow: "立即体验"
            },
            hero: {
                title: "锐视测控平台",
                subtitle: "基于C#/.NET的AI增强开源测控解决方案",
                description: "集成先进AI技术、MISD方法和开源生态，为PXI模块化仪器提供完整的软件开发环境。减少70%编程量，调试时间从30分钟缩短至2分钟，让测控开发变得更加高效和智能。",
                cta1: "核心特性",
                cta2: "MISD演示",
                cta3: "AI演示"
            },
            features: {
                ai: {
                    badge: "AI增强"
                },
                opensource: {
                    badge: "开源生态"
                },
                misd: {
                    badge: "MISD方法"
                },
                autonomous: {
                    badge: "自主可控"
                }
            },
            coreFeatures: {
                title: "核心技术特性",
                subtitle: "锐视测控平台融合了最新的AI技术、开源理念和工程实践，为测控开发提供革命性的解决方案",
                ai: {
                    title: "AI技术集成",
                    feature1: "内置AI Agent智能助手",
                    feature2: "自动代码生成和优化",
                    feature3: "智能参数调优",
                    feature4: "实时错误检测和修复",
                    effect: "效果：减少70%编程量"
                }
            },
            stats: {
                programming: "减少编程量",
                debugging: "调试时间",
                accuracy: "测量精度",
                compatibility: "硬件兼容性"
            },
            features: {
                title: "核心技术特性",
                ai: {
                    title: "AI技术集成",
                    desc: "内置AI Agent智能助手，支持自然语言交互，自动生成测控代码，智能参数优化和故障诊断"
                },
                misd: {
                    title: "MISD方法",
                    desc: "模块仪器软件词典方法，通过统一的硬件API语法树，让AI理解底层硬件，实现智能代码生成"
                },
                opensource: {
                    title: "开源生态",
                    desc: "完全开源的C#/.NET解决方案，提供透明的源代码和丰富的开发工具包，支持深度定制"
                },
                dotnet: {
                    title: ".NET框架",
                    desc: "基于Microsoft .NET框架构建，提供强大的类库支持，确保高性能和跨平台兼容性"
                },
                signal: {
                    title: "信号处理",
                    desc: "SeeSharpTools SDK提供先进的数字信号处理功能，支持FFT、滤波器设计和ScottPlot可视化"
                },
                autonomous: {
                    title: "自主可控",
                    desc: "国产自主研发，完全掌握核心技术，确保技术安全和持续发展能力"
                }
            },
            workflow: {
                title: "MISD方法工作流程",
                step1: {
                    title: "硬件识别",
                    desc: "自动识别连接的PXI模块和设备"
                },
                step2: {
                    title: "语法树构建",
                    desc: "构建统一的硬件API语法树"
                },
                step3: {
                    title: "AI分析",
                    desc: "AI理解硬件特性和用户需求"
                },
                step4: {
                    title: "代码生成",
                    desc: "自动生成优化的测控代码"
                }
            },
            comparison: {
                title: "开发方式对比",
                traditional: {
                    title: "传统开发方式",
                    manual: "手动编写驱动代码",
                    complex: "复杂的硬件配置",
                    time: "耗时的调试过程",
                    error: "容易出现参数错误"
                },
                ai: {
                    title: "AI + MISD开发方式",
                    auto: "AI自动生成代码",
                    simple: "智能硬件配置",
                    fast: "快速调试验证",
                    optimize: "智能参数优化"
                }
            },
            demo: {
                title: "AI Agent演示",
                subtitle: "体验AI增强的测控开发",
                placeholder: "请描述您的测控需求，例如：我需要采集8通道模拟信号...",
                send: "发送",
                clear: "清空",
                examples: {
                    title: "示例问题",
                    example1: "如何配置16通道数据采集？",
                    example2: "生成信号发生器控制代码",
                    example3: "PXI系统故障诊断方法"
                }
            }
        },
        
        // AI问答模态框
        aiModal: {
            title: "AI智能问答",
            subtitle: "简仪科技锐视测控平台专业技术咨询",
            question: "您的问题",
            answer: "AI专业回答",
            recommendations: "相关简仪科技产品推荐",
            analyzing: "AI正在分析并推荐相关产品...",
            reason: "推荐理由：",
            learnMore: "了解详情",
            getQuote: "获取报价",
            copy: "复制回答",
            followUp: "追问",
            visitWebsite: "访问官网",
            copied: "回答已复制到剪贴板",
            copyFailed: "复制失败，请手动复制",
            followUpPrompt: "请输入您的追问："
        },
        
        // 产品相关
        products: {
            categories: {
                dataAcquisition: "数据采集",
                signalGeneration: "信号发生",
                digitalIO: "数字I/O",
                rfMicrowave: "射频微波"
            },
            actions: {
                consult: "咨询",
                compare: "对比",
                quote: "报价"
            },
            noProducts: "该分类暂无产品信息",
            moreInfo: "需要更多产品信息或技术支持？",
            compareInDev: "产品对比功能开发中，请访问官网获取详细对比信息"
        },
        
        // 解决方案构建器
        solutionBuilder: {
            title: "智能方案配置器",
            subtitle: "根据您的需求自动生成PXI系统方案",
            measurementType: "测量类型",
            channelCount: "通道数量",
            frequencyRange: "频率范围",
            accuracy: "精度要求",
            budget: "预算范围",
            generate: "生成方案",
            cancel: "取消",
            result: {
                title: "推荐方案",
                subtitle: "基于您的需求生成的PXI系统配置",
                chassis: "机箱配置",
                controller: "控制器配置",
                modules: "功能模块",
                cost: "成本估算",
                reason: "推荐理由",
                getDetailedQuote: "获取详细报价",
                consultSolution: "咨询方案"
            },
            options: {
                measurementTypes: {
                    placeholder: "请选择测量类型",
                    dataAcquisition: "数据采集",
                    signalGeneration: "信号发生",
                    rfTest: "射频测试",
                    digitalIO: "数字I/O",
                    mixedSignal: "混合信号测试"
                },
                channels: {
                    placeholder: "请选择通道数量",
                    "1-8": "1-8通道",
                    "9-16": "9-16通道",
                    "17-32": "17-32通道",
                    "32+": "32通道以上"
                },
                frequency: {
                    placeholder: "请选择频率范围",
                    "DC-1MHz": "DC - 1MHz",
                    "1MHz-100MHz": "1MHz - 100MHz",
                    "100MHz-1GHz": "100MHz - 1GHz",
                    "1GHz+": "1GHz以上"
                },
                accuracyLevels: {
                    placeholder: "请选择精度要求",
                    standard: "标准精度",
                    high: "高精度",
                    ultraHigh: "超高精度"
                },
                budgetRanges: {
                    placeholder: "请选择预算范围",
                    "under100k": "10万以下",
                    "100k-500k": "10-50万",
                    "500k-1m": "50-100万",
                    "over1m": "100万以上"
                }
            }
        },
        
        // 知识库
        knowledgeBase: {
            title: "技术知识库",
            subtitle: "PXI技术文档管理和AI智能检索",
            heroTitle: "知识库",
            heroSubtitle: "技术文档搜索、上传与管理中心",
            backHome: "返回首页",
            tabs: {
                search: "搜索文档",
                upload: "上传文档",
                manage: "文档管理"
            },
            search: {
                placeholder: "搜索技术文档、产品手册、应用笔记...",
                button: "搜索",
                categories: {
                    systemArchitecture: "系统架构",
                    productSpecs: "产品规格",
                    softwareDevelopment: "软件开发",
                    applicationNotes: "应用笔记"
                },
                categoryDescs: {
                    systemArchitecture: "PXI系统架构文档",
                    productSpecs: "产品技术规格书",
                    softwareDevelopment: "开发指南和API文档",
                    applicationNotes: "应用案例和解决方案"
                },
                results: "搜索结果",
                popular: "热门文档",
                noDocuments: "暂无文档，请先上传一些技术资料",
                loadFailed: "加载失败，请稍后重试",
                loading: "加载文档列表..."
            },
            upload: {
                title: "上传技术文档",
                selectFile: "选择文件",
                dragDrop: "点击选择文件或拖拽文件到此处",
                supportedFormats: "支持 PDF, Word, TXT, Markdown 格式，最大 50MB",
                category: "文档分类",
                categories: {
                    general: "通用文档",
                    systemArchitecture: "系统架构",
                    productSpecs: "产品规格",
                    softwareDevelopment: "软件开发",
                    applicationNotes: "应用笔记",
                    troubleshooting: "故障排除"
                },
                upload: "上传文档",
                uploading: "上传中...",
                processing: "处理中...",
                reset: "重置",
                success: "上传成功！",
                failed: "上传失败",
                selectFileFirst: "请选择要上传的文件"
            },
            manage: {
                title: "文档管理",
                refresh: "刷新",
                ask: "问答",
                delete: "删除",
                confirmDelete: "确定要删除这个文档吗？此操作不可撤销。",
                deleteSuccess: "文档删除成功",
                deleteFailed: "删除文档失败，请稍后重试",
                refreshed: "文档列表已刷新",
                loading: "加载文档列表...",
                empty: "暂无文档",
                emptyDesc: "请先上传一些技术资料",
                loadFailed: "加载失败",
                loadFailedDesc: "请稍后重试"
            },
            support: {
                needHelp: "需要技术支持或更多资料？",
                visitWebsite: "访问简仪科技官网",
                aiConsult: "AI技术咨询"
            }
        },
        
        // 通知消息
        notifications: {
            systemError: "系统连接异常，部分功能可能不可用",
            pleaseEnterQuestion: "请输入您的问题",
            aiSearchFailed: "AI搜索失败，请稍后重试",
            generateSolutionFailed: "生成方案失败，请稍后重试",
            pleaseEnterKeyword: "请输入搜索关键词",
            documentQAFailed: "文档问答失败，请稍后重试"
        }
    },
    
    // 英文配置
    en: {
        // 通用
        common: {
            company: "JYTEK",
            platform: "SeeSharp Platform",
            loading: "Loading...",
            error: "Error",
            success: "Success",
            warning: "Warning",
            info: "Info",
            confirm: "Confirm",
            cancel: "Cancel",
            close: "Close",
            save: "Save",
            delete: "Delete",
            edit: "Edit",
            view: "View",
            search: "Search",
            reset: "Reset",
            submit: "Submit",
            back: "Back",
            next: "Next",
            previous: "Previous",
            home: "Home",
            about: "About",
            contact: "Contact",
            more: "More"
        },
        
        // 导航栏
        nav: {
            home: "Home",
            platform: "SeeSharp Platform",
            products: "Products",
            solutions: "Solution Builder",
            support: "Knowledge Base",
            about: "About",
            contact: "Contact",
            language: "Language",
            chinese: "中文",
            english: "English",
            brand: "SeeSharp Platform",
            tagline: "JYTEK Professional Test & Measurement Solutions"
        },
        
        // 首页
        home: {
            title: "SeeSharp Platform - JYTEK Professional PXI Test & Measurement Solutions",
            subtitle: "AI-Enhanced Open Source PXI Test & Measurement Solution",
            description: "Professional test & measurement platform based on C#/.NET, integrated with AI technology, providing complete hardware drivers, signal processing and data analysis solutions",
            hero: {
                title: "SeeSharp Platform",
                subtitle: "Open Source Test & Measurement Ecosystem",
                description: "Integrated with advanced AI technology, providing intelligent Q&A, product recommendations, solution configuration and other professional services<br>Making PXI test & measurement technical consultation more efficient and convenient"
            },
            aiSearch: {
                title: "AI Smart Q&A Assistant",
                placeholder: "Enter your PXI technical questions, e.g.: How to choose the right data acquisition module?",
                button: "Ask",
                thinking: "AI thinking...",
                waiting: "AI is waiting for your question...",
                analyzing: "Analyzing your question: "
            },
            features: {
                title: "Platform Features",
                subtitle: "AI-powered intelligent PXI test & measurement solution platform",
                ai: {
                    title: "AI Smart Q&A",
                    desc: "Professional PXI technical AI assistant providing 24/7 intelligent technical consultation and solution recommendations"
                },
                recommendation: {
                    title: "Intelligent Product Recommendation",
                    desc: "Smart product recommendations based on requirement analysis, quickly find the most suitable PXI modules and solutions"
                },
                solution: {
                    title: "Automated Solution Configuration",
                    desc: "Intelligent system configuration tool that automatically generates optimal PXI system solutions based on application requirements"
                },
                knowledge: {
                    title: "Knowledge Base Search",
                    desc: "Massive technical document intelligent search, quickly access product manuals, application notes and technical specifications"
                }
            },
            quickActions: {
                title: "Quick Actions",
                productCenter: "Product Center",
                solutionBuilder: "Solution Builder",
                knowledgeBase: "Knowledge Base",
                aiConsult: "AI Consultation"
            },
            products: {
                title: "Product Categories",
                subtitle: "Professional PXI modular instrument product lines to meet various test & measurement application requirements",
                loading: "Loading product categories...",
                error: "Failed to load product categories",
                retry: "Please try again later or visit JYTEK official website for product information",
                visitWebsite: "Visit Website",
                count: "products"
            },
            hotQuestions: {
                title: "Popular Questions",
                subtitle: "Most concerned PXI technical questions and answers from users",
                q1: {
                    title: "How to choose the right PXI data acquisition module?",
                    desc: "Understand key parameters and selection criteria for data acquisition modules"
                },
                q2: {
                    title: "What are the synchronization and triggering mechanisms of PXI systems?",
                    desc: "Deep understanding of PXI system clock synchronization and triggering principles"
                },
                q3: {
                    title: "How does SeeSharp Platform communicate with PXI modules?",
                    desc: "Learn JYTEK's proprietary software platform driver development and API usage"
                },
                q4: {
                    title: "How to select and configure PXI chassis?",
                    desc: "Understand PXI chassis specifications, slots and expansion capabilities"
                },
                q5: {
                    title: "How to design automated test systems?",
                    desc: "Learn automated test system architecture design and implementation"
                },
                q6: {
                    title: "How to estimate the cost of PXI systems?",
                    desc: "Understand PXI system cost structure and budget planning"
                }
            }
        },
        
        // 锐视测控平台页面
        platform: {
            title: "SeeSharp Platform - JYTEK AI-Enhanced Open Source Test & Measurement Solution",
            subtitle: "AI-Enhanced Open Source PXI Test & Measurement Solution",
            nav: {
                backHome: "Back to Home",
                features: "Core Features",
                misd: "MISD Method",
                aiAgent: "AI Agent",
                tryNow: "Try Now"
            },
            hero: {
                title: "SeeSharp Platform",
                subtitle: "AI-Enhanced Open Source Test & Measurement Solution Based on C#/.NET",
                description: "Integrated with advanced AI technology, MISD method and open source ecosystem, providing complete software development environment for PXI modular instruments. Reducing 70% programming effort and debugging time from 30 minutes to 2 minutes, making test & measurement development more efficient and intelligent.",
                cta1: "Core Features",
                cta2: "MISD Demo",
                cta3: "AI Demo"
            },
            features: {
                ai: {
                    badge: "AI Enhanced"
                },
                opensource: {
                    badge: "Open Source"
                },
                misd: {
                    badge: "MISD Method"
                },
                autonomous: {
                    badge: "Autonomous"
                }
            },
            coreFeatures: {
                title: "Core Technical Features",
                subtitle: "SeeSharp Platform integrates the latest AI technology, open source concepts and engineering practices to provide revolutionary solutions for test & measurement development",
                ai: {
                    title: "AI Technology Integration",
                    feature1: "Built-in AI Agent Assistant",
                    feature2: "Automatic Code Generation and Optimization",
                    feature3: "Intelligent Parameter Tuning",
                    feature4: "Real-time Error Detection and Repair",
                    effect: "Effect: 70% Programming Reduction"
                }
            },
            stats: {
                programming: "Programming Reduction",
                debugging: "Debugging Time",
                accuracy: "Measurement Accuracy",
                compatibility: "Hardware Compatibility"
            },
            features: {
                title: "Core Technical Features",
                ai: {
                    title: "AI Technology Integration",
                    desc: "Built-in AI Agent assistant supporting natural language interaction, automatic test code generation, intelligent parameter optimization and fault diagnosis"
                },
                misd: {
                    title: "MISD Method",
                    desc: "Modular Instrument Software Dictionary method with unified hardware API syntax tree, enabling AI to understand underlying hardware for intelligent code generation"
                },
                opensource: {
                    title: "Open Source Ecosystem",
                    desc: "Fully open source C#/.NET solution providing transparent source code and rich development toolkits with deep customization support"
                },
                dotnet: {
                    title: ".NET Framework",
                    desc: "Built on Microsoft .NET framework providing powerful library support, ensuring high performance and cross-platform compatibility"
                },
                signal: {
                    title: "Signal Processing",
                    desc: "SeeSharpTools SDK provides advanced digital signal processing capabilities supporting FFT, filter design and ScottPlot visualization"
                },
                autonomous: {
                    title: "Autonomous & Controllable",
                    desc: "Independently developed in China with complete mastery of core technologies, ensuring technical security and sustainable development"
                }
            },
            workflow: {
                title: "MISD Method Workflow",
                step1: {
                    title: "Hardware Recognition",
                    desc: "Automatically identify connected PXI modules and devices"
                },
                step2: {
                    title: "Syntax Tree Construction",
                    desc: "Build unified hardware API syntax tree"
                },
                step3: {
                    title: "AI Analysis",
                    desc: "AI understands hardware characteristics and user requirements"
                },
                step4: {
                    title: "Code Generation",
                    desc: "Automatically generate optimized test & measurement code"
                }
            },
            comparison: {
                title: "Development Method Comparison",
                traditional: {
                    title: "Traditional Development",
                    manual: "Manual driver code writing",
                    complex: "Complex hardware configuration",
                    time: "Time-consuming debugging process",
                    error: "Prone to parameter errors"
                },
                ai: {
                    title: "AI + MISD Development",
                    auto: "AI automatic code generation",
                    simple: "Intelligent hardware configuration",
                    fast: "Fast debugging verification",
                    optimize: "Intelligent parameter optimization"
                }
            },
            demo: {
                title: "AI Agent Demo",
                subtitle: "Experience AI-Enhanced Test & Measurement Development",
                placeholder: "Please describe your test & measurement requirements, e.g.: I need to acquire 8-channel analog signals...",
                send: "Send",
                clear: "Clear",
                examples: {
                    title: "Example Questions",
                    example1: "How to configure 16-channel data acquisition?",
                    example2: "Generate signal generator control code",
                    example3: "PXI system fault diagnosis methods"
                }
            }
        },
        
        // AI问答模态框
        aiModal: {
            title: "AI Smart Q&A",
            subtitle: "JYTEK SeeSharp Platform Professional Technical Consultation",
            question: "Your Question",
            answer: "AI Professional Answer",
            recommendations: "Related JYTEK Product Recommendations",
            analyzing: "AI is analyzing and recommending related products...",
            reason: "Recommendation Reason: ",
            learnMore: "Learn More",
            getQuote: "Get Quote",
            copy: "Copy Answer",
            followUp: "Follow Up",
            visitWebsite: "Visit Website",
            copied: "Answer copied to clipboard",
            copyFailed: "Copy failed, please copy manually",
            followUpPrompt: "Please enter your follow-up question: "
        },
        
        // 产品相关
        products: {
            categories: {
                dataAcquisition: "Data Acquisition",
                signalGeneration: "Signal Generation",
                digitalIO: "Digital I/O",
                rfMicrowave: "RF & Microwave"
            },
            actions: {
                consult: "Consult",
                compare: "Compare",
                quote: "Quote"
            },
            noProducts: "No products available in this category",
            moreInfo: "Need more product information or technical support?",
            compareInDev: "Product comparison feature is under development, please visit our website for detailed comparison information"
        },
        
        // 解决方案构建器
        solutionBuilder: {
            title: "Intelligent Solution Builder",
            subtitle: "Automatically generate PXI system solutions based on your requirements",
            measurementType: "Measurement Type",
            channelCount: "Channel Count",
            frequencyRange: "Frequency Range",
            accuracy: "Accuracy Requirement",
            budget: "Budget Range",
            generate: "Generate Solution",
            cancel: "Cancel",
            result: {
                title: "Recommended Solution",
                subtitle: "PXI system configuration generated based on your requirements",
                chassis: "Chassis Configuration",
                controller: "Controller Configuration",
                modules: "Function Modules",
                cost: "Cost Estimation",
                reason: "Recommendation Reason",
                getDetailedQuote: "Get Detailed Quote",
                consultSolution: "Consult Solution"
            },
            options: {
                measurementTypes: {
                    placeholder: "Please select measurement type",
                    dataAcquisition: "Data Acquisition",
                    signalGeneration: "Signal Generation",
                    rfTest: "RF Testing",
                    digitalIO: "Digital I/O",
                    mixedSignal: "Mixed Signal Testing"
                },
                channels: {
                    placeholder: "Please select channel count",
                    "1-8": "1-8 Channels",
                    "9-16": "9-16 Channels",
                    "17-32": "17-32 Channels",
                    "32+": "32+ Channels"
                },
                frequency: {
                    placeholder: "Please select frequency range",
                    "DC-1MHz": "DC - 1MHz",
                    "1MHz-100MHz": "1MHz - 100MHz",
                    "100MHz-1GHz": "100MHz - 1GHz",
                    "1GHz+": "1GHz+"
                },
                accuracyLevels: {
                    placeholder: "Please select accuracy requirement",
                    standard: "Standard Accuracy",
                    high: "High Accuracy",
                    ultraHigh: "Ultra High Accuracy"
                },
                budgetRanges: {
                    placeholder: "Please select budget range",
                    "under100k": "Under $15K",
                    "100k-500k": "$15K - $75K",
                    "500k-1m": "$75K - $150K",
                    "over1m": "Over $150K"
                }
            }
        },
        
        // 知识库
        knowledgeBase: {
            title: "Technical Knowledge Base",
            subtitle: "PXI Technical Documentation Management and AI Intelligent Search",
            tabs: {
                search: "Search Documents",
                upload: "Upload Documents",
                manage: "Document Management"
            },
            search: {
                placeholder: "Search technical documents, product manuals, application notes...",
                categories: {
                    systemArchitecture: "System Architecture",
                    productSpecs: "Product Specifications",
                    softwareDevelopment: "Software Development",
                    applicationNotes: "Application Notes"
                },
                results: "Search Results",
                popular: "Popular Documents",
                noDocuments: "No documents available, please upload some technical materials first",
                loadFailed: "Loading failed, please try again later"
            },
            upload: {
                title: "Upload Technical Documents",
                selectFile: "Select File",
                dragDrop: "Click to select file or drag file here",
                supportedFormats: "Supports PDF, Word, TXT, Markdown formats",
                category: "Document Category",
                categories: {
                    general: "General Documents",
                    systemArchitecture: "System Architecture",
                    productSpecs: "Product Specifications",
                    softwareDevelopment: "Software Development",
                    applicationNotes: "Application Notes",
                    troubleshooting: "Troubleshooting"
                },
                upload: "Upload Document",
                reset: "Reset",
                uploading: "Uploading...",
                success: "Upload successful!",
                failed: "Upload failed",
                selectFileFirst: "Please select a file to upload"
            },
            manage: {
                title: "Document Management",
                refresh: "Refresh",
                ask: "Q&A",
                delete: "Delete",
                confirmDelete: "Are you sure you want to delete this document? This action cannot be undone.",
                deleteSuccess: "Document deleted successfully",
                deleteFailed: "Failed to delete document, please try again later",
                refreshed: "Document list refreshed"
            },
            support: {
                needHelp: "Need technical support or more materials?",
                visitWebsite: "Visit JYTEK Official Website",
                aiConsult: "AI Technical Consultation"
            }
        },
        
        // 通知消息
        notifications: {
            systemError: "System connection error, some features may be unavailable",
            pleaseEnterQuestion: "Please enter your question",
            aiSearchFailed: "AI search failed, please try again later",
            generateSolutionFailed: "Failed to generate solution, please try again later",
            pleaseEnterKeyword: "Please enter search keyword",
            documentQAFailed: "Document Q&A failed, please try again later"
        }
    }
};

// 当前语言
let currentLanguage = localStorage.getItem('language') || 'zh';

// 国际化函数
function t(key, params = {}) {
    const keys = key.split('.');
    let value = i18nConfig[currentLanguage];
    
    for (const k of keys) {
        if (value && typeof value === 'object' && k in value) {
            value = value[k];
        } else {
            console.warn(`Translation key not found: ${key}`);
            return key;
        }
    }
    
    // 参数替换
    if (typeof value === 'string' && Object.keys(params).length > 0) {
        return value.replace(/\{\{(\w+)\}\}/g, (match, param) => {
            return params[param] || match;
        });
    }
    
    return value;
}

// 切换语言
function switchLanguage(lang) {
    if (lang && (lang === 'zh' || lang === 'en')) {
        currentLanguage = lang;
        localStorage.setItem('language', lang);
        
        // 更新页面内容
        updatePageContent();
        
        // 触发语言切换事件
        document.dispatchEvent(new CustomEvent('languageChanged', { detail: { language: lang } }));
    }
}

// 获取当前语言
function getCurrentLanguage() {
    return currentLanguage;
}

// 更新页面内容
function updatePageContent() {
    // 更新所有带有 data-i18n 属性的元素
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        const translation = t(key);
        
        if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
            if (element.type === 'submit' || element.type === 'button') {
                element.value = translation;
            } else {
                element.placeholder = translation;
            }
        } else {
            element.textContent = translation;
        }
    });
    
    // 更新页面标题
    const titleKey = document.querySelector('meta[name="i18n-title"]');
    if (titleKey) {
        document.title = t(titleKey.getAttribute('content'));
    }
    
    // 更新语言切换按钮状态
    updateLanguageSwitcher();
}

// 更新语言切换器状态
function updateLanguageSwitcher() {
    // 更新语言切换按钮
    document.querySelectorAll('.language-switcher').forEach(switcher => {
        const zhBtn = switcher.querySelector('[data-lang="zh"]');
        const enBtn = switcher.querySelector('[data-lang="en"]');
        
        if (zhBtn && enBtn) {
            // 移除所有活动状态
            zhBtn.classList.remove('active', 'bg-blue-600', 'text-white');
            enBtn.classList.remove('active', 'bg-blue-600', 'text-white');
            zhBtn.classList.add('text-gray-600', 'hover:text-gray-800');
            enBtn.classList.add('text-gray-600', 'hover:text-gray-800');
            
            // 添加当前语言的活动状态
            const activeBtn = currentLanguage === 'zh' ? zhBtn : enBtn;
            activeBtn.classList.remove('text-gray-600', 'hover:text-gray-800');
            activeBtn.classList.add('active', 'bg-blue-600', 'text-white');
        }
    });
    
    // 更新下拉菜单中的语言选择
    document.querySelectorAll('.language-dropdown').forEach(dropdown => {
        const zhOption = dropdown.querySelector('[data-lang="zh"]');
        const enOption = dropdown.querySelector('[data-lang="en"]');
        
        if (zhOption && enOption) {
            zhOption.classList.remove('bg-blue-50', 'text-blue-600');
            enOption.classList.remove('bg-blue-50', 'text-blue-600');
            
            const activeOption = currentLanguage === 'zh' ? zhOption : enOption;
            activeOption.classList.add('bg-blue-50', 'text-blue-600');
        }
    });
}

// 创建语言切换器HTML
function createLanguageSwitcher(type = 'button') {
    if (type === 'dropdown') {
        return `
            <div class="relative language-dropdown">
                <button class="flex items-center space-x-2 px-3 py-2 text-sm text-gray-600 hover:text-gray-800 rounded-lg hover:bg-gray-100">
                    <i class="fas fa-globe"></i>
                    <span data-i18n="nav.language">${t('nav.language')}</span>
                    <i class="fas fa-chevron-down text-xs"></i>
                </button>
                <div class="absolute right-0 mt-2 w-32 bg-white rounded-lg shadow-lg border border-gray-200 z-50 hidden">
                    <a href="#" data-lang="zh" onclick="switchLanguage('zh')" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-t-lg">
                        ${t('nav.chinese')}
                    </a>
                    <a href="#" data-lang="en" onclick="switchLanguage('en')" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-b-lg">
                        ${t('nav.english')}
                    </a>
                </div>
            </div>
        `;
    } else {
        return `
            <div class="language-switcher flex items-center space-x-1 bg-gray-100 rounded-lg p-1">
                <button data-lang="zh" onclick="switchLanguage('zh')" class="px-3 py-1 text-sm rounded-md transition-colors">
                    中文
                </button>
                <button data-lang="en" onclick="switchLanguage('en')" class="px-3 py-1 text-sm rounded-md transition-colors">
                    EN
                </button>
            </div>
        `;
    }
}

// 初始化国际化
function initializeI18n() {
    // 检测浏览器语言
    if (!localStorage.getItem('language')) {
        const browserLang = navigator.language || navigator.userLanguage;
        if (browserLang.startsWith('en')) {
            currentLanguage = 'en';
        } else {
            currentLanguage = 'zh';
        }
        localStorage.setItem('language', currentLanguage);
    }
    
    // 更新页面内容
    updatePageContent();
    
    // 设置语言切换器事件
    setupLanguageSwitcherEvents();
}

// 设置语言切换器事件
function setupLanguageSwitcherEvents() {
    // 下拉菜单事件
    document.querySelectorAll('.language-dropdown').forEach(dropdown => {
        const button = dropdown.querySelector('button');
        const menu = dropdown.querySelector('div');
        
        if (button && menu) {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                menu.classList.toggle('hidden');
            });
            
            // 点击外部关闭菜单
            document.addEventListener('click', (e) => {
                if (!dropdown.contains(e.target)) {
                    menu.classList.add('hidden');
                }
            });
        }
    });
}

// 获取当前语言的URL前缀
function getLanguagePrefix() {
    return currentLanguage === 'en' ? '/en' : '';
}

// 获取本地化的URL
function getLocalizedUrl(path) {
    const prefix = getLanguagePrefix();
    return prefix + path;
}

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeI18n();
});

// 导出函数供全局使用
window.t = t;
window.switchLanguage = switchLanguage;
window.getCurrentLanguage = getCurrentLanguage;
window.createLanguageSwitcher = createLanguageSwitcher;
window.getLocalizedUrl = getLocalizedUrl;
