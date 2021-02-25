const getId = id => document.getElementById(id);
const queryD = q => document.querySelector(q);
const queryAll = q => document.querySelectorAll(q);

const makeRequest = async (req, path) => {
  try {
    const response = await fetch(`${window.origin}/${path}`, {
      method: 'POST',
      body: JSON.stringify(req),
      headers: new Headers({
        'content-type': 'application/json',
      }),
    });

    const text = await response.text();
    const json = JSON.parse(text);

    return [json, response.status];
  } catch (err) {
    return [{ message: err.message }, -1];
  }
};

const wait = async miliseconds =>
  new Promise((resolve, reject) => {
    setTimeout(() => resolve(), miliseconds);
  });

export { getId, queryD, queryAll, makeRequest, wait };
