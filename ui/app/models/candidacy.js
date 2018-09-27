import DS from 'ember-data';
import {computeI18NChoice, computeDateFormat} from 'ui/lib/common';

const { computed, get } = Ember;

let candidacy_states = [
  ["posted", "Submitted"],
  ["cancelled", "Candidacy_cancelled"]
];

export default DS.Model.extend({
  candidate: DS.belongsTo('user', {label: 'candidacy.label.candidate', formAttrs: {optionLabelAttr: 'full_name_current'}}),
  position: DS.belongsTo('position', {label: 'candidacy.label.position', formAttrs: {optionLabelAttr: 'code_and_title'}}),
  state: DS.attr({type: 'select', choices: candidacy_states, defaultValue: 'posted'}),
  state_verbose: computeI18NChoice('state', candidacy_states),
  othersCanView: DS.attr({type: 'boolean', label: 'candidacy.label.others_can_view', displayComponent: 'boolean-display'}),
  submitted_at: DS.attr('date'),
  submitted_at_format: computeDateFormat('submitted_at'),
  updated_at: DS.attr('date'),
  updated_at_format: computeDateFormat('updated_at'),
  cv: DS.belongsTo('apella-file', {label: 'candidacy.label.cv'}),
  pubs_note: DS.belongsTo('apella-file', {label: 'candidacy.label.pubs_note'}),
  diplomas: DS.hasMany('apella-files', {label: 'candidacy.label.diploma'}),
  publications: DS.hasMany('apella-files', {label: 'candidacy.label.publication'}),
  self_evaluation_report: DS.belongsTo('apella-file', {label: 'candidacy.label.self_evaluation'}),
  statement_file: DS.belongsTo('apella-file', {label: 'candidacy.label.statement_file'}),
  attachment_files: DS.hasMany('apella-file', {label: 'candidacy.label.attachment_files'}),

  title: computed('position.code', 'candidate.username', function(){
    return `${get(this, 'position.code')} (${get(this, 'candidate.username')})`;
  }),
  // TMP gets value on candidacy details
  position_department: DS.attr()

});
