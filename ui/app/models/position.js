import DS from 'ember-data';
import ENV from 'ui/config/environment';
import get_label from '../utils/common/label_list_item';

const { computed, get } = Ember,
      CHOICES = ENV.APP.resource_choices;


export default DS.Model.extend({
  title: DS.attr(),
  description: DS.attr({type:'text'}),
  discipline: DS.attr(),
  author: DS.belongsTo('user', {
    attrs: {
      optionLabelAttr: 'username',
    },
  }),
  department: DS.belongsTo('department', {attrs: {optionLabelAttr: 'title'}}),
  subject_area: DS.belongsTo('subject_area', {attrs: {optionLabelAttr: 'title'}}),
  subject: DS.belongsTo('subject', {attrs: {optionLabelAttr: 'title'}}),
  fek: DS.attr(),
  fek_posted_at: DS.attr('date', {attrs: {time: true}}),
  assistants: DS.hasMany('user', {attrs: {optionLabelAttr: 'username'}}),
  electors: DS.hasMany('user', {attrs: {optionLabelAttr: 'username'}}),
  committee: DS.hasMany('user', {attrs: {optionLabelAttr: 'username'}}),
  elected: DS.belongsTo('user', {attrs: {optionLabelAttr: 'username'}}),
  state: DS.attr({type: 'select', choices: CHOICES.POSITION_STATES, defaultValue: 2}),
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

  state_verbose: computed('state',function() {
    let list = CHOICES.POSITION_STATES;
    return get_label(list, get(this, 'state'));
  }),

});
