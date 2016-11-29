import DS from 'ember-data';
import ENV from 'ui/config/environment';
import get_label from '../utils/common/label_list_item';
import moment from 'moment';

const { computed, get } = Ember,
      CHOICES = ENV.APP.resource_choices,
      DATE_FORMAT = ENV.APP.date_format;


export default DS.Model.extend({
  title: DS.attr(),
  description: DS.attr({type:'text'}),
  discipline: DS.attr(),
  department_dep_number: DS.attr(),

  author: DS.belongsTo('institution-manager', {
    formAttrs: {
      optionLabelAttr: 'full_name_current'
    }
  }),
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
    formComponent: 'select-subject',
    formAttrs: {
      optionLabelAttr: 'title_current',
    }
  }),
  fek: DS.attr(),
  fek_posted_at: DS.attr('date', {formAttrs: {time: true}}),
  assistants: DS.hasMany('user', {formAttrs: {optionLabelAttr: 'username'}}),
  electors: DS.hasMany('user', {formAttrs: {optionLabelAttr: 'username'}}),
  committee: DS.hasMany('user', {formAttrs: {optionLabelAttr: 'username'}}),
  elected: DS.belongsTo('user', {formAttrs: {optionLabelAttr: 'username'}}),
  state: DS.attr({type: 'select', choices: CHOICES.POSITION_STATES, defaultValue: 'posted'}),
  starts_at: DS.attr('date'),
  ends_at: DS.attr('date'),
  created_at: DS.attr('date'),
  updated_at: DS.attr('date'),
  // Use in candidacy select list
  code_and_title: computed('code', 'title', function() {
    return `${this.get('code')} -  ${this.get('title')}`;
  }),

  code: computed('id', function(){
    return `APP${this.get('id')}`;
  }),

  state_verbose: computed('state','i18n.locale', function() {
    let list = CHOICES.POSITION_STATES;
    return this.get('i18n').t(get_label(list, get(this, 'state')))
  }),

  fek_posted_at_format: computed('fek_posted_at', function(){
    return moment(this.get('fek_posted_at')).format(DATE_FORMAT);
  }),

  starts_at_format: computed('starts_at', function(){
    return moment(this.get('starts_at')).format(DATE_FORMAT);
  }),

  ends_at_format: computed('ends_at', function(){
    return moment(this.get('ends_at')).format(DATE_FORMAT);
  }),




});
