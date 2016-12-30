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
    head = [fs.basic, fs.details],
    tail = [fs.assistants];

  if(state === 'posted') {
    if(before_open) {
      return head.concat(tail);
    }
    else if (open) {
      return head.concat(fs.candidacies, tail);
    }
    // closed
    else {
      return head.concat(fs.candidacies, fs.committee, fs.electors_regular, fs.electors_substitite, tail);
    }
  }
  else if(state === 'cancelled') {
      return head.concat(tail);
  }
  // in all other states
  else {
    return head.concat(fs.candidacies, fs.committee, fs.electors_regular, fs.electors_substitite, tail);
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
    head = [fs.basic, fs.details],
    tail = [fs.assistants];

  if(state === 'posted') {
    if(before_open) {
      return head.concat(tail);
    }
    else {
      return head.concat(fs.candidacies, tail);
    }
  }
  else if(state === 'cancelled') {
      return head.concat(fs.history, tail);
  }
  // in all other states
  else {
    return head.concat(fs.candidacies, fs.committee, fs.electors_regular, fs.electors_substitite, fs.history, tail);
  }
};

const pick_create_fs = function() {
  let fs = position.create;
  return [fs.basic].concat(fs.details, fs.assistants);
};


export default ApellaGen.extend({
  modelName: 'position',
  auth: true,
  path: 'positions',

  abilityStates: {
    is_latest: computed('model.is_latest', function(){
      return get(this, 'model.is_latest');
    }),
    owned: computed('user.user_id', 'model.author', 'role', 'model.assistants.[]', function() {
      let id = get(this, 'user.id').toString();

      let is_attached_assistant = false;
      let is_institutionmanager = get(this, 'role') === 'institutionmanager';
      let is_author = this.get('model.author.user_id') == get(this, 'user.user_id');

      if (this.get('model.assistants')) {
        if (this.get('model.assistants').getEach('id')) {
          let res = this.get('model.assistants').getEach('id');
          if (res.includes(id)) {
            is_attached_assistant = true;
          }
        }
      }

      return is_author || is_attached_assistant || is_institutionmanager;
    }), // we expect server to reply with owned resources
    'open': computed('model.state', 'model.ends_at', 'owned', 'is_latest',  function() {
      return get(this, 'model.state') === 'open' &&
        moment(get(this, 'model.ends_at')).isBefore(new Date()) &&
        get(this, 'is_latest') &&
        get(this, 'owned');
    }),
    closed: computed('model.starts_at', 'owned', 'is_latest',  function() {
      return moment(get(this, 'model.starts_at')).isBefore(moment(new Date())) &&
        get(this, 'is_latest') &&
        get(this, 'owned');
    }),
    electing: computed('model.state', 'closed', 'owned', 'is_latest', function() {
      return get(this, 'model.state') === 'posted' &&
        get(this, 'closed') &&
        get(this, 'is_latest') &&
        get(this, 'owned');
    }),
    before_open: computed('owned', 'model.starts_at', 'is_latest',  function(){
      return moment(new Date()).isBefore(moment(get(this, 'model.starts_at'))) &&
        get(this, 'is_latest') &&
        get(this, 'owned');
    }),
    is_latest: computed('model.is_latest', function(){
      return get(this, 'model.is_latest')
    }),
    can_create: computed('user.can_create_positions', function() {
      return get(this, 'user.can_create_positions');
    })
  },

  common: {
    validators: {
      title: [validate.presence(true), validate.length({min:4, max:200})],
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
      fields: ['code', 'title'],
      serverSide: true
    },
    filter: {
      active: true,
      meta: {
        fields: ['department']
      },
      serverSide: true,
      search: true,
    },
    page: {
      title: 'position.menu_label',
    },
    menu: {
      icon: 'business_center',
      label: 'position.menu_label'
    },
    layout: 'table',
    row: {
      fields: ['code', 'title', 'state_calc_verbose', field('department.title_current', {label: 'department.label'})],
      actions: ['gen:details','applyCandidacy', 'gen:edit', 'remove', 'cancelPosition' ],
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
