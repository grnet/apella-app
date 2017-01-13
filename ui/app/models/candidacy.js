import DS from 'ember-data';
import ENV from 'ui/config/environment';
import {computeI18N, computeI18NChoice, computeDateFormat} from 'ui/lib/common';
import get_label from '../utils/common/label_list_item';

const { computed, get } = Ember,
      CHOICES = ENV.APP.resources;


export default DS.Model.extend({
  candidate: DS.belongsTo('user', {label: 'candidacy.label.candidate', formAttrs: {optionLabelAttr: 'full_name_current'}}),
  position: DS.belongsTo('position', {label: 'candidacy.label.position', formAttrs: {optionLabelAttr: 'code_and_title'}}),
  state: DS.attr({type: 'select', choices: CHOICES.CANDIDACY_STATES, defaultValue: 'posted'}),
  state_verbose: computeI18NChoice('state', CHOICES.CANDIDACY_STATES),
  othersCanView: DS.attr({type: 'boolean', label: 'candidacy.label.others_can_view'}),
  submitted_at: DS.attr('date'),
  submitted_at_format: computeDateFormat('submitted_at'),
  updated_at: DS.attr('date'),
  updated_at_format: computeDateFormat('submitted_at'),
  cv: DS.belongsTo('apella-file', {label: 'candidacy.label.cv'}),
  diplomas: DS.hasMany('apella-files', {label: 'candidacy.label.diploma'}),
  publications: DS.hasMany('apella-files', {label: 'candidacy.label.publication'}),
  self_evaluation_report: DS.attr({label: 'candidacy.label.self_evaluation'}),
  attachment_files: DS.attr({label: 'candidacy.label.attachment_files'}),

  title: computed('position.code', 'candidate.username', function(){
    return `${get(this, 'position.code')} (${get(this, 'candidate.username')})`
  })

});
