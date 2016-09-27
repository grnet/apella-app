import DS from 'ember-data';

export default DS.Model.extend({
  candidate: DS.belongsTo('user', {label: 'candidacy.label.candidate', attrs:{type: 'select', optionLabelAttr: 'username'}}),
  position: DS.attr({label: 'candidacy.label.position'}),
  state: DS.attr({label: 'candidacy.label.state'}),
  othersCanView: DS.attr({label: 'candidacy.label.others_can_view'}),
  submittedAt: DS.attr('date'),
  cv: DS.attr({label: 'candidacy.label.cv'}),
  diploma: DS.attr({label: 'candidacy.label.diploma'}),
  publication: DS.attr({label: 'candidacy.label.publication'}),
  selfEvaluation: DS.attr({label: 'candidacy.label.self_evaluation'}),
  additionalFiles: DS.attr({label: 'candidacy.label.additional_files'})
});
