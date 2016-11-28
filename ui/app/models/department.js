import DS from 'ember-data';
import gen from 'ember-gen/lib/attrs';
import titleI18NMixin from 'ui/mixins/title-current';

export default DS.Model.extend(titleI18NMixin, {
  title: DS.attr({formComponent: 'i18n-input-field'}),
  dep_number: DS.attr(),
  school: gen.belongsTo('school', {formAttrs: {optionLabelAttr: 'title_current'}}),
  institution: gen.belongsTo('institution', {formAttrs: {optionLabelAttr: 'title_current'}}),
});
