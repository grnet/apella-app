import Ember from 'ember';
import fetch from 'ember-network/fetch';

const {
  RSVP: { Promise }
} = Ember;


function uploadFile(file, url, token, file_data_key='file_path') {
  let data = new FormData();
  data.append(file_data_key, file.file);

  Object.keys(file).forEach((key) => {
    if (key !== 'file') {
      data.append(key, file[key]);
    }
  });

  return fetch(url, {
    method: 'POST',
    headers: {
      'Authorization': `Token ${token}`
    },
    body: data
  }).then((resp) => {
    if (resp.status < 200 || resp.status > 299) {
      return resp.json().then((jresp) => {
        throw jresp;
      })
    } else {
      return file;
    }
  })
}


function uploadFiles(files, url, token) {
  // TODO: support for multiple uploads?
}

export { uploadFile, uploadFiles };
