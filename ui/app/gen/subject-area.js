import {ApellaGen, i18nField} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';

const {
  computed,
  get
} = Ember;

export default ApellaGen.extend({
  modelName: 'subject_area',
  auth: true,
  path: 'subject-areas',
  session: Ember.inject.service(),

  common: {
    validators: {
      title: [i18nValidate([validate.presence(true), validate.length({min:4, max:200})])],
    }
  },
  list: {
    page: {
      title: 'subject_area.menu_label',
    },
    menu: {
      icon: 'school',
      label: 'subject_area.menu_label',
      display: computed(function() {
        let role = get(this, 'session.session.authenticated.role');
        let permittedRoles = ['helpdeskuser', 'helpdeskadmin'];

        return (permittedRoles.includes(role) ? true : false);
      })
    },
    filter: {
      active: false,
      serverSide: true,
      search: true,
      searchFields: ['title']
    },

    layout: 'table',
    sortBy: 'title_current:asc',
     row: {
      fields: ['title_current'],
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
