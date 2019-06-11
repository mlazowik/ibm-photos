import React from "react";
import "carbon-components/css/carbon-components.min.css";
import {
  Content,
  Header,
  HeaderGlobalAction,
  HeaderGlobalBar,
  HeaderName
} from "carbon-components-react";

import Search20 from "@carbon/icons-react/es/search/20";
import Notification20 from "@carbon/icons-react/es/notification/20";
import AppSwitcher20 from "@carbon/icons-react/es/app-switcher/20";

const noop = () => {};

function App() {
  return (
    <>
      <Header aria-label="IBM Platform Name">
        <HeaderName href="#">Photos</HeaderName>
        <HeaderGlobalBar>
          <HeaderGlobalAction aria-label="Search" onClick={noop}>
            <Search20 />
          </HeaderGlobalAction>
          <HeaderGlobalAction
            aria-label="Notifications"
            isActive
            onClick={noop}
          >
            <Notification20 />
          </HeaderGlobalAction>
          <HeaderGlobalAction aria-label="App Switcher" onClick={noop}>
            <AppSwitcher20 />
          </HeaderGlobalAction>
        </HeaderGlobalBar>
      </Header>
      <Content>
        <p>Test</p>
      </Content>
    </>
  );
}

export default App;
