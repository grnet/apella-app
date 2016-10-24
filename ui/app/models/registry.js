import DS from 'ember-data';
import ENV from 'ui/config/environment';
import get_label from '../utils/common/label_list_item';

const { computed, get } = Ember,
      CHOICES = ENV.APP.resource_choices;

export default DS.Model.extend({
  type: DS.attr({type: 'select', choices: CHOICES.REGISTRY_TYPES, defaultValue: 2}),
  department: DS.belongsTo('department', {attrs: {optionLabelAttr: 'title'}}),
  members: DS.hasMany('user', {attrs: {optionLabelAttr: 'username'}}),

  type_verbose: computed('type', 'i18n.locale', function() {
    let id = get(this, 'id') + '';
    let list = CHOICES.REGISTRY_TYPES;
    return this.get('i18n').t(get_label(list, id))
  }),

  institution: computed('department.school.institution', function() {
    return get(this, 'department.school.institution');
  })
});
