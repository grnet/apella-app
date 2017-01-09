import {field} from 'ember-gen';
import {i18nField} from 'ui/lib/common';
import {disable_field} from 'ui/utils/common/fields';
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
        i18nField('candidate.last_name', {label: 'last_name.label'}),
        i18nField('candidate.first_name', {label: 'first_name.label'}),
        i18nField('candidate.father_name', {label: 'father_name.label'}),
        field('submitted_at_format', {label: 'submitted_at.label'}),
        field('updated_at_format', {label: 'updated_at.label'})
      ],
      actions: ['goToDetails'],
      actionsMap: {
        goToDetails: goToDetails
      }
    },
  },
  displayComponent: 'gen-display-field-table',
  readonly: true
});

const assistantsField = field('assistants', {
  label: null,
  modelMeta: {
    row: {
      fields: ['id',
        i18nField('last_name', {label: 'last_name.label'}),
        i18nField('first_name', {label: 'first_name.label'}),
        field('email', {label: 'email.label'}),
      ],
      actions: ['goToDetails'],
      actionsMap: {
        goToDetails: goToDetails
      }
    },
  },
  displayComponent: 'gen-display-field-table'

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
        fields: computed('', function() {
          // all electors tables have ena extra column
          if(field_name.startsWith('electors')) {
            return ['id',
              i18nField('last_name', {label: 'last_name.label'}),
              i18nField('first_name', {label: 'first_name.label'}),
              i18nField('department.title', {label: 'department.label'}),
              i18nField('department.institution.title'),
              'is_foreign_descr',
              field('email', {label: 'email.label'}),
              'active_elections'
            ];
          }
          else {
            return ['id',
              i18nField('last_name', {label: 'last_name.label'}),
              i18nField('first_name', {label: 'first_name.label'}),
              i18nField('department.title', {label: 'department.label'}),
              i18nField('department.institution.title'),
              'is_foreign_descr',
              field('email', {label: 'email.label'}),
            ];
          }
        }),
        actions: ['goToDetails'],
        actionsMap: {
          goToDetails: goToDetails
        }
      },
    },
    displayComponent: 'gen-display-field-table'

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
  },
  displayComponent: 'gen-display-field-table'
});

export {
  assistantsField, candidaciesField, committeeElectorsField, historyField
};
