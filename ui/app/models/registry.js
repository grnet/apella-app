import DS from 'ember-data';
import ENV from 'ui/config/environment';
import {computeI18NChoice} from 'ui/lib/common';

const {
  computed: { readOnly }, get, set
} = Ember;

const  CHOICES = ENV.APP.resources;

export default DS.Model.extend({
  type: DS.attr({type: 'select', choices: CHOICES.REGISTRY_TYPES, translate: true}),
  department: DS.belongsTo('department', { autocomplete: true, formAttrs: {optionLabelAttr: 'title_current'}}),
  members: DS.attr(),
  type_verbose: computeI18NChoice('type', CHOICES.REGISTRY_TYPES),
  institution: readOnly('department.institution'),
  registry_set_decision_file: DS.belongsTo('apella-file'),
  members_count: DS.attr(),

  removeMembers(members) {
    let store = get(this, 'store');
    let promises = members.map((member) => {
      store.findRecord('registry-member', member.id, {backgroundReload: false}).then(function(rm) {
        rm.destroyRecord();
      });
    })

    return Ember.RSVP.Promise.all(promises).then( (res) => {
      return true;
    })
  },

  addMembers(members) {
    let store = get(this, 'store');
    let registry_id = get(this, 'id');
    let promises = members.map((member) => {
      let membership = store.createRecord('registry-member', {registry_id:registry_id, professor_id:member.id });
      membership.save();
    })

    return Ember.RSVP.Promise.all(promises).then( (res) => {
      return true;
    })
  },

  save: function(options) {
    let store = this.get('store');
    let membersToAdd = get(this, 'members.add');
    let membersToRemove = this.get('members.remove');

    return DS.PromiseObject.create({
      promise: this.removeMembers(membersToRemove).then(()=> {
        this.addMembers(membersToAdd).then(()=> {
          this._internalModel.save(options);
        })
      })
    });

  },

});
