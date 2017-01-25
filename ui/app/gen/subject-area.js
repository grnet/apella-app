import {ApellaGen, i18nField} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';

const {
  computed,
  get
} = Ember;

export default ApellaGen.extend({
  order: 1500,
  modelName: 'subject_area',
  auth: true,
  path: 'subject-areas',
  session: Ember.inject.service(),

  common: {
    validators: {
      title: [i18nValidate([validate.presence(true), validate.length({min:3, max:200})])],
    }
  },
  list: {
    page: {
      title: 'subject_area.menu_label',
    },
    menu: {
      icon: 'school',
      label: 'subject_area.menu_label',
      display: computed('role', function() {
        let role = get(this, 'session.session.authenticated.role');
        let permittedRoles = ['helpdeskuser', 'helpdeskadmin'];

        return (permittedRoles.includes(role) ? true : false);
      })
    },
    filter: {
      active: false,
      serverSide: true,
      search: true,
      meta: {},
      searchFields: ['title']
    },
    sort: {
      active: true,
      fields: ['title'],
      serverSide: true
    },
    layout: 'table',
     row: {
      fields: [i18nField('title')],
      actions: ['gen:edit', 'remove']
    },
  },
  details: {
    page: {
      title: computed.readOnly('model.title_current')
    },
    fields: ['title_current']
  }
});
