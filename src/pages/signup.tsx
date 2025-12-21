import React from 'react';
import Layout from '@theme/Layout';
import SignUp from '@site/src/components/SignUp';

export default function SignUpPage(): JSX.Element {
  return (
    <Layout
      title="Sign Up"
      description="Create your account and join the robotics community"
    >
      <SignUp />
    </Layout>
  );
}
