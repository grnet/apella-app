import DS from 'ember-data';
import Ember from 'ember';
import BaseFieldMixin from 'ember-gen/lib/base-field';
import ENV from 'ui/config/environment';
import fetch from 'ember-network/fetch';

const {
  on,
  get, set,
  computed,
  computed: { alias, reads },
  observer,
  $,
  inject
} = Ember;


export default Ember.Component.extend(BaseFieldMixin, {

  tagName: 'div',
  multiple: reads('fattrs.multiple'),
  session: inject.service('session'),
  messages: inject.service('messages'),
  inProgress: false,

  inputAttrs: {
    readonly: true
  },

  files: computed('value.[]', 'value.id', function() {
    let multiple = get(this, 'multiple');
    let value = get(this, 'value');
    if (value instanceof DS.PromiseObject) {
      value = value.content;
    }
    if (value instanceof DS.PromiseManyArray) {
      return value;
    }
    if (value instanceof DS.Model) {
      return [value];
    }
    if (value instanceof DS.ManyArray) { 
      return value;
    }
    if (value instanceof Array) { 
      return value;
    }
    if (value) { return [value]; }
    return [];
  }),

  canAdd: computed('files.length', 'multiple', function() {
    return get(this, 'multiple') ? true : get(this, 'files.length') === 0;
  }),

  reloadRecord() {
    let errors = get(this, 'object._content.errors');
    errors && errors.clear();
    return get(this, 'object._content').reload().then((record) => {
      let key = get(this, 'field.key');
      let multiple = get(this, 'multiple');
      let value = get(record, key);
      let change = get(this, `object.${key}`);
      let changeset = get(this, 'object');

      if (!multiple) {
        set(this, `object.${key}`, get(record, key));
      }
      return record;
    });
  },


  actions: {

    downloadFile(file, event) {
      event.preventDefault();
      if (file instanceof DS.PromiseObject) {
        file = file.content;
      }
      file && file.download().then((url) => {
        window.open(url);
      });
      return false;
    },

    deleteFile(file) {
      set(this, 'inProgress', true);
      return file.destroyRecord().then(() => {
        return this.reloadRecord();
      }).catch((err) => {
        this.get('messages').setError('delete.file.error');
        throw err;
      }).finally(() => {
        set(this, 'inProgress', false);
      });
    },

    handleAddClick() {
      this.$().find("[type=file]").click();
    },

    onUploadSuccess(file) {
      this.reloadRecord().finally(() => {
        set(this, 'inProgress', false);
      });
      this.$().find("[type=file]").val('');
    },

    handleFile(event) {
      let multiple = get(this, 'multiple');
      let token = get(this, 'session.session.authenticated.auth_token');
      let id = get(this, 'object.id');
      let path = get(this, 'fattrs.path');
      let kind = get(this, 'fattrs.kind');
      let adapter = get(this, 'store').adapterFor(path);
      let url = adapter._buildURL(path, id) + '/upload/';

      let target = event.target || this.fileInput;
      let files = target.files;
      if (!files.length) { return; }
      let file = files[0]; // TODO: support for multiple uploads?

      let data = new FormData();
      data.append('file_kind', kind);
      data.append('file_path', file);
      data.append('file_description', '');

      set(this, 'inProgress', true);
      return fetch(url, {
        method: 'POST',
        headers: {
          'Authorization': `Token ${token}`
        },
        body: data
      }).then((resp) => {
        if (resp.status < 200 || resp.status > 299) {
          resp.json().then((jresp) => {
            this.get('messages').setError(jresp.detail || jresp.message || resp.statusText);
            throw jresp;
          }).catch(() => {
            this.get('messages').setError(resp.statusText);
            throw resp;
          });
        } else {
          this.send('onUploadSuccess', file);
          return file;
        }
      }).finally((err) => {
          set(this, 'inProgress', false);
      });
    }
  }
});
