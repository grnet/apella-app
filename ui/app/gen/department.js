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
      dep_number: [validate.presence(true), validate.number({integer: true})]
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
    sortBy: 'title_current:asc',
    row: {
      fields: ['title_current', field('school.title_current', {label: 'school.label', type: 'text'}), 'institution.title_current'],
      actions: ['gen:details', 'gen:edit', 'remove']
    }
  },
  details: {
    page: {
      title: computed.readOnly('model.title_current')
    },
  },
  create: {
    onSubmit(model) {
      this.transitionTo('department.record.index', model)
    }
  }
});
