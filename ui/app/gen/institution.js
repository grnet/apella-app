import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';
import {field} from 'ember-gen';

export default gen.CRUDGen.extend({
  modelName: 'institution',
  path: 'institutions',
  common: {
    menu: {
      icon: 'location_city',
      label: 'institution.menu_label'
    },
    validators: {
      title: [i18nValidate([validate.presence(true), validate.length({min:4, max:50})])],
      organization: [validate.format({allowBlank: true, type: 'url'})],
      regulatory_framework: [validate.format({allowBlank: true, type: 'url'})],
    }
  },
  list: {
    sortBy: 'organization:asc',
    layout: 'table',
    fields: ['title_current', 'organization', 'regulatory_framework'],
    page: {
      title: 'institution.menu_label',
    }
  },
  create: {
    fields: ['title', 'organization', 'regulatory_framework'],
    page: {
      title: 'institution.create_title'
    },
  },
  edit: {
    fields: ['title', 'organization', 'regulatory_framework'],
  }
});
