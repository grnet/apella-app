import DS from 'ember-data';

const STATES = [
    ['1', 'Draft'],
    ['2', 'Posted'],
    ['3', 'Electing'],
    ['4', 'Successful'],
    ['5', 'Failed']
]

export default DS.Model.extend({
  title: DS.attr(),
  description: DS.attr({type:'text'}),
  discipline: DS.attr(),
  author: DS.belongsTo('user', {
    attrs: {
      optionLabelAttr: 'username',
      disabled: true,
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
  state: DS.attr({type: 'select', choices: STATES}),
  starts_at: DS.attr('date'),
  ends_at: DS.attr('date'),
  created_at: DS.attr('date'),
  updated_at: DS.attr('date'),
  // Use in candidacy select list
  id_and_title: Ember.computed('id', 'title', function() {
    return `${this.get('id')} -  ${this.get('title')}`;
  })
});
