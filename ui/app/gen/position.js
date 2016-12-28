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


const {
  computed,
  computed: { reads },
  get,
  merge, assign
} = Ember;


const candidaciesField = field('candidacies', {
    valueQuery: function(store, params, model, value) {
      let position_id = model.get('id');
      // no use of params for now
      let query = {position: position_id};
      return store.query('candidacy', query);
    },
    label: null,
    modelMeta: {
      row: {
        fields: ['id',
          field('candidate.last_name_current', {label: 'last_name.label'}),
          field('candidate.first_name_current', {label: 'first_name.label'}),
          field('candidate.father_name_current', {label: 'father_name.label'}),
          field('submitted_at_format', {label: 'submitted_at.label'}),
          field('updated_at_format', {label: 'updated_at.label'})
        ],
        actions: ['goToDetails'],
        actionsMap: {
          goToDetails: goToDetails
        }
      },
    }
  });

const assistantsField = field('assistants', {
  label: null,
  modelMeta: {
    row: {
      fields: ['id',
        field('last_name_current', {label: 'last_name.label'}),
        field('first_name_current', {label: 'first_name.label'}),
        field('email', {label: 'email.label'}),
      ],
      actions: ['goToDetails'],
      actionsMap: {
        goToDetails: goToDetails
      }
    },
  }
});

function get_registry_members(registry, store, params) {
    let registry_id = registry.get('id'),
      query = assign({}, params, { id: registry_id, registry_members: true});

    return store.query('professor', query)
};
/*
 * These fields can get a value from the members of a registry.
 * The table with the members data have the same form
 */
function committeeElectorsField(field_name, registry_type) {
  let label = `registry.type.${registry_type}`;

  return field(field_name, {
  label: label,
  query: computed('position', function() {
    return function(table, store, field, params) {
      let departmentID = table.get("form.changeset.department.id");
      return store.query('registry', {department: departmentID}).then(function (registries) {
        /*
         * There are max 2 registries per department
         * Here we take the external (type 2) registry
         */
        let registry = registries.findBy('type', registry_type);
        return get_registry_members(registry, store, params);
      });
    };
  }),
  modelMeta: {
    row: {
      fields: ['id',
        field('last_name_current', {label: 'last_name.label'}),
        field('first_name_current', {label: 'first_name.label'}),
        field('email', {label: 'email.label'}),
      ],
      actions: ['goToDetails'],
      actionsMap: {
        goToDetails: goToDetails
      }
    },
  }
});
};

