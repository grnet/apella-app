import DS from 'ember-data';
import Ember from 'ember';
import BaseFieldMixin from 'ember-gen/lib/base-field';
import ENV from 'ui/config/environment';
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


export default Ember.Component.extend(BaseFieldMixin, {

  tagName: 'div',
  multiple: reads('fattrs.multiple'),
  replace: reads('fattrs.replace'),
  readonly: reads('field.readonly'),
  disabled: reads('field.disabled'),
  session: inject.service('session'),
  messages: inject.service('messages'),
  inProgress: false,
  attributeBindings: ['disabled'],

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

  canDelete: computed('readonly', 'disabled', function() {
    let {readonly, disabled} = this.getProperties('readonly', 'disabled');
    return !(readonly || disabled);
  }),

  canReplace: computed('readonly', 'disabled', 'replace', function() {
    let {readonly, disabled, replace} = this.getProperties('readonly', 'disabled', 'replace');
    return replace && !(readonly || disabled);
  }),

  canAdd: computed('files.length', 'multiple', function() {
    return get(this, 'multiple') ? true : get(this, 'files.length') === 0;
  }),

  reloadRecord() {
    let errors = get(this, 'object._content.errors');
    errors && errors.clear();
    let object = get(this, 'object._content') || get(this, 'object');
    return object.reload().then((record) => {
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
        return this.reloadRecord().then(() => {
          this.get('messages').setSuccess('delete.file.success');
        });
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
      let messages = get(this, 'messages');

      let target = event.target || this.fileInput;
      let files = target.files;
      if (!files.length) { return; }

      set(this, 'inProgress', true);
      let file = {
        file: files[0],
        file_kind: kind,
        file_description: ''
      };

      return uploadFile(file, url, token).then((file) => {
        this.send('onUploadSuccess', file);
        messages.setSuccess('file.upload.success');
        return file;
      }).catch((err) => {
        messages.setError('file.upload.error');
        throw err;
      }).finally((err) => {
        target.value = '';
        set(this, 'inProgress', false);
      });
    }
  }
});
