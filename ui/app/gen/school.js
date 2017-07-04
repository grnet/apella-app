import {ApellaGen, i18nField, filterSelectSortTitles} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';
import {field} from 'ember-gen';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';

const {
  computed,
  get
} = Ember;

const FIELDS = [
  i18nField('title'),
  field('institution.title_current', {label: 'institution.label', type: 'text'})
]

export default ApellaGen.extend({
  order: 1200,
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
      display: computed('role', function() {
        let role = get(this, 'session.session.authenticated.role');
        let permittedRoles = ['helpdeskuser', 'helpdeskadmin'];

        return (permittedRoles.includes(role) ? true : false);
      })
    },
    sort: {
      active: true,
      serverSide: true,
      fields: ['title']
    },
    filter: {
      active: true,
      meta: {
        fields: [filterSelectSortTitles('institution')]
      },
      serverSide: true,
      search: true,
      searchFields: ['title']
    },
    row: {
      fields: FIELDS,
      actions: ['gen:details', 'gen:edit', 'remove']
    },
  },
  details: {
    page: {
      title: computed.readOnly('model.title_current')
    },
    fieldsets: [{
      fields: FIELDS,
      layout: {
        flex: [50, 50]
      }
    }]
  }
});
