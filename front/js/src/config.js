const dev = {
  API_ROOT: "http://159.122.177.2:30170/"
};

const prod = {
  API_ROOT: "/"
};

const config = process.env.REACT_APP_STAGE === "prod" ? prod : dev;

export { config };
