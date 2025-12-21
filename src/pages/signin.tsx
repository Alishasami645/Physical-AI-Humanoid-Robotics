import React from 'react';
import Layout from '@theme/Layout';
import SignIn from '@site/src/components/SignIn';

export default function SignInPage(): JSX.Element {
  return (
    <Layout
      title="Sign In"
      description="Sign in to your robotics account"
    >
      <SignIn />
    </Layout>
  );
}
