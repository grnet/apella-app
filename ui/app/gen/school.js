import {ApellaGen} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';
import {field} from 'ember-gen';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';

const {
  computed,
  get
} = Ember;

export default ApellaGen.extend({
  modelName: 'school',
  auth: true,
  path: 'schools',
  session: Ember.inject.service(),

  common: {
    validators: {
      title: [i18nValidate([validate.presence(true), validate.length({min:4, max:200})])]
    }
  },
  list: {
    page: {
      title: 'school.menu_label',
    },
    menu: {
      icon: 'account_balance',
      label: 'school.menu_label',
      display: computed(function() {
        let role = get(this, 'session.session.authenticated.role');
        let permittedRoles = ['helpdeskuser', 'helpdeskadmin'];

        return (permittedRoles.includes(role) ? true : false);
      })
    },
    layout: 'table',
    row: {
      fields: ['title_current', field('institution.title_current', {label: 'institution.label', type: 'text'})],
      actions: ['gen:details', 'gen:edit', 'remove']
    },
  },
  details: {
    page: {
      title: computed.readOnly('model.title_current')
    }
  }
});
