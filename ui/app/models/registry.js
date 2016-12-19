import DS from 'ember-data';
import ENV from 'ui/config/environment';
import {computeI18NChoice} from 'ui/lib/common';

const { computed, get } = Ember,
      CHOICES = ENV.APP.resources;

export default DS.Model.extend({
  type: DS.attr({type: 'select', choices: CHOICES.REGISTRY_TYPES, defaultValue: 2}),
  department: DS.belongsTo('department', {formAttrs: {optionLabelAttr: 'title_current'}}),
  members: DS.hasMany('professor'),

  type_verbose: computeI18NChoice('type', CHOICES.REGISTRY_TYPES),

  institution: computed('department.institution', function() {
    return get(this, 'department.institution');
  })
});
