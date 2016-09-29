import validate from 'ember-gen/validate';
import gen from 'ember-gen/lib/gen';

export default gen.CRUDGen.extend({
  modelName: 'position',
  common: {
    validators: {
      title: [validate.presence(true), validate.length({min:4, max:50})],
      description: [validate.presence(true), validate.length({max:300})],
    }
  }

});
