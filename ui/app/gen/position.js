import {field} from 'ember-gen';
import {disable_field} from 'ui/utils/common/fields';
import {ApellaGen, urlValidator} from 'ui/lib/common';
import validate from 'ember-gen/validate';
import gen from 'ember-gen/lib/gen';
import {afterToday, beforeToday, afterDays} from 'ui/validators/dates';
import moment from 'moment';
import {
  goToDetails, applyCandidacy, positionActions
} from 'ui/utils/common/actions';
import {position} from 'ui/lib/position/fieldsets';

/*
 * This gen is used for displaying:
 * - Helpdesk admins, helpdesk users: all positions, in all states
 * - Institution managers: positions of their institution, in all states
 * - Assistants: positions of their departments, in all states
 * - Professors: positions of their department, in all states
 */


// TODO: DRY position and position_recent

const {
  computed,
  computed: { reads },
  get,
  merge, assign
} = Ember;

const pick_edit_fs = function() {
  let role = get(this, 'role'),
    starts_at = get(this, 'model.starts_at'),
    ends_at = get(this, 'model.ends_at'),
    state = get(this, 'model.state'),
    now = moment(),
    before_open = now.isBefore(starts_at),
    open = now.isBetween(starts_at, ends_at, null, []),
    fs = position.edit,
    head = [fs.basic, fs.details],
    res;

  if(state === 'posted') {
    if(before_open) {
      res = head;
    }
    else if (open) {
      res = head.concat(fs.candidacies);
    }
    // closed
    else {
      res = head.concat(fs.candidacies/*, fs.electors_regular, fs.electors_substitite*/);
    }
  }
  else if(state === 'cancelled') {
      res = head;
  }
  // in all other states
  else {
    res = head.concat(fs.candidacies);
  }

  // if (state === 'electing') {
    //res = res.concat(fs.electors, fs.electors_regular, fs.electors_substitite, fs.committee, fs.election);
  // }

  return res.concat(fs.assistant_files);
};

/*
 * pick_details_fs_by_state:  same as position_recent, but there is no need to
 * have it separately then pick_details_fs
 */
const pick_details_fs_by_state = function(fs, state, before_open, head, display_candidacies) {
  let res;

  if(state === 'posted') {
    if(before_open) {
      res = head;
    }
    else {
      if (display_candidacies) {
        res =  head.concat(fs.candidacies);
      }
      else {
        res = head;
      }
    }
  }
  else if(state === 'cancelled') {
      res =  head/*.concat(fs.history)*/;
  }
  // in all other states
  else {
    if (display_candidacies) {
      res = head.concat(fs.candidacies/*, fs.electors, fs.electors_regular, fs.electors_substitite, fs.committee, fs.election*/ /*, fs.history, */);
    }
    else {
      // res = head.concat(fs.electors, fs.electors_regular, fs.electors_substitite, fs.committee, fs.election/*, fs.history, */);
      res = head;
    }
  }
  return res.concat(fs.assistant_files);
};

const pick_details_fs = function() {
  let role = get(this, 'role'),
    user_id = get(this, 'user.user_id') + '',
    role_id = get(this, 'user.id') + '',
    starts_at = get(this, 'model.starts_at'),
    // ends_at = get(this, 'model.ends_at'),
    state = get(this, 'model.state'),
    now = moment(),
    before_open = now.isBefore(starts_at),
    fs = position.details,
    head = [fs.basic, fs.details],
    position_model = get(this, 'model'),
    store = get(position_model, 'store'),
    committees_members_ids, electors_ids, participations_in_position,
    display_candidacies = true;

 return pick_details_fs_by_state(fs, state, before_open, head, display_candidacies);
};

const pick_create_fs = function() {
  let fs = position.create;
  return [fs.basic].concat(fs.details);
};


