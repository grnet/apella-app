import {field} from 'ember-gen';
import {ApellaGen} from 'ui/lib/common';
import validate from 'ember-gen/validate';
import _ from 'lodash/lodash';
import {disable_field} from 'ui/utils/common/fields';
import {cancelCandidacy, goToPosition} from 'ui/utils/common/actions';

const {
        set, get, computed, computed: { alias },
        getOwner
      } = Ember;

let POSITION_FIELDS = ['position', 'position.title',
    'position.department.institution.title_current',
    'position.department.title_current', 'position.discipline',
    'position.fek', 'position.fek_posted_at_format',
    'position.starts_at_format', 'position.ends_at_format',
    'position.state_calc_verbose' ];

let POSITION_FIELDSET =  {
      label: 'candidacy.position_section.title',
      text: 'candidacy.position_section.subtitle',
      fields: _.map(POSITION_FIELDS, disable_field),
      layout: {
        flex: [30, 30, 30, 30, 30, 30, 30, 30, 30, 30 ]
      },
      flex: 100
};

let CANDIDATE_FIELDSET =  {
      label: 'candidacy.candidate_section.title',
      text: 'candidacy.candidate_section.subtitle',
      fields: _.map(['candidate', 'cv', 'diploma', 'publication'], disable_field),
      flex: 50,
      layout: {
        flex: [50, 50, 50, 50]
      },
};

let CANDIDACY_FIELDSET =  {
      label: 'candidacy.candidacy_section.title',
      fields: ['selfEvaluation', 'additionalFiles', 'othersCanView'],
      flex: 50,
      layout: {
        flex: [50, 50, 50, 50]
      }
};


let FS = {
  common: [
    POSITION_FIELDSET,
    CANDIDATE_FIELDSET,
    CANDIDACY_FIELDSET
  ],
  list:  ['position.code', 'position.title', 'position.department.institution.title_current',
          'position.department.title_current',
          'position.state_calc_verbose', field('state_verbose', {label: 'candidacy.state'})],
  create_helpdeskadmin: [
    POSITION_FIELDSET,
    {
      label: 'fieldsets.labels.candidate',
      fields: [field('candidate', {
        query: function(table, store, field, params) {
          let promises = [
            store.query('user', {role: 'professor'}),
            store.query('user', {role: 'candidate'}),
          ]

          var promise = Ember.RSVP.all(promises).then(function(arrays) {
            var mergedArray = Ember.A();
            arrays.forEach(function (records) {
              mergedArray.pushObjects(records.toArray());
            });
            return mergedArray.uniqBy('id')
          })

          return DS.PromiseArray.create({
            promise: promise,
          })
        }
      })],
    },
  ],
};


export default ApellaGen.extend({
  appIndex: true,
  modelName: 'candidacy',
  path: 'candidacies',
  session: Ember.inject.service(),

  abilityStates: {
    // resolve ability for position model
    positionAbility: computed('model.position.id', 'role', 'user', 'model', function() {
      let ability = getOwner(this).lookup('ability:positions')
      let props = this.getProperties('role', 'user');
      props.model = get(this, 'model.position');
      ability.setProperties(props);
      return ability;
    }),

    owned: computed('role', 'user.user_id', 'model.candidate.id', function() {
      let is_institutionmanager = get(this, 'role') === 'institutionmanager';
      let is_candidate_owning = get(this, 'user.user_id') == get(this, 'model.candidate.id')
      return is_institutionmanager || is_candidate_owning;
    }), // we expect server to reply with owned resources if user is an institution manager
    others_can_view: alias('model.othersCanView'),
    participates: computed('role', function() {
      let role = get(this, 'role');
      return role === 'professor'; // TODO: resolve user.id participates
    }),
    owned_open: computed('owned', 'model.position.is_open', 'model.state', function() {
      let position_is_open = get(this, 'model.position.is_open');
      let candidacy_is_not_cancelled = get(this, 'model.state') != 'cancelled';
      return get(this, 'owned') && position_is_open && candidacy_is_not_cancelled;
    })
  },

  common: {
    preloadModels: ['position', 'institution', 'department'],
    fieldsets: FS.common,
    validators: {
    }
  },
  list: {
    layout: 'table',
    actions: [],

    getModel: function(params) {
      let role = get(this, 'session.session.authenticated.role');
      if (role == 'candidate' || role == 'professor') {
        let user_id = get(this, 'session.session.authenticated.user_id');
        params = params || {};
        params.candidate = user_id;
      }
      return this.store.query('candidacy', params);
    },
    sortBy: 'position.code:asc',
    search: {
      fields: FS.list,
    },
    page: {
      title: 'candidacy.menu_label',
    },
    menu: {
      label: 'candidacy.menu_label',
      icon: 'assignment',
      display: computed('role', function() {
        let role = get(this, 'role');
        let forbiddenRoles = ['institutionmanager', 'assistant'];
        return (forbiddenRoles.includes(role) ? false : true);
      })
    },
    row: {
      fields: FS.list,
      actions: ['gen:details', 'goToPosition', 'gen:edit', 'cancelCandidacy'],
      actionsMap: {
        cancelCandidacy: cancelCandidacy,
        goToPosition: goToPosition,
      }
    }
  },
  create: {
    fieldsets: computed('model.position', 'role', function(){
      if (get(this, 'role') == 'helpdeskadmin') {
        return FS.create_helpdeskadmin
      } else {
        return FS.common
      }
    }),
    onSubmit(model) {
      this.transitionTo('candidacy.record.index', model)
    },
    getModel(params) {
      var self = this;
      if (params.position) {
        let position = get(self,'store').findRecord('position', params.position);
        let user_id = get(this, 'session.session.authenticated.user_id');
        let role = get(this, 'session.session.authenticated.role');
        let user = get(self, 'store').findRecord('user', user_id);
        return position.then(function(position){
          let c = self.store.createRecord('candidacy', {
            position: position,
          });
          if (role != 'helpdeskadmin') {
            return user.then(function(user) {
              set(c, 'candidate', user);
              return c
            }, function(error) {
              self.transitionTo('candidacy.index');
            })
          } else {
            return c
          }
        }, function(error) {
          self.transitionTo('candidacy.index')
        })
      }
      this.transitionTo('candidacy.index')
    },
    routeMixins: {
      queryParams: {'position': { refreshModel: true }},
    }
  },
  details: {
    page: {
      title: computed.readOnly('model.position.code')
    },
  },
});
