module.exports = {
  title: "Physical AI & Humanoid Robotics",
  url: "https://alishasami645.github.io",
  baseUrl: "/Physical-AI-Humanoid-Robotics/",
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
            "https://github.com/alishasami645/Physical-AI-Humanoid-Robotics/tree/main/",
        },
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      },
    ],
  ],

  // ✅ New markdown hooks to replace deprecated option
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: "warn", // or "throw" if you want build to fail on broken links
    },
  },

  themeConfig: {
    navbar: {
      title: "Physical AI & Humanoid Robotics",
      logo: { alt: "Logo", src: "img/logo-book.png" },
      items: [
        {
          type: "docSidebar",
          sidebarId: "tutorialSidebar", // must match sidebars.js
          position: "left",
          label: "Book",
        },
        {
          href: "https://github.com/alishasami645/Physical-AI-Humanoid-Robotics",
          label: "GitHub",
          position: "right",
        },
      ],
    },
  },
};
