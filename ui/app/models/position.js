import DS from 'ember-data';
import ENV from 'ui/config/environment';
import {computeI18N, computeI18NChoice, computeDateFormat} from 'ui/lib/common';
import get_label from '../utils/common/label_list_item';


const { computed, get } = Ember,
      CHOICES = ENV.APP.resources;


export default DS.Model.extend({
  title: DS.attr(),
  description: DS.attr({type:'text'}),
  discipline: DS.attr(),
  department_dep_number: DS.attr(),

  department: DS.belongsTo('department', {
    formAttrs: {
      optionLabelAttr: 'title_current'
    }
  }),
  subject_area: DS.belongsTo('subject-area', {
    formAttrs: {
      optionLabelAttr: 'title_current'
    }
  }),
  subject: DS.belongsTo('subject', {
    formComponent: 'select-onchange',
    formAttrs: {
      lookupModel: 'subject_area',
      changedChoices: function(store, value) {
        return store.query('subject', {area: get(value, 'id')})
      },
      optionLabelAttr: 'title_current',
    }
  }),
  fek: DS.attr(),
  fek_posted_at: DS.attr('date'),
  fek_posted_at_format: computeDateFormat('fek_posted_at'),
  assistants: DS.hasMany('assistant'),
  electors: DS.hasMany('professor', {formAttrs: {optionLabelAttr: 'username'}}),
  committee: DS.hasMany('professor', {formAttrs: {optionLabelAttr: 'username'}}),
  elected: DS.belongsTo('user', {formAttrs: {optionLabelAttr: 'username'}}),
  state: DS.attr({type: 'select', choices: CHOICES.POSITION_STATES, defaultValue: 'posted'}),
  state_verbose: computeI18NChoice('state', CHOICES.POSITION_STATES),
  starts_at: DS.attr('date'),
  starts_at_format: computeDateFormat('starts_at'),
  ends_at: DS.attr('date'),
  ends_at_format: computeDateFormat('ends_at'),
  created_at: DS.attr('date'),
  updated_at: DS.attr('date'),
  code: DS.attr(),
  // Use in candidacy select list
  code_and_title: computed('code', 'title', function() {
    return `${this.get('code')} -  ${this.get('title')}`;
  }),

  candidacies: DS.hasMany('candidacy'),

  participation: DS.attr(),
  participation_current: computed('participation', 'i18n.locale', function(){
    return this.get('i18n').t(this.get('participation'));
  }),


});
