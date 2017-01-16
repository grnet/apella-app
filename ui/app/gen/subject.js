import {ApellaGen, i18nField} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';
import {field} from 'ember-gen/lib/util';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';

const {
  computed,
  get
} = Ember;

let FIELDS = [i18nField('title'), i18nField('area.title')];


export default ApellaGen.extend({
  order: 1400,
  modelName: 'subject',
  auth: true,
  path: 'subjects',
  session: Ember.inject.service(),

  common: {
    preloadModels: ['subject-area'],
    validators: {
      title: [i18nValidate([validate.presence(true), validate.length({min:3, max:200})])],
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
      icon: 'subject',
      label: 'subject.menu_label',
      display: computed('role', function() {
        let role = get(this, 'role');
        let permittedRoles = ['helpdeskuser', 'helpdeskadmin'];
        return (permittedRoles.includes(role) ? true : false);
      })
    },
    layout: 'table',
    row: {
      fields: FIELDS,
      actions: ['gen:edit', 'remove']
    }
  },
  details: {
    page: {
      title: computed.readOnly('model.title_current')
    },
    fields: FIELDS
  }
});
