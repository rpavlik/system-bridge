import React, { ReactElement } from "react";
import dynamic from "next/dynamic";
import { Container } from "@mui/material";
import { GetStaticProps } from "next";

import Layout from "../../components/Common/Layout";
import useStyles from "../../assets/jss/components/layout";

const WebRTC = dynamic(() => import("../../components/WebRTC/WebRTC"), {
  ssr: false,
});

function PageData(): ReactElement {
  const classes = useStyles();

  return (
    <Layout
      classes={classes}
      title="WebRTC"
      url="https://system-bridge.timmo.dev"
      description="Frontend for System Bridge"
      noHeader
      noFooter
    >
      <Container className={classes.mainFill} component="article" maxWidth="xl">
        <WebRTC />
      </Container>
    </Layout>
  );
}

export const getStaticProps: GetStaticProps = async () => {
  return {
    props: {},
    revalidate: 1,
  };
};

export default PageData;
