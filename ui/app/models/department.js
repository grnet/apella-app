import DS from 'ember-data';
import gen from 'ember-gen/lib/attrs';
import titleI18NMixin from 'ui/mixins/title-current';

export default DS.Model.extend(titleI18NMixin, {
  title: DS.attr({formComponent: 'i18n-input-field'}),
  school: gen.belongsTo('school', {attrs: {optionLabelAttr: 'title_current'}}),
  institution: gen.belongsTo('institution', {attrs: {optionLabelAttr: 'title_current'}}),
});
