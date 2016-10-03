import DS from 'ember-data';
import ENV from 'ui/config/environment';

const CHOICES = ENV.APP.resource_choices;

export default DS.Model.extend({
  username: DS.attr(),
  role: DS.attr({type: 'select', choices: CHOICES.USER_ROLES}),
  role_verbose: Ember.computed('role', function(){
    let role_id = `${this.get('role')}`;
    return (CHOICES.USER_ROLES.find(x => x[0] == role_id) || [0, ''])[1]
  }),
});
