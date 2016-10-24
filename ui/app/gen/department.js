import gen from 'ember-gen/lib/gen';
import {field} from 'ember-gen';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';

export default gen.CRUDGen.extend({
  modelName: 'department',
  path: 'departments',
  common: {
    menu: {
      icon: 'domain',
      label: 'department.menu_label'
    },
    validators: {
      title: [i18nValidate([validate.presence(true), validate.length({min:4, max:50})])],
    }
  },
  list: {
    layout: 'table',
    sortBy: 'title_current:asc',
    fields: ['title_current', field('school.title_current', {label: 'school.label', type: 'text'})],
    page: {
      title: 'department.menu_label',
    }
  },
  create: {
    page: {
      title: 'department.create_title'
    },
  }
});
