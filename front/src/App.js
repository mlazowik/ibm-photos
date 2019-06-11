import axios from "axios";
import React, { useEffect, useState } from "react";
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

import Gallery from "react-photo-gallery";
import InfiniteScroll from "react-infinite-scroller";

const noop = () => {};

function App() {
  const BATCH = 50;

  const [allPhotos, setAllPhotos] = useState([]);
  const [photos, setPhotos] = useState({ list: [], hasMore: false });
  const [initialLoad, setInitialLoad] = useState(true);

  useEffect(() => {
    async function fetchPhotos() {
      const result = await axios("//127.0.0.1:8000/media/photos.json");
      setAllPhotos(result.data);
      setPhotos({
        list: result.data.slice(0, BATCH),
        hasMore: BATCH < result.data.length
      });
    }
    fetchPhotos();
  }, []);

  function loadMorePhotos() {
    const newSize = photos.list.length + BATCH;
    setPhotos({
      list: allPhotos.slice(0, newSize),
      hasMore: newSize < allPhotos.length
    });
    setInitialLoad(false);
  }

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
        <InfiniteScroll
          pageStart={0}
          initialLoad={initialLoad}
          hasMore={photos.hasMore}
          loadMore={loadMorePhotos}
        >
          <Gallery photos={photos.list} margin={3} />
        </InfiniteScroll>
      </Content>
    </>
  );
}

export default App;
