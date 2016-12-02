import {ApellaGen} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';

const {
  computed,
  get
} = Ember;

let FS = {
  list : ['title_current', 'area.title_current']
}


export default ApellaGen.extend({
  modelName: 'subject',
  auth: true,
  path: 'subjects',
  common: {
    preloadModels: ['subject-area'],
    validators: {
      title: [i18nValidate([validate.presence(true), validate.length({min:4, max:50})])],
    }
  },
  list: {
    page: {
      title: 'subject.menu_label',
    },
    menu: {
      icon: 'local_library',
      label: 'subject.menu_label'
    },
    layout: 'table',
    sort: { serverSide: true },
    search: { serverSide: true },
    row: {
      fields: FS.list,
      actions: ['gen:edit', 'remove']
    }
  },
  details: {
    page: {
      title: computed.readOnly('model.title_current')
    }
  }
});
