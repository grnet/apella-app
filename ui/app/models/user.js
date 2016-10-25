import DS from 'ember-data';
import ENV from 'ui/config/environment';
import get_label from '../utils/common/label_list_item';

const { computed, get } = Ember,
      CHOICES = ENV.APP.resource_choices;

export default DS.Model.extend({
  username: DS.attr(),
  password: DS.attr({attrs: {type: 'password'}}),
  email: DS.attr(),
  first_name: DS.attr({component: 'i18n-input-field'}),
  last_name: DS.attr({component: 'i18n-input-field'}),
  father_name: DS.attr({component: 'i18n-input-field'}),
  role: DS.attr({type: 'select', choices: CHOICES.USER_ROLES}),
  id_passport: DS.attr(),
  mobile_phone_number: DS.attr(),
  home_phone_number: DS.attr(),

  role_verbose: computed('role', function(){
    let role_id = this.get('role');
    let role_list = CHOICES.USER_ROLES;
    return  get_label(role_list, role_id);
  }),

  first_name_current: computed('first_name', 'i18n.locale',  function() {
    let lang = this.get('i18n.locale');
    return this.get('first_name')[lang];
  }),

  last_name_current: computed('last_name', 'i18n.locale',  function() {
    let lang = this.get('i18n.locale');
    return this.get('last_name')[lang];
  }),

  father_name_current: computed('father_name', 'i18n.locale',  function() {
    let lang = this.get('i18n.locale');
    return this.get('father_name')[lang];
  }),

  full_name_current: computed('first_name_current', 'last_name_current', function(){
    return `${this.get('first_name_current')} ${this.get('last_name_current')}`
  })
});
