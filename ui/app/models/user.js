import DS from 'ember-data';
import ENV from 'ui/config/environment';

const CHOICES = ENV.APP.resource_choices;

export default DS.Model.extend({
  username: DS.attr(),
  role: DS.attr({type: 'select', choices: CHOICES.USER_ROLES}),

});
