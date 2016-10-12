import DS from 'ember-data';
import gen from 'ember-gen/lib/attrs';

export default DS.Model.extend({
  title: gen.attr(),
  area: gen.belongsTo('subject_area', {attrs: {optionLabelAttr: 'title'}}),
});
