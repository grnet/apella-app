import DS from 'ember-data';
import gen from 'ember-gen/lib/attrs';

export default DS.Model.extend({
  title: gen.attr(),
  institution: DS.belongsTo('institution', {attrs: {optionLabelAttr: 'title_current'}}),
});
