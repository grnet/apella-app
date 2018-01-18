import Ember from 'ember';
import fetch from "ember-network/fetch";
import ENV from 'ui/config/environment';
import ApellaFileComponent from 'ui/components/apella-file-field';
import {uploadFile} from 'ui/utils/files';

const {
  on,
  get, set,
  computed,
  computed: { alias, reads },
  observer,
  $,
  inject
} = Ember;


export default ApellaFileComponent.extend({

  store: Ember.inject.service(),
  success: '',

  actions: {
    handleFile(event) {
      let token = get(this, 'session.session.authenticated.auth_token');
      let path = 'candidacy';
      let adapter = get(this, 'store').adapterFor(path);
      let url = adapter._buildURL(path) + '/upgrade_role/';
      let messages = get(this, 'messages');
      let target = event.target || this.fileInput;
      let files = target.files;

      if (!files.length) { return; }

      set(this, 'inProgress', true);
      let file = {
        file: files[0],
        file_description: ''
      };

      return uploadFile(file, url, token).then((resp) => {
        set(this, 'success', resp);
        messages.setSuccess('file.upload.success');
      }).catch((err) => {
        set(this, 'errors', [err]);
        messages.setError('file.upload.error');
        throw err;
      }).finally((err) => {
        target.value = '';
        set(this, 'inProgress', false);
      });
    }
  }

})


