import gen from 'ember-gen/lib/gen';

export default gen.CRUDGen.extend({
  modelName: 'user',
  path: 'users',
  common: {
    menu: {
      icon: 'face',
      label: 'user.menu_label'
    }
  },
  list: {
    fields: ['username', 'role_verbose'],
    page: {
      title: 'user.menu_label',
    }
  },
  create: {
    page: {
      title: 'user.create_title',
    }
  }
});
