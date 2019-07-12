const dev = {
  API_ROOT: "//127.0.0.1:8000/"
};

const prod = {
  API_ROOT: "/"
};

const config = process.env.REACT_APP_STAGE === "prod" ? prod : dev;

export { config };
