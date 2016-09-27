import DS from 'ember-data';

export default DS.Model.extend({
  title: DS.attr(),
  institution: DS.belongsTo('institution', {attrs: {optionLabelAttr: 'title'}}),

});
