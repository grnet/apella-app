import DS from 'ember-data';
import gen from 'ember-gen/lib/attrs';
import {computeI18N} from 'ui/lib/common';

export default DS.Model.extend({
  title: DS.attr({formComponent: 'i18n-input-field'}),
  area: gen.belongsTo('subject_area', {formAttrs: {optionLabelAttr: 'title_current'}}),

  title_current: computeI18N('title'),


});
