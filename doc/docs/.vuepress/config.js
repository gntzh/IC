module.exports = {
    base: '/IC/',
    title: '电子元器件管理系统',
    description: '对使用方法，构键技术，部署方法等作以说明。',
    evergreen: true,
    plugins: [
        '@vuepress/pwa', {
            serviceWorker: true,
            updatePopup: true
        }],
    head: [
        ['link', { rel: 'icon', href: `/favicon.png` },
            ['link', { rel: 'manifest', href: '/manifest.json' }],]
    ],
    themeConfig: {
        logo: '/favicon.png',
        nav: [
            { text: '主页', link: '/' },
            { text: '介绍', link: '/guide/' },
            { text: '关于', link: '/about/' },
            { text: 'Github', link: 'https://github.com/ShoorDay/IC' },
        ],
        sidebarDepth: 2,
        collapsable: true,
        sidebar: {
            '/guide/': [
                '',
                '功能需求',
                '后端',
                '前端',
                '部署',
                '部署参考'
            ]
        }
    }
}