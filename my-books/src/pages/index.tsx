import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();

  return (
    <header className={clsx("hero", "hero--primary")} style={{ padding: "8rem 0" }}>
      <div
        className="container"
        style={{
          display: "flex",
          flexDirection: "row",
          alignItems: "left",
          justifyContent: "space-between",
          gap: "2rem",
          flexWrap: "wrap",
        }}
      >
        
        

        {/* Center Text */}
        <div style={{ flex: "1 1 350px", textAlign: "left" }}>
          <h1 className="hero__title" style={{ }}>
            {siteConfig.title}
          </h1>
          <p className="hero__subtitle" style={{  }}>
            {siteConfig.tagline}
          </p>
          <div style={{}}>
            <Link className="button button--secondary button--lg" to="/docs/intro">
              Get Started 
            </Link>
          </div>
        </div>

        {/* Right Image */}
        <div style={{ flex: "350px", textAlign: "left"}}>
          <img
            src="/img/ai.png" 
            alt="Right Robot"
            style={{
              width: "100%",
              maxWidth: "320px",
              animation: "float 3.5s ease-in-out infinite",
            }}
          />
        </div>
      </div>
      
    </header>
  );
}



export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}




