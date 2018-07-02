import DS from 'ember-data';
import ENV from 'ui/config/environment';
import {computeI18NChoice} from 'ui/lib/common';

const {
  computed: { readOnly }, get, set,
  inject
} = Ember;

const  CHOICES = ENV.APP.resources;

export default DS.Model.extend({
  messages: inject.service('messages'),
  type: DS.attr({type: 'select', choices: CHOICES.REGISTRY_TYPES, translate: true}),
  department: DS.belongsTo('department', { autocomplete: true, formAttrs: {optionLabelAttr: 'title_current'}}),
  members: DS.attr(),
  type_verbose: computeI18NChoice('type', CHOICES.REGISTRY_TYPES),
  institution: readOnly('department.institution'),
  registry_set_decision_file: DS.belongsTo('apella-file'),
  members_count: DS.attr(),

  handleMembers(membersToAdd, membersToRemove) {
    let store = get(this, 'store');
    let registry_id = get(this, 'id');
    let promises = [];

    let promises_add = membersToAdd.map((member) => {
      let membership = store.createRecord('registry-member', {registry_id:registry_id, professor_id:member.id });
      return membership.save().then( (res) => {
        return;
      }, (err) => {
        let msg = err.errors[0].detail || 'error';
        return [msg, member.id];
      });
    })

    let promises_remove = membersToRemove.map((member) => {
      return store.findRecord('registry-member', member.id, {backgroundReload: false}).then(function(rm) {
        return rm.destroyRecord().then( (res) => {
          return;
        }, (err) => {
          let msg = err.errors[0].detail || 'error';
          return [msg, member.id];
        });
      });
    })

    promises = promises_add.concat(promises_remove)

    return Ember.RSVP.Promise.all(promises).then( (res) => {
      return  res;
    })
  },

  cleanResult(res) {
    // res is an array of null values and error messages in the form of
    // res = [null, null, ['already.in.registry',42], ['in.other.registry', 17]]

    // Remove null values from res
    // outcome: [['already.in.registry',42], ['in.other.registry', 17]]
    let errors = res.filter(x => x);
    if (errors.length === 0) return false;

    let i18n = get(this, 'i18n');
    // Aggregate error messages
    // outcome: {'already.in.registy': [42], 'in.other.registry': [17]}
    errors =  errors.reduce((result, error) => {
        (result[error[0]] || (result[error[0]] = [])).push(error[1])
        return result;
    }, {});

    let errors_for = i18n.t('error.for.users');

    // Translate errors and concat to error message string
    // outcome: 'Errors for users: 42 (Already in registry) 17 (In other registry)
    errors = Object.keys(errors).reduce( (result, key) => {
      let value = errors[key];
      return `${result} ${value.join(' , ')} (${i18n.t(key)})`
    }, errors_for);

    return errors;
  },

  save: function(options) {
    let store = this.get('store');
    let membersToAdd = get(this, 'members.add');
    let membersToRemove = this.get('members.remove');
    // If there are not members to add or remove, just
    // save the model
    if (!(membersToAdd || membersToRemove)) {
      return this._internalModel.save(options);
    }

    return DS.PromiseObject.create({
      promise: this.handleMembers(membersToAdd, membersToRemove).then((res) => {
        let error_msg = this.cleanResult(res);
        this._internalModel.save().then((res) => {
          if (error_msg) {
            get(this, 'messages').setError(error_msg, {closeTimeout: 100000});
          }
        })
      })
    });

  },


});
