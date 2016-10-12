import DS from 'ember-data';
import gen from 'ember-gen/lib/attrs';

export default DS.Model.extend({
  title: gen.attr(),
  school: gen.belongsTo('school', {attrs: {optionLabelAttr: 'title'}}),
});
