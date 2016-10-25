import gen from 'ember-gen/lib/gen';

export default gen.CRUDGen.extend({
  modelName: 'institution-manager',
  path: 'managers',
  common: {
    menu: {
      label: 'manager.menu_label',
      icon: 'sentiment very satisfied'
    }
  },
  list: {
    layout: 'table',
    page: {
      title: 'manager.menu_label',
    },
    label: 'manager.menu_label',
    fields: ['id', 'institution.title_current', 'username'],
    menu: {
      label: 'manager.menu_label',
    },
    row: {
      label: 'manager.menu_label',
      icon: 'person',
    },
  },
  create: {
    page: {
      title: 'manager.create_title'
    },
  },
  details: {
    fields: ['id', 'username', 'last_name'],
  }
});
