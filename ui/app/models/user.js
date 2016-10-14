import DS from 'ember-data';
import ENV from 'ui/config/environment';
import get_label from '../utils/common/label_list_item';

const CHOICES = ENV.APP.resource_choices;

export default DS.Model.extend({
  username: DS.attr(),
  role: DS.attr({type: 'select', choices: CHOICES.USER_ROLES}),
  role_verbose: Ember.computed('role', function(){
    let role_id = `${this.get('role')}`;
    let role_list = CHOICES.USER_ROLES;

    return  get_label(role_list, role_id);
  }),
});
