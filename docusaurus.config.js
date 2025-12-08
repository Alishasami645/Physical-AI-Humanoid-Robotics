// module.exports = {
//   title: "Physical AI & Humanoid Robotics",
//   url: "https://alishasami645.github.io",
//   baseUrl: "/Physical-AI-Humanoid-Robotics/",
//   onBrokenLinks: "throw",
//   onBrokenMarkdownLinks: "warn",
//   favicon: "img/favicon.ico",

//   organizationName: "alishasami645",
//   projectName: "Physical-AI-Humanoid-Robotics",

//   presets: [
//     [
//       "@docusaurus/preset-classic",
//       {
//         docs: {
//           sidebarPath: require.resolve("./sidebars.js"),
//           editUrl:
//             "https://github.com/alishasami645/Physical-AI-Humanoid-Robotics/tree/main/",
//         },
//         theme: {
//           customCss: require.resolve("./src/css/custom.css"),
//         },
//       },
//     ],
//   ],
  

//   themeConfig: {
//     navbar: {
//       title: "Physical AI & Humanoid Robotics",
//       logo: { alt: 'Logo', src: 'img/logo-book.png' },
//       items: [
//         {
//           type: "docSidebar",
//           sidebarId: "tutorialSidebar", // must match sidebars.js
//           position: "left",
//           label: "Book",
//         },
//         {
//           href: "https://github.com/alishasami645/Physical-AI-Humanoid-Robotics",
//           label: "GitHub",
//           position: "right",
//         },
//       ],
//     },
//   },
// };




const {themes: prismThemes} = require('prism-react-renderer');

const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Bringing Artificial Intelligence to Life, Guiding Humanoid Robots from Simulation to Reality.',
  favicon: 'img/favicon.ico',
  url: 'https://alishasami645.github.io',
  baseUrl: '/Physical-AI-Humanoid-Robotics/',
  organizationName: 'alishasami645',
  projectName: 'Physical-AI-Humanoid-Robotics',
  onBrokenLinks: 'throw',
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },
  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.js',
          editUrl: 'https://github.com/alishasami645/Physical-AI-Humanoid-Robotics/tree/main/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      },
    ],
  ],
  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    colorMode: { respectPrefersColorScheme: true },
    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      logo: { alt: 'Logo', src: 'img/logo-book.png' },
      items: [
        { type: 'docSidebar', sidebarId: 'tutorialSidebar', position: 'left', label: 'Book' },
        { href: 'https://github.com/Alishasami645', label: 'GitHub', position: 'right' },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        { title: 'Docs', items: [{ label: 'Book', to: '/docs/intro' }] },
        { title: 'Community', items: [{ label: 'LinkedIn', href: 'https://www.linkedin.com/in/alisha-sami-95b624379' }] },
        { title: 'More', items: [{ label: 'GitHub', href: 'https://github.com/Alishasami645' }] },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} My Project, Inc. Built with Docusaurus.`,
    },
    prism: { theme: prismThemes.github, darkTheme: prismThemes.dracula },
  },
};

module.exports = config;