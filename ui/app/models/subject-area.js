import DS from 'ember-data';
import titleI18NMixin from 'ui/mixins/title-current';

export default DS.Model.extend(titleI18NMixin, {
  title: DS.attr({formComponent: 'i18n-input-field'}),
});
