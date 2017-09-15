import {field} from 'ember-gen';
import {i18nField, i18nUserSortField,  get_registry_members, fileField, filterSelectSortTitles} from 'ui/lib/common';
import {disable_field, departmentInstitutionFilterField} from 'ui/utils/common/fields';
import {getFile} from 'ui/utils/files';
import moment from 'moment';
import {
  goToDetails, applyCandidacy, cancelPosition
} from 'ui/utils/common/actions';
import {
  fs_user, fs_contact, fs_prof_domestic, fs_prof_foreign, peak_fs_professors
} from 'ui/lib/professors_quick_details';


const {
  computed,
  computed: { reads },
  get,
  merge, assign
} = Ember;

let candidacy_quick_details_fs =  {
    fields: [
      field('id', {label: 'candidacy.id'}),
      'candidate.id',
      'candidate.old_user_id',
      i18nField('candidate.full_name', {label: 'full_name'}),
      i18nField('candidate.father_name', {label: 'father_name.label'}),
      'othersCanView',
      fileField('cv', 'candidate', 'cv', {
        readonly: true,
      }),
      fileField('diplomas', 'candidate', 'diplomas', {
        readonly: true
      }),
      fileField('publications', 'candidate', 'publications', {
        readonly: true
      }),
      fileField('statement_file', 'candidacy', 'statement_file', {
        readonly: true,
      }),
      fileField('self_evaluation_report', 'candidacy', 'self_evaluation_report', {
        readonly: true,
      }, {replace: true}),
      fileField('attachment_files', 'candidacy', 'attachment_files', {
        readonly: true,
        sortBy: 'filename',
      }, {multiple: true} ),
    ],
    layout: {
      flex: [33, 33, 33, 33, 33, 33, 100, 100, 100, 100, 100, 100]
    }
};

let candidacies_colums = [
    field('id', {label: 'candidacy.id'}),
    i18nField('candidate.full_name'),
    field('submitted_at_format', {label: 'submitted_at.label'}),
    field('updated_at_format', {label: 'updated_at.label'}),
    field('state_verbose', {label: 'candidacy.state'})
  ];

// params used for view details of candidacy from position view
const candidaciesField = function(type, hidden, calc, calc_params) {
  return field('candidacies', {
    refreshValueQuery: true,
    valueQuery: function(store, params, model, value) {
      model = model._content ? model._content : model;
      let position_id = model.get('id'),
        position_department = model.belongsTo('department').link();
      // no use of params for now
      let query = {
        position: position_id,
        latest: true
      };
      return store.query('candidacy', query).then(function(candidacies) {
        return candidacies.setEach('position_department', position_department)
      });
    },
    label: null,
    modelMeta: {
      row: {
        fields: candidacies_colums,
        actions: ['view_details'],
        actionsMap: {
          remove: {
            hidden: true
          },
          view_details: {
            icon: 'open_in_new',
            detailsMeta: {
              fieldsets: computed('model', function() {
                let candidate = get(this, 'model').get('candidate').get('full_name_current');
                return [candidacy_quick_details_fs];
              })
            },
            action: function() {},
            permissions: [{resource: 'candidacies', action: 'view'}],
            label: 'view.professor.details',
            confirm: true,
            prompt: {
              title: computed('model.candidate.full_name_current', function() {
                return this.get('model').get('candidate.full_name_current')
              }),
              cancel: 'close',
              contentComponent: 'model-quick-view'
            }
          }
        }
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


let rowCommitteeElectors = function(field_name, serverSide) {
  let sortFields = (serverSide ? ['user_id', 'last_name_current'] : ['user_id', 'last_name_current', 'first_name_current']),
    searchFields = (serverSide ? ['last_name_current', 'discipline_text'] : ['last_name.el', 'last_name.en', 'first_name.el','first_name.en', 'email', 'username', 'discipline_text', 'old_user_id']);


  let display = serverSide;
  return {
    /*
     * For electors table only, make user confirm his choice if he chooses to
     * select a professor who is currently on leave.
     */
    row: {
      onSelect(item, selected) {
        let prompt = Ember.getOwner(this).lookup('service:prompt');
        if (item.get('on_leave')) {
          let accept = prompt.prompt(
            {
              ok: 'ok',
              cancel: 'cancel',
              message: 'prompt.selectOnLeave.message',
              title: 'prompt.selectOnLeave.title',
            }).then( () => {
            selected.addObject(item);
          })
        } else {
          selected.addObject(item);
        }
      },
      fields: computed('role', function() {
        // all electors tables have an extra column
        let role = get(this, 'role');
        let restricted = (role == 'candidate' || role == 'professor');
        if(field_name.startsWith('electors')) {
          let res = [
            'user_id',
            'old_user_id',
            i18nUserSortField('last_name', {label: 'last_name.label'}),
            i18nField('first_name', {label: 'first_name.label'}),
            i18nField('department.title', {label: 'department.label'}),
            field('institution_global', {label: 'institution.label'}),
            'is_foreign_descr',
            'on_leave_verbose',
          ];
          if (!restricted) {
            res.push(field('email', {label: 'email.label'}))
            res.push('active_elections');
          }
          return res;
        }
        else {
          let res = [
            'user_id',
            'old_user_id',
            i18nUserSortField('last_name', {label: 'last_name.label'}),
            i18nField('first_name', {label: 'first_name.label'}),
            i18nField('department.title', {label: 'department.label'}),
            field('institution_global', {label: 'institution.label'}),
            'is_foreign_descr',
            'on_leave_verbose',
          ];
          if (!restricted) {
            res.push(field('email', {label: 'email.label'}))
          }
          return res;
        }
      }),
      actions: ['view_details'],
      actionsMap: {
        view_details: {
          icon: 'open_in_new',
          detailsMeta: {
            fieldsets: computed('model', peak_fs_professors)
          },
          action: function() {},
          permissions: [{resource: 'professors', action: 'view'}],
          hidden: false,
          label: 'view.professor.details',
          confirm: true,
          prompt: {
            title: computed('model.user_id', function() {
              return get(this, 'model.full_name_current');
            }),
            cancel: 'close',
            contentComponent: 'model-quick-view'
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
      searchPlaceholder: computed('role', function() {
        /*
         * TODO: Separate the search fields and placeholder for each type of
         * roles
         */
        return 'search.placeholder.members';
      }),
      serverSide: serverSide,
      active: display,
      searchFields: searchFields,
      meta: {
        fields: [
          field('user_id', {type: 'string'}),
          filterSelectSortTitles('institution'),
          departmentInstitutionFilterField('members_department'),
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
    modelMeta: rowCommitteeElectors(field_name, modelMetaSide),
    selectModelMeta: rowCommitteeElectors(field_name, selectModelMetaSide),
    displayComponent: 'gen-display-field-table'

  });
};

const historyField = function(position_id) {
  return field('past_positions', {
    valueQuery: function(store, params, model, value) {
      let id = model.get('id');
      let query = {id: id, history: true};
      return store.query('position', query);
    },
    label: null,
    modelMeta: {
      row: {
        fields: [field('id', {label: 'position.state.id'}), 'state_calc_verbose',
          field('updated_at_format', {label: 'updated_at.label'})
        ],
        actions: ['goToDetails'],
        actionsMap: {
          goToDetails: goToDetails('position_history', undefined, true, position_id)
        }
      },
    },
    displayComponent: 'gen-display-field-table'
  });
};

export {
  contactField, candidaciesField, committeeElectorsField,
  historyField
};
