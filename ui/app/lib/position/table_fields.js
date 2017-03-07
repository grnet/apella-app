import {field} from 'ember-gen';
import {i18nField, get_registry_members} from 'ui/lib/common';
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

// params used for view details of candidacy from position view
const candidaciesField = function(type, hidden, calc, calc_params) {
  return field('candidacies', {
    refreshValueQuery: true,
    valueQuery: function(store, params, model, value) {
      let position_id = model.get('id');
      // no use of params for now
      let query = {
        position: position_id,
        latest: true
      };
      return store.query('candidacy', query);
    },
    label: null,
    modelMeta: {
      row: {
        fields: [
          'id',
          i18nField('candidate.full_name', {label: 'last_name.label'}),
          field('submitted_at_format', {label: 'submitted_at.label'}),
          field('updated_at_format', {label: 'updated_at.label'}),
          field('state_verbose', {label: 'candidacy.state'})
        ],
        actions: ['goToDetails', 'remove'],
        actionsMap: {
          goToDetails: goToDetails(type, hidden, calc, calc_params),
          remove: { hidden: true }
        },
      },
    },
    displayComponent: 'gen-display-field-table',
    disabled: true
  });
};

const managers_columns = [
  i18nField('full_name', {label: 'full_name_current.label'}),
  'role_verbose',
  field('email', {label: 'email.label'}),
  'home_phone_number'
];

const contactField = field('institution-managers', {
  label: null,
  modelName: 'institution-manager',
  modelMeta: {
    row: {
      fields: managers_columns,
    },
  },
  valueQuery: function(store, params, model, value) {
    // find department and its institution

    return model.get('department')
      .then(function(department) {
        return  department.get('institution')
          .then(function(institution) {
            let institution_id = institution.get('id'),
              department_id = model.get('department').get('id'),
              query_institution_manager = {
                institution: institution_id,
                is_verified: true,
                manager_role: 'institutionmanager'
              },
              query_assistants = {
                departments: department_id,
                is_verified: true,
                is_secretary: true,
                can_create_positions: true
              };

            return store.query('institution-manager', query_institution_manager)
              .then(function(institution_managers) {

                if(institution_managers.get('length') >= 1){
                  let position_managers = [];

                  institution_managers.forEach(function(institution_manager) {
                    let institution_manager_id = institution_manager.get('id'),
                     sub_institution_manager_id = `sub-${institution_manager_id}`,
                     sub;

                     /* The info of sub_institution_manager are on the model of
                     * institution manager. We extract them and create a
                     * institution-manager model with role sub_institution_manager.
                     * We do this because we want to display his info in a table.
                     */
                    if(!store.hasRecordForId('institution-manager', sub_institution_manager_id)) {
                      let first_name = institution_manager.get('sub_first_name'),
                        last_name = institution_manager.get('sub_last_name'),
                        email = institution_manager.get('sub_email'),
                        home_phone = institution_manager.get('sub_home_phone_number');

                      sub = store.createRecord('institution-manager', {
                        role: 'sub_institution_manager',
                        id: sub_institution_manager_id,
                        first_name: first_name,
                        last_name: last_name,
                        email: email,
                        home_phone_number: home_phone
                      });
                    }
                    else {
                      sub = store.peekRecord('institution-manager', sub_institution_manager_id);
                    }
                    position_managers.push(institution_manager, sub);
                  });

                  return store.query('assistant', query_assistants).then(function(assistants) {
                    return assistants.toArray().concat(position_managers);
                  });
                }
                else return [];
              });
          });
      });
  },
  displayComponent: 'gen-display-field-table'

});

/*
 * These fields can get a value from the members of a registry.
 * The table with the members data have the same form
 */


