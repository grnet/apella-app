import DS from 'ember-data';
import gen from 'ember-gen/lib/attrs';
import {computeI18N} from 'ui/lib/common';

export default DS.Model.extend({
  title: DS.attr({formComponent: 'i18n-input-field'}),
  dep_number: DS.attr({defaultValue: 0}),
  school: gen.belongsTo('school', {formAttrs: {optionLabelAttr: 'title_current'}}),
  institution: gen.belongsTo('institution', {formAttrs: {optionLabelAttr: 'title_current'}}),

  title_current: computeI18N('title'),
});
