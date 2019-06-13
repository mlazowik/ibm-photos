import axios from "axios";
import React, { useEffect, useState } from "react";

import styles from "./App.module.css";

import Gallery from "react-photo-gallery";
import InfiniteScroll from "react-infinite-scroller";

import "carbon-components/css/carbon-components.min.css";
import {
  Content,
  Header,
  HeaderGlobalAction,
  HeaderGlobalBar,
  HeaderName,
  Search
} from "carbon-components-react";
import Search20 from "@carbon/icons-react/es/search/20";
import Notification20 from "@carbon/icons-react/es/notification/20";
import AppSwitcher20 from "@carbon/icons-react/es/app-switcher/20";

import { noop } from "./noop";
import { config } from "./config";
import { useDebounce } from "./debounce";

function App() {
  const BATCH = 50;

  const [allPhotos, setAllPhotos] = useState([]);
  const [photos, setPhotos] = useState({ list: [], hasMore: false });
  const [initialLoad, setInitialLoad] = useState(true);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);

  const debouncedQuery = useDebounce(query, 200);

  useEffect(() => {
    async function fetchPhotos() {
      const escaped = encodeURIComponent(debouncedQuery);

      const result = await axios(
        `${config.API_ROOT}api/photos/?query=${escaped}`
      );
      setAllPhotos(result.data);
      setPhotos({
        list: result.data.slice(0, BATCH),
        hasMore: BATCH < result.data.length
      });
      setLoading(false);
    }

    setLoading(true);
    fetchPhotos();
  }, [debouncedQuery]);

  function loadMorePhotos() {
    const newSize = photos.list.length + BATCH;
    setPhotos({
      list: allPhotos.slice(0, newSize),
      hasMore: newSize < allPhotos.length
    });
    setInitialLoad(false);
  }

  function onSerach(event) {
    setLoading(true);
    setQuery(event.target.value);
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
        <Search
          className={styles.search}
          light={false}
          name=""
          defaultValue=""
          labelText="Search"
          closeButtonLabelText=""
          placeHolderText="Search"
          id="search-1"
          value={query}
          onChange={onSerach}
        />
        <InfiniteScroll
          pageStart={0}
          initialLoad={initialLoad}
          threshold={2000}
          hasMore={photos.hasMore}
          loadMore={loadMorePhotos}
        >
          <div className={loading ? styles.loading : ""}>
            <Gallery photos={photos.list} margin={3} />
          </div>
        </InfiniteScroll>
      </Content>
    </>
  );
}

export default App;
