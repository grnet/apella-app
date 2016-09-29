import DS from 'ember-data';

export default DS.Model.extend({
  title: DS.attr(),
  school: DS.belongsTo('school', {attrs: {optionLabelAttr: 'title'}}),
});
