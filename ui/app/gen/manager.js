import gen from 'ember-gen/lib/gen';

export default gen.CRUDGen.extend({
  modelName: 'manager',
  list: {
    fields: ['id', 'username', 'last_name'],
    row: {
      icon: 'person',
    }
  },
  create:{
  },
  details: {
    fields: ['id', 'username', 'last_name'],
  }
});
