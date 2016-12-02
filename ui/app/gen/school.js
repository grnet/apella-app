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
  common: {
    validators: {
      title: [i18nValidate([validate.presence(true), validate.length({min:4, max:50})])]
    }
  },
  list: {
    page: {
      title: 'school.menu_label',
    },
    menu: {
      icon: 'account_balance',
      label: 'school.menu_label'
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
