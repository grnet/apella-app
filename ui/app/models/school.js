import DS from 'ember-data';
import gen from 'ember-gen/lib/attrs';
import titleI18NMixin from 'ui/mixins/title-current';

export default DS.Model.extend(titleI18NMixin, {
  title: DS.attr({formComponent: 'i18n-input-field'}),
  institution: DS.belongsTo('institution', {formAttrs: {optionLabelAttr: 'title_current'}}),
});
