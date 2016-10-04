import gen from 'ember-gen/lib/gen';

export default gen.CRUDGen.extend({
  modelName: 'manager',
  common: {
    menu: {
      icon: 'do not disturb on',
      label: 'manager.menu_label'
    }
  },
  list: {
    page: {
      title: 'manager.menu_label',
    },
    label: 'manager.menu_label',
    fields: ['id', 'username', 'last_name'],
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
