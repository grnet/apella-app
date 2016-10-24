import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';

export default gen.CRUDGen.extend({
  modelName: 'subject_area',
  path: 'subject_areas',
  common: {
    menu: {
      icon: 'school',
      label: 'subject_area.menu_label'
    },
    validators: {
      title: [i18nValidate([validate.presence(true), validate.length({min:4, max:50})])],
    }
  },
  list: {
    layout: 'table',
    sortBy: 'title_current:asc',
    fields: ['title_current'],
    page: {
      title: 'subject_area.menu_label',
    }
  },
  create: {
    page: {
      title: 'subject_area.create_title',
    }
  }
});
