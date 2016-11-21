import DS from 'ember-data';
import gen from 'ember-gen/lib/attrs';
import titleI18NMixin from 'ui/mixins/title-current';

export default DS.Model.extend(titleI18NMixin, {
  title: DS.attr({component: 'i18n-input-field'}),
  area: gen.belongsTo('subject_area', {formAttrs: {optionLabelAttr: 'title_current'}}),


});
