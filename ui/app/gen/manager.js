import gen from 'ember-gen/lib/gen';

export default gen.CRUDGen.extend({
  modelName: 'manager',
  list: {
    fields: ['id', 'username', 'last_name'],
    row: {
      icon: 'person',
    },
    menu: {
      icon: 'do not disturb on'
    }
  },
  create:{
  },
  details: {
    fields: ['id', 'username', 'last_name'],
  }
});
