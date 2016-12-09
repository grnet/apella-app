import DS from 'ember-data';

export default DS.Model.extend({
  user: DS.belongsTo('user'),
  area: DS.hasMany('subject-area'),
  subject: DS.hasMany('subject'),
  institution: DS.hasMany('institution'),
  department: DS.hasMany('department'),
});
