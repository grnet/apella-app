import {field} from 'ember-gen';
import {disable_field} from 'ui/utils/common/fields';
import {ApellaGen, urlValidator} from 'ui/lib/common';
import validate from 'ember-gen/validate';
import gen from 'ember-gen/lib/gen';
import {afterToday, beforeToday, afterDays} from 'ui/validators/dates';
import moment from 'moment';
import {
  goToDetails, applyCandidacy, cancelPosition
} from 'ui/utils/common/actions';
import {position} from 'ui/lib/position/fieldsets';

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
    head = [fs.basic, fs.details];

  if(state === 'posted') {
    if(before_open) {
      return head;
    }
    else if (open) {
      return head.concat(fs.candidacies);
    }
    // closed
    else {
      return head.concat(fs.candidacies, fs.committee, fs.electors_regular, fs.electors_substitite);
    }
  }
  else if(state === 'cancelled') {
      return head;
  }
  // in all other states
  else {
    return head.concat(fs.candidacies, fs.committee, fs.electors_regular, fs.electors_substitite);
  }
};

const pick_details_fs = function() {
  let role = get(this, 'role'),
    starts_at = get(this, 'model.starts_at'),
    ends_at = get(this, 'model.ends_at'),
    state = get(this, 'model.state'),
    now = moment(),
    before_open = now.isBefore(starts_at),
    fs = position.details,
    head = [fs.basic, fs.details];

  if(state === 'posted') {
    if(before_open) {
      return head;
    }
    else {
      return head.concat(fs.candidacies);
    }
  }
  else if(state === 'cancelled') {
      return head/*.concat(fs.history)*/;
  }
  // in all other states
  else {
    return head.concat(fs.candidacies, fs.committee, fs.electors_regular, fs.electors_substitite/*, fs.history, */);
  }
};

const pick_create_fs = function() {
  let fs = position.create;
  return [fs.basic].concat(fs.details);
};


export default ApellaGen.extend({
  order: 800,
  modelName: 'position',
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
    before_open: computed('model.starts_at', 'is_latest', 'can_create', function(){
      return moment(new Date()).isBefore(moment(get(this, 'model.starts_at'))) &&
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
      description: [validate.presence(true), validate.length({max:300})],

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
    sort: {
      active: true,
      fields: ['code', 'title', 'old_code'],
      serverSide: true
    },
    filter: {
      active: true,
      meta: {
        fields: [
          field('department', {
            autocomplete: true,
            type: 'model',
            displayAttr: 'title_current',
            modelName: 'department'
          }),
          'state'
        ]
      },
      serverSide: true,
      search: true,
      searchPlaceholder: 'search.placeholder_positions'
    },
    page: {
      title: 'position.menu_label',
    },
    menu: {
      icon: 'event_available',
      label: 'position.menu_label'
    },
    layout: 'table',
    row: {
      fields: computed('role', function(){
        let role = get(this, 'role');
        let f = [
          'code', 'old_code', 'title', 'state_calc_verbose',
          field('department.title_current', {label: 'department.label'}),
        ];
        if (!(role == 'institutionmanager' || role == 'assistant')) {
          f.pushObject(field('institution.title_current'));
        }
        return f;
      }),

      actions: ['gen:details','applyCandidacy', 'remove', 'cancelPosition' ],
      actionsMap: {
        applyCandidacy: applyCandidacy,
        cancelPosition: cancelPosition
      }
    }
  },
  edit: {
    fieldsets: computed('role', 'model.state', 'model.starts_at', 'model.ends_at', pick_edit_fs),
  },
  details: {
    page: {
      title: computed.readOnly('model.code')
    },
    fieldsets: computed('role', 'model.state', 'model.starts_at', 'model.ends_at', pick_details_fs),
  }
});