let rowCommiteeElectors = function(field_name, serverSide) {
  let sortFields = (serverSide ? ['user_id', 'last_name'] : ['user_id', 'last_name_current', 'first_name_current']),
    searchFields = (serverSide ? ['last_name_current', 'discipline_text'] : ['last_name.el', 'last_name.en', 'discipline_text']);


   // For now, hide client side functionality
  let display = serverSide;
  return {
    row: {
      fields: computed('role', function() {
        // all electors tables have an extra column
        let role = get(this, 'role');
        let restricted = (role == 'candidate' || role == 'professor');
        if(field_name.startsWith('electors')) {
          let res = [
            'id',
            'old_user_id',
            i18nField('last_name', {label: 'last_name.label'}),
            i18nField('first_name', {label: 'first_name.label'}),
            i18nField('department.title', {label: 'department.label'}),
            i18nField('department.institution.title'),
            'is_foreign_descr',
          ];
          if (!restricted) {
            res.push(field('email', {label: 'email.label'}))
            res.push('active_elections');
          }
          return res;
        }
        else {
          let res = ['id',
            'old_user_id',
            i18nField('last_name', {label: 'last_name.label'}),
            i18nField('first_name', {label: 'first_name.label'}),
            i18nField('department.title', {label: 'department.label'}),
            i18nField('department.institution.title'),
            'is_foreign_descr',
          ];
          if (!restricted) {
            res.push(field('email', {label: 'email.label'}))
          }
          return res;
        }
      }),
      actions: ['goToProfessorDetails'],
      actionsMap: {
        goToProfessorDetails: {
            label: 'details.label',
            icon: 'remove red eye',
            permissions: [{resource: 'professors', action: 'view'}],
            hidden: false,
            action: function(route, model) {
              let resource = model.get('_internalModel.modelName'),
                dest_route = `${resource}.record.index`;
              route.transitionTo(dest_route, model);
            }
        }
      }
    },
    paginate: {
      active: display,
      serverSide: serverSide,
      limits: [10, 20, 30]
    },
    filter: {
      search: true,
      searchPlaceholder: 'search.placeholder_members',
      serverSide: serverSide,
      active: display,
      searchFields: searchFields,
      meta: {
        fields: [
          field('user_id', {type: 'string'}),
          field('institution', {
            type: 'model',
            autocomplete: true,
            displayAttr: 'title_current',
            modelName: 'institution',
          }),
          field('rank')
        ]
      }
    },
    sort: {
      serverSide: serverSide,
      active: display,
      fields: sortFields
    }
  };
};



function committeeElectorsField(field_name, registry_type, modelMetaSide, selectModelMetaSide) {
  let label = `registry.type.${registry_type}`;
  return field(field_name, {
    label: label,
    refreshValueQuery: modelMetaSide,
    disabled: computed('model.changeset.committee_set_file', 'model.changeset.electors_set_file', function(){

      // changeset.<field> value can be either a model or a model promise
      function getFile(content, key) {
        let value = get(content, `model.changeset.${key}`)
        if (value && (value instanceof DS.Model)) { return value; }
        return value && value.content;
      }
      let file1 = getFile(this, 'committee_set_file');
      let file2 = getFile(this, 'electors_set_file');

      if(field_name.startsWith('committee')) {
        return !file1;
      } else {
        return !file2;
      }
    }),
    query: computed('position', function(table, store, field, params) {
      return function(table, store, field, params) {
        // TODO: Retrieve department id doesn't work
        let departmentID = table.get("form.changeset.department.id");
        return store.query('registry', {department: departmentID}).then(function (registries) {
            /*
             * There are max 2 registries per department
             * Here we take the external (type 2) registry
             */
          let registry = registries.findBy('type', registry_type);
          if(!registry) {
            return []
          }
          else
            return get_registry_members(registry, store, params);
          });
      };
    }),
    modelMeta: rowCommiteeElectors(field_name, modelMetaSide),
    selectModelMeta: rowCommiteeElectors(field_name, selectModelMetaSide),
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
        goToDetails: goToDetails(undefined, false, false)
      }
    },
  },
  displayComponent: 'gen-display-field-table'
});

export {
  contactField, candidaciesField, committeeElectorsField,
  historyField
};
