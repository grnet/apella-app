import gen from 'ember-gen/lib/gen';
import {field} from 'ember-gen';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';

export default gen.CRUDGen.extend({
  modelName: 'school',
  path: 'schools',
  common: {
    menu: {
      icon: 'account_balance',
      label: 'school.menu_label'
    },
    validators: {
      title: [i18nValidate([validate.presence(true), validate.length({min:4, max:50})])]
    }
  },
  list: {
    layout: 'table',
    fields: ['title_current', field('institution.title_current', {label: 'institution.label', type: 'text'})],
    page: {
      title: 'school.menu_label',
    }
  },
  create: {
    page: {
      title: 'school.create_title'
    },
  },
});
