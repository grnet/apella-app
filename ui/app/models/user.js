import DS from 'ember-data';

const ROLES = [
  ['1', 'Insitution Manager'],
  ['2', 'Candidate'],
  ['3', 'Elector'],
  ['4', 'Committee'],
  ['5', 'Assistant'],
]

export default DS.Model.extend({
  username: DS.attr(),
  role: DS.attr({type: 'select', attr: { choices: ROLES}}),

});