export default ApellaGen.extend({
  order: 800,
  modelName: 'position',
  resourceName: 'positions',
  auth: true,
  path: 'positions',

  abilityStates: {
    is_latest: computed('model.is_latest', function(){
       return get(this, 'model.is_latest');
    }),
    can_create: computed('user.can_create_positions', 'role', function() {
      let role = get(this, 'role');
      let can_create = get(this, 'user.can_create_positions');
      if (role === 'assistant') {
        return can_create;
      }
      return true
    }),
    'open': computed('model.state', 'model.ends_at', 'is_latest',  function() {
      return get(this, 'model.state') === 'open' &&
        moment(get(this, 'model.ends_at')).isBefore(new Date()) &&
        get(this, 'is_latest')
    }),
    electing: computed('state', 'can_create', 'is_latest', function() {
      return get(this, 'model.state') === 'electing' &&
        get(this, 'is_latest') &&
        get(this, 'can_create');
    }),
    before_open: computed('model.is_posted', 'is_latest', 'can_create', function(){
      return get(this, 'model.is_posted') &&
        get(this, 'is_latest') &&
        get(this, 'can_create');
    }),
    after_closed: computed('model.is_closed', 'is_latest', 'can_create', function(){
      return get(this, 'model.is_closed') &&
        get(this, 'is_latest') &&
        get(this, 'can_create');
    }),
    revoked: computed('model.state', 'is_latest', 'can_create', function(){
      return get(this, 'model.state') === 'revoked' &&
        get(this, 'is_latest') &&
        get(this, 'can_create');
    }),
    owned: computed('model.author.user_id', 'user.user_id', 'role',  function() {
      let is_author = this.get('model.author.user_id') == get(this, 'user.user_id');
      let is_manager = get(this, 'role') == 'institutionmanager';
      return is_manager || is_author;
    }),
    owned_by_assistant: computed('role', 'user.can_create_positions', 'is_latest', function(){
      let is_assistant = get(this, 'role') == 'assistant';
      let can_create = get(this, 'user.can_create_positions');
      let is_latest = get(this, 'is_latest');
      return is_assistant && can_create && is_latest;
    })
  },

  common: {
    validators: {
      title: [validate.presence(true), validate.length({min:3, max:200})],
      description: [validate.presence(true), validate.length({max:4000})],

      /*
       * Heldesk admin can modify starts_at, ends_at dates without any client
       * side constrains.
       */

      starts_at: computed('role', function() {
        let role = get(this, 'role');

        if(role === 'helpdeskadmin') {
          return [];
        }
        else  {
          return [afterToday()];
        }
      }),
      ends_at:  computed('role', function() {
        let role = get(this, 'role');
        if(role === 'helpdeskadmin') {
          return [];
        }
        else  {
          return [afterDays({on:'starts_at', days:30})];
        }
      }),
      fek_posted_at: [beforeToday()],
      fek: urlValidator,
      electors_meeting_to_set_committee_date: [afterToday()],
      department_dep_number: [validate.presence(true), validate.number({integer: true})]
    }
  },
  create: {
    onSubmit(model) {
      this.transitionTo('position.record.index', model);
    },
    fieldsets: pick_create_fs(),
  },
  list: {
    getModel: function(params) {
      params = params || {};
      let user = get(this, 'session.session.authenticated'),
        role = user.role;
      if(role === 'professor') {
        let department_id = user.department.split('/').slice(-2)[0];
        params.department = department_id;
      }
      return this.store.query('position', params);
    },
    sort: {
      active: true,
      fields: ['code', 'title', 'old_code'],
      serverSide: true
    },
    filter: {
      active: true,
      serverSide: true,
      search: true,
      searchPlaceholder: 'search.placeholder_positions',
      meta: {
        fields: computed('user.role', function() {
          let user_role = get(this, 'user.role'),
            roles_institution = ['helpdeskadmin', 'helpdeskuser'],
            roles_department = ['institutionmanager', 'assistant'],
            filter_model, dataKey, user_institution;

          if (user_role === 'professor') {
            return ['state_expanded'];
          }
          else if (roles_institution.indexOf(user_role) > -1) {
            filter_model = 'institution';
            dataKey = 'department__institution';
          }
          else if (roles_department.indexOf(user_role) > -1) {
            filter_model = 'department';
            dataKey = 'department';
            user_institution = get(this, 'user.institution').split('/').slice(-2)[0];
          }
          return [
            field(filter_model, {
              autocomplete: true,
              type: 'model',
              modelName: filter_model,
              displayAttr: 'title_current',
              dataKey: dataKey,
              query: function(select, store, field, params) {
                let locale = get(select, 'i18n.locale'),
                  ordering_param = `title__${locale}`;
                params = params || {};
                params.ordering = ordering_param;
                if(filter_model === 'institution'){
                  params.category = 'Institution';
                }
                else if (filter_model === 'department') {
                  params.institution = user_institution;
                }
                return store.query(filter_model, params)
              }
            }),
            'state_expanded'
          ]
        })
      }
    },
    page: {
      title: 'position.menu_label',
    },
    menu: {
      icon: 'event_available',
      label: computed(function() {
        let role = get(this, 'session.session.authenticated.role');
        if (role === 'professor'){
          return 'position_department.menu_label';
        }
        else {
          return 'position.menu_label';
        }
    }),
      display: computed('role', function() {
        let role = get(this, 'role');
        if (role === 'candidate') {
          return false;
        }
        else {
          return true;
        }
      })
    },
    layout: 'table',
    row: {
      fields: computed('role', function(){
        let role = get(this, 'role');
        let f = [
          field('code', { dataKey: 'id' }), 'old_code', 'title', 'state_calc_verbose',
          field('department.title_current', {label: 'department.label'}),
        ];
        if (!(role == 'institutionmanager' || role == 'assistant')) {
          f.pushObject(field('institution.title_current'));
        }
        return f;
      }),

      actions: ['gen:details','applyCandidacy', 'gen:edit', 'remove', 'cancelPosition', 'setElecting', 'setRevoked', 'setFailed', 'setSuccessful' ],
      actionsMap: {
        applyCandidacy: applyCandidacy,
        cancelPosition: positionActions.cancelPosition,
        setElecting: positionActions.setElecting,
        setRevoked: positionActions.setRevoked,
        setFailed: positionActions.setFailed,
        setSuccessful: positionActions.setSuccessful,
      }
    }
  },
  edit: {
    fieldsets: computed('role', 'model.state', 'model.starts_at', 'model.ends_at', pick_edit_fs),
  },
  details: {
    /*
     * for details view should preload candidacies in order to run checks and
     * decide if the candidacies fs should be rendered.
     */
    getModel(params, model) {
      let position_id = get(model, 'id'),
        store = get(model, 'store'),
        query = { position: position_id };

      return store.query('candidacy', query).then(function() {
        return model;
      });
    },
    page: {
      title: computed.readOnly('model.code')
    },
    fieldsets: computed('role', 'user.id', 'user.user_id', 'model.state', 'model.starts_at', 'model.ends_at', pick_details_fs),
  }
});
