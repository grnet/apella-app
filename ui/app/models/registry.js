import DS from 'ember-data';
import ENV from 'ui/config/environment';
import {computeI18NChoice} from 'ui/lib/common';

const {
  computed: { readOnly },
} = Ember;

const  CHOICES = ENV.APP.resources;

export default DS.Model.extend({
  __api__: {
    normalize: function(hash, serializer) {
      delete hash.members;
      hash.links = {
        members: ENV.APP.backend_host + '/registries/' + hash.id + '/members/?ordering=user__last_name__en'
      };
      return hash;
    }
  },
  type: DS.attr({type: 'select', choices: CHOICES.REGISTRY_TYPES, translate: true}),
  department: DS.belongsTo('department', { autocomplete: true, formAttrs: {optionLabelAttr: 'title_current'}}),
  members: DS.hasMany('professor', { async: true }),
  type_verbose: computeI18NChoice('type', CHOICES.REGISTRY_TYPES),
  institution: readOnly('department.institution'),
  registry_set_decision_file: DS.belongsTo('apella-file'),
  members_count: DS.attr()
});
