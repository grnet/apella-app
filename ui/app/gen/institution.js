import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';

export default gen.CRUDGen.extend({
  modelName: 'institution',
  common: {
    menu: {
      icon: 'location_city',
      label: 'institution.menu_label'
    },
    validators: {
      title: [i18nValidate([validate.presence(true), validate.length({min:4, max:50})])]
    }
  },
  list: {
    tableLayout: true,
    selectable: true,
    page: {
      title: 'institution.menu_label',
    }
  },
  create: {
    page: {
      title: 'institution.create_title'
    },
  }
});
