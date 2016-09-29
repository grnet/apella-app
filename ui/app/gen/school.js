import gen from 'ember-gen/lib/gen';

export default gen.CRUDGen.extend({
  modelName: 'school',
  common: {
    menu: {
      icon: 'account_balance'
    }
  }
});
