import DS from 'ember-data';
import ENV from 'ui/config/environment';
import get_label from '../utils/common/label_list_item';

const { computed, get } = Ember,
      CHOICES = ENV.APP.resources;

export default DS.Model.extend({
  type: DS.attr({type: 'select', choices: CHOICES.REGISTRY_TYPES, defaultValue: 2}),
  department: DS.belongsTo('department', {formAttrs: {optionLabelAttr: 'title_current'}}),
  members: DS.hasMany('professor'),

  type_verbose: computed('type', 'i18n.locale', function() {
    let type = get(this, 'type');
    let list = CHOICES.REGISTRY_TYPES;
    return this.get('i18n').t(get_label(list, type))
  }),

  institution: computed('department.institution', function() {
    return get(this, 'department.institution');
  })
});
