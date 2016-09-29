import gen from 'ember-gen/lib/gen';

export default gen.CRUDGen.extend({
  modelName: 'user',
  common: {
    menu: {
      icon: 'face',
    }
  }
});
