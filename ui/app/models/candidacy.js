import DS from 'ember-data';
import ENV from 'ui/config/environment';
import {computeI18N, computeI18NChoice, computeDateFormat} from 'ui/lib/common';

const { computed, get } = Ember,
      CHOICES = ENV.APP.resources;

let candidacy_states = CHOICES.CANDIDACY_STATES.map(function(el){
  if (el[1] == 'Posted') {
    return [el[0], 'Submitted']
  } else {
    return el;
  }
});

export default DS.Model.extend({
  candidate: DS.belongsTo('user', {label: 'candidacy.label.candidate', formAttrs: {optionLabelAttr: 'full_name_current'}}),
  position: DS.belongsTo('position', {label: 'candidacy.label.position', formAttrs: {optionLabelAttr: 'code_and_title'}}),
  state: DS.attr({type: 'select', candidacy_states, defaultValue: 'posted'}),
  state_verbose: computeI18NChoice('state', candidacy_states),
  othersCanView: DS.attr({type: 'boolean', label: 'candidacy.label.others_can_view'}),
  submitted_at: DS.attr('date'),
  submitted_at_format: computeDateFormat('submitted_at'),
  updated_at: DS.attr('date'),
  updated_at_format: computeDateFormat('submitted_at'),
  cv: DS.belongsTo('apella-file', {label: 'candidacy.label.cv'}),
  diplomas: DS.hasMany('apella-files', {label: 'candidacy.label.diploma'}),
  publications: DS.hasMany('apella-files', {label: 'candidacy.label.publication'}),
  self_evaluation_report: DS.belongsTo('apella-file', {label: 'candidacy.label.self_evaluation'}),
  attachment_files: DS.hasMany('apella-file', {label: 'candidacy.label.attachment_files'}),

  title: computed('position.code', 'candidate.username', function(){
    return `${get(this, 'position.code')} (${get(this, 'candidate.username')})`
  })

});
