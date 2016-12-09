import DS from 'ember-data';
import ENV from 'ui/config/environment';
import get_label from '../utils/common/label_list_item';

const { computed, get } = Ember,
      CHOICES = ENV.APP.resources;


export default DS.Model.extend({
  candidate: DS.belongsTo('user', {label: 'candidacy.label.candidate', formAttrs: {optionLabelAttr: 'username'}}),
  position: DS.belongsTo('position', {label: 'candidacy.label.position', formAttrs: {optionLabelAttr: 'code_and_title'}}),
  state: DS.attr({type: 'select', choices: CHOICES.CANDIDACY_STATES, defaultValue: 'posted'}),
  othersCanView: DS.attr({type: 'boolean', label: 'candidacy.label.others_can_view'}),
  submittedAt: DS.attr('date'),
  cv: DS.attr({label: 'candidacy.label.cv'}),
  diploma: DS.attr({label: 'candidacy.label.diploma'}),
  publication: DS.attr({label: 'candidacy.label.publication'}),
  selfEvaluation: DS.attr({label: 'candidacy.label.self_evaluation'}),
  additionalFiles: DS.attr({label: 'candidacy.label.additional_files'}),

  state_verbose: computed('state','i18n.locale', function() {
    let list = CHOICES.CANDIDACY_STATES;
    return this.get('i18n').t(get_label(list, get(this, 'state')))
  }),

});
