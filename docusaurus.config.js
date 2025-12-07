module.exports = {
  title: "Physical AI & Humanoid Robotics",
  url: "https://github.com/Alishasami645",
  baseUrl: "/Physical-AI-Humanoid-Robotics",
  onBrokenLinks: "throw",
  favicon: "img/favicon.ico",

  organizationName: "alishasami645",
  projectName: "Physical-AI-Humanoid-Robotics",

  presets: [
    [
      "@docusaurus/preset-classic",
      {
        docs: {
          sidebarPath: require.resolve("./sidebars.js"),
          editUrl:
            "https://github.com/Alishasami645/Physical-AI-Humanoid-Robotics/tree/main/",
        },
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      },
    ],
  ],

  markdown: {
    hooks: {
      onBrokenMarkdownLinks: "warn",
    },
  },

  themeConfig: {
    navbar: {
      title: "Physical AI & Humanoid Robotics",
      logo: { alt: "Logo", src: "img/logo-book.png" },
      items: [
        {
          type: "docSidebar",
          sidebarId: "tutorialSidebar",
          position: "left",
          label: "Book",
        },
        {
          href: "https://github.com/Alishasami645/Physical-AI-Humanoid-Robotics",
          label: "GitHub",
          position: "right",
        },
      ],
    },
  },
};
