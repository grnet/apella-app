import gen from 'ember-gen/lib/gen';
import validate from 'ember-gen/validate';

export default gen.CRUDGen.extend({
  modelName: 'user',
  path: 'users',
  common: {
    menu: {
      icon: 'face',
      label: 'user.menu_label'
    },
    validators: {
      mobile_phone_number: [validate.format({ type: 'phone' })],
      home_phone_number: [validate.format({ type: 'phone' })],
      email: [validate.format({ type: 'email' })],
    }
  },
  list: {
    layout: 'table',
    sortBy: 'username:asc',
    fields: ['username', 'email', 'full_name_current', 'role_verbose'],
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
