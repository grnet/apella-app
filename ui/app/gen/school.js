import gen from 'ember-gen/lib/gen';
import {field} from 'ember-gen';

export default gen.CRUDGen.extend({
  modelName: 'school',
  path: 'schools',
  common: {
    menu: {
      icon: 'account_balance',
      label: 'school.menu_label'
    }
  },
  list: {
    layout: 'table',
    fields: ['title', field('institution.title_current', {label: 'institution.label', type: 'text'})],
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
