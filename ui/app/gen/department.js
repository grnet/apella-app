import {ApellaGen} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';
import {field} from 'ember-gen';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';

const {
  get,
  computed
} = Ember;

export default ApellaGen.extend({
  modelName: 'department',
  auth: true,
  path: 'departments',
  common: {
    proloadModels: ['institution', 'department'],
    validators: {
      title: [i18nValidate([validate.presence(true), validate.length({min:4, max:50})])],
    }
  },
  list: {
    menu: {
      icon: 'domain',
      label: 'department.menu_label'
    },
    page: {
      title: 'department.menu_label',
    },
    layout: 'table',
    paginate: {
      limit: [10, 15]
    },
    sortBy: 'title_current:asc',
    row: {
      fields: ['title_current', field('school.title_current', {label: 'school.label', type: 'text'}), 'institution.title_current'],
      actions: ['gen:details', 'gen:edit', 'remove']
    }
  },
  details: {
    page: {
      title: computed.readOnly('model.id')
    },
    create: [field('title_current', {component: 'i18n-input-field'})]
  }
});
