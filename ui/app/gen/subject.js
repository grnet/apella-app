import {ApellaGen, i18nField} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';
import {field} from 'ember-gen/lib/util';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';

const {
  computed,
  get
} = Ember;

let FS = {
  list : [i18nField('title'), i18nField('area.title')]
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
    sort: {
      active: true,
      fields: ['title'],
      serverSide: true
    },
    filter: {
      active: true,
      meta: {
        fields: [i18nField('title'), 'area']
      },
      serverSide: true,
      search: true,
      searchFields: ['title']
    },
    page: {
      title: 'subject.menu_label',
    },
    menu: {
      icon: 'local_library',
      label: 'subject.menu_label'
    },
    layout: 'table',
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
