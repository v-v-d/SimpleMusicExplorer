const baseURL = "http://127.0.0.1:8000/api/v1/";

const removeTokenIf401 = func => {
  async function wrapper() {
    const response = await func(...arguments);
    if (response.status === 401) {
      localStorage.removeItem("token");
    }
    return response;
  }
  return wrapper;
};

const logged = func => {
  async function wrapper() {
    try {
      return await func(...arguments);
    } catch (error) {
      console.log(`Error: ${error.stack}`);
    }
  }
  return wrapper;
};

let request = async ({
  url,
  method = "GET",
  body = null,
  headers = { "Content-type": "application/json" },
  authorized = false,
  params = null
} = {}) => {
  if (authorized) {
    Object.assign(headers, {
      Authorization: localStorage.getItem("token")
    });
  }

  let uri = `${baseURL}${url}`;

  if (params && params instanceof Object) {
    uri = new URL(uri);
    uri.search = new URLSearchParams(params).toString();
  }

  return await fetch(uri, {
    method: method,
    body: body ? JSON.stringify(body) : null,
    headers: headers
  });
};

request = logged(removeTokenIf401(request));

export default request;
