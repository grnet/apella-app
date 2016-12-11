import Ember from 'ember';
import DS from 'ember-data';
import ENV from 'ui/config/environment';

const CHOICES = ENV.APP.resource_choices;

export default Ember.Mixin.create({
  institution: DS.belongsTo('institution', {label: 'institution.label', formAttrs: {optionLabelAttr: 'title_current'}}),
  can_create_registries: DS.attr({type: 'boolean', defaultValue: false }),
  can_create_positions: DS.attr({type: 'boolean', defaultValue: false }),
});