const historyField = field('past_positions', {
    valueQuery: function(store, params, model, value) {
      let id = model.get('id');
      let query = {id: id, history: true};
      return store.query('position', query);
    },
    label: null,
    modelMeta: {
      row: {
        fields: ['id', 'code', 'state_calc_verbose',
          field('updated_at_format', {label: 'updated_at.label'})
        ],
        actions: ['goToDetails'],
        actionsMap: {
          goToDetails: goToDetails
        }
      },
    }
  });



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
       * Other users that can create or edit these dates can do it before the
       * position is open. Only then we use validators.
       * In all the other cases there will be no client side validation (but
       * the fields will be disabled).
       * TODO: When gen doesn't validate disabled fields, remove the
       * corresponding checks.
       */

      starts_at: computed('model.starts_at', 'role', function() {
        let role = get(this, 'role'),
          starts_at = get(this, 'model').get('starts_at'),
          // is_disabled: TRUE when now.isAfter(starts_at), field: disabled
          is_disabled = (starts_at ? moment().isAfter(moment(starts_at)) : false);
        if(role === 'helpdeskadmin' || is_disabled) {
          return [];
        }
        else  {
          return [afterToday()];
        }
      }),
      ends_at:  computed('model.starts_at', 'role', function() {
        let role = get(this, 'role'),
          starts_at = get(this, 'model').get('starts_at'),
          // is_disabled: TRUE when now.isAfter(starts_at), field: disabled
          is_disabled = (starts_at ? moment().isAfter(moment(starts_at)) : false);
        if(role === 'helpdeskadmin' || is_disabled) {
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
    fieldsets: [{
      label: 'fieldsets.labels.basic_info',
      fields: ['title', 'department', 'description',
        'discipline','subject_area', 'subject'],
      layout: {
        flex: [50, 50, 100, 100, 50, 50]
      }
    }, {
      label: 'fieldsets.labels.details',
      fields: ['fek', 'fek_posted_at', 'starts_at', 'ends_at'],
      layout: {
        flex: [50, 50, 50, 50]
      },
    }, {
      label: 'assistants.label',
      text: 'assistants_on_position_explain',
      fields: [assistantsField]
    }],
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
    fieldsets: [{
      label: 'fieldsets.labels.basic_info',
      fields: [disable_field('code'), disable_field('state_calc_verbose'), 'title',
        'department', 'description', 'discipline','subject_area', 'subject'],
      layout: {
        flex: [50, 50, 50, 50, 100, 100, 50, 50]
      }
    }, {
      label: 'fieldsets.labels.details',
      fields: computed('role', 'model.starts_at', 'state', function() {
        let role = get(this, 'role');
        // admin user can edit all these fields
        if(role === 'helpdeskadmin') {
          return ['fek', 'fek_posted_at', 'starts_at', 'ends_at'];
        }
        // other users can edit date fields until the position become open
        else {
          let starts_at = this.get('model').get('starts_at'),
            before_open = moment().isBefore(starts_at),
            start_field, end_field;
          if(before_open) {
            start_field = 'starts_at';
            end_field = 'ends_at';
          }
          else {
            start_field = disable_field('starts_at');
            end_field = disable_field('starts_at')
          }
          return [disable_field('fek'), disable_field('fek_posted_at'), start_field, end_field];
        }
      }),
      layout: {
        flex: [50, 50, 50, 50]
      },
    }, {
      label: 'committee_members.label',
      fields: [
        committeeElectorsField('committee_internal', '1'),
        committeeElectorsField('committee_external', '2')
      ],
      layout: {
        flex: [100, 100]
      }
    }, {
      label: 'electors_regular_members.label',
      fields: [
        committeeElectorsField('electors_regular_internal', '1'),
        committeeElectorsField('electors_regular_external', '2')
      ],
      layout: {
        flex: [100, 100]
      }
    }, {
      label: 'electors_substitute_members.label',
      fields: [
        committeeElectorsField('electors_substitute_internal', '1'),
        committeeElectorsField('electors_substitute_external', '2')
      ],
      layout: {
        flex: [100, 100]
      }
    }, {
      label: 'assistants.label',
      text: 'assistants_on_position_explain',
      fields: [assistantsField]
    }],
  },
  details: {
    page: {
      title: computed.readOnly('model.code')
    },
    fieldsets: [{
      label: 'fieldsets.labels.basic_info',
      fields: ['code', 'state_calc_verbose', 'title',
        field('department.title_current', {label: 'department.label'}),
        'description', 'discipline', field('subject_area.title_current',{label: 'subject_area.label'}),
        field('subject.title_current', {label: 'subject.label'})],
      layout: {
        flex: [50, 50, 50, 50, 100, 100, 50, 50]
      }
    }, {
      label: 'fieldsets.labels.details',
      fields: ['fek', field('fek_posted_at_format', {label: 'fek_posted_at.label'}),
        field('starts_at_format', {label: 'starts_at.label'}),
        field('ends_at_format', {label: 'ends_at.label'})],
      layout: {
        flex: [50, 50, 50, 50]
      }
    },
    {
      label: 'candidacy.menu_label',
      fields: [candidaciesField]
    }, {
      label: 'committee_members.label',
      fields: [
        committeeElectorsField('committee_internal', '1'),
        committeeElectorsField('committee_external', '2')
      ],
      layout: {
        flex: [100, 100]
      }
    }, {
      label: 'electors_regular_members.label',
      fields: [
        committeeElectorsField('electors_regular_internal', '1'),
        committeeElectorsField('electors_regular_external', '2')
      ],
      layout: {
        flex: [100, 100]
      }
    }, {
      label: 'electors_substitute_members.label',
      fields: [
        committeeElectorsField('electors_substitute_internal', '1'),
        committeeElectorsField('electors_substitute_external', '2')
      ],
      layout: {
        flex: [100, 100]
      }
    },
    {
      label: 'assistants.label',
      text: 'assistants_on_position_explain',
      fields: [assistantsField]
    },
    {
      label: 'position.history.title',
      fields: [historyField]
    }]
  }
});
