import DS from 'ember-data';
import {computeI18N} from 'ui/lib/common';

export default DS.Model.extend({
  title: DS.attr({formComponent: 'i18n-input-field'}),
  institution: DS.belongsTo('institution', {formAttrs: {optionLabelAttr: 'title_current'}}),

  title_current: computeI18N('title'),
});
