import DS from 'ember-data';
import gen from 'ember-gen/lib/attrs';

export default DS.Model.extend({
  title: DS.attr({component: 'i18n-input-field'}),
  area: gen.belongsTo('subject_area', {attrs: {optionLabelAttr: 'title'}}),
});
